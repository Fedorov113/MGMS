from django.urls import path
from msys.api.entry_views import *


urlpatterns = [
    path('schema_expanded/', SchemaView.as_view()),

    path('schema/', SchemaList.as_view()),
    path('schema_json/<str:schema_name>/', SchemaJson.as_view()),

]
