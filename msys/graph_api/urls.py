from django.urls import path

from .views import *

urlpatterns = [
    path('study/', StudyList.as_view()),
    path('study/<str:study>/source/', SourceList.as_view()),
    path('source/<str:source>/entries/', AddEntry.as_view()),

    path('source/', SourceList.as_view()),

    path('disease/', DiseaseList.as_view()),

    path('add_entry/', AddEntry.as_view()),



    path('sample_mg/', SampleMgList.as_view()),
    path('test/', Test.as_view()),

]
