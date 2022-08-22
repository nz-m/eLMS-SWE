from django.db import models
from main.models import Student, Course

# Create your models here.
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')], default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_absence = models.IntegerField(default=0)


    def __str__(self):
        return self.student.name + ' - ' + self.course.name + ' - ' + self.date.strftime('%d-%m-%Y')
