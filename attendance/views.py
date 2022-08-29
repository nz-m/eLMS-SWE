from django.contrib import messages
from django.shortcuts import render, redirect
from . models import Attendance
from main.models import Student, Course, Faculty
from main.views import is_faculty_authorised


def attendance(request, code):
    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        students = Student.objects.filter(course__code=code)

        return render(request, 'attendance/attendance.html', {'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course)})


def createRecord(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            date = request.POST['dateCreate']
            course = Course.objects.get(code=code)
            students = Student.objects.filter(course__code=code)
            # check if attendance record already exists for the date
            if Attendance.objects.filter(date=date, course=course).exists():
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course), 'error': "Attendance record already exists for the date " + date})
            else:
                for student in students:
                    attendance = Attendance(
                        student=student, course=course, date=date, status=False)
                    attendance.save()

                messages.success(
                    request, 'Attendance record created successfully for the date ' + date)
                return redirect('/attendance/' + str(code))
        else:
            return redirect('/attendance/' + str(code))
    else:
        return redirect('std_login')


def loadAttendance(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST':
            date = request.POST['date']
            course = Course.objects.get(code=code)
            students = Student.objects.filter(course__code=code)
            attendance = Attendance.objects.filter(course=course, date=date)
            # check if attendance record exists for the date
            if attendance.exists():
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course), 'attendance': attendance, 'date': date})
            else:
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course), 'error': 'Could not load. Attendance record does not exist for the date ' + date})

    else:
        return redirect('std_login')


def submitAttendance(request, code):
    if is_faculty_authorised(request, code):
        try:
            students = Student.objects.filter(course__code=code)
            course = Course.objects.get(code=code)
            if request.method == 'POST':
                date = request.POST['datehidden']
                for student in students:
                    attendance = Attendance.objects.get(
                        student=student, course=course, date=date)
                    if request.POST.get(str(student.student_id)) == '1':
                        attendance.status = True
                    else:
                        attendance.status = False
                    attendance.save()
                messages.success(
                    request, 'Attendance record submitted successfully for the date ' + date)
                return redirect('/attendance/' + str(code))

            else:
                return render(request, 'attendance/attendance.html', {'code': code, 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course)})
        except:
            return render(request, 'attendance/attendance.html', {'code': code, 'error': "Error! could not save", 'students': students, 'course': course, 'faculty': Faculty.objects.get(course=course)})
