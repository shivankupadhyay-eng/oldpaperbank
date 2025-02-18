from rest_framework import serializers
from.models import QuestionPaper

class QuestionPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuestionPaper
        fields=['year','semester','subject','college','image']
        

class FileUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    upi_id = serializers.CharField(max_length=100)
    file = serializers.FileField()
    comment = serializers.CharField(max_length=400)
    
    def validate_file(self, value):
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        return value
