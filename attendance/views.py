from django.shortcuts import render, redirect
from . models import Attendance
from main.models import Student, Course

# REFACTORING NEEDED
# AUTHORIZATION CHECK NEEDED


def attendance(request, code):
    course = Course.objects.get(code=code)
    students = Student.objects.filter(course=code)
    return render(request, 'attendance/attendance.html', {'students': students,'course': course})
 

def loadStudents(request, code):
    students = Student.objects.filter(course=code)
    course = Course.objects.get(code=code)
    date = request.POST.get('date')
    for student in students:
        # check if attendance record exists for the student and date
        attendance_record = Attendance.objects.filter(student=student, date=date)
        if attendance_record.count() == 0:
            # if not, create a new attendance record
            attendance = Attendance(student=student, date=date, course = course)
            attendance.save()
    addendance_data = Attendance.objects.filter(course=course, date=date)
    # get absent count for each student with at least one attendance record having status 'P' as by default all attendance records have status 'A'
    for attendance in addendance_data:
        if attendance.status == 'P':
            attendance.total_absence = 0
        else:
            attendance.total_absence = Attendance.objects.filter(student=attendance.student, date=date, status='A').count()
        attendance.save()

    return render(request, 'attendance/attendance.html', {'attendance_data': addendance_data,'course': course})


def submitAttendance(request, code, date):
    attendance_list = request.POST.getlist('checkbox')
    for attendance in attendance_list:
        attendance_record = Attendance.objects.get(id=attendance)
        attendance_record.status = 'P'
        attendance_record.date = date
        attendance_record.save()
    return redirect('attendance', code=code)

    


    

    
    
    