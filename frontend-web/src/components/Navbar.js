import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import ScienceIcon from '@mui/icons-material/Science';

const Navbar = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: '#1a237e' }}>
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <ScienceIcon sx={{ mr: 2 }} />
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, fontWeight: 'bold', letterSpacing: '.1rem' }}
          >
            CHEM-VISUALIZER
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;