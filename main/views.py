from django.shortcuts import render

# Create your views here.
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


# Display all courses (student view)
def myCourses(request):
    try:
        if request.session.get('student_id'):
            student = Student.objects.get(
                student_id=request.session['student_id'])
            courses = student.course.all()
            faculty = student.course.all().values_list('faculty_id', flat=True)

            context = {
                'courses': courses,
                'student': student,
                'faculty': faculty
            }

            return render(request, 'main/myCourses.html', context)
        else:
            return redirect('std_login')
    except:
        return render(request, 'error.html')


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