from django.urls import path

from .views import *

urlpatterns = [
    path('sample_mg/', SampleMgList.as_view()),
    path('source/', SourceList.as_view()),
]
