import React, { useState } from 'react';
import PropTypes from 'prop-types';
import ConsultaCard from './components/ConsultaCard';
import { Container, Typography, Box, Grid, Tabs, Tab, Divider, ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import consultas from './consultas';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function App() {
  const [value, setValue] = useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  
  // Agrupar por modelo y luego por categoría
  const groupedConsultas = consultas.reduce((acc, consulta) => {
    const modelName = consulta.dbInfo.model || 'Otros';
    const categoryName = consulta.category || 'General';
    if (!acc[modelName]) acc[modelName] = {};
    if (!acc[modelName][categoryName]) acc[modelName][categoryName] = [];
    acc[modelName][categoryName].push(consulta);
    return acc;
  }, {});
  
  const modelOrder = ['Administración', 'Documental', 'Grafo', 'Clave-Valor'];
  const orderedModels = modelOrder.filter(model => groupedConsultas[model]);


  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4, textAlign: 'center', position: 'relative' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Plataforma Integral de Gestión de Talento IT
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mt: 2, maxWidth: '800px', mx: 'auto' }}>
          Una demo de arquitectura de datos distribuidos para gestionar el ciclo de vida del talento, integrando reclutamiento, formación, evaluación y relaciones laborales.
        </Typography>
      </Box>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="database model tabs" centered>
          {orderedModels.map((modelName, idx) => (
            <Tab label={`${modelName} (${Object.values(groupedConsultas[modelName])[0][0].dbInfo.name})`} {...a11yProps(idx)} key={idx} />
          ))}
        </Tabs>
      </Box>

      {orderedModels.map((modelName, modelIdx) => (
        <TabPanel value={value} index={modelIdx} key={modelIdx}>
          {Object.entries(groupedConsultas[modelName]).map(([categoryName, queries], catIdx) => (
            <Box key={catIdx} sx={{ mb: 5 }}>
              <Typography variant="h5" component="h3" gutterBottom>
                {categoryName}
              </Typography>
              <Divider sx={{ mb: 3 }} />
              <Grid container spacing={4} justifyContent="center">
                {queries.map((consulta, cIdx) => (
                  <Grid item key={cIdx} xs={12} md={6} lg={4}>
                    <ConsultaCard {...consulta} />
                  </Grid>
                ))}
              </Grid>
            </Box>
          ))}
        </TabPanel>
      ))}
    </Container>
  );
}

export default function AppWrapper() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  );
}