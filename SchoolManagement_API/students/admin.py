from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Students)
admin.site.register(models.Subjects)
admin.site.register(models.Section)
admin.site.register(models.Schedule)
admin.site.register(models.StudentSubject)
admin.site.register(models.SubjectAverage)
