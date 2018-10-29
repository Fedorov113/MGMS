from rest_framework import serializers
from msys.models import *
from django.conf import settings

import requests
import json

class DatasetHardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetHard
        fields = '__all__'

    # coverts to JSON
    # validation for data passed

    def validate_df_name(self, value):
        qs = DatasetHard.objects.filter(df_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("The Dataset name must be unique")
        return value


class RealSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealSample
        fields = '__all__'

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'

class MgFileSerializer(serializers.ModelSerializer):
    container = serializers.PrimaryKeyRelatedField( required=False, queryset=MgSampleFileContainer.objects.all())

    class Meta:
        model = MgFile
        fields = '__all__'

class MgSampleFileContainerSerializer(serializers.ModelSerializer):

    files = MgFileSerializer(many=True)
    mg_sample = serializers.PrimaryKeyRelatedField(required=False, queryset=MgSample.objects.all())

    class Meta:
        model = MgSampleFileContainer
        # fields = ['files', 'preprocessing']
        fields = '__all__'
        extra_fields = ['files', 'reads_total', 'bps_total']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(MgSampleFileContainerSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
    #
    # def create(self, validated_data):
    #     print('creating file container in it')
    #     if 'files' in validated_data.keys():
    #
    #         files_data = validated_data.pop('files')
    #         print(files_data)
    #         container = MgSampleFileContainer.objects.create(**validated_data)
    #
    #         for file_data in files_data:
    #             MgFile.objects.create(container=container, **file_data)
    #
    #         return container
    #     else:
    #         return MgSampleFileContainer.objects.create(**validated_data)


class MgSampleSerializer(serializers.ModelSerializer):

    containers = MgSampleFileContainerSerializer(many=True)

    class Meta:
        model = MgSample
        fields = '__all__'
        extra_fields = ['containers']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(MgSampleSerializer, self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def create(self, validated_data):
        if 'containers' in validated_data.keys():
            containers_data = validated_data.pop('containers')
            mg_sample = MgSample.objects.create(**validated_data)

            for container_data in containers_data:
                if 'files' in container_data.keys():
                    files_data = container_data.pop('files')
                    cont = MgSampleFileContainer.objects.create(mg_sample=mg_sample, **container_data)
                    for file_data in files_data:
                        new_file = MgFile.objects.create(container=cont, **file_data)

                        url = settings.ASSHOLE_URL+'/api/fs/sample/import/'

                        post_data={
                            'orig_file': new_file.orig_file_location,
                            'hdf_name': mg_sample.dataset_hard.df_name,
                            'new_name': mg_sample.name_on_fs+'_'+new_file.strand,
                            'sample': mg_sample.name
                        }

                        r = requests.post(url, data = json.dumps(post_data))

                        success = r.json().get('success')
                        print(success)
                        print(type(success) == bool)

                        if success:
                            new_file.import_success = True
                            new_file.save()

            return mg_sample
        else:
            return MgSample.objects.create(**validated_data)

