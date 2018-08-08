#encoding: utf-8

"""
Here we have some super simple and stupid and non-scalable funcitons.. but they are nice for now.
"""

import pytz
import os
from datetime import datetime
from dateutil.parser import parse as duparse
from elasticsearch import Elasticsearch
import collections


def get_all_content(step_size=20):
    es = Elasticsearch()
    step_size = 20
    counter = 0
    search_res = es.search(size=step_size * (counter + 1), from_=step_size * counter)
    content_res = search_res['hits']['hits']
    list_content = []
    while len(content_res) > 0:
        list_content.extend(content_res)
        counter += 1
        search_res = es.search(size=step_size, from_=step_size * counter + 1)
        content_res = search_res['hits']['hits']
    return list_content


def count_index(all_content):
    return collections.Counter([x['_index'] for x in all_content]).most_common(10)


def count_source(all_content):
    return collections.Counter([x['_source']['source'] for x in all_content]).most_common(10)


def count_category(all_content):
    return collections.Counter([x['_source']['category'] for x in all_content]).most_common(10)


def count_source_cat(all_content):
    return collections.Counter([(x['_source']['source'], x['_source']['category']) for x in
                                 all_content]).most_common(10)

# Search through it...
def identify_duplicate_titles(all_content):
    title_id_combi = [(x['_source']['title'], x['_id']) for x in all_content]
    title_id_combi = sorted(title_id_combi)
    prev_title = title_id_combi[0][0]
    temp_id_list = [title_id_combi[0][1]]
    full_dict = {}
    for i_title, i_id in title_id_combi[1:]:
        if i_title == prev_title:
            temp_id_list.append(i_id)
        else:
            if len(temp_id_list) > 1:
                full_dict.update({i_title: temp_id_list})
            temp_id_list = [i_id]
            prev_title = i_title
    return full_dict


def find_duplicate_titles(duplicate_dict):
    es = Elasticsearch()
    test_dates = []
    test_content = []
    for k, v in duplicate_dict.items():
        temp_cont = []
        for i_id in v:
            i_query_dict = {'query': {'match': {'_id': i_id}}}
            res = es.search(body=i_query_dict)
            if len(res['hits']['hits']) == 1:
                art_date = res['hits']['hits'][0]['_source']['date']
                art_content = res['hits']['hits'][0]['_source']
                temp_cont.append(art_content)
                test_dates.append(art_date)
            else:
                print('we have mutliple results on this id..')
        test_content.append(temp_cont)
    return test_content


def delete_duplicate_titles(index, duplicate_dict):
    es = Elasticsearch()
    for k, v in duplicate_dict.items():
        if len(v) > 1:
            for i_id in v[1:]:
                query_dict = {'query': {'match': {'_id': i_id}}}
                es.delete_by_query(index=index, body=query_dict)

