import json

import requests
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import generics

from msys.models.entry_models import Entry, Schema
from .entry_serializers import *

def recursive_node_to_dict(node):
    result = {
        'name': node.name, 'id': node.pk,
         #notice the use of node._cached_children instead of node.get_children()
        'children' : [recursive_node_to_dict(c) for c in node._cached_children]
    }
    return result

def flat_tree_to_dict(nodes, max_depth):
    tree = []
    last_levels = [None] * max_depth
    for n in nodes:
        d = {'name': n.name,
             'schema': n.schema}
        if n.level == 0:
            tree.append(d)
        else:
            parent_dict = last_levels[n.level - 1]
            if 'children' not in parent_dict:
                parent_dict['children'] = []
            parent_dict['children'].append(d)
        last_levels[n.level] = d
    return tree

class SchemaView(APIView):
    def get(self, request):
        ee = Schema.objects.get(pk=1)
        # dd = recursive_node_to_dict(ee)
        tree_json = json.dumps(flat_tree_to_dict(Schema.objects.all(), 5))
        tree_json = tree_json.replace('\\', '')
        return HttpResponse(tree_json, content_type='application/json')

class EntryList(generics.ListCreateAPIView):  # Detail View
    queryset = Entry.objects.all()
    serializer_class = EventDataSerializer

class SchemaList(generics.ListCreateAPIView):  # Detail View
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer