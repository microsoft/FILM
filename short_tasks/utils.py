# This source code is licensed under the MIT license

import string
import pdb


index_rechange = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5
}

def get_csqa_match(pred, label, candidates):
    select_index = None
    for char in pred:
        if char in index_rechange:
            select_index = char
            break
    if select_index is None:
        select_index = 'A'

    select_answer = candidates[index_rechange[select_index]]

    if select_answer == label:
        return 1
    else:
        return 0


def _fix_fracs(string):
    substrs = string.split("\\frac")
    new_str = substrs[0]
    if len(substrs) > 1:
        substrs = substrs[1:]
        for substr in substrs:
            new_str += "\\frac"
            if substr[0] == "{":
                new_str += substr
            else:
                try:
                    assert len(substr) >= 2
                except:
                    return string
                a = substr[0]
                b = substr[1]
                if b != "{":
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}{" + b + "}" + post_substr
                    else:
                        new_str += "{" + a + "}{" + b + "}"
                else:
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}" + b + post_substr
                    else:
                        new_str += "{" + a + "}" + b
    string = new_str
    return string


def _fix_a_slash_b(string):
    if len(string.split("/")) != 2:
        return string
    a = string.split("/")[0]
    b = string.split("/")[1]
    try:
        a = int(a)
        b = int(b)
        assert string == "{}/{}".format(a, b)
        new_string = "\\frac{" + str(a) + "}{" + str(b) + "}"
        return new_string
    except:
        return string


def _remove_right_units(string):
    # "\\text{ " only ever occurs (at least in the val set) when describing units
    if "\\text{ " in string:
        splits = string.split("\\text{ ")
        assert len(splits) == 2
        return splits[0]
    else:
        return string


def _fix_sqrt(string):
    if "\\sqrt" not in string:
        return string
    splits = string.split("\\sqrt")
    new_string = splits[0]
    for split in splits[1:]:
        if split[0] != "{":
            a = split[0]
            new_substr = "\\sqrt{" + a + "}" + split[1:]
        else:
            new_substr = "\\sqrt" + split
        new_string += new_substr
    return new_string


def _strip_string(string):
    # linebreaks
    string = string.replace("\n", "")
    # print(string)

    # remove inverse spaces
    string = string.replace("\\!", "")
    # print(string)

    # replace \\ with \
    string = string.replace("\\\\", "\\")
    # print(string)

    # replace tfrac and dfrac with frac
    string = string.replace("tfrac", "frac")
    string = string.replace("dfrac", "frac")
    # print(string)

    # remove \left and \right
    string = string.replace("\\left", "")
    string = string.replace("\\right", "")
    # print(string)

    # Remove circ (degrees)
    string = string.replace("^{\\circ}", "")
    string = string.replace("^\\circ", "")

    # remove dollar signs
    string = string.replace("\\$", "")

    # remove units (on the right)
    string = _remove_right_units(string)

    # remove percentage
    string = string.replace("\\%", "")
    string = string.replace("\%", "")

    # " 0." equivalent to " ." and "{0." equivalent to "{." Alternatively, add "0" if "." is the start of the string
    string = string.replace(" .", " 0.")
    string = string.replace("{.", "{0.")
    # if empty, return empty string
    if len(string) == 0:
        return string
    if string[0] == ".":
        string = "0" + string

    # to consider: get rid of e.g. "k = " or "q = " at beginning
    if len(string.split("=")) == 2:
        if len(string.split("=")[0]) <= 2:
            string = string.split("=")[1]

    # fix sqrt3 --> sqrt{3}
    string = _fix_sqrt(string)

    # remove spaces
    string = string.replace(" ", "")

    # \frac1b or \frac12 --> \frac{1}{b} and \frac{1}{2}, etc. Even works with \frac1{72} (but not \frac{72}1). Also does a/b --> \\frac{a}{b}
    string = _fix_fracs(string)

    # manually change 0.5 --> \frac{1}{2}
    if string == "0.5":
        string = "\\frac{1}{2}"

    # NOTE: X/Y changed to \frac{X}{Y} in dataset, but in simple cases fix in case the model output is X/Y
    string = _fix_a_slash_b(string)

    return string

