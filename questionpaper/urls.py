from django.urls import path
from .views import QuestionPaperListView, FileUploadView, DownloadExcelView, QuestionPaperUploadView
urlpatterns=[
    
    path("list-papers/",QuestionPaperListView.as_view()),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download-excel/', DownloadExcelView.as_view(), name='download-excel'),
    path('upload-question-paper/', QuestionPaperUploadView.as_view(), name='upload-question-paper'),

    
]