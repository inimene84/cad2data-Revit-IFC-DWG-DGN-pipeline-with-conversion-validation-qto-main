import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControlLabel,
  Switch,
  Chip,
  IconButton,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from '@mui/material';
import { Download, Assessment, Refresh, Add, Delete, Visibility } from '@mui/icons-material';
import { api } from '../services/api';

interface Report {
  id: number;
  name: string;
  project_id: number | null;
  type: string;
  status: string;
  total_cost: number | null;
  file_path: string | null;
  created_at: string;
}

const Reports = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    type: 'boq',
    include_vat: true,
    region: 'Tartu',
  });

  const fetchReports = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/v1/reports');
      setReports(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load reports');
      console.error('Error fetching reports:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleOpenDialog = () => {
    setFormData({
      name: `BOQ Report - ${new Date().toLocaleDateString('et-EE')}`,
      type: 'boq',
      include_vat: true,
      region: 'Tartu',
    });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      await api.post('/v1/reports/generate', formData);
      handleCloseDialog();
      fetchReports();
    } catch (err: any) {
      setError(err.message || 'Failed to generate report');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = async (reportId: number, reportName: string) => {
    try {
      const response = await api.get(`/v1/reports/${reportId}/download`);
      const data = response.data;

      if (data.pdf_base64) {
        // Decode base64 and download PDF
        const byteCharacters = atob(data.pdf_base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = data.filename || `${reportName}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } else {
        // Download as JSON
        const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = data.filename || `${reportName}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to download report');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this report?')) {
      try {
        await api.delete(`/v1/reports/${id}`);
        fetchReports();
      } catch (err: any) {
        setError(err.message || 'Failed to delete report');
      }
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'boq':
        return 'Bill of Quantities';
      case 'cost_estimate':
        return 'Cost Estimate';
      case 'materials_list':
        return 'Materials List';
      default:
        return type;
    }
  };

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ textAlign: 'center', mt: 4 }}>
          Loading Reports...
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>Reports</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" startIcon={<Refresh />} onClick={fetchReports}>
            Refresh
          </Button>
          <Button variant="contained" startIcon={<Assessment />} onClick={handleOpenDialog}>
            Generate Report
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {reports.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 6 }}>
            <Assessment sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary">
              No reports generated yet
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Generate your first BOQ report to get started
            </Typography>
            <Button variant="contained" startIcon={<Add />} onClick={handleOpenDialog}>
              Generate Report
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent sx={{ p: 0 }}>
            <TableContainer component={Paper} elevation={0}>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                    <TableCell><strong>ID</strong></TableCell>
                    <TableCell><strong>Report Name</strong></TableCell>
                    <TableCell><strong>Type</strong></TableCell>
                    <TableCell><strong>Status</strong></TableCell>
                    <TableCell align="right"><strong>Total Cost</strong></TableCell>
                    <TableCell><strong>Created</strong></TableCell>
                    <TableCell align="center"><strong>Actions</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {reports.map((report) => (
                    <TableRow key={report.id} hover>
                      <TableCell>{report.id}</TableCell>
                      <TableCell><strong>{report.name}</strong></TableCell>
                      <TableCell>
                        <Chip label={getTypeLabel(report.type)} size="small" variant="outlined" />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={report.status}
                          size="small"
                          color={report.status === 'completed' ? 'success' : 'default'}
                        />
                      </TableCell>
                      <TableCell align="right">
                        {report.total_cost ? `€${report.total_cost.toLocaleString('et-EE', { minimumFractionDigits: 2 })}` : '-'}
                      </TableCell>
                      <TableCell>
                        {new Date(report.created_at).toLocaleDateString('et-EE')}
                      </TableCell>
                      <TableCell align="center">
                        <IconButton
                          size="small"
                          onClick={() => handleDownload(report.id, report.name)}
                          title="Download"
                        >
                          <Download fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={() => handleDelete(report.id)}
                          color="error"
                          title="Delete"
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {/* Generate Report Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Generate Report</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Report Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
              required
            />
            <FormControl fullWidth>
              <InputLabel>Report Type</InputLabel>
              <Select
                value={formData.type}
                label="Report Type"
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              >
                <MenuItem value="boq">Bill of Quantities (BOQ)</MenuItem>
                <MenuItem value="cost_estimate">Cost Estimate</MenuItem>
                <MenuItem value="materials_list">Materials List</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Region</InputLabel>
              <Select
                value={formData.region}
                label="Region"
                onChange={(e) => setFormData({ ...formData, region: e.target.value })}
              >
                <MenuItem value="Tallinn">Tallinn</MenuItem>
                <MenuItem value="Tartu">Tartu</MenuItem>
                <MenuItem value="Pärnu">Pärnu</MenuItem>
                <MenuItem value="Narva">Narva</MenuItem>
              </Select>
            </FormControl>
            <FormControlLabel
              control={
                <Switch
                  checked={formData.include_vat}
                  onChange={(e) => setFormData({ ...formData, include_vat: e.target.checked })}
                />
              }
              label="Include VAT (22%)"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleGenerate}
            variant="contained"
            disabled={!formData.name || generating}
          >
            {generating ? 'Generating...' : 'Generate Report'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Reports;
