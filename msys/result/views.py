import json

import requests
from rest_framework.views import APIView
from django.http import HttpResponse

from mgms import settings
from msys.models.result_models import GeneralResult

class ResultView(APIView):
    def post(self, request):
        data = request.data

        print(data['input'])
        print(data['result'])

        gr = GeneralResult(name=data['result'], input=json.dumps(data['input']), raw_res=json.dumps(data['raw_res']))
        gr.save()
        return HttpResponse(json.dumps('At least we are here'), content_type='application/json')

class ResultRequest(APIView):
    """
    Accepts result request for one result.
    """
    def post(self, request):

        data = json.loads(request.body)
        res = data['desired_results']
        print(res)

        input_objects = res['input_objects']
        # Need to manually create query for every input object type?
        # Here we check what exists and db and what not
        for i, input in enumerate(res['input']):
            if input_objects[0] == 'MgSampleFile':
                input_obj = data_models.MgFile.objects.filter(
                    strand=input[input_objects[0]]['strand'],
                    container__preprocessing=input[input_objects[0]]['preproc'],
                    container__mg_sample__name_on_fs=input[input_objects[0]]['sample'],
                    container__mg_sample__dataset_hard__df_name=input[input_objects[0]]['df']
                )

                if len(list(input_obj)) == 1:
                    print(list(input_obj)[0])

                else:
                    print('len: ' + str(len(list(input_obj))))

        # Make request to asshole
        url = settings.ASSHOLE_URL + '/explorer/request_result/'
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        return HttpResponse(json.dumps({'res': 'dev'}), content_type='application/json')
