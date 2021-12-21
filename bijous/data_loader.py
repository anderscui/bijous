# coding=utf-8
from bijous.config import EN_DICT_PATH


def read_lines(file_path):
    with open(file_path) as f:
        for line in f:
            yield line


def load_en_vocab():
    return {line.strip().lower() for line in read_lines(EN_DICT_PATH)}


en_vocab = load_en_vocab()
