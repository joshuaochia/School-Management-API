from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Students)
admin.site.register(models.StudentSubject)
admin.site.register(models.Project)
admin.site.register(models.Assignment)
admin.site.register(models.FileAssignment)
admin.site.register(models.FileProject)
admin.site.register(models.TeacherSubject)