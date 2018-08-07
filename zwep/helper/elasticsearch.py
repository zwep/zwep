#encoding: utf-8

"""
Example usage of delete_by_query
"""

from elasticsearch import Elasticsearch

es = Elasticsearch()
index = 'news'
query_dict = {'query': {'match': {'source': 'nos'}}}
es.delete_by_query(index, query_dict)

