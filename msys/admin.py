from django.contrib import admin

# Register your models here.

from .models.data_models import *

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
admin.site.register(Schema)
admin.site.register(EventData)



