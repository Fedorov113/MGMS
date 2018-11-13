from django.db import models
from .data_models import SampleSource
from mptt.models import MPTTModel, TreeForeignKey


class Schema(MPTTModel):
    name = models.CharField(max_length=128, unique=True)
    # JSON
    schema = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Entry(MPTTModel):
    source = models.ForeignKey(SampleSource, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    # JSON
    data = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')




    OBSERVATION = 'OBSERVATION' # for recording information from the patient's world - anything measured by a clinician,
    #  a laboratory or by them, or reported by the patient as a symptom, event or concern
    EVALUATION = 'EVALUATION' # for recording opinions and summary statements (usually clinical), such as problems,
    # diagnoses, risk assessments, goals etc that are generally based on Observation evidence
    INSTRUCTION = 'INSTRUCTION' # for recording orders, prescriptions, directives and any other requested interventions
    ACTION = 'ACTION' # for recording actions, which may be due to Instructions, e.g. drug administrations, procedures etc.
    ADMIN_ENTRY = 'ADMIN_ENTRY' # for recording administrative events, e.g. admission, discharge, consent etc
    ENTRY_TYPES = (
        (OBSERVATION, 'OBSERVATION'),
        (EVALUATION, 'EVALUATION'),
        (INSTRUCTION, 'INSTRUCTION'),
        (ACTION, 'ACTION'),
        (ADMIN_ENTRY, 'ADMIN_ENTRY')
    )
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES, default=OBSERVATION)
    #
    def __str__(self):
        return self.source.source_name+'__'+self.schema.name