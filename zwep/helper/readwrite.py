# encoding: utf-8

"""
Read and write helpers..
"""

import os
from bs4 import BeautifulSoup as bs
import glob
import inspect
import re
import warnings

from zwep.helper import miscfunction as misc


def read_txt_file(path, n_files=None):
    """
    This loads .txt files specified in the :param path: value

    :param path: location of the data
    :param n_files: the amount of reviews to be loaded
    :return: list of strings

    TODO review if the removing of html tags in permitted in here
    """

    intent_path = path + '\*.txt'
    list_files = glob.glob(intent_path)
    sub_list_files = list_files[0:n_files]
    # Removes html tags... maybe not put this here
    content_files = [re.sub('<.*>', ' ', y) for x in sub_list_files for y in open(x, encoding='utf-8').readlines()]
    return content_files


def read_html_obj(input_html):
    """
    This is general function to read html objects. The reason for this is to do a reading with the right necoding.
    In this case this is the ascii encoding wher ewe ignore certain warnings

    :param input_html: html text (str)
    :return: beautiful soup object
    """

    # Here we store the objects that cannot be found.
    # This is not returned yet, but can be used for debugging
    failed_obj = []
    depth = 1 * (len(inspect.stack()) - 20)

    if os.path.isfile(input_html):
        try:
            print('\t'*depth + '  Loading file {0}'.format(input_html))
            with open(input_html, 'r', encoding='utf-8') as f:
                html_text = f.read()
        except TypeError:
            warnings.warn('\t TypeError - Failed id: {0}'.format(input_html))
            failed_obj.append(input_html)
            html_text = -1

        except UnicodeDecodeError:
            with open(input_html, 'r') as f:
                html_text = f.read()
    else:
        print('\t'*depth + '  file is not found {0}'.format(input_html))
        html_text = -1

    html_obj = bs(html_text, 'lxml')
    return html_obj


def load_html_obj(path, n=None):
    """
    Returns a list of html objects, given the path

    :param path: path to html objects
    :param n: subsets the amount of html objects loaded
    :return: a list of Beautiful Soup objects corresponding to the htmls
    """
    depth = 1 * (len(inspect.stack()) - 20)

    if isinstance(path, str):
        if n is None:
            url_html_list = glob.glob(os.path.join(path, "*html"))
        else:
            url_html_list = glob.glob(os.path.join(path, "*html"))[:n]
    elif isinstance(path, list):
        url_html_list = path
    else:
        url_html_list = ''
        print('\t'*depth + '  Unkown input type:', type(path))

    return [(read_html_obj(x), os.path.basename(x)[:-5]) for x in url_html_list]


def save_html_object(html_obj, path, overwrite=False):
    """
    With this we can save the html objects to a specific path

    :param html_obj: a list of tuples.. first one is the content, second item is the file name
    :param path:
    :return: list with objects that are not saved...
    """
    misc.info_fun(save_html_object.__name__)
    depth = 1 * (len(inspect.stack()) - 20)

    # Here we store the objects that cannot be found.
    failed_obj = []

    for i_obj, obj_name in html_obj:
        temp_file_path = os.path.join(path, obj_name)
        try:
            if os.path.isfile(temp_file_path):
                if overwrite:
                    print('\t'*depth + '  saving to location {0}'.format(temp_file_path))
                    with open(os.path.join(path, obj_name), 'w') as f:
                        f.write(i_obj)
                else:
                    print('\t'*depth + '  file is already at location {0}'.format(temp_file_path))
            else:
                print('\t'*depth + '  saving to location {0}'.format(temp_file_path))
                with open(os.path.join(path, obj_name), 'w') as f:
                    f.write(i_obj)

        except TypeError:
            warnings.warn('\t TypeError - Failed id: {0}'.format(obj_name))
            os.remove(temp_file_path)
            failed_obj.append((i_obj, obj_name))

        except UnicodeEncodeError:
            try:
                with open(os.path.join(path, obj_name), 'wb') as f:
                    f.write(i_obj)
            except TypeError:
                warnings.warn('\t TypeError - Failed id: {0}'.format(obj_name))
                os.remove(temp_file_path)
                failed_obj.append((i_obj, obj_name))

            # warnings.warn('UnicodeEncodeError - Failed id: {0}'.format(obj_name))
            # os.remove(temp_file_path)
            # failed_obj.append((i_obj, obj_name))

    return failed_obj