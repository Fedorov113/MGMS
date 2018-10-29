import json

from django.http import HttpResponse
from rest_framework.views import APIView

from msys.models import *


class ResultView(APIView):
    def post(self, request, type_of_res):
        data = request.data

        print(type_of_res)

        sample = MgSample.objects.get(name_on_fs=data['input']['name_on_fs'])
        container = MgSampleFileContainer.objects.filter(mg_sample=sample).get(preprocessing=data['input']['preproc'])
        mg_file = MgFile.objects.get(container=container, strand=data['input']['strand'])

        mg_file.reads = data['result']['reads']
        mg_file.bps = data['result']['bp']
        mg_file.save()

        return HttpResponse(json.dumps('At least we are here'), content_type='application/json')