"""
1 Python programming test
1.1 Description
Implement this python function:
def create_regexp(match_words, non_match_words):
"""
Take two lists of words and return a relatively short regular expression
that will match ALL words in match_words
and match NO words in non_match_words
Generally the created regexp must be shorter than the length of the
concatenated list of all input words, the shorter the better.
:param match_words: list of words the returned regexp will match
:param non_match_words: list of words the returned regexp will NOT match
:return: str regexp
"""
1.2 Validation function
You can verify your program with this function:
def validate_solution(regexp, match_words, non_match_words):
assert len(match_words)>1
assert len(non_match_words)>1
for word in match_words: assert re.search(regexp, word)
for word in non_match_words: assert not re.search(regexp, word)
print("All ok")
1.3 Example usage
Validation should work with any match_words and non_match_words:
>>> match_words=[’flower’,’grass’]
>>> non_match_words=[’milk’,’honey’,’water’]
>>> my_regexp = create_regexp(match_words, non_match_words)
This generated regexp example is relatively short:
>>> print(my_regexp)
"o.er|^gra"

1

And it passes the validation:
>>> validate_solution(my_regexp, match_words, non_match_words)
All ok.

"""



import re


def check_not_matches(regex, non_match_words):
    for word in non_match_words:
        if re.search(regex, word):
            return False
    return True


def get_shorter(regex, non_match_words, start=True):
    result = regex
    if start:
        for i in range(len(result)):
            if check_not_matches(result[i:], non_match_words) and len(result[i:]) < len(result):
                return get_shorter(result[i:], non_match_words, start=start)
        return result
    else:
        for i in range(len(result)-1, -1, -1):
            if check_not_matches(result[0:i], non_match_words) and len(result[i:]) < len(result):
                return get_shorter(result[0:i], non_match_words, start=start)
        return result


def get_min_regex_for_word(word, non_match_words):
    start = False
    start_regex = ""
    for i in range(1, len(word)):
        start_regex = word[0:i]
        if start_regex == word:
            start = True
            start_regex = f"^{word}$"
            break
        if check_not_matches(start_regex, non_match_words):
            start = True
            break
    start_regex = get_shorter(start_regex, non_match_words)
    end = False
    end_regex = ""
    for i in range(len(word)-1, -1, -1):
        end_regex = word[i:]
        if end_regex == word:
            end = True
            end_regex = f"^{word}$"
            break
        if check_not_matches(end_regex, non_match_words):
            end = True
            break
    end_regex = get_shorter(end_regex, non_match_words, start=False)
    if start and end:
        return min([start_regex, end_regex], key=lambda x: len(x))
    elif start:
        return start_regex
    else:
        return end_regex


def create_regex(match_words, non_match_words):
    regex = ""
    for word in match_words:
        regex += get_min_regex_for_word(word, non_match_words)
        regex += "|"
    return regex[0:-1]


def validate_solution(regex, match_words, non_match_words):
    assert len(match_words) > 1
    assert len(non_match_words) > 1
    for word in match_words:
        assert re.search(regex, word)
    for word in non_match_words:
        assert not re.search(regex, word)
    print("All ok")


match_words = ["flower", "grass", "bro", 'brod']
non_match_words = ["milk", "honey", "water", "fly", "brotfloweher", "grab", "brodefs", "lower"]
my_regexp = create_regex(match_words, non_match_words)
validate_solution(my_regexp, match_words, non_match_words)
print(my_regexp)
