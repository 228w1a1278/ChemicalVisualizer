from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import datetime
# core/views.py
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from .models import FileUpload, EquipmentData
from .serializers import FileUploadSerializer, EquipmentDataSerializer

class UploadCSVView(APIView):
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Check "Last 5" Constraint
        if FileUpload.objects.count() >= 5:
            # Delete the oldest upload
            oldest = FileUpload.objects.order_by('uploaded_at').first()
            if oldest:
                oldest.delete()

        # 2. Parse CSV using Pandas
        try:
            df = pd.read_csv(file_obj)
            
            # IMPROVEMENT: Strip whitespace from column names to avoid "Format" errors
            df.columns = df.columns.str.strip()
            
            # Check columns again
            required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing = [col for col in required_cols if col not in df.columns]
            
            if missing:
                return Response(
                    {"error": f"Missing columns: {missing}. Found: {list(df.columns)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response({"error": f"Failed to read CSV: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Create FileUpload Record
        upload_instance = FileUpload.objects.create(file_name=file_obj.name)

        # 4. Save Data Points (Bulk Create for performance)
        data_instances = [
            EquipmentData(
                upload=upload_instance,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )
            for _, row in df.iterrows()
        ]
        EquipmentData.objects.bulk_create(data_instances)

        return Response({"message": "File uploaded and processed successfully", "id": upload_instance.id}, status=status.HTTP_201_CREATED)

class DashboardDataView(APIView):
    """
    Returns data for the latest upload to display on the dashboard.
    """
    def get(self, request):
        # Get the most recent upload
        latest_upload = FileUpload.objects.order_by('-uploaded_at').first()
        
        if not latest_upload:
            return Response({"message": "No data available"}, status=status.HTTP_204_NO_CONTENT)

        data_points = latest_upload.data_points.all()

        # 1. Calculate Summary Stats
        stats = data_points.aggregate(
            avg_flow=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temp=Avg('temperature'),
            total_count=Count('id')
        )

        # 2. Calculate Type Distribution (for Charts)
        # Result: [{'equipment_type': 'Pump', 'count': 4}, ...]
        type_dist = data_points.values('equipment_type').annotate(count=Count('id'))

        # 3. Serialize Data Table
        serializer = EquipmentDataSerializer(data_points, many=True)

        return Response({
            "filename": latest_upload.file_name,
            "uploaded_at": latest_upload.uploaded_at,
            "stats": stats,
            "distribution": type_dist,
            "data": serializer.data
        })

class HistoryView(APIView):
    """
    Returns list of last 5 uploads.
    """
    def get(self, request):
        uploads = FileUpload.objects.order_by('-uploaded_at')[:5]
        serializer = FileUploadSerializer(uploads, many=True)
        return Response(serializer.data)



class ExportPDFView(APIView):
    def get(self, request):
        # 1. Get latest data
        latest_upload = FileUpload.objects.order_by('-uploaded_at').first()
        if not latest_upload:
            return Response({"error": "No data to export"}, status=404)
            
        data_points = latest_upload.data_points.all()
        
        # Calculate stats
        avg_flow = data_points.aggregate(Avg('flowrate'))['flowrate__avg']
        avg_pressure = data_points.aggregate(Avg('pressure'))['pressure__avg']
        
        # 2. Set up PDF Response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Report_{latest_upload.file_name}.pdf"'
        
        # 3. Draw PDF
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        
        # Header
        p.setFont("Helvetica-Bold", 20)
        p.drawString(50, height - 50, "Chemical Equipment Report")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        p.drawString(50, height - 100, f"Source File: {latest_upload.file_name}")
        
        # Stats Box
        p.setStrokeColor(colors.blue)
        p.rect(50, height - 180, 500, 60, fill=0)
        p.drawString(70, height - 140, f"Total Units: {data_points.count()}")
        p.drawString(200, height - 140, f"Avg Flowrate: {int(avg_flow)} m3/h")
        p.drawString(400, height - 140, f"Avg Pressure: {round(avg_pressure, 1)} bar")
        
        # Data Table Header
        y = height - 220
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Equipment Name")
        p.drawString(250, y, "Type")
        p.drawString(400, y, "Flowrate")
        p.line(50, y-5, 500, y-5)
        
        # Data Rows
        y -= 25
        p.setFont("Helvetica", 10)
        for item in data_points[:20]: # Limit to 20 rows for one page demo
            if y < 50: break # Simple pagination check
            p.drawString(50, y, item.equipment_name)
            p.drawString(250, y, item.equipment_type)
            p.drawString(400, y, str(item.flowrate))
            y -= 20
            
        p.showPage()
        p.save()
        
        return response
def home(request):
    return HttpResponse("<h1>Chemical Visualizer Backend is Live! 🚀</h1><p>Use /api/summary/ to get data.</p>")