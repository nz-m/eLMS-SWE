from django.contrib import admin


from .models import Student, Faculty, Course ,Announcement, Assignment, Submission, Material

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Announcement)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Material)

