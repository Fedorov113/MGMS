from django.db import models
import json
import base64
from django.core.files.base import ContentFile

# from .data_models import MgFile


class GeneralResult(models.Model):
    name = models.CharField(max_length=256)

    # JSON representation of input
    input = models.TextField()
    # JSON - stored only if no specific model is defined
    raw_res = models.TextField()

    def save(self, *args, **kwargs):
        print('IN GENERAL SAVE')
        super().save(*args, **kwargs)
        result_model = globals()[self.name.capitalize() + 'Result']
        result_instance = result_model()
        # try:
        result_instance.save(input=self.input, raw_res=self.raw_res, gr=self.pk)
        # self.raw_res = '{}'
        # except:
        #     print('ERROR')
        # super().save(*args, **kwargs)


def fastqc_img_path(instance, filename):
    return '{df}/{preproc}/{sample}/{strand}/fastqc/{file}.png'.format(
        df=instance.mg_file.container.mg_sample.dataset_hard.df_name,
        preproc=instance.mg_file.container.preprocessing,
        sample=instance.mg_file.container.mg_sample.name_on_fs,
        strand=instance.mg_file.strand,
        file=filename)


class ProfileResult(models.Model):
    # mg_file = models.ForeignKey(MgFile, on_delete=models.CASCADE)
    general_result = models.ForeignKey(GeneralResult, on_delete=models.CASCADE)

    bp = models.IntegerField()
    reads = models.IntegerField()

    file_type = models.CharField(max_length=128)
    encoding = models.CharField(max_length=128)
    seq_len = models.CharField(max_length=128)

    basic_statistics = models.CharField(max_length=10)
    per_base_seq_qual = models.CharField(max_length=10)
    per_seq_qual_scores = models.CharField(max_length=10)
    per_base_seq_cont = models.CharField(max_length=10)
    per_sec_gc = models.CharField(max_length=10)
    per_base_n = models.CharField(max_length=10)
    seq_len_dist = models.CharField(max_length=10)
    seq_dupl_levels = models.CharField(max_length=10)
    overrepresented = models.CharField(max_length=10)
    adapter_cont = models.CharField(max_length=10)

    adapter_content_img = models.ImageField(upload_to=fastqc_img_path)
    duplication_levels = models.ImageField(upload_to=fastqc_img_path)
    per_base_n_content = models.ImageField(upload_to=fastqc_img_path)
    per_base_quality = models.ImageField(upload_to=fastqc_img_path)
    per_base_sequence_content = models.ImageField(upload_to=fastqc_img_path)
    per_sequence_gc_content = models.ImageField(upload_to=fastqc_img_path)
    per_sequence_quality = models.ImageField(upload_to=fastqc_img_path)
    sequence_length_distribution = models.ImageField(upload_to=fastqc_img_path)

    def save(self, *args, **kwargs):
        input_obj = json.loads(kwargs.pop('input'))
        raw_res = json.loads(kwargs.pop('raw_res'))

        input_obj = input_obj['MgSampleFile']
        input_obj = MgFile.objects.get(
            strand=input_obj['strand'],
            container__preprocessing=input_obj['preproc'],
            container__mg_sample__name_on_fs=input_obj['sample'],
            container__mg_sample__dataset_hard__df_name=input_obj['df']
        )

        self.mg_file = input_obj
        gr = kwargs.pop('gr')
        gr_o = GeneralResult.objects.get(pk=gr)
        self.general_result = gr_o


        self.bp = raw_res['bp']
        self.reads = raw_res['reads']

        self.file_type = raw_res['File type']
        self.encoding = raw_res['Encoding']
        self.seq_len = raw_res['Sequence length']

        self.basic_statistics = raw_res['Basic Statistics']
        self.per_base_seq_qual = raw_res['Per base sequence quality']
        self.per_seq_qual_scores = raw_res['Per sequence quality scores']
        self.per_base_seq_cont = raw_res['Per base sequence content']
        self.per_sec_gc = raw_res['Per sequence GC content']
        self.per_base_n = raw_res['Per base N content']
        self.seq_len_dist = raw_res['Sequence Length Distribution']
        self.seq_dupl_levels = raw_res['Sequence Duplication Levels']
        self.overrepresented = raw_res['Overrepresented sequences']
        self.adapter_cont = raw_res['Adapter Content']

        # [2:-1] because strip b'*' from str
        self.adapter_content_img = ContentFile(base64.b64decode(raw_res['adapter_content'][2:-1]), name='adapter_content')
        self.duplication_levels = ContentFile(base64.b64decode(raw_res['duplication_levels'][2:-1]), name='duplication_levels')
        self.per_base_n_content = ContentFile(base64.b64decode(raw_res['per_base_n_content'][2:-1]), name='per_base_n_content')
        self.per_base_quality = ContentFile(base64.b64decode(raw_res['per_base_quality'][2:-1]), name='per_base_quality')
        self.per_base_sequence_content = ContentFile(base64.b64decode(raw_res['per_base_sequence_content'][2:-1]), name='per_base_sequence_content')
        self.per_sequence_gc_content = ContentFile(base64.b64decode(raw_res['per_sequence_gc_content'][2:-1]), name='per_sequence_gc_content')
        self.per_sequence_quality = ContentFile(base64.b64decode(raw_res['per_sequence_quality'][2:-1]), name='per_sequence_quality')
        self.sequence_length_distribution = ContentFile(base64.b64decode(raw_res['sequence_length_distribution'][2:-1]), name='sequence_length_distribution')

        super().save(*args, **kwargs)  # Call the "real" save() method.

