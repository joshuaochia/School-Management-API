from django.contrib import admin
from . import models

admin.site.register(models.StudentBalance)
admin.site.register(models.StudentPayment)
admin.site.register(models.EmployeeSalary)
admin.site.register(models.EmployeeOT)
admin.site.register(models.EmployeeLeave)
admin.site.register(models.SchoolPayedHolidays)
