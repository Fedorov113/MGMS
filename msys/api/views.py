from rest_framework import generics, mixins, viewsets
from rest_framework.generics import get_object_or_404

from msys.models import DatasetHard
from msys.api.serializers import *
from django.db.models import Q


class DatasetHardList(generics.ListCreateAPIView):  # Detail View
    queryset = DatasetHard.objects.all()
    serializer_class = DatasetHardSerializer

class DatasetHardDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = DatasetHard.objects.all()
    serializer_class = DatasetHardSerializer

class LibraryList(generics.ListCreateAPIView):  # Detail View
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class LibraryDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class MgSampleList(generics.ListCreateAPIView):
    serializer_class = MgSampleSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        #print(kwargs.get('data'))

        return super(MgSampleList, self).get_serializer(*args, **kwargs)


    def get_queryset(self):
        qs = MgSample.objects.all()
        if 'pk' in self.kwargs:
            hard_df_pk = self.kwargs['pk']
            if hard_df_pk is not None:
                qs = qs.filter(
                    Q(dataset_hard=hard_df_pk)
                ).distinct()
        return qs

class MgSampleDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = MgSample.objects.all()
    serializer_class = MgSampleSerializer

class RealSampleAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = RealSampleSerializer

    def get_queryset(self):
        qs = RealSample.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(df_name__icontains=query) |
                Q(df_description__icontains=query)
            ).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class MgSampleFileContainerList(generics.ListCreateAPIView):  # Detail View
#     queryset = MgSampleFileContainer.objects.all()
#     serializer_class = MgSampleFileContainerSerializer

