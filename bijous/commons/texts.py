# coding=utf-8
import string

EN_LETTERS = set(string.ascii_letters)
DIGITS = set(string.digits)


def is_chinese_char(c):
    return '\u4e00' <= c <= '\u9fa5'


def is_english_char(c):
    return c in EN_LETTERS


def is_digit_char(c):
    return c in DIGITS


def ngrams(text, n=2):
    for i in range(len(text) - n + 1):
        yield text[i:i + n]
