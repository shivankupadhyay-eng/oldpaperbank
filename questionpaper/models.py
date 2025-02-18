from django.db import models
import uuid 

class QuestionPaper(models.Model):
    id=models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    image=models.ImageField(upload_to="questionPaperImage/")
    year=models.IntegerField()
    semester=models.PositiveIntegerField(default=1)
    subject=models.CharField(max_length=200)
    college=models.CharField(max_length=200)