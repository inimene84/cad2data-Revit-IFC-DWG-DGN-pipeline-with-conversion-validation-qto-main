import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Card, CardContent, Grid, Select, MenuItem, FormControl, InputLabel
} from '@mui/material';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { api } from '../services/api';

const COLORS = ['#1FB8CD', '#FFC185', '#B4413C', '#4A90E2', '#50C878'];

const Analytics = () => {
  const [period, setPeriod] = useState('30d');
  const [costTrends, setCostTrends] = useState([]);
  const [materialBreakdown, setMaterialBreakdown] = useState([]);
  const [processingMetrics, setProcessingMetrics] = useState({
    files_processed: 0,
    avg_processing_time: 0,
    success_rate: 0,
    total_elements: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, [period]);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const [costs, materials, metrics] = await Promise.all([
        api.get(`/v1/analytics/cost-trends?period=${period}`),
        api.get(`/v1/analytics/material-breakdown?period=${period}`),
        api.get(`/v1/analytics/processing-metrics?period=${period}`)
      ]);
      
      // Extract data from API response structure: {version, period, data}
      setCostTrends(Array.isArray(costs.data?.data) ? costs.data.data : (Array.isArray(costs.data) ? costs.data : []));
      setMaterialBreakdown(Array.isArray(materials.data?.data) ? materials.data.data : (Array.isArray(materials.data) ? materials.data : []));
      setProcessingMetrics(metrics.data?.data || metrics.data || {
        files_processed: 0,
        avg_processing_time: 0,
        success_rate: 0,
        total_elements: 0
      });
    } catch (error) {
      console.error('Error loading analytics:', error);
      // Set empty defaults on error to prevent map errors
      setCostTrends([]);
      setMaterialBreakdown([]);
      setProcessingMetrics({
        files_processed: 0,
        avg_processing_time: 0,
        success_rate: 0,
        total_elements: 0
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Analytics & Insights
        </Typography>
        <Typography variant="body1">Loading analytics data...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" fontWeight={700}>
          Analytics & Insights
        </Typography>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Time Period</InputLabel>
          <Select value={period} onChange={(e) => setPeriod(e.target.value)} label="Time Period">
            <MenuItem value="7d">Last 7 days</MenuItem>
            <MenuItem value="30d">Last 30 days</MenuItem>
            <MenuItem value="90d">Last 90 days</MenuItem>
            <MenuItem value="1y">Last year</MenuItem>
          </Select>
        </FormControl>
      </Box>
      
      <Grid container spacing={3}>
        {/* Cost Trends Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Cost Trends</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={Array.isArray(costTrends) ? costTrends : []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="total_cost" stroke="#1FB8CD" name="Total Cost" />
                  <Line type="monotone" dataKey="material_cost" stroke="#FFC185" name="Material Cost" />
                  <Line type="monotone" dataKey="labor_cost" stroke="#B4413C" name="Labor Cost" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Material Breakdown Chart */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Material Breakdown</Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={Array.isArray(materialBreakdown) ? materialBreakdown : []}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    label
                  >
                    {Array.isArray(materialBreakdown) && materialBreakdown.length > 0 && materialBreakdown.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Processing Metrics */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Processing Metrics</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={3}>
                  <Typography variant="h4">{processingMetrics.files_processed || 0}</Typography>
                  <Typography variant="body2" color="text.secondary">Files Processed</Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="h4">{processingMetrics.avg_processing_time || 0}s</Typography>
                  <Typography variant="body2" color="text.secondary">Avg Processing Time</Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="h4">{processingMetrics.success_rate || 0}%</Typography>
                  <Typography variant="body2" color="text.secondary">Success Rate</Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="h4">{processingMetrics.total_elements || 0}</Typography>
                  <Typography variant="body2" color="text.secondary">Total Elements</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;
