from django.urls import path
from .views import UploadCSVView, DashboardDataView, HistoryView ,ExportPDFView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload-csv'),
    path('summary/', DashboardDataView.as_view(), name='dashboard-summary'),
    path('history/', HistoryView.as_view(), name='upload-history'),
    path('export-pdf/', ExportPDFView.as_view(), name='export-pdf'),
]
