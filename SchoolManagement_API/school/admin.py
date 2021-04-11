from django.contrib import admin
from .models import (
    School, Policies, Department, Courses,
    Employees
    )


admin.site.register(School)
admin.site.register(Policies)
admin.site.register(Department)
admin.site.register(Courses)
admin.site.register(Employees)
