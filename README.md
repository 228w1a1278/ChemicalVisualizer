# Chemical Equipment Parameter Visualizer

A hybrid Web and Desktop application for visualizing chemical equipment data, built with Django, React, and PyQt5.

## 🚀 Features
- **Hybrid Architecture:** Common Django backend serving both Web (React) and Desktop (PyQt5) frontends.
- **Data Analysis:** automatic calculation of Flowrate, Pressure, and Temperature statistics.
- **Interactive Charts:** Chart.js for Web and Matplotlib for Desktop.
- **PDF Reporting:** Generate professional PDF summaries of the data.

## 🛠️ Setup Instructions

### 1. Backend (Django)
```bash
cd ChemicalProject
python -m venv venv
# Windows: venv\Scripts\activate  |  Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
