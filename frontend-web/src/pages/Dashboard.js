import React, { useEffect, useState } from 'react';
import { Container, Grid, Paper, Typography, Box, Alert, Button, CircularProgress } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import SpeedIcon from '@mui/icons-material/Speed';
import OpacityIcon from '@mui/icons-material/Opacity';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import AssessmentIcon from '@mui/icons-material/Assessment';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';


import { getSummary, uploadFile } from '../services/api';
import KpiCard from '../components/KpiCard';
import Navbar from '../components/Navbar';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');


  const fetchData = async () => {
    try {
      const res = await getSummary();
      setData(res.data);
      setError('');
    } catch (err) {
      console.error(err);
      if(err.response && err.response.status !== 204) setError("Failed to fetch data.");
    }
  };

  useEffect(() => { fetchData(); }, []);

const handleDownloadPdf = () => {
  window.open('http://127.0.0.1:8000/api/export-pdf/', '_blank');
};

const handleFileChange = async (e) => {
    if (!e.target.files[0]) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', e.target.files[0]);

    try {
      await uploadFile(formData);
      await fetchData(); 
      setError('');
    } catch (err) {
      console.error("Upload Error Details:", err); 
      
      const backendMsg = err.response?.data?.error || "Upload failed. Please check CSV format.";
      setError(backendMsg);
    } finally {
      setLoading(false);
    }
  };

  const chartData = {
    labels: data?.distribution?.map(d => d.equipment_type) || [],
    datasets: [
      {
        label: 'Count of Equipment',
        data: data?.distribution?.map(d => d.count) || [],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div style={{ backgroundColor: '#f4f6f8', minHeight: '100vh', paddingBottom: '20px' }}>
      <Navbar />
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <div>
            <Typography variant="h4" fontWeight="bold" color="textPrimary">
              Dashboard Overview
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              {data ? `Latest Data: ${data.filename}` : 'Please upload a CSV file'}
            </Typography>
          </div>

          {/* Upload Button */}
          <Button
            variant="contained"
            component="label"
            startIcon={loading ? <CircularProgress size={20} color="inherit"/> : <CloudUploadIcon />}
            sx={{ padding: '10px 20px', fontSize: '1rem', backgroundColor: '#1976d2' }}
          >
            {loading ? "Processing..." : "Upload CSV"}
            <input type="file" hidden accept=".csv" onChange={handleFileChange} />
          </Button>
        <Button 
           variant="outlined" 
           color="secondary"
           startIcon={<PictureAsPdfIcon />}
           onClick={handleDownloadPdf}
           sx={{ mr: 2, padding: '10px 20px' }} 
          >
          Download Report
        </Button>

        </Box>

        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        {data && (
          <>
            <Grid container spacing={3} mb={4}>
              <Grid item xs={12} sm={6} md={3}>
                <KpiCard title="Total Units" value={data.stats.total_count} unit="" icon={<AssessmentIcon />} color="#3f51b5" />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <KpiCard title="Avg Flowrate" value={Math.round(data.stats.avg_flow)} unit="m³/h" icon={<SpeedIcon />} color="#2e7d32" />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <KpiCard title="Avg Pressure" value={data.stats.avg_pressure.toFixed(1)} unit="bar" icon={<OpacityIcon />} color="#ed6c02" />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <KpiCard title="Avg Temp" value={Math.round(data.stats.avg_temp)} unit="°C" icon={<ThermostatIcon />} color="#d32f2f" />
              </Grid>
            </Grid>

            {/* Main Content: Chart & Table */}
            <Grid container spacing={3}>
              {/* Chart Section */}
              <Grid item xs={12} md={7}>
                <Paper sx={{ p: 3, display: 'flex', flexDirection: 'column', height: 400 }}>
                  <Typography component="h2" variant="h6" color="primary" gutterBottom>
                    Equipment Distribution
                  </Typography>
                  <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
                  </Box>
                </Paper>
              </Grid>

              {/* Data Preview Table */}
              <Grid item xs={12} md={5}>
                <Paper sx={{ p: 3, display: 'flex', flexDirection: 'column', height: 400, overflow: 'auto' }}>
                  <Typography component="h2" variant="h6" color="primary" gutterBottom>
                    Recent Records
                  </Typography>
                  <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ borderBottom: '2px solid #eee' }}>
                        <th style={{ padding: '8px' }}>Name</th>
                        <th style={{ padding: '8px' }}>Type</th>
                        <th style={{ padding: '8px' }}>Flow</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.data.slice(0, 8).map((row, i) => (
                        <tr key={i} style={{ borderBottom: '1px solid #eee' }}>
                          <td style={{ padding: '8px' }}>{row.equipment_name}</td>
                          <td style={{ padding: '8px' }}>{row.equipment_type}</td>
                          <td style={{ padding: '8px' }}>{row.flowrate}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </Paper>
              </Grid>
            </Grid>
          </>
        )}
      </Container>
    </div>
  );
};

export default Dashboard;