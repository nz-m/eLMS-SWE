from django.db import models
from main.models import Student, Course

# Create your models here.


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    status = models.BooleanField(default=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name + ' - ' + self.course.name + ' - ' + self.date.strftime('%d-%m-%Y')

    def total_absent(self):
        attendance = Attendance.objects.filter(
            student=self.student, status=False).count()
        if attendance == 0:
            return attendance
        else:
            return attendance - 1

    def total_present(self):
        present = Attendance.objects.filter(
            student=self.student, status=True).count()
        if present == 0:
            return present
        else:
            return present - 1
