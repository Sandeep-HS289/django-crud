from django.urls import path
from . import views 

urlpatterns = [
    path("", views.home, name="home"),
    path('put/<int:id>/',views.home,name='update'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('jsonrequest/',views.jsonresponse,name='jsonapi'),
    path('students/',views.students,name='students'),
    path('student/<int:id>/',views.student,name='student'),
    path('redirect/',views.redirect_example),
    path('query/',views.querystudent),
]