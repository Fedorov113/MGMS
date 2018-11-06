from django.urls import path

from msys.api.event_views import *

urlpatterns = [

    path('event_type/', EventTypeList.as_view()),
    path('event_data/', EventDataList.as_view()),
    path('event_schema/', EventSchemaList.as_view()),

]
