from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.PositiveIntegerField(help_text='Длительность в часах', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_avg_color(self):
        # Этот метод будет использоваться в дашборде для цвета среднего балла
        avg = self.avg_grade  # это поле создается аннотацией в views.py
        if avg is None:
            return 'secondary'
        elif avg >= 90:
            return 'success'
        elif avg >= 70:
            return 'info'
        elif avg >= 50:
            return 'warning'
        else:
            return 'danger'

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} → {self.course}"

class Grade(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='grade')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comment = models.TextField(blank=True)

    def get_score_color(self):
        if self.score is None:
            return 'secondary'  # серый если нет оценки
        score_float = float(self.score)  # конвертируем Decimal в float для сравнения
        if score_float >= 90:
            return 'success'    # темно-зеленый (90-100)
        elif score_float >= 70:
            return 'info'       # светло-зеленый/голубой (70-89) 
        elif score_float >= 50:
            return 'warning'    # желтый (50-69)
        else:
            return 'danger'     # красный (0-49)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.course} : {self.score}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.course.title} - {self.get_day_of_week_display()} {self.start_time}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_overdue(self):
        from django.utils import timezone
        return timezone.now() > self.due_date
    
class Document(models.Model):
    DOCUMENT_TYPES = [
        ('lecture', 'Лекция'),
        ('assignment', 'Задание'),
        ('material', 'Учебный материал'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    file_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other', verbose_name="Тип файла")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Курс")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    
    def __str__(self):
        return self.title
    
    def get_file_icon(self):
        icons = {
            'pdf': '📕',
            'doc': '📄',
            'docx': '📄',
            'xls': '📊',
            'xlsx': '📊',
            'ppt': '📽️',
            'pptx': '📽️',
            'jpg': '🖼️',
            'png': '🖼️',
            'zip': '📦',
        }
        ext = self.file.name.split('.')[-1].lower()
        return icons.get(ext, '📁')
    
    def get_file_size(self):
        try:
            size = self.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except:
            return "Unknown"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=100, default='general')  # можно по курсам
    
    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"