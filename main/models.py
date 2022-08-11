from django.db import models
# Create your models here.


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    department = models.CharField(max_length=100, null=False)
    role = models.CharField(
        default="Student", max_length=100, null=False, blank=True)
    course = models.ManyToManyField(
        'Course', related_name='students', blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_student.png')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_student.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name


class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)
    department = models.CharField(max_length=100, null=False)
    role = models.CharField(
        default="Faculty", max_length=100, null=False, blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,
                              null=False, default='profile_pics/default_faculty.png')

    def delete(self, *args, **kwargs):
        if self.photo != 'profile_pics/default_faculty.png':
            self.photo.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    department = models.CharField(max_length=100, null=False)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    studentKey = models.IntegerField(null=False, unique=True)
    facultyKey = models.IntegerField(null=False, unique=True)

    class Meta:
        unique_together = ('code', 'department', 'name')
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.name


class Announcement(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-datetime']

    def __str__(self):
        return self.title


class Assignment(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    deadline = models.DateTimeField(null=False)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    marks = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to='submissions/', null=True,)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    marks = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.student.name + " - " + self.assignment.title

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name_plural = "Submissions"
        ordering = ['datetime']


class Material(models.Model):
    course_code = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=2000, null=False)
    datetime = models.DateTimeField(auto_now_add=True, null=False)
    file = models.FileField(upload_to='materials/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Materials"
        ordering = ['-datetime']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
