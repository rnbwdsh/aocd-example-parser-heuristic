from aocd.examples import Example
from aocd.examples import Page


def extract_heuristic(page: Page, datas: list[str]) -> list[Example]:
    input_data = answer_a = answer_b = None
    if not datas:
        return []
    # iterate from b to a, because the input_data is more likely to be in the first article
    for article in [page.article_b, page.article_a]:
        if not article:  # null/empty check
            continue
        candidates = [c.text.rstrip("\r\n") for c in article.find_all("code")]
        if len(candidates) == 0:
            return []
        elif len(candidates) == 1:
            input_data = candidates[0]
        else:
            scores = [different_rate(datas[0], c) for c in candidates]
            if input_data is None:
                input_data = candidates[scores.index(min(scores))]
            if article is page.article_a:
                answer_a = candidates[-1]
            else:
                answer_b = candidates[-1]

    return [Example(input_data=input_data, answer_a=answer_a, answer_b=answer_b)]


def _simplify(s: str):
    """ Special characters should match exactly, for letters, same class matching is good enough """
    if s.isupper():
        return "A"
    elif s.islower():
        return "a"
    elif s.isdigit():
        return "1"
    else:
        return s


def different_rate(a: str, b: str):
    """ Ratio of different to common character classes. see tests for examples """
    a = set(map(_simplify, a))
    b = set(map(_simplify, b))
    return len((a | b) - (a & b)) / len(a | b)
