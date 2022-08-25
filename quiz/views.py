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
        publish_status = request.POST.get('checkbox')
        quiz = Quiz(title=title, description=description, start=start,
                    end=end, publish_status=publish_status, course=course)
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
                            option3=option3, option4=option4, answer=answer, quiz=quiz, marks=marks)

        question.save()
    if 'saveOnly' in request.POST:
        return redirect('allQuizzes', code=code)
    return render(request, 'quiz/addQuestion.html', {'course': course, 'quiz': quiz})


def allQuizzes(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)
    time = datetime.datetime.now()

    for quiz in quizzes:
        quiz.total_questions = Question.objects.filter(quiz=quiz).count()
    return render(request, 'quiz/allQuizzes.html', {'course': course, 'quizzes': quizzes, 'time': time})


def quizSummary(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    obtained_marks = 0
    for question in questions:
        if request.POST.get(question.id) == question.answer:
            obtained_marks += question.marks
    quiz.total_marks_obtained = obtained_marks

    return render(request, 'quiz/quizSummary.html', {'course': course, 'quiz': quiz, 'questions': questions})


# REFACTOR NEEDED
def myQuizzes(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)
    student = Student.objects.get(student_id=request.session['student_id'])
    # check if that student has already attempted this quiz
    for quiz in quizzes:
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz)
        if student_answers.count() > 0:
            quiz.attempted = True
        else:
            quiz.attempted = False

    active_quizzes = []
    previous_quizzes = []

    for quiz in quizzes:
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz)
        if quiz.end < datetime.datetime.now() or student_answers.count() > 0:
            previous_quizzes.append(quiz)
        else:
            active_quizzes.append(quiz)

    for previousQuiz in previous_quizzes:
        total_marks_obtained = 0
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=previousQuiz)

        for student_answer in student_answers:
            total_marks_obtained += student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0
        previousQuiz.total_marks_obtained = total_marks_obtained

        previousQuiz.total_marks = 0
        for question in previousQuiz.question_set.all():
            previousQuiz.total_marks += question.marks

        try:
            previousQuiz.percentage = (
                total_marks_obtained / previousQuiz.total_marks) * 100
            previousQuiz.percentage = round(previousQuiz.percentage, 2)
        except ZeroDivisionError:
            previousQuiz.percentage = 0

    for previousQuiz in previous_quizzes:
        previousQuiz.total_questions = Question.objects.filter(
            quiz=previousQuiz).count()
    for activeQuiz in active_quizzes:
        activeQuiz.total_questions = Question.objects.filter(
            quiz=activeQuiz).count()

    return render(request, 'quiz/myQuizzes.html', {'course': course, 'quizzes': quizzes, 'active_quizzes': active_quizzes, 'previous_quizzes': previous_quizzes})


def startQuiz(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    total_questions = questions.count()

    marks = 0
    for question in questions:
        marks += question.marks
    quiz.total_marks = marks

    return render(request, 'quiz/portalStdNew.html', {'course': course, 'quiz': quiz, 'questions': questions, 'total_questions': total_questions})


def studentAnswer(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    student = Student.objects.get(student_id=request.session['student_id'])

    for question in questions:
        answer = request.POST.get(str(question.id))
        student_answer = StudentAnswer(student=student, quiz=quiz, question=question,
                                       answer=answer, marks=question.marks if answer == question.answer else 0)
        student_answer.save()
    return redirect('myQuizzes', code=code)


def quizResult(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    try:
        student = Student.objects.get(student_id=request.session['student_id'])
        student_answers = StudentAnswer.objects.filter(
            student=student, quiz=quiz)
        total_marks_obtained = 0
        for student_answer in student_answers:
            total_marks_obtained += student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0
        quiz.total_marks_obtained = total_marks_obtained
        quiz.total_marks = 0
        for question in questions:
            quiz.total_marks += question.marks
        quiz.percentage = (total_marks_obtained / quiz.total_marks) * 100
        quiz.percentage = round(quiz.percentage, 2)
    except:
        quiz.total_marks_obtained = 0
        quiz.total_marks = 0
        quiz.percentage = 0

    for question in questions:
        student_answer = StudentAnswer.objects.get(
            student=student, question=question)
        question.student_answer = student_answer.answer
    return render(request, 'quiz/quizResult.html', {'course': course, 'quiz': quiz, 'questions': questions})


def quizSummary(request, code, quiz_id):
    course = Course.objects.get(code=code)
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    time = datetime.datetime.now()
    total_students = Student.objects.filter(course=course).count()
    for question in questions:
        question.A = StudentAnswer.objects.filter(
            question=question, answer='A').count()
        question.B = StudentAnswer.objects.filter(
            question=question, answer='B').count()
        question.C = StudentAnswer.objects.filter(
            question=question, answer='C').count()
        question.D = StudentAnswer.objects.filter(
            question=question, answer='D').count()

    if request.method == 'POST':
        quiz.publish_status = True
        quiz.save()
        return redirect('quizSummary', code=code, quiz_id=quiz.id)
    return render(request, 'quiz/quizSummaryFaculty.html', {'course': course, 'quiz': quiz, 'questions': questions, 'time': time, 'total_students': total_students})
