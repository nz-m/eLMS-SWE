from django.urls import path
from . import views

urlpatterns = [
    path('attendance/<int:code>', views.attendance, name='attendance'),
    path('loadStudents/<int:code>', views.loadStudents, name='loadStudents'),
    path('submitAttendance/<int:code>/<str:date>', views.submitAttendance, name='submitAttendance'),
]