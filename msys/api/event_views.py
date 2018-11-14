from rest_framework import generics, mixins, viewsets
from rest_framework.generics import get_object_or_404

from django.db.models import Q

# class EventDataList(generics.ListCreateAPIView):  # Detail View
#     queryset = EventData.objects.all()
#     serializer_class = EventDataSerializer
#
# class EventSchemaList(generics.ListCreateAPIView):  # Detail View
#     queryset = SchemaOld.objects.all()
#     serializer_class = SchemaSerializer
#
# class EventTypeList(generics.ListCreateAPIView):  # Detail View
#     queryset = EventType.objects.all()
#     serializer_class = EventTypeSerializer