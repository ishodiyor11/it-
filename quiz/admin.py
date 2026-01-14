from django.contrib import admin
from .models import Subject, Question, Option, QuizAttempt

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_filter = ('subject', 'difficulty')
    search_fields = ('content',)

admin.site.register(Subject)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(QuizAttempt)
