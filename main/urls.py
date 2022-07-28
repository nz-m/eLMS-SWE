from django.urls import path
from . import views

urlpatterns = [
    path('', views.std_login, name='std_login'),
    path('facultyCourses/', views.facultyCourses, name='facultyCourses'),
    path('login/', views.std_login, name='std_login'),
    path('logout/', views.std_logout, name='std_logout'),
    path('faculty/<int:code>/', views.course_page_faculty, name='faculty'),
    path('addAnnouncement/<int:code>/',
         views.addAnnouncement, name='addAnnouncement'),
    path('announecement/<int:code>/<int:id>/',
         views.deleteAnnouncement, name='deleteAnnouncement'),
    path('edit/<int:code>/<int:id>/',
         views.editAnnouncement, name='editAnnouncement'),
    path('update/<int:code>/<int:id>/',
         views.updateAnnouncement, name='updateAnnouncement'),
    path('addAssignment/<int:code>/', views.addAssignment, name='addAssignment'),
    path('course-material/<int:code>/',
         views.addCourseMaterial, name='addCourseMaterial'),
    path('course-material/<int:code>/<int:id>/',
         views.deleteCourseMaterial, name='deleteCourseMaterial'),

]
