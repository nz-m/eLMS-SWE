from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<int:code>', views.quiz, name='quiz'),
    path('addQuestion/<int:code>/<int:quiz_id>', views.addQuestion, name='addQuestion'),
    path('allQuizzes/<int:code>', views.allQuizzes, name='allQuizzes'),
    path('quizSummary/<int:code>/<int:quiz_id>', views.quizSummary, name='quizSummary'),
    path('myQuizzes/<int:code>', views.myQuizzes, name='myQuizzes'),
    path('startQuiz/<int:code>/<int:quiz_id>', views.startQuiz, name='startQuiz'),
    path('studentAnswer/<int:code>/<int:quiz_id>', views.studentAnswer, name='studentAnswer'),
    path('quizResult/<int:code>/<int:quiz_id>', views.quizResult, name='quizResult'),
  
]