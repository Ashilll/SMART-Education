from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Student, Course, Enrollment, Grade, Teacher, Document, ChatMessage  # ← ДОБАВЬ ChatMessage
from .forms import EnrollmentForm, GradeForm, StudentForm, CourseForm, TeacherForm, DocumentForm, ChatMessageForm  # ← ДОБАВЬ ChatMessageForm
from django.contrib import messages

def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_teachers = Teacher.objects.count()
    
    grades = Grade.objects.filter(score__isnull=False)
    avg_score = grades.aggregate(avg=models.Avg('score'))['avg'] or 0
    
    top_students = Student.objects.annotate(
        avg_grade=models.Avg('enrollments__grade__score')
    ).filter(avg_grade__isnull=False).order_by('-avg_grade')[:5]
    
    courses_stats = Course.objects.annotate(
        student_count=models.Count('enrollments'),
        avg_grade=models.Avg('enrollments__grade__score')
    )
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_teachers': total_teachers,
        'avg_score': round(float(avg_score), 2),
        'top_students': top_students,
        'courses_stats': courses_stats,
    }
    return render(request, 'students/dashboard.html', context)

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrollments = student.enrollments.select_related('course').all()
    return render(request, 'students/student_detail.html', {'student': student, 'enrollments': enrollments})

def course_list(request):
    courses = Course.objects.select_related('teacher').all()
    return render(request, 'students/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = course.enrollments.select_related('student').all()

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.course = course
            try:
                enrollment.save()
                messages.success(request, 'Студент успешно записан на курс')
                return redirect('course_detail', course_id=course.id)
            except:
                messages.error(request, 'Ошибка: этот студент уже записан')
    else:
        form = EnrollmentForm()

    return render(request, 'students/course_detail.html', {
        'course': course,
        'enrollments': enrollments,
        'form': form
    })

def update_grade(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    try:
        grade = enrollment.grade
    except Grade.DoesNotExist:
        grade = None

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            g = form.save(commit=False)
            g.enrollment = enrollment
            g.save()
            messages.success(request, 'Оценка сохранена')
            return redirect('course_detail', course_id=enrollment.course.id)
    else:
        form = GradeForm(instance=grade)

    return render(request, 'students/update_grade.html', {'form': form, 'enrollment': enrollment})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Студент успешно добавлен!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно добавлен!')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'students/add_course.html', {'form': form})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Преподаватель успешно добавлен!')
            return redirect('course_list')
    else:
        form = TeacherForm()
    return render(request, 'students/add_teacher.html', {'form': form})

# 📁 ФУНКЦИИ ДЛЯ ФАЙЛОВ
def document_list(request):
    documents = Document.objects.all().select_related('course').order_by('-uploaded_at')
    return render(request, 'students/document_list.html', {'documents': documents})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            if request.user.is_authenticated:
                document.uploaded_by = request.user
            document.save()
            messages.success(request, 'Файл успешно загружен!')
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'students/upload_document.html', {'form': form})

def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    messages.success(request, 'Файл удален!')
    return redirect('document_list')

def chat_room(request, room_name='general'):
    # ВАЖНО: фильтруем сообщения ТОЛЬКО по текущей комнате
    messages = ChatMessage.objects.filter(room=room_name).order_by('timestamp')[:50]
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            # Используем гостевого пользователя для всех
            from django.contrib.auth.models import User
            try:
                guest_user = User.objects.get(username='guest')
            except User.DoesNotExist:
                # Если пользователя нет - создаем
                guest_user = User.objects.create_user(
                    username='guest',
                    email='guest@test.ru',
                    password='123'
                )
            message.user = guest_user
            message.room = room_name  # ВАЖНО: сохраняем в текущую комнату
            message.save()
            return redirect('chat_room', room_name=room_name)
    else:
        form = ChatMessageForm()
    
    return render(request, 'students/chat_room.html', {
        'messages': messages,
        'form': form,
        'room_name': room_name
    })
def snake_game(request):
    return render(request, 'students/snake_game.html', {
        'page_title': 'Змейка знаний'
    })
def schedule(request):
    return render(request, 'students/schedule.html', {
        'page_title': 'Расписание занятий'
    })