import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Grid,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Paper,
  Divider,
  TextField,
  Select,
  MenuItem,
  FormControl,
  FormControlLabel,
  Switch,
  InputLabel,
  CircularProgress,
} from '@mui/material';
import {
  CloudUpload,
  InsertDriveFile,
  PictureAsPdf,
  Description,
  Architecture,
  Delete,
  CheckCircle,
  Error,
  Warning,
  PlayArrow,
  Visibility,
  Download,
  Send,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useSnackbar } from 'notistack';
import { api } from '../services/api';

interface UploadedFile {
  id: string;
  file: File;
  status: 'pending' | 'uploading' | 'processing' | 'completed' | 'error';
  progress: number;
  result?: any;
  error?: string;
}

const FileUpload = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [activeStep, setActiveStep] = useState(0);
  const [projectName, setProjectName] = useState('');
  const [workflowType, setWorkflowType] = useState('auto');
  const [country, setCountry] = useState('EE');
  const [processing, setProcessing] = useState(false);
  const [estimating, setEstimating] = useState(false);
  const [costEstimate, setCostEstimate] = useState<any>(null);
  const [useN8nWorkflow, setUseN8nWorkflow] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  const steps = ['Select Files', 'Configure Processing', 'Process & Estimate'];

  // n8n webhook URL for cost estimation
  const N8N_WEBHOOK_URL = 'https://n8n.construction.thorspark.cloud/webhook/cost-estimation';

  const countries = [
    { code: 'EE', name: 'Estonia', vat: 24 },
    { code: 'FI', name: 'Finland', vat: 25.5 },
    { code: 'DE', name: 'Germany', vat: 19 },
    { code: 'LV', name: 'Latvia', vat: 21 },
    { code: 'LT', name: 'Lithuania', vat: 21 },
    { code: 'PL', name: 'Poland', vat: 23 },
    { code: 'SE', name: 'Sweden', vat: 25 },
  ];

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      id: Math.random().toString(36).substring(7),
      file,
      status: 'pending' as const,
      progress: 0,
    }));
    setFiles(prev => [...prev, ...newFiles]);
    enqueueSnackbar(`${acceptedFiles.length} file(s) added`, { variant: 'success' });
  }, [enqueueSnackbar]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
      'application/octet-stream': ['.dwg', '.dxf', '.ifc'],
    },
    multiple: true,
  });

  const getFileIcon = (file: File) => {
    const extension = file.name.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return <PictureAsPdf color="error" />;
      case 'xls':
      case 'xlsx':
        return <Description color="success" />;
      case 'dwg':
      case 'dxf':
      case 'ifc':
        return <Architecture color="primary" />;
      default:
        return <InsertDriveFile />;
    }
  };

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const processFile = async (uploadedFile: UploadedFile) => {
    // Update status to uploading
    setFiles(prev => prev.map(f =>
      f.id === uploadedFile.id ? { ...f, status: 'uploading', progress: 30 } : f
    ));

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile.file);
      formData.append('project_name', projectName || 'Unnamed Project');
      formData.append('workflow_type', workflowType);

      // Determine endpoint based on file type
      let endpoint = '/extract-pdf';
      const extension = uploadedFile.file.name.split('.').pop()?.toLowerCase();
      if (['xls', 'xlsx'].includes(extension || '')) {
        endpoint = '/extract-excel';
      } else if (['dwg', 'dxf', 'ifc'].includes(extension || '')) {
        endpoint = '/process-cad';
      }

      // Update progress
      setFiles(prev => prev.map(f =>
        f.id === uploadedFile.id ? { ...f, progress: 60 } : f
      ));

      const response = await api.post(endpoint, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 100));
          setFiles(prev => prev.map(f =>
            f.id === uploadedFile.id ? { ...f, progress: Math.min(90, percentCompleted) } : f
          ));
        },
      });

      // Update status to completed
      setFiles(prev => prev.map(f =>
        f.id === uploadedFile.id
          ? { ...f, status: 'completed', progress: 100, result: response.data }
          : f
      ));

      enqueueSnackbar(`${uploadedFile.file.name} processed successfully`, { variant: 'success' });
    } catch (error: any) {
      setFiles(prev => prev.map(f =>
        f.id === uploadedFile.id
          ? { ...f, status: 'error', error: error.message }
          : f
      ));
      enqueueSnackbar(`Error processing ${uploadedFile.file.name}`, { variant: 'error' });
    }
  };

  // Run DDC cost estimation on extracted materials
  const runCostEstimation = async (materials: any[]) => {
    setEstimating(true);
    try {
      const materialsPayload = materials.map(m => ({
        name: m.name || m.description || m.material,
        quantity: parseFloat(m.quantity) || 1,
        unit: m.unit || 'unit',
        category: m.category
      }));

      let responseData;

      if (useN8nWorkflow) {
        // Use n8n webhook for cost estimation
        enqueueSnackbar('Using n8n workflow for estimation...', { variant: 'info' });
        const response = await fetch(N8N_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            project_name: projectName || 'Unnamed Project',
            country: country,
            materials: materialsPayload,
            language: 'en'
          })
        });
        responseData = await response.json();
      } else {
        // Use direct API call
        const response = await api.post('/v1/vector/estimate', {
          materials: materialsPayload,
          language: 'en',
          country: country
        });
        responseData = response.data;
      }

      setCostEstimate(responseData);

      // Auto-save to reports
      try {
        await api.post('/v1/reports', {
          name: `${projectName || 'Unnamed Project'} - Cost Estimate`,
          total_cost: responseData.total_gross,
          items_count: responseData.items_count,
          data: responseData,
          source: useN8nWorkflow ? 'n8n_workflow' : 'api'
        });
        enqueueSnackbar('Cost estimate saved to reports', { variant: 'success' });
      } catch (e) {
        console.error('Failed to save report:', e);
      }

      enqueueSnackbar(`Cost estimation complete: €${responseData.total_gross?.toLocaleString()}`, { variant: 'success' });
    } catch (error: any) {
      console.error('Cost estimation error:', error);
      enqueueSnackbar('Cost estimation failed', { variant: 'error' });
    }
    setEstimating(false);
  };

  const processAllFiles = async () => {
    setProcessing(true);
    const pendingFiles = files.filter(f => f.status === 'pending');

    // Process files in parallel (max 3 at a time)
    const batchSize = 3;
    for (let i = 0; i < pendingFiles.length; i += batchSize) {
      const batch = pendingFiles.slice(i, i + batchSize);
      await Promise.all(batch.map(processFile));
    }

    setProcessing(false);
    setActiveStep(2);

    // Collect all materials from completed files and run estimation
    const completedFiles = files.filter(f => f.status === 'completed');
    const allMaterials: any[] = [];
    completedFiles.forEach(f => {
      if (f.result?.construction_items) {
        // Handle CAD/Excel extraction response
        allMaterials.push(...f.result.construction_items);
      } else if (f.result?.materials) {
        allMaterials.push(...f.result.materials);
      } else if (f.result?.extracted_data) {
        // Handle different response formats
        const data = f.result.extracted_data;
        if (Array.isArray(data)) {
          allMaterials.push(...data);
        }
      }
    });

    if (allMaterials.length > 0) {
      await runCostEstimation(allMaterials);
    }
  };

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle color="success" />;
      case 'error':
        return <Error color="error" />;
      case 'uploading':
      case 'processing':
        return <CircularProgress size={20} />;
      default:
        return <Warning color="warning" />;
    }
  };

  const handleNext = () => {
    if (activeStep === 1) {
      processAllFiles();
    } else {
      setActiveStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    setActiveStep(prev => prev - 1);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        File Upload & Processing
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Upload construction files for AI-powered analysis and BOQ generation
      </Typography>

      {/* Stepper */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stepper activeStep={activeStep}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </CardContent>
      </Card>

      {/* Step Content */}
      {activeStep === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Box
                  {...getRootProps()}
                  sx={{
                    border: '2px dashed',
                    borderColor: isDragActive ? 'primary.main' : 'divider',
                    borderRadius: 2,
                    p: 6,
                    textAlign: 'center',
                    cursor: 'pointer',
                    bgcolor: isDragActive ? 'action.hover' : 'background.default',
                    transition: 'all 0.3s',
                    '&:hover': {
                      borderColor: 'primary.main',
                      bgcolor: 'action.hover',
                    },
                  }}
                >
                  <input {...getInputProps()} />
                  <CloudUpload sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    or click to browse
                  </Typography>
                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Chip label="PDF" size="small" />
                    <Chip label="Excel" size="small" />
                    <Chip label="DWG" size="small" />
                    <Chip label="IFC" size="small" />
                  </Box>
                </Box>

                {files.length > 0 && (
                  <Box sx={{ mt: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Files ({files.length})
                    </Typography>
                    <List>
                      <AnimatePresence>
                        {files.map((file) => (
                          <motion.div
                            key={file.id}
                            initial={{ opacity: 0, y: -20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, x: -100 }}
                          >
                            <ListItem
                              sx={{
                                border: '1px solid',
                                borderColor: 'divider',
                                borderRadius: 1,
                                mb: 1,
                              }}
                              secondaryAction={
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                  {getStatusIcon(file.status)}
                                  <IconButton
                                    edge="end"
                                    onClick={() => removeFile(file.id)}
                                    disabled={file.status !== 'pending'}
                                  >
                                    <Delete />
                                  </IconButton>
                                </Box>
                              }
                            >
                              <ListItemIcon>{getFileIcon(file.file)}</ListItemIcon>
                              <ListItemText
                                primary={file.file.name}
                                secondary={formatFileSize(file.file.size)}
                              />
                              {file.status === 'uploading' && (
                                <Box sx={{ width: 100, mr: 2 }}>
                                  <LinearProgress variant="determinate" value={file.progress} />
                                </Box>
                              )}
                            </ListItem>
                          </motion.div>
                        ))}
                      </AnimatePresence>
                    </List>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Supported Formats
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon><PictureAsPdf color="error" /></ListItemIcon>
                    <ListItemText primary="PDF Documents" secondary="Construction plans, BOQs" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon><Description color="success" /></ListItemIcon>
                    <ListItemText primary="Excel Files" secondary="Material lists, cost sheets" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon><Architecture color="primary" /></ListItemIcon>
                    <ListItemText primary="CAD Files" secondary="DWG, DXF, IFC models" />
                  </ListItem>
                </List>
              </CardContent>
            </Card>

            <Alert severity="info">
              <Typography variant="subtitle2" fontWeight={600}>
                Tips for Best Results
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                • Upload clear, high-quality documents
                <br />
                • Include material specifications
                <br />
                • Use standard CAD formats
                <br />
                • Maximum file size: 100MB
              </Typography>
            </Alert>
          </Grid>
        </Grid>
      )}

      {activeStep === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Processing Configuration
                </Typography>

                <Box sx={{ mt: 3 }}>
                  <TextField
                    fullWidth
                    label="Project Name"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="Enter project name"
                    sx={{ mb: 3 }}
                  />

                  <FormControl fullWidth sx={{ mb: 3 }}>
                    <InputLabel>Workflow Type</InputLabel>
                    <Select
                      value={workflowType}
                      onChange={(e) => setWorkflowType(e.target.value)}
                      label="Workflow Type"
                    >
                      <MenuItem value="auto">Auto-detect (Recommended)</MenuItem>
                      <MenuItem value="boq">BOQ Generation</MenuItem>
                      <MenuItem value="materials">Materials Extraction</MenuItem>
                      <MenuItem value="cad">CAD Processing</MenuItem>
                      <MenuItem value="compliance">Compliance Check</MenuItem>
                      <MenuItem value="3d">3D Visualization</MenuItem>
                    </Select>
                  </FormControl>

                  <FormControl fullWidth sx={{ mb: 3 }}>
                    <InputLabel>Country (VAT)</InputLabel>
                    <Select
                      value={country}
                      onChange={(e) => setCountry(e.target.value)}
                      label="Country (VAT)"
                    >
                      {countries.map(c => (
                        <MenuItem key={c.code} value={c.code}>
                          {c.name} ({c.vat}% VAT)
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  <FormControlLabel
                    control={
                      <Switch
                        checked={useN8nWorkflow}
                        onChange={(e) => setUseN8nWorkflow(e.target.checked)}
                        color="secondary"
                      />
                    }
                    label="Use n8n Workflow (advanced)"
                    sx={{ mb: 2 }}
                  />

                  <Alert severity={useN8nWorkflow ? "warning" : "info"} sx={{ mb: 2 }}>
                    {files.length} file(s) will be processed with DDC CWICR cost estimation
                    {useN8nWorkflow ? ' via n8n workflow' : ' via API'}
                    ({countries.find(c => c.code === country)?.name} {countries.find(c => c.code === country)?.vat}% VAT)
                  </Alert>

                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                      Files to Process:
                    </Typography>
                    {files.map((file) => (
                      <Chip
                        key={file.id}
                        label={file.file.name}
                        icon={getFileIcon(file.file) as any}
                        sx={{ m: 0.5 }}
                        variant="outlined"
                      />
                    ))}
                  </Paper>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Workflow Options
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText
                      primary="Auto-detect"
                      secondary="AI automatically selects best workflow"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="BOQ Generation"
                      secondary="Generate bill of quantities"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Materials Extraction"
                      secondary="Extract and analyze materials"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="CAD Processing"
                      secondary="Process CAD/BIM models"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeStep === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Processing Results
                </Typography>

                {processing ? (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <CircularProgress size={60} />
                    <Typography variant="h6" sx={{ mt: 2 }}>
                      Processing files...
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      This may take a few moments
                    </Typography>
                  </Box>
                ) : (
                  <List>
                    {files.map((file) => (
                      <ListItem
                        key={file.id}
                        sx={{
                          border: '1px solid',
                          borderColor: file.status === 'completed' ? 'success.main' : file.status === 'error' ? 'error.main' : 'divider',
                          borderRadius: 1,
                          mb: 1,
                        }}
                      >
                        <ListItemIcon>{getFileIcon(file.file)}</ListItemIcon>
                        <ListItemText
                          primary={file.file.name}
                          secondary={
                            file.status === 'completed'
                              ? `Successfully processed - ${file.result?.construction_items?.length || file.result?.materials_found || 0} materials found`
                              : file.status === 'error'
                                ? `Error: ${file.error}`
                                : 'Processing...'
                          }
                        />
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          {getStatusIcon(file.status)}
                          {file.status === 'completed' && (
                            <>
                              <IconButton size="small">
                                <Visibility />
                              </IconButton>
                              <IconButton size="small">
                                <Download />
                              </IconButton>
                            </>
                          )}
                        </Box>
                      </ListItem>
                    ))}
                  </List>
                )}

                {/* Cost Estimation Results */}
                {estimating && (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <CircularProgress size={40} />
                    <Typography variant="body1" sx={{ mt: 2 }}>
                      Running DDC CWICR cost estimation...
                    </Typography>
                  </Box>
                )}

                {costEstimate && (
                  <Box sx={{ mt: 3 }}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="h6" gutterBottom color="primary">
                      💰 Cost Estimation Results
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.dark' }}>
                          <Typography variant="h5" fontWeight="bold">
                            €{costEstimate.total_gross?.toLocaleString()}
                          </Typography>
                          <Typography variant="caption">Total (incl. VAT)</Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5">
                            €{costEstimate.total_net?.toLocaleString()}
                          </Typography>
                          <Typography variant="caption">Net Cost</Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5">
                            {costEstimate.items_count}
                          </Typography>
                          <Typography variant="caption">Items Estimated</Typography>
                        </Paper>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <Typography variant="h5">
                            {costEstimate.avg_confidence}%
                          </Typography>
                          <Typography variant="caption">Confidence</Typography>
                        </Paper>
                      </Grid>
                    </Grid>
                    <Alert severity="success" sx={{ mt: 2 }}>
                      Cost estimate saved to Reports! VAT Rate: {(costEstimate.vat_rate * 100)}% ({costEstimate.country})
                    </Alert>
                  </Box>
                )}

                {!processing && !estimating && files.some(f => f.status === 'completed') && (
                  <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                    <Button
                      variant="contained"
                      startIcon={<Send />}
                      onClick={() => window.location.href = '/reports'}
                    >
                      View Reports
                    </Button>
                    <Button variant="outlined" startIcon={<Download />}>
                      Download Results
                    </Button>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Navigation Buttons */}
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Button
          disabled={activeStep === 0}
          onClick={handleBack}
        >
          Back
        </Button>
        <Button
          variant="contained"
          onClick={handleNext}
          disabled={
            (activeStep === 0 && files.length === 0) ||
            (activeStep === 2) ||
            processing
          }
          startIcon={activeStep === 1 ? <PlayArrow /> : undefined}
        >
          {activeStep === 0 ? 'Next' : activeStep === 1 ? 'Process Files' : 'Finish'}
        </Button>
      </Box>
    </Box>
  );
};

export default FileUpload;
