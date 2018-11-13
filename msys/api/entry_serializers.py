from rest_framework import serializers
from msys.models.entry_models import *
from django.conf import settings

import requests
import json

class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = '__all__'

class EventDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
