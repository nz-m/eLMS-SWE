from django.shortcuts import render, redirect
from .models import Quiz, Question,StudentAnswer

from main.models import Course


# AUTHORIZATION CHECK NEEDED, IMPORT AUTH FUNCTIONS



# Create your views here.
def quiz(request, code):
    course = Course.objects.get(code=code)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start = request.POST.get('start')
        end = request.POST.get('end')
        quiz = Quiz(title=title, description=description, start=start, end=end, course=course)
        quiz.save()
        return redirect('addQuestion', code=code, quiz_id=quiz.id)
    return render(request, 'quiz/quiz.html', {'course': course})

def addQuestion(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answer = request.POST.get('answer')
      
        question = Question(question=question, option1=option1, option2=option2, option3=option3, option4=option4, answer=answer, quiz=quiz)
        question.save()
    if 'saveOnly' in request.POST:
        return redirect('allQuizzes', code=code)
    return render(request, 'quiz/addQuestion.html', {'course': course, 'quiz': quiz})

       
def allQuizzes(request,code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)
    for quiz in quizzes:
        quiz.total_questions = Question.objects.filter(quiz=quiz).count()
    return render(request, 'quiz/allQuizzes.html', {'course': course, 'quizzes': quizzes})
   

def quizSummary(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz/quizSummary.html', {'course': course, 'quiz': quiz, 'questions': questions}) 

def myQuizzes(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)
    for quiz in quizzes:
        quiz.total_questions = Question.objects.filter(quiz=quiz).count()
        total_marks = 0
        for question in Question.objects.filter(quiz=quiz):
            total_marks += question.marks
        quiz.total_marks = total_marks
    return render(request, 'quiz/myQuizzes.html', {'course': course, 'quizzes': quizzes})
        
    
    



