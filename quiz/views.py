import datetime
from django.shortcuts import render, redirect
from .models import Quiz, Question, StudentAnswer
from main.models import Student, Course


# AUTHORIZATION CHECK NEEDED, IMPORT AUTH FUNCTIONS


# Create your views here.
def quiz(request, code):
    course = Course.objects.get(code=code)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start = request.POST.get('start')
        end = request.POST.get('end')
        quiz = Quiz(title=title, description=description,
                    start=start, end=end, course=course)
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
        marks = request.POST.get('marks')

        question = Question(question=question, option1=option1, option2=option2,
                            option3=option3, option4=option4, answer=answer, marks=marks, quiz=quiz)
        question.save()
    if 'saveOnly' in request.POST:
        return redirect('allQuizzes', code=code)
    return render(request, 'quiz/addQuestion.html', {'course': course, 'quiz': quiz})


def allQuizzes(request, code):
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


# REFACTOR NEEDED
def myQuizzes(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)
    student = Student.objects.get(student_id=request.session['student_id'])

    active_quizzes = []
    previous_quizzes = []

    for quiz in quizzes:
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz)
        if quiz.end < datetime.datetime.now() or student_answers.count() > 0:
            previous_quizzes.append(quiz)
        else:
            active_quizzes.append(quiz)
    # get total marks for each quiz
    for activeQuiz in active_quizzes:
        total_marks = 0
        for student_answer in StudentAnswer.objects.filter(student=student, quiz=activeQuiz):
            if student_answer.answer == student_answer.question.answer:
                total_marks += 1
        activeQuiz.total_marks = total_marks
    for previousQuiz in previous_quizzes:
        total_marks = 0
        for student_answer in StudentAnswer.objects.filter(student=student, quiz=previousQuiz):
            if student_answer.answer == student_answer.question.answer:
                total_marks += 1
        previousQuiz.total_marks = total_marks

    # get correct answers for each previous quiz
    for previousQuiz in previous_quizzes:
        correct_answers = 0
        for student_answer in StudentAnswer.objects.filter(student=student, quiz=previousQuiz):
            if student_answer.answer == student_answer.question.answer:
                correct_answers += 1
        previousQuiz.correct_answers = correct_answers
    # get total question for each previous quiz and active quiz
    for previousQuiz in previous_quizzes:
        previousQuiz.total_questions = Question.objects.filter(
            quiz=previousQuiz).count()
    for activeQuiz in active_quizzes:
        activeQuiz.total_questions = Question.objects.filter(
            quiz=activeQuiz).count()

    return render(request, 'quiz/myQuizzes.html', {'course': course, 'active_quizzes': active_quizzes, 'previous_quizzes': previous_quizzes})



def startQuiz(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quiz/portalStdNew.html', {'course': course, 'quiz': quiz, 'questions': questions})


def studentAnswer(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    # get student instance from session
    student = Student.objects.get(student_id=request.session['student_id'])
    # get student answer from forM OF RADIO BUTTONS NAME = QUESTION_ID
    for question in questions:
        answer = request.POST.get(str(question.id))
        student_answer = StudentAnswer(
            student=student, question=question, answer=answer, quiz=quiz)
        student_answer.save()
    # redirect to myQuizzes
    return redirect('myQuizzes', code=code)


def quizResult(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    student = Student.objects.get(student_id=request.session['student_id'])
    student_answers = StudentAnswer.objects.filter(
        student=student, quiz=quiz)
    total_marks = 0
    for student_answer in student_answers:
        if student_answer.answer == student_answer.question.answer:
            total_marks += 1
    # add student answer to questions
    for question in questions:
        student_answer = StudentAnswer.objects.get(
            student=student, question=question)
        question.student_answer = student_answer.answer
    return render(request, 'quiz/quizResult.html', {'course': course, 'quiz': quiz, 'questions': questions, 'total_marks': total_marks})
