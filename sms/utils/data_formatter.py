import re


def result_list_to_dict(result):
    return [row._asdict() for row in result]


def result_row_to_dict(result_row):
    return result_row._asdict()


def list_to_searchable_dropdown(result, label_key, value_key):
    if type(result) == list:
        data = []

        for row in result:
            data.append({
                'label': row[label_key],
                'value': row[value_key]
            })

    else:
        data = result

    return data


def convert_capitalize_word_to_lower_case(value):
    """
    used to convert capitalize word into lower case.

    Args:
        value ([string]): string to be converted

    """
    # finding all lower case word from string and take only first index

    if '/' in value:
        value = value.split('/')
        value = '_or_'.join(value)

    if '-' in value:
        value = value.split('-')
        value = '_'.join(value)

    if '_' not in value:
        find_lower_case = re.findall('([a-z]+)', value)

        # finding all capitalize word from string
        find_capitalize_word = re.findall('([A-Z][a-z]+)', value)

        # join both the list
        new_list = [find_lower_case[0]] + find_capitalize_word

        # join string by underscore (_)
        join_string = '_'.join(new_list)
    else:
        join_string = value

    # convert string into lower case
    lower_case_string = join_string.lower()

    return lower_case_string


def rename_dict_keys(data):
    """ used to renamed nested dict keys from capitalize word to lower case.

    Args:
        data ([dict]):

    Returns:
        [dict]: return renamed nested dict keys from capitalize word to lower case.
    """
    if type(data) is dict:
        for key in list(data.keys()):
            new_key = convert_capitalize_word_to_lower_case(key)
            data[new_key] = data.pop(key)
            if type(data[new_key]) is dict or type(data[new_key]) is list:
                data[new_key] = rename_dict_keys(data[new_key])
    elif type(data) is list:
        for item in data:
            item = rename_dict_keys(item)
    return data


def strip_special_chars(value):
    return (re.sub('[^A-Za-z0-9]+', ' ', value)).strip()