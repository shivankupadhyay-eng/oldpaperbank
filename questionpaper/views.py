from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import QuestionPaper
from.serializers import QuestionPaperSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer
import os
from django.http import FileResponse, HttpResponse
import openpyxl


class QuestionPaperUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = QuestionPaperSerializer(data=request.data)
        if serializer.is_valid():
            question_paper = serializer.save()
            return Response({
                "message": "Question paper uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionPaperListView(APIView):
    def get(self,request):
        college=request.GET.get("college")
        semester=request.GET.get("semester")
        subject=request.GET.get("subject")
        year=request.GET.get("year")
        if not college:
            return Response(
                {"error": "College name is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question_paper=QuestionPaper.objects.filter(college=college,semester=semester,subject=subject,year=year)
        Question_paper_serializer=QuestionPaperSerializer(question_paper,many=True)
        
        return Response(Question_paper_serializer.data,status=status.HTTP_200_OK)
      


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    excel_file_path = "uploads/user_data.xlsx"  # Path to store Excel file

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            name = serializer.validated_data['name']
            upi_id = serializer.validated_data['upi_id']
            comment = serializer.validated_data['comment']

            # Ensure uploads directory exists
            os.makedirs("uploads", exist_ok=True)

            # Save file temporarily
            file_path = f"uploads/{file.name}"
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Save data to XLSX file (including the comment)
            self.save_to_excel(name, upi_id, file.name, comment)

            return Response({
                "message": "File uploaded successfully and data saved in Excel",
                "name": name,
                "upi_id": upi_id,
                "file_name": file.name,
                "comment": comment
            })
        return Response(serializer.errors, status=400)

    def save_to_excel(self, name, upi_id, file_name, comment):
        """Save the uploaded data in an XLSX file, including the comment."""
        excel_file = self.excel_file_path

        if not os.path.exists(excel_file):
            # Create a new workbook if file doesn't exist
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "User Uploads"
            # Add headers including Comment
            ws.append(["Name", "UPI ID", "File Name", "Comment"])
        else:
            # Load existing workbook
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active

        # Append new data including comment
        ws.append([name, upi_id, file_name, comment])

        # Save the workbook
        wb.save(excel_file)


class DownloadExcelView(APIView):
    excel_file_path = "uploads/user_data.xlsx"

    def get(self, request, *args, **kwargs):
        if os.path.exists(self.excel_file_path):
            response = FileResponse(
                open(self.excel_file_path, 'rb'),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="user_data.xlsx"'
            return response
        else:
            return HttpResponse("File not found", status=404)