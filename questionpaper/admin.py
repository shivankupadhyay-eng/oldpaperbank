from django.contrib import admin
from .models import QuestionPaper

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display=['id','semester','subject','college','year','image']