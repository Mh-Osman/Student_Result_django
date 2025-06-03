from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('institution/', views.institution, name='institution'),
    # path('institution/<name>/', views.institution, name='institution'),
    path('institution/<name>/<uid>/', views.institution, name='institution'),
    path('add_student/<name>/<uid>/', views.add_student, name='add_student'),
    path('students/<roll>/', views.students, name='students'),

]
