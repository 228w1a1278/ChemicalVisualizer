import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFileDialog, 
                             QTableWidget, QTableWidgetItem, QFrame, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/api"

# --- Custom KPI Card Widget ---
class KPICard(QFrame):
    def __init__(self, title, color_code):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                border-left: 5px solid {color_code};
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("color: #666; font-size: 12px; font-weight: bold; text-transform: uppercase;")
        
        self.value_lbl = QLabel("-")
        self.value_lbl.setStyleSheet("color: #333; font-size: 24px; font-weight: bold;")
        
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.value_lbl)
        self.setLayout(layout)

    def set_value(self, value, unit=""):
        self.value_lbl.setText(f"{value} {unit}")

# --- Matplotlib Canvas ---
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

# --- Main Window ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Visualizer (Desktop)")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #f4f6f8;") # Light gray background like React

        # Main Layout Container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # 1. Header & Actions
        header_layout = QHBoxLayout()
        
        title = QLabel("Dashboard Overview")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a237e;")
        
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setStyleSheet("color: #666;")

        btn_upload = QPushButton("Upload CSV")
        btn_upload.setCursor(Qt.PointingHandCursor)
        btn_upload.setStyleSheet("""
            QPushButton {
                background-color: #1976d2; color: white; border: none; 
                padding: 10px 20px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1565c0; }
        """)
        btn_upload.clicked.connect(self.upload_file)

        btn_refresh = QPushButton("Refresh Data")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32; color: white; border: none; 
                padding: 10px 20px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1b5e20; }
        """)
        btn_refresh.clicked.connect(self.fetch_data)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.status_lbl)
        header_layout.addWidget(btn_refresh)
        header_layout.addWidget(btn_upload)
        self.layout.addLayout(header_layout)

        # 2. KPI Section
        kpi_layout = QHBoxLayout()
        self.card_count = KPICard("Total Units", "#3f51b5")
        self.card_flow = KPICard("Avg Flowrate", "#2e7d32")
        self.card_pressure = KPICard("Avg Pressure", "#ed6c02")
        self.card_temp = KPICard("Avg Temp", "#d32f2f")
        
        kpi_layout.addWidget(self.card_count)
        kpi_layout.addWidget(self.card_flow)
        kpi_layout.addWidget(self.card_pressure)
        kpi_layout.addWidget(self.card_temp)
        self.layout.addLayout(kpi_layout)

        # 3. Content Section (Chart + Table)
        content_layout = QHBoxLayout()

        # Left: Chart
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: white; border-radius: 8px;")
        chart_layout = QVBoxLayout(chart_frame)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        chart_layout.addWidget(QLabel("Equipment Distribution"))
        chart_layout.addWidget(self.canvas)
        content_layout.addWidget(chart_frame, stretch=2)

        # Right: Table
        table_frame = QFrame()
        table_frame.setStyleSheet("background-color: white; border-radius: 8px;")
        table_layout = QVBoxLayout(table_frame)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Flowrate"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("border: none;")
        
        table_layout.addWidget(QLabel("Recent Records"))
        table_layout.addWidget(self.table)
        content_layout.addWidget(table_frame, stretch=1)

        self.layout.addLayout(content_layout)

        # Initial Data Load
        self.fetch_data()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.status_lbl.setText("Uploading...")
            try:
                files = {'file': open(file_path, 'rb')}
                response = requests.post(f"{API_URL}/upload/", files=files)
                if response.status_code == 201:
                    self.status_lbl.setText("Upload Successful")
                    self.fetch_data()
                else:
                    QMessageBox.critical(self, "Error", f"Upload Failed: {response.text}")
                    self.status_lbl.setText("Error")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def fetch_data(self):
        try:
            response = requests.get(f"{API_URL}/summary/")
            if response.status_code == 200:
                data = response.json()
                self.update_ui(data)
                self.status_lbl.setText(f"Data Loaded: {data['filename']}")
            elif response.status_code == 204:
                 self.status_lbl.setText("No data available.")
        except Exception as e:
            self.status_lbl.setText("Connection Error")
            print(e)

    def update_ui(self, data):
        # Update KPIs
        stats = data['stats']
        self.card_count.set_value(stats['total_count'])
        self.card_flow.set_value(int(stats['avg_flow'] or 0), "m³/h")
        self.card_pressure.set_value(round(stats['avg_pressure'] or 0, 1), "bar")
        self.card_temp.set_value(int(stats['avg_temp'] or 0), "°C")

        # Update Chart
        dist = data['distribution']
        labels = [d['equipment_type'] for d in dist]
        counts = [d['count'] for d in dist]
        
        self.canvas.axes.cla() # Clear previous
        bars = self.canvas.axes.bar(labels, counts, color='#3f51b5', alpha=0.7)
        self.canvas.axes.set_title("Equipment Count by Type")
        self.canvas.draw()

        # Update Table
        rows = data['data']
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row['equipment_name']))
            self.table.setItem(i, 1, QTableWidgetItem(row['equipment_type']))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['flowrate'])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Global Font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())