import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, Button, Collapse, CircularProgress, Alert, Box, Chip, useTheme } from '@mui/material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark, materialLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

const API_BASE_URL = "http://localhost:8000";

const ResultsDisplay = ({ data, isAction = false }) => {
  const theme = useTheme();
  const syntaxTheme = theme.palette.mode === 'dark' ? materialDark : materialLight;

  if (data === null || data === undefined) {
    return <Typography variant="body2" color="text.secondary">La consulta no devolvió un cuerpo de respuesta.</Typography>;
  }
  if (Array.isArray(data) && data.length === 0) {
    return <Typography variant="body2" color="text.secondary">La consulta devolvió un array vacío [].</Typography>;
  }

  const displayData = (isAction || !Array.isArray(data)) ? data : [data];
  return (
    <SyntaxHighlighter language="json" style={syntaxTheme} customStyle={{ maxHeight: '400px', overflowY: 'auto' }}>
      {JSON.stringify(displayData, null, 2)}
    </SyntaxHighlighter>
  );
};

const ConsultaCard = ({ title, description, dbInfo, codeSnippet, endpoint, body, method = 'GET' }) => {
  const [showQuery, setShowQuery] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasExecuted, setHasExecuted] = useState(false);
  const [responseStatus, setResponseStatus] = useState(null);
  
  const theme = useTheme();
  const syntaxTheme = theme.palette.mode === 'dark' ? materialDark : materialLight;

  const isAction = method !== 'GET';

  const handleExecute = async () => {
    setHasExecuted(true);
    setLoading(true);
    setError('');
    setResults(null);
    setResponseStatus(null);
    try {
      const url = `${API_BASE_URL}${endpoint}`;
      let response;
      switch (method) {
        case 'POST':
          response = await axios.post(url, body || {});
          break;
        case 'PUT':
          // Hardcoded body for this specific demo case
          const requestBody = { seniority: "Principal Engineer" };
          response = await axios.put(url, requestBody);
          break;
        case 'DELETE':
          response = await axios.delete(url);
          break;
        case 'GET':
        default:
          response = await axios.get(url);
          break;
      }
      setResults(response.data);
      setResponseStatus({ code: response.status, text: response.statusText });
    } catch (err) {
      if (err.response) {
        setError('El servidor respondió con un error.');
        setResults(err.response.data || { info: "La respuesta de error no contenía un cuerpo JSON." });
        setResponseStatus({ code: err.response.status, text: err.response.statusText });
      } else if (err.request) {
        setError('No se pudo conectar con el servidor. Verifique que el backend esté activo y accesible.');
      } else {
        setError('Ocurrió un error inesperado al preparar la consulta.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getChipColor = (dbName) => ({ MongoDB: 'success', Neo4j: 'info', Redis: 'warning' }[dbName] || 'default');
  const getMethodChipColor = (httpMethod) => {
    switch(httpMethod) {
      case 'POST': return 'secondary';
      case 'PUT': return 'warning';
      case 'DELETE': return 'error';
      default: return 'primary';
    }
  };

  return (
    <Card sx={{ margin: 2, boxShadow: 3, borderRadius: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Box>
            <Typography variant="h5" component="div">{title}</Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">{description}</Typography>
          </Box>
          {dbInfo && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, alignItems: 'flex-end' }}>
              <Chip label={dbInfo.name} color={getChipColor(dbInfo.name)} size="small" />
              <Chip label={dbInfo.model} variant="outlined" size="small" />
            </Box>
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 1, my: 2 }}>
          <Button variant="outlined" size="small" onClick={() => setShowQuery(!showQuery)}>
            {showQuery ? 'Ocultar' : 'Ver'} Detalles
          </Button>
          <Button variant="contained" size="small" onClick={handleExecute} disabled={loading} color={getMethodChipColor(method)}>
            {loading ? <CircularProgress size={24} /> : (isAction ? 'Ejecutar Acción' : 'Ejecutar Consulta')}
          </Button>
        </Box>

        <Collapse in={showQuery}>
          <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>Comando:</Typography>
          <SyntaxHighlighter language="python" style={syntaxTheme} customStyle={{ borderRadius: '4px' }}>
            {codeSnippet}
          </SyntaxHighlighter>
          <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>Endpoint:</Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p:1, backgroundColor: theme.palette.background.paper, borderRadius: '4px' }}>
            <Chip label={method} color={getMethodChipColor(method)} size="small" />
            <Typography component="span" sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>
              {endpoint}
            </Typography>
          </Box>
        </Collapse>
        
        {loading && <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}><CircularProgress /></Box>}
        
        {hasExecuted && !loading && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6" sx={{ mb: 1 }}>Respuesta:</Typography>
            
            {responseStatus && (
              <Box sx={{ p: 1, backgroundColor: theme.palette.background.paper, borderRadius: '4px', mb: 1 }}>
                <Typography component="p" sx={{ fontFamily: 'monospace', fontWeight: 'bold', color: responseStatus.code >= 400 ? 'error.main' : 'success.main' }}>
                  {`${method} ${endpoint} HTTP/1.1 ${responseStatus.code} ${responseStatus.text}`}
                </Typography>
              </Box>
            )}

            {error && <Alert severity="warning" sx={{ my: 1 }}>{error}</Alert>}
            
            {(results !== null) && <ResultsDisplay data={results} isAction={isAction} />}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ConsultaCard;
