from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Enrollment, Grade, Student, Course, Teacher, Document, ChatMessage  # ← ДОБАВЬ ChatMessage

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'})
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score', 'comment']
        widgets = {
            'score': forms.NumberInput(attrs={
                'min': 0,
                'max': 100,
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            })
        }
    
    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0 or score > 100):
            raise forms.ValidationError("Оценка должна быть от 0 до 100 баллов")
        return score

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'teacher', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'bio', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'file_type', 'course']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите сообщение...',
                'autocomplete': 'off'
            })
        }