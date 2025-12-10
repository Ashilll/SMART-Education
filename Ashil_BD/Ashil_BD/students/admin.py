from django.contrib import admin
from django.utils.html import format_html
from .models import Student, Teacher, Course, Enrollment, Grade, Announcement

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'photo_preview')
    search_fields = ('name', 'email')
    list_filter = ('age',)

    def photo_preview(self, obj):
        if hasattr(obj, 'photo') and obj.photo:
            return format_html('<img src="{}" width="60" style="border-radius:5px;">', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = "Фото"

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name','email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'teacher', 'duration')
    search_fields = ('title', 'code')
    list_filter = ('teacher',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    search_fields = ('student__name', 'course__title')
    list_filter = ('course',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'score')
    search_fields = ('enrollment__student__name', 'enrollment__course__title')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'visible')
    list_filter = ('visible',)
    search_fields = ('title',)

# Настройки панели администратора
admin.site.site_header = "Панель управления Ashil_BD"
admin.site.site_title = "Админка Ashil_BD"
admin.site.index_title = "Добро пожаловать в Ashil_BD Admin"