def remove_boxed(s):
    left = "\\boxed{"
    try:
        assert s[:len(left)] == left
        assert s[-1] == "}"
        return s[len(left):-1]
    except:
        return None

def last_boxed_only_string(string):
    idx = string.rfind("\\boxed")
    if idx < 0:
        idx = string.rfind("\\fbox")
        if idx < 0:
            return None

    i = idx
    right_brace_idx = None
    num_left_braces_open = 0
    while i < len(string):
        if string[i] == "{":
            num_left_braces_open += 1
        if string[i] == "}":
            num_left_braces_open -= 1
            if num_left_braces_open == 0:
                right_brace_idx = i
                break
        i += 1

    if right_brace_idx == None:
        retval = None
    else:
        retval = string[idx:right_brace_idx + 1]

    return retval


def get_final_result_math(completion):
    if 'Q:' in completion:
        completion = completion.split('Q:')[0].strip()
    if 'Question:' in completion:
        completion = completion.split('Question:')[0].strip()
    if 'The answer is: ' in completion:
        completion = completion.replace('The answer is: ', 'The answer is ')


    if 'The answer is ' not in completion:
        result = last_boxed_only_string(completion)
        result = remove_boxed(result)
    else:
        result = completion.split('The answer is ')[-1].strip()

        if result == "":
            return ""

        if result[-1] == '.':
            result = result[:-1]

        result = result.replace('$', '').strip()

        if 'boxed{' in result:
            result = last_boxed_only_string(result)
            result = remove_boxed(result)


    if result is None:
        return ''

    if result == '':
        return ''

    try:
        result = _strip_string(result)
    except:
        return ''

    assert result is not None

    return result


def get_final_result_gsm8k(completion):
    if '\n\nQ: ' in completion:
        completion = completion.split('\n\nQ: ')[0]
    if '\n\nQuestion: ' in completion:
        completion = completion.split('\n\nQuestion: ')[0]
    if 'The answer is: ' in completion:
        completion = completion.replace('The answer is: ', 'The answer is ')

    while completion[-1] in ['.', '\n']:
        completion = completion[:-1]

    if 'The answer is ' not in completion:
        # print(completion)
        # pdb.set_trace()
        return 0.

    result = completion.lower().split('the answer is ')[-1].split(' ')[0]

    if len(result) == 0:
        return 0.

    if result[-1] == '.':
        result = result[:-1]

    if '£' in result:
        result = result.replace('£', '')
    if '€' in result:
        result = result.replace('€', '')

    if len(result) == 0:
        return 0.

    if result[-1] == '.':
        result = result[:-1]
    result = result.replace(',', '')

    if '=' in result:
        result = result.split('=')[-1]
        result = result.strip()

    if '>>' in result:
        result = result.split('>>')[-1]
        result = result.strip()

    result_str = ''
    result = result.lower()
    for char in result:
        if char in string.ascii_lowercase:
            continue
        else:
            result_str += char
    result = result_str


    if ':' in result:
        result = result.split(':')[0]

    for char in ['$', '"']:
        result = result.replace(char, '')

    if '%' in result:
        result = result.strip()
        if result[-1] == '%':
            result = result[:-1]
        else:
            return 0.
        # percentage = 0.01

    if len(result) == 0:
        return 0.

    if result[-1] in ['/']:
        result = result[:-1]

    result = result.replace(' ', '')

    try:
        if ('+' in result) or ('-' in result) or ('*' in result) or ('/' in result):
            result = eval(result)
        result = float(result)
    except:
        # print('\n', result)
        # pdb.set_trace()
        result = 0

    return result