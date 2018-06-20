# encoding: utf-8

"""

Here we have a bunch of misc-functions that we use in other programmes...

They are mainly focussed around list editing, dict search or information messaging.
All functions are written in 'native' Python to reduce the overhead of other libraries and also a
fun challenge for myself.

"""

import inspect
import datetime


def info_fun(fun_name):
    depth = 4 * (len(inspect.stack()) - 21)
    current_time = str(datetime.datetime.now())
    display_fun_text = '\n' + '-'*depth + '> {fname} : {t0} '.format(fname=fun_name, t0=current_time)
    print(display_fun_text)


def polynomial(x, a, b, c, d=0):
    """
    polynomals
    :param x: range of x..
    :param a: quadratic thing
    :param b: linear coefficient
    :param c: constant coefficient
    :param d: translate coefficient
    :return:
    """
    return [a * (i - d) ** 2 + b * (i - d) + c for i in x]


def cmap_rainbow(n):
    """

    :param n:
    :return:
    """
    x0 = 64
    y1 = polynomial(range(x0), 0, -1/(2*x0), 0.5) + polynomial(range(2*x0), 0, 1/(2*x0), -0.5, -x0)
    a2 = (4*x0 - 1)
    y2 = polynomial(range(a2), -1/(a2 ** 2), 0, 1)
    a3 = (2*x0 - 1)
    y3 = polynomial(range(a2), -1/(a3 ** 2), 0, 1, a3)
    y4 = [1] * n
    ycol = [None] * 4

    for i, y in enumerate([y1, y2, y3, y4]):
        if i == 1 or i == 2:
            ycol[i] = y + [0] * (max(n - len(y),0))
        else:
            ycol[i] = y + [1] * (max(n - len(y),0))
        ycol[i] = ycol[i][0:n]
    return list(map(list, zip(*ycol)))


def split_list_of_list(input_list, x):
    """
    splits list of list by item x
    :param input_list: a list of list..
    :param x: input element to split on
    :return:
    """
    return [i_list for i_list in input_list if not x == i_list]


def n_diff_cluster(input_list, n, return_index=False):
    """
    Groups a list based on the difference between the value n.

    By default returns the clustered values instead of the index

    :param input_list: list of integers
    :param return_index: option to get either index or values
    :param n: the allowed difference between consecutive elements
    :return:
    """

    prev = None
    temp_group = []
    for i, x in enumerate(input_list):
        if not prev or (x - prev) == n:
            if return_index:
                temp_group.extend([i])
            else:
                temp_group.extend([input_list[i]])
        else:
            yield list(temp_group)
            if return_index:
                temp_group = [i]
            else:
                temp_group = [input_list[i]]
        prev = x
    if temp_group:
        yield list(temp_group)


def find_ngrams(input_list, n):
    """
     Because its awesome
    :param input_list: list of items
    :param n: size of ngram
    :return: ngram
    """
    return zip(*[input_list[i:] for i in range(n)])


def transform_to_color(x):
    """
    Based on the amount of unique points in the label list...
    Return a list that contains a translation to distinct colors
    """
    unique_x = list(set(x))
    n = len(unique_x)
    color_x = cmap_rainbow(n)
    dict_color = dict(zip(unique_x, color_x))
    x_to_color = list(map(dict_color.get, x))
    return x_to_color


def cluster_diff_list(input_list, mapped_list=None):
    """
    Provides a way to cluster indices and map then to another vector. Example

    x = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3]
    y = [5, 6, 1, 2, 3, 5, 5, 7, 8, 8, 9, 1]  # This one is related to x by index.

    :param input_list: list with (possibliy) indices that might be related to mapped_list
    :param mapped_list: optional arugment to map the found 'clusters' to a different mapping
    :return: list of list with cluster ids or mapped cluster ids
    """
    prev = 0
    res = []
    if mapped_list is None:
        mapped_list = input_list

    id_pos = [i for i, x in enumerate(diff_list(input_list)) if x > 0]
    for i in id_pos:
        res.append(list(mapped_list[prev:(i+1)]))
        prev = i + 1
    return res


def diff_list(input_list):
    """
    Returns the difference of a list

    :param input_list: list with numeric values
    :return: list with numeric values, but
    """
    return [j-i for i, j in zip(input_list[:-1], input_list[1:])]


def color_back_red(x, x_text):
    """
    Formats the background of a string. Using formatted string defined in colorama

    :param x: input text
    :param x_text: piece of text that needs to be highlighted
    :return: string that, when printed, shows the color red.
    """
    col_back_red = '\x1b[41m'
    col_style_normal = '\x1b[22m'

    x_split = x.replace(x_text, ' ::: ').split(':::')
    x_red_text = col_back_red + x_text + col_style_normal
    return x_red_text.join(x_split)


def color_back_red_index(x, index):
    """
    Formats the background of a string by using index instead of text. Using formatted string defined in colorama
    :param x:
    :param index:
    :return:
    """
    list_x = list(x)
    col_back_red = '\x1b[41m'
    col_style_normal = '\x1b[22m'

    for i_index in index:
        list_x[i_index] = col_back_red + list_x[i_index] + col_style_normal

    return ''.join(list_x)


def subset_list(y, n_min):
    """
    Subsets a list by looking at the length of each element.

    :param y: input list of list
    :param n_min: the minimum length for a list in the lists
    :return: index of the succesful  list, and value of them
    """
    y_index = []
    y_sub = []
    y_index_sub = [(i, x) for i, x in enumerate(y) if len(x) > n_min]
    if len(y_index_sub) != 0:
        # This here is needed to unzip the tuple and map it to two lists.
        y_index, y_sub = list(map(list, zip(*y_index_sub)))
    return y_index, y_sub


def linspace(a, b, n):
    """
    Exactly same functionality as np.linspace.

    :param a: starting point
    :param b: ending point
    :param n: length of the list..
    :return: list with length n
    """
    return [a + x*(b-a)/(n-1) for x in range(n)]


def dict_find(key, dictionary):
    """
    Used to find the values of a certain key in a nested dict

    :param key:
    :param dictionary:
    :return:
    """
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in dict_find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in dict_find(key, d):
                    yield result


def compare_dict(dict1, dict2):
    for x1 in dict1.keys():
        z = dict1.get(x1) == dict2.get(x1)
        if not z:
            print('key', x1)
            print('value A', dict1.get(x1), '\nvalue B', dict2.get(x1))
            print('-----\n')


def get_item_occurence(input_list):
    """
    Counts the occurence of subsequence elements while preserving the order in which they happened

    e.g.
    x = ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'a', 'a', 'c']
    y = get_item_occurence(x)
    print(y)
        [('a', 4), ('b', 3), ('a', 2), ('c', 1)]
    :param input_list: input list with string items
    :return: list with tuples
    """
    i_count = 1
    n_class = 0
    count_classes = []
    group_classes = [n_class]
    temp_classes = input_list[0]

    for i_class in input_list[1:] + ['stop']:
        if i_class == temp_classes:
            group_classes.append(n_class)
            i_count += 1
        else:
            n_class += 1
            group_classes.append(n_class)
            count_classes.append((temp_classes, i_count))
            i_count = 1

            temp_classes = i_class

    return count_classes, group_classes[:-1]  # Second last because of the 'stop' trigger
