// src/components/KpiCard.js
import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

// Rename function from KPI_Card to KpiCard
const KpiCard = ({ title, value, unit, icon, color }) => {
  return (
    <Card sx={{ height: '100%', boxShadow: 3, borderLeft: `5px solid ${color}` }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <div>
            <Typography color="textSecondary" gutterBottom variant="subtitle2" textTransform="uppercase">
              {title}
            </Typography>
            <Typography variant="h4" component="div" fontWeight="bold">
              {value} <span style={{ fontSize: '0.6em', color: '#777' }}>{unit}</span>
            </Typography>
          </div>
          <Box sx={{ color: color, transform: 'scale(1.5)', opacity: 0.8 }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default KpiCard;
