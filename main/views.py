import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Student, Course, Announcement, Assignment, Submission, Material, Faculty
from django.template.defaulttags import register
from django.db.models import Count, Q
from django.http import HttpResponseRedirect


def is_student_authorised(request, code):
    course = Course.objects.get(code=code)
    if request.session.get('student_id') and course in Student.objects.get(student_id=request.session['student_id']).course.all():
        return True
    else:
        return False


def is_faculty_authorised(request, code):
    if request.session.get('faculty_id') and code in Course.objects.filter(faculty_id=request.session['faculty_id']).values_list('code', flat=True):
        return True
    else:
        return False


# Login page for both student and faculty
def std_login(request):
    try:
        # If the user is already logged in, redirect to the course page
        if request.session.get('student_id'):
            return redirect('/my/')
        elif request.session.get('faculty_id'):
            return redirect('/facultyCourses/')
        else:
            # If the user is not logged in, display the login page
            if request.method == 'POST':
                id = request.POST["id"]
                password = (request.POST["password"])
                try:
                    # Checks if id matches any student, if no match found, checks if id matches any faculty
                    if Student.objects.filter(student_id=id).exists():
                        student = Student.objects.get(student_id=id)
                        if str(student.student_id) == id and str(student.password) == password:

                            request.session['student_id'] = id
                            return redirect('myCourses')
                        else:
                            # id matches but student password is wrong
                            messages.error(
                                request, 'Incorrect password. Please try again.', extra_tags='alert')
                            return redirect('std_login')

                    else:
                        # Checks if id matches any faculty
                        if Faculty.objects.filter(faculty_id=id).exists():
                            faculty = Faculty.objects.get(faculty_id=id)
                            if str(faculty.faculty_id) == id and str(faculty.password) == password:
                                request.session['faculty_id'] = id
                                return redirect('facultyCourses')

                            else:
                                # id matches but faculty password is wrong
                                messages.error(
                                    request, 'Incorrect password. Please try again.', extra_tags='alert')
                                return redirect('std_login')
                        else:
                            # id does not match any student or faculty
                            messages.error(
                                request, 'Incorrect user id. Please try again.', extra_tags='alert')
                            return redirect('std_login')
                except:
                    # id does not match any student or faculty
                    messages.error(
                        request, 'Invalid login credentials.', extra_tags='alert')
                    return redirect('std_login')

            else:
                return render(request, 'login_page.html')
    except:
        return render(request, 'error.html')


# Clears the session on logout
def std_logout(request):
    request.session.flush()
    return redirect('std_login')


# Display all courses (faculty view)
def facultyCourses(request):
    try:
        if request.session['faculty_id']:
            faculty = Faculty.objects.get(
                faculty_id=request.session['faculty_id'])
            courses = Course.objects.filter(
                faculty_id=request.session['faculty_id'])
            # Student count of each course to show on the faculty page
            studentCount = Course.objects.all().annotate(student_count=Count('students'))

            studentCountDict = {}

            for course in studentCount:
                studentCountDict[course.code] = course.student_count

            @register.filter
            def get_item(dictionary, course_code):
                return dictionary.get(course_code)

            context = {
                'courses': courses,
                'faculty': faculty,
                'studentCount': studentCountDict
            }

            return render(request, 'main/facultyCourses.html', context)

        else:
            return redirect('std_login')
    except:

        return redirect('std_login')


# Particular course page (faculty view)
def course_page_faculty(request, code):
    course = Course.objects.get(code=code)
    if request.session.get('faculty_id'):
        try:
            announcements = Announcement.objects.filter(course_code=course)
            assignments = Assignment.objects.filter(
                course_code=course.code)
            materials = Material.objects.filter(course_code=course.code)
            studentCount = Student.objects.filter(course=course).count()

        except:
            announcements = None
            assignments = None
            materials = None

        context = {
            'course': course,
            'announcements': announcements,
            'assignments': assignments[:3],
            'materials': materials,
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id']),
            'studentCount': studentCount
        }

        return render(request, 'main/faculty_course.html', context)
    else:
        return redirect('std_login')


def error(request):
    return render(request, 'error.html')


def addAnnouncement(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST' and request.POST['title'] and request.POST['content']:

            course = Course.objects.get(code=code)
            announcement = Announcement(course_code=course, title=request.POST['title'],
                                        description=request.POST['content'])
            announcement.save()
            return redirect('/faculty/' + str(code))
        else:
            return render(request, 'main/announcement.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
    else:
        return redirect('std_login')


def deleteAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code=code, id=id)
            announcement.delete()
            return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')


def editAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        announcement = Announcement.objects.get(course_code_id=code, id=id)
        context = {
            'announcement': announcement,
            'course': Course.objects.get(code=code),
            'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])
        }
        return render(request, 'main/update-announcement.html', context)
    else:
        return redirect('std_login')


def updateAnnouncement(request, code, id):
    if is_faculty_authorised(request, code):
        try:
            announcement = Announcement.objects.get(course_code_id=code, id=id)
            announcement.title = request.POST['title']
            announcement.description = request.POST['content']
            announcement.save()
            return redirect('/faculty/' + str(code))
        except:
            return redirect('/faculty/' + str(code))

    else:
        return redirect('std_login')


def addAssignment(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST' and request.POST['title'] and request.POST['content']:
            try:
                course = Course.objects.get(code=code)
                course_code = course
                title = request.POST['title']
                description = request.POST['content']
                deadline = request.POST['datetime']
                marks = request.POST['marks']
                file = request.FILES['file']
                assignment = Assignment(course_code=course_code, title=title,
                                        description=description, deadline=deadline, marks=marks, file=file)

                assignment.save()
                return redirect('/faculty/' + str(code))
            except:

                return render(request, 'main/assignment.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})

        else:
            return render(request, 'main/assignment.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
    else:
        return redirect('std_login')


def addCourseMaterial(request, code):
    if is_faculty_authorised(request, code):
        if request.method == 'POST' and request.POST['title'] and request.POST['content']:
            try:
                course = Course.objects.get(code=code)
                course_material = Material(course_code=course, title=request.POST['title'],
                                           description=request.POST['content'], file=request.FILES['file'])
                course_material.save()
                return redirect('/faculty/' + str(code))
            except:
                return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
        else:
            return render(request, 'main/course-material.html', {'course': Course.objects.get(code=code), 'faculty': Faculty.objects.get(faculty_id=request.session['faculty_id'])})
    else:
        return redirect('std_login')


def deleteCourseMaterial(request, code, id):
    if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        course_material = Material.objects.get(course_code=course, id=id)
        course_material.delete()
        return redirect('/faculty/' + str(code))
    else:
        return redirect('std_login')
