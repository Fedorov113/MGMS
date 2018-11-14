from django.urls import path

from msys.result.views import ResultRequest
from msys.result.views import ResultView
from msys.api.event_views import *
from msys.api.entry_views import *


urlpatterns = [

    path('result/', ResultView.as_view()),
    path('result_request/', ResultRequest.as_view()),


    path('schema_expanded/', SchemaView.as_view()),

    path('schema/', SchemaList.as_view()),
    path('schema_json/<str:schema_name>/', SchemaJson.as_view()),

]
