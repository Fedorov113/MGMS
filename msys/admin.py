from django.contrib import admin

# Register your models here.

from .models.result_models import GeneralResult, ProfileResult
from .models.entry_models import Schema



admin.site.register(GeneralResult)
admin.site.register(ProfileResult)

admin.site.register(Schema)






