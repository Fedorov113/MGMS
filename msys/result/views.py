import json

import requests
from rest_framework.views import APIView
from django.http import HttpResponse

from mgms import settings
from msys.models.data_models import MgSampleFileContainer, MgFile, MgSample


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

class ResultRequest(APIView):
    def post(self, request):
        data = json.loads(request.body)

        desired_files = []
        for req in data['desired_results']:
                if req['request']['type'] == 'profile':
                    if req['request']['result'] == 'fastqc':
                        if req['input']['type'] == 'reads_file':
                            mg_file = MgFile.objects.get(pk=req['input']['id'])

                            df = str(mg_file.container.mg_sample.dataset_hard)
                            sample_name_on_fs = str(mg_file.container.mg_sample.name_on_fs)
                            preproc = str(mg_file.container.preprocessing)
                            strand = str(mg_file.strand)
                            out_file_wc = 'datasets/{df}/reads/{preproc}/{sample}/profile/{sample}_{strand}_fastqc.zip'
                            out_file = out_file_wc.format(df=df, sample=sample_name_on_fs,
                                                          preproc=preproc, strand=strand)

                            desired_files.append(out_file)
                    elif req['request']['result'] == 'count':
                        if req['input']['type'] == 'file':
                            blabla = []

        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        url = settings.ASSHOLE_URL + "/explorer/celery_snakemake_list/?dry=0&drmaa=1&threads=6&jobs=4"
        data = {'desired_files': desired_files}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(data)

        return HttpResponse (json.dumps({'erf': 'SUCsdfgsdCESS'}), content_type='application/json')