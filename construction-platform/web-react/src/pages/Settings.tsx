import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Switch, 
  FormControlLabel, 
  TextField, 
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Divider,
  Grid,
  Alert,
} from '@mui/material';
import { Save, Refresh } from '@mui/icons-material';
import { api } from '../services/api';
import { useSnackbar } from 'notistack';

const Settings = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [loading, setLoading] = useState(false);
  
  // Form state
  const [settings, setSettings] = useState({
    language: 'en',
    region: 'tartu',
    enableNotifications: true,
    darkMode: false,
    n8nWebhookUrl: 'https://n8n.srv1071801.hstgr.cloud/webhook',
    apiKey: '',
    defaultWorkflow: 'auto',
    includeVat: true,
  });

  const handleChange = (field: string) => (event: any) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      // Save to localStorage as fallback
      localStorage.setItem('userSettings', JSON.stringify(settings));
      
      // Try to save to API if endpoint exists
      try {
        await api.post('/v1/settings', settings);
        enqueueSnackbar('Settings saved successfully!', { variant: 'success' });
      } catch (apiError: any) {
        // If API endpoint doesn't exist, just save to localStorage
        if (apiError.response?.status === 404) {
          enqueueSnackbar('Settings saved locally!', { variant: 'success' });
        } else {
          throw apiError;
        }
      }
    } catch (error: any) {
      console.error('Error saving settings:', error);
      enqueueSnackbar('Failed to save settings. Saved locally instead.', { variant: 'warning' });
      // Still save to localStorage as fallback
      localStorage.setItem('userSettings', JSON.stringify(settings));
    } finally {
      setLoading(false);
    }
  };

  const handleTestConnection = async () => {
    try {
      await api.get('/v1/health');
      enqueueSnackbar('Connection successful!', { variant: 'success' });
    } catch (error) {
      enqueueSnackbar('Connection failed. Please check your settings.', { variant: 'error' });
    }
  };

  // Load settings from localStorage on mount
  React.useEffect(() => {
    const saved = localStorage.getItem('userSettings');
    if (saved) {
      try {
        setSettings(JSON.parse(saved));
      } catch (e) {
        console.error('Error loading settings:', e);
      }
    }
  }, []);

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        Settings
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>General Settings</Typography>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Language</InputLabel>
                <Select 
                  value={settings.language} 
                  onChange={handleChange('language')}
                  label="Language"
                >
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="et">Estonian</MenuItem>
                </Select>
              </FormControl>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Region</InputLabel>
                <Select 
                  value={settings.region} 
                  onChange={handleChange('region')}
                  label="Region"
                >
                  <MenuItem value="tartu">Tartu</MenuItem>
                  <MenuItem value="tallinn">Tallinn</MenuItem>
                  <MenuItem value="parnu">Pärnu</MenuItem>
                </Select>
              </FormControl>
              <FormControlLabel
                control={
                  <Switch 
                    checked={settings.enableNotifications} 
                    onChange={handleChange('enableNotifications')}
                  />
                }
                label="Enable notifications"
              />
              <FormControlLabel
                control={
                  <Switch 
                    checked={settings.darkMode} 
                    onChange={handleChange('darkMode')}
                  />
                }
                label="Dark mode"
              />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>API Configuration</Typography>
              <TextField
                fullWidth
                label="N8N Webhook URL"
                value={settings.n8nWebhookUrl}
                onChange={handleChange('n8nWebhookUrl')}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="API Key"
                type="password"
                value={settings.apiKey}
                onChange={handleChange('apiKey')}
                placeholder="Enter API key"
                sx={{ mb: 2 }}
              />
              <Alert severity="info" sx={{ mb: 2 }}>
                API settings are configured in your N8N workflows
              </Alert>
              <Button 
                variant="outlined" 
                startIcon={<Refresh />}
                onClick={handleTestConnection}
              >
                Test Connection
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Processing Defaults</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel>Default Workflow</InputLabel>
                    <Select 
                      value={settings.defaultWorkflow} 
                      onChange={handleChange('defaultWorkflow')}
                      label="Default Workflow"
                    >
                      <MenuItem value="auto">Auto-detect</MenuItem>
                      <MenuItem value="boq">BOQ Generation</MenuItem>
                      <MenuItem value="materials">Materials Extraction</MenuItem>
                      <MenuItem value="cad">CAD Processing</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={6}>
                  <FormControlLabel
                    control={
                      <Switch 
                        checked={settings.includeVat} 
                        onChange={handleChange('includeVat')}
                      />
                    }
                    label="Include VAT in calculations (22%)"
                  />
                </Grid>
              </Grid>
              <Divider sx={{ my: 3 }} />
              <Button 
                variant="contained" 
                startIcon={<Save />}
                onClick={handleSave}
                disabled={loading}
              >
                {loading ? 'Saving...' : 'Save Settings'}
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;
