from django.db import models

class FileUpload(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.uploaded_at})"

class EquipmentData(models.Model):
    upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='data_points')
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50) # e.g., Pump, Valve
    flowrate = models.IntegerField()
    pressure = models.FloatField()
    temperature = models.IntegerField()

    def __str__(self):
        return f"{self.equipment_name} - {self.equipment_type}"