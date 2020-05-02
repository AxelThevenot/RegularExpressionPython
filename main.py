import re
import os
import time
import json

class SGR:
    """
    Select Graphic Rendition to display styles on the console

    If you want to know more about or change colors,
    you can find any information you want with the url below
    https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters"""
    reset = '\033[0m'
    bold = '\033[1m'
    blink = '\033[5m'
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        purple = '\033[35m'
        cyan = '\033[36m'
    class bg:
        green = '\033[42m'
        purple = '\033[45m'
        cyan = '\033[46m'

    @staticmethod
    def render_element(name, element, start='', sep=' : ', end='\n'):
        bold_name_part= f'{SGR.bold}{SGR.fg.cyan}{name}'
        element_part = f'{SGR.reset}{element}'
        return start + bold_name_part + sep + element_part + end

def get_data(filename):
    # read the file
    file = open(filename, 'r')
    data = json.load(file)
    file.close()
    # get the regex on the second line
    regex = data['Regular Expressions']
    # get the regex on the 5th line and more
    tests = data['Texts to test']
    return regex, tests

def test_regex(regex, test, main_color, match_color):
    r = re.compile(regex) # compile the regex
    # get all the start and end index of the matches
    m = r.search(test)
    # get groups and group dict
    groups = m.groups() if m is not None else ()
    group_dict = m.groupdict() if m is not None else {}
    # get all the matches
    matches = [[match.start(),match.end()] for match in r.finditer(test)]
    # set the main color
    colored_match = f'{main_color}'
    last_end = 0
    # colorize the matches with match_color otherwise use the main_color
    for start, end in matches:
        # part without match
        colored_match += test[last_end:start]
        # part with match
        colored_match += f'{match_color}{test[start:end]}{main_color}'
        last_end = end
    # part without match
    colored_match += test[last_end:]
    n_match = len(matches)
    return n_match, groups, group_dict, colored_match

if __name__ == '__main__':
    filename = 'file.json'

    while True:
        # 'clear' on Linux or OS X and 'cls' on Windows
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            # extract regex from,the json file and texts to test
            regex, tests = get_data(filename)
            # display the regex
            bold_regex = f'{SGR.bold}{regex}{SGR.reset}'
            output_str = SGR.render_element('Input regex', bold_regex)
            # for each test
            for test in tests:
                # apply the regex and return the matches/groups/group_dict
                result = test_regex(regex, test, SGR.reset, SGR.bg.purple)
                n_match, groups, group_dict, colored_match = result
                # display on the console the matches
                output_str += SGR.render_element('\n Test', test)
                output_str += SGR.render_element('Colored match',
                                                  colored_match, start='\t')
                output_str += SGR.render_element('Number of match',
                                                  n_match, start='\t')
                # display on the console groups and group_dict if exist
                if len(groups):
                    groups_str = f'({", ".join(groups)})'
                    output_str += SGR.render_element('Groups',
                                                      groups_str, start='\t')
                if len(group_dict):
                    group_dict = [f'{k}: {v}' for k, v in group_dict.items()]
                    groups_dict_str = '{' + ", ".join(group_dict) + '}'
                    output_str += SGR.render_element('Groups dictionnary',
                                                      groups_dict_str,
                                                      start='\t')
            print(output_str)
        except Exception as e:
            print(e)
        finally:
            input(f'\nPress enter to actualize{SGR.blink}...{SGR.reset}\n')
