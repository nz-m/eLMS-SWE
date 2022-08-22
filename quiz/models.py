
from django.db import models
from main.models import Student, Course

# Create your models here.


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def duration(self):
        return self.end - self.start

    def total_questions(self):
        return Question.objects.filter(quiz=self).count()

    def total_marks(self):
        return Question.objects.filter(quiz=self).aggregate(total_marks=models.Sum('marks'))['total_marks']


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    marks = models.IntegerField(default=0, null=False)
    option1 = models.TextField(null=False, blank=False, default='',)
    option2 = models.TextField(null=False, blank=False, default='')
    option3 = models.TextField(null=False, blank=False, default='')
    option4 = models.TextField(null=False, blank=False, default='')
    answer = models.CharField(max_length=1, choices=(
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='A')

    def __str__(self):
        return self.question

    def get_answer(self):
        case = {
            'A': self.option1,
            'B': self.option2,
            'C': self.option3,
            'D': self.option4,
        }
        return case[self.answer]


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1, choices=(
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')), default='', null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.student.name + ' ' + self.quiz.title + ' ' + self.question.question
