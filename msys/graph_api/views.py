from msys.neomodels.mg_data_models import SampleMg, Source, Sample
from rest_framework.views import APIView
from django.http import HttpResponse
import json

def serialize_sample_mg_full(node):
    props = node.__properties__
    props['containers'] = []
    for c in node.container.all():
        props['containers'].append(serialize_sample_mg_container_full(c))
    return props

def serialize_sample_mg_container_full(node):
    props = node.__properties__
    return node.__properties__

class SampleMgList(APIView):
    def get(self, params):
        print('GETTING NODES')
        mg_sample_full = []
        s = SampleMg.nodes.all()
        print(s)
        for node in s:
            mg_sample_full.append(serialize_sample_mg_full(node))

        print('samples')
        return HttpResponse(json.dumps(mg_sample_full), content_type='application/json')

def serialize_source(node):
    return  node.__properties__

class SourceList(APIView):
    def get(self, params):
        sources = Source.nodes.all()
        sources_list = []
        for s in sources:
            sources_list.append(serialize_source(s))

        return HttpResponse(json.dumps(sources_list), content_type='application/json')

    def post(self, request):
        data = request.data
        s = Source(name=data['name'], description=data['description']).save()

        return HttpResponse(json.dumps(serialize_source(s)), content_type='application/json')