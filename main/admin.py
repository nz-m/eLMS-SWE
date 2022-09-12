from django.contrib import admin

# Register your models here.
from .models import Student, Faculty, Course, Department, Assignment

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Assignment)
