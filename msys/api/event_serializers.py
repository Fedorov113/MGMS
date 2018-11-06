from rest_framework import serializers
from msys.models.data_models import *
from django.conf import settings

import requests
import json

class EventSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchema
        fields = '__all__'

class EventDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventData
        fields = '__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'
