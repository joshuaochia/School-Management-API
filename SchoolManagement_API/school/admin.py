from django.contrib import admin
from .models import (
    School, Policies, Department, Courses,
    Employees, Schedule, Section, Subjects
    )


admin.site.register(School)
admin.site.register(Policies)
admin.site.register(Department)
admin.site.register(Courses)
admin.site.register(Employees)
admin.site.register(Subjects)
admin.site.register(Section)
admin.site.register(Schedule)