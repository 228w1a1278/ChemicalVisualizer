# Chemical Equipment Parameter Visualizer - Hybrid Analytics Platform (Django + React + PyQt5)

Welcome to the **Chemical Equipment Parameter Visualizer**, a fully functional hybrid application built using Django REST Framework, React.js, and PyQt5. This project demonstrates how a single robust backend can simultaneously power a modern web dashboard and a native desktop application. 

Whether you’re a correction agent or a hiring manager, this project reflects my capabilities in full-stack development, including complex data parsing with Pandas, API design, responsive frontend logic, and cross-platform integration.

## 🗳️ About the Project
This application is designed for the analysis and visualization of chemical equipment data. It features a **Hybrid Architecture** where a Django backend serves as the central "brain," processing CSV uploads and serving analytical data via API.

Users can interact with the system through two interfaces:
1.  **Web Dashboard (React):** A responsive browser-based UI for uploading files, viewing interactive charts, and generating PDF reports.
2.  **Desktop App (PyQt5):** A native OS application that syncs in real-time with the web data, providing a seamless experience across platforms.

## 🔑 Core Features
* **Hybrid Synchronization:** Upload a file on the Desktop app, and the Web dashboard updates instantly (and vice versa).
* **Data Analytics Engine:** Uses **Pandas** to calculate average flowrates, pressures, and equipment distributions from raw CSV data.
* **Interactive Visualization:**
    * **Web:** Dynamic charts using **Chart.js** and **Material UI**.
    * **Desktop:** Native plotting using **Matplotlib** embedded in PyQt5.
* **PDF Report Generation:** One-click export of a professional summary report using **ReportLab**.
* **Smart History Management:** The backend automatically manages storage, keeping only the last 5 datasets to ensure efficiency.

## 🔧 Tech Stack
* **Backend Framework:** Python Django + Django REST Framework (DRF)
* **Data Processing:** Pandas (CSV parsing & Analytics)
* **Frontend (Web):** React.js + Material UI (MUI) + Chart.js
* **Frontend (Desktop):** Python PyQt5 + Matplotlib
* **Database:** SQLite (Lightweight & efficient)
* **Tools:** Git, GitHub, VS Code, Postman

## 📽️ Working of the App
* **Web Dashboard:** The entry point where users can upload `sample_equipment_data.csv`. It displays KPI cards (Total Units, Avg Pressure) and a bar chart of equipment types.
* **Desktop Interface:** A standalone window mimicking the web UI. It connects to the same API to fetch and display data. It includes a "Refresh" feature to pull the latest changes from the server.
* **PDF Reporting:** Users can click "Download Report" on the web interface to generate a timestamped PDF summary of the current dataset.
* **API Logic:** The Django view handles file validation, parses columns, cleans data, and enforces the "Max 5 Files" history rule before saving to the database.

---

## 🚀 Installation & Setup Guide

Follow these steps to run the entire system locally. You will need **3 separate terminal windows**.

### 1️⃣ Backend Setup (The Brain)
*The Django server must be running first.*

```bash
# 1. Navigate to the project root
cd ChemicalProject

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install django djangorestframework pandas django-cors-headers reportlab

# 4. Run migrations & Start Server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver