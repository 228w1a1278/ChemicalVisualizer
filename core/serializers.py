# core/serializers.py
from rest_framework import serializers
from .models import FileUpload, EquipmentData

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file_name', 'uploaded_at']
