from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import (
    StudentViewSet, CourseViewSet, TeacherViewSet,
    EnrollmentViewSet, GradeViewSet, DocumentViewSet
)

# Создаем router для API
router = DefaultRouter()
router.register(r'api/students', StudentViewSet)
router.register(r'api/courses', CourseViewSet)
router.register(r'api/teachers', TeacherViewSet)
router.register(r'api/enrollments', EnrollmentViewSet)
router.register(r'api/grades', GradeViewSet)
router.register(r'api/documents', DocumentViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enrollment/<int:enrollment_id>/grade/', views.update_grade, name='update_grade'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('snake-game/', views.snake_game, name='snake_game'),
    path('schedule/', views.schedule, name='schedule'),
    path('snake-game/', views.snake_game, name='snake_game'),
    # API URLs
    path('', include(router.urls)),
]