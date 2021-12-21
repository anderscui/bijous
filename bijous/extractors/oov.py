# coding=utf-8
import time

from collections import Counter
from math import log
from typing import List, Union

import jieba

from bijous.commons.texts import is_chinese_char, is_english_char, is_digit_char, ngrams
from bijous.data_loader import en_vocab, read_lines

jieba.initialize()

SENT_START, SENT_END = 'SOS', 'EOS'


def get_gram_counts(texts: List[str], max_len, min_count=1):
    part_counters = {n_gram: Counter() for n_gram in range(1, max_len + 1)}
    for n_gram in range(1, max_len + 1):
        cur_counter = part_counters[n_gram]
        for sent in texts:
            cur_counter.update(ngrams(sent, n=n_gram))
        if min_count > 1:
            cur_counter = Counter({k: cnt for k, cnt in cur_counter.items() if cnt >= min_count})
        part_counters[n_gram] = cur_counter
    return part_counters


def entropy(sents, part_counters, max_len=2, min_count=1):
    def part_entropy(counter: Counter):
        total = sum(counter.values())
        probs = [c/total for c in counter.values()]
        e = -sum(p * log(p) for p in probs)
        return e

    start = time.time()
    gram_counts = {n_gram: {} for n_gram in range(2, max_len+1)}
    for n_gram in range(2, max_len+1):
        cur_g_counts = part_counters[n_gram]
        part_counts = gram_counts[n_gram]  # a dict
        for sent in sents:
            if len(sent) < n_gram:
                continue

            for i in range(len(sent) - n_gram + 1):
                part = sent[i:i+n_gram]
                if cur_g_counts.get(part, 0) < min_count:
                    continue

                if part not in part_counts:
                    part_counts[part] = {'before': Counter(), 'after': Counter()}

                if i == 0:
                    before = SENT_START
                else:
                    before = sent[i-1]
                if i == len(sent) - n_gram:
                    after = SENT_END
                else:
                    after = sent[i+n_gram]

                part_counts[part]['before'][before] += 1
                part_counts[part]['after'][after] += 1

        print(f'after {n_gram}: {time.time() - start}')

    start = time.time()
    entropies = {n_gram: {} for n_gram in range(2, max_len+1)}
    for n_gram, part_counts in gram_counts.items():
        for part in part_counts:
            c_before = part_counts[part]['before']
            c_after = part_counts[part]['after']
            e_before, e_after = part_entropy(c_before), part_entropy(c_after)
            entropies[n_gram][part] = (e_before + e_after, e_before, e_after)

    print(f'calc entropy: {time.time() - start}')

    return entropies


def mutual_info(gram_counters, max_len=2, min_count=1):
    def mutual(joint_count, left_count, right_count, total):
        return log(total * joint_count / left_count / right_count)

    word_mutual_info = {n_gram: Counter() for n_gram in range(1, max_len+1)}
    total_chars = sum(gram_counters[1].values())
    if total_chars == 0:
        return word_mutual_info

    for n_gram in range(2, max_len+1):
        cur_counter = gram_counters[n_gram]
        for part in cur_counter:
            if cur_counter[part] >= min_count:
                mutual_scores = []
                for i in range(len(part)-1):
                    left, right = part[:i+1], part[i+1:]
                    mutual_score = mutual(gram_counters[len(part)][part],
                                          gram_counters[len(left)][left],
                                          gram_counters[len(right)][right], total_chars)
                    mutual_scores.append(mutual_score)

                word_mutual_info[n_gram][part] = min(mutual_scores)
    return word_mutual_info


def filter_word(word: str, known_words=None):
    def is_valid_char(c):
        return is_chinese_char(c) or is_english_char(c)

    if known_words is None:
        known_words = en_vocab

    if word.lower() in known_words:
        return False
    if not any(is_valid_char(c) for c in word):
        return False
    if all(is_digit_char(c) for c in word):
        return False
    if any(kw in word for kw in ' ,，、.。?？!！"“”'):
        return False
    if word.startswith(tuple('>》)）:：')) or word.endswith(tuple('<《(（')):
        return False
    if len([c for c in word if c in '>》)）']) != len([c for c in word if c in '<《(（']):
        return False
    return True


def calc_grams_info(texts: List[str], max_len=5, min_count=5):
    start = time.time()
    gram_counts = get_gram_counts(texts, max_len=max_len, min_count=min_count)
    print(f'calc gram_counts: {time.time() - start}')

    start = time.time()
    entropies = entropy(texts, gram_counts, max_len=max_len, min_count=min_count)
    print(f'calc entropies: {time.time() - start}')

    start = time.time()
    text_mutual_info = mutual_info(gram_counts, max_len=max_len, min_count=min_count)
    print(f'calc mutual info: {time.time() - start}')
    return entropies, text_mutual_info


def extract_words_of_len(text_entropies, text_mutual_info, top=1000, word_len=2, word_filter=None):
    if word_filter is None:
        word_filter = lambda w: True

    word_entropies = Counter({gram: entro[0] for gram, entro in text_entropies[word_len].items()
                              if entro[1] > 0.1 and entro[2] > 0.1})
    word_mutual = text_mutual_info[word_len]
    # TODO: join like this?
    joint_size = 2 * top
    joint = {part for part, entro in word_entropies.most_common(joint_size)} & {part for part, cnt in word_mutual.most_common(joint_size)}
    joint = {part for part in joint if word_filter(part)}

    merged_info = Counter()
    for word, entro_value in word_entropies.most_common(joint_size):
        if word not in joint:
            continue
        merged_info[word] += entro_value

    for word, mutual_value in word_mutual.most_common(joint_size):
        if word not in joint:
            continue
        merged_info[word] += mutual_value

    return {k: v for k, v in merged_info.most_common(top)}


def extract_words(data_source: Union[List[str], str], top=1000, max_len=5, min_count=5, word_filter=filter_word, with_score=True):
    if isinstance(data_source, str):
        texts = [line.strip() for line in read_lines(data_source)]
    else:
        texts = data_source

    text_entropies, text_mutual_info = calc_grams_info(texts, max_len, min_count)
    c = Counter()
    for i in range(2, max_len+1):
        c.update(extract_words_of_len(text_entropies, text_mutual_info, top=top, word_len=i, word_filter=word_filter))
    return c.most_common(top) if with_score else [k for k, _ in c.most_common(top)]


def is_in_jieba(word):
    return jieba.dt.FREQ.get(word, 0) > 0


if __name__ == '__main__':
    file = '/data/comments.txt'

    TOP = 10000
    MAX_LEN = 5
    MIN_FREQ = 10
    with_score = False

    extracted = extract_words(file, TOP, max_len=MAX_LEN, min_count=MIN_FREQ, with_score=with_score)
    print(len(extracted))

    if with_score:
        for k, score in extracted:
            if is_in_jieba(k):
                continue
            print(k, score)
    else:
        for k in extracted:
            if is_in_jieba(k):
                continue
            print(k)
