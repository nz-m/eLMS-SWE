from django.urls import path
from . import views

urlpatterns = [
    path('attendance/<int:code>', views.attendance, name='attendance'),
    path('createRecord/<int:code>', views.createRecord, name='createRecord'),
    path('submitAttendance/<int:code>',
         views.submitAttendance, name='submitAttendance'),
    path('loadAttendance/<int:code>', views.loadAttendance, name='loadAttendance'),
]
