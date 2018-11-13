from django.contrib import admin

# Register your models here.

from .models.data_models import *
from .models.result_models import GeneralResult, ProfileResult
from .models.entry_models import Schema, Entry

admin.site.register(DatasetHard)
admin.site.register(DatasetSoft)

admin.site.register(SampleSource)
admin.site.register(RealSample)

admin.site.register(Library)
admin.site.register(LibrarySample)

admin.site.register(SequencingRun)
admin.site.register(MgSample)
admin.site.register(MgSampleFileContainer)
admin.site.register(MgFile)

admin.site.register(EventType)
admin.site.register(EventData)

admin.site.register(GeneralResult)
admin.site.register(ProfileResult)

admin.site.register(Schema)
admin.site.register(Entry)






