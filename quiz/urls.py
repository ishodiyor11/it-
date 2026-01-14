from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('take/<int:subject_id>/', views.take_quiz, name='take-quiz'),
]
