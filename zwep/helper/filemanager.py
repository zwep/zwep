# encoding: utf-8

"""

"""

import re
import itertools
import glob
import os


def create_dir(unique_dir, path, display=True):
    """
    Creates the needed directory in a given path

    :return:
    """

    counter = 0
    created_dir = []
    for i_dir in unique_dir:
        if not os.path.isdir(i_dir):
            counter += 1
            created_dir.append(i_dir)
            os.makedirs(i_dir)

    if display:
        if not counter:
            print('No directories were created')
        else:
            print('The following directories were created:')
            for i in created_dir:
                print(i)


def find_files(self, path):
    """
    If you find a file somewhere.. make sure that we know about it.. some how..
    Or make a script that checks that validity of all the places...

    And reports back ill positioned files?

    :param path:
    :return:
    """

    list_files = glob.glob(path + "\\**", recursive=True)

    return [i_file for i_file in self.file_name if re.search(i_file, '::'.join(list_files))]


def update_file_location(self, path, input_file_name):
    """
    Updates the location of the files... where the RID locations are 'true'
    :param path:
    :param input_file_name:
    :return:
    """

    z1 = self.get_rid_path(self.file_name)
    z2 = self.get_local_path(path, self.file_name)


def delete_files(path, input_file_name):
    """

    :param path:
    :param input_file_name:
    :return:
    """
    for i_file in input_file_name:
        os.remove(path + '\\' + i_file)


def get_local_path(path, input_file_name, ends_with='.html'):
    """
    Returns the location to the current (local) path where it finds the files in input_file_name
    :param path:
    :param input_file_name:
    :param ends_with: parameter to filter out the directories
    :return:
    """

    list_files = glob.glob(path + "\\**", recursive=True)
    list_html_files = [x for x in list_files if x.endswith(ends_with)]
    path_re = re.sub(r'\\', r'\\\\', path)  # needed becausee of weird escape characters
    path_re_format = '(\\\\{i_file}|{path_re})'  # needed because of last escape characters \\
    list_of_file_dir = {}

    for i_file in input_file_name:
        temp = {i_file: [re.sub(path_re_format.format(path_re=path_re, i_file=i_file), '', x) for x in
                         list_html_files if i_file in x]}
        list_of_file_dir.update(temp)
    return list_of_file_dir


def get_rid_path(self, input_file_name):
    """
    Returns the paths that are found in the current (prepped) RID version

    :return:
    """
    list_of_file_dir = {}
    for i_file in input_file_name:
        i_index = [i for i, x in enumerate(self.file_name) if i_file in x]
        if len(i_index) == 1:
            i_index = i_index[0]
            dir_loc = list(itertools.chain(*itertools.chain(self.prep_rid_data[i_index].values())))
            list_of_file_dir.update({i_file: dir_loc})
        elif len(i_index) == 0:
            print('We have not found this file: ', i_file)
        else:
            print('We have found this name twice: ', i_file)
    return list_of_file_dir
