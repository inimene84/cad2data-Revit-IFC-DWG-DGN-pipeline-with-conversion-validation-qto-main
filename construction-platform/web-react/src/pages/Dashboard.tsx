import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Avatar,
  Chip,
  IconButton,
  Paper,
  useTheme,
  Alert,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Construction,
  Assessment,
  CloudUpload,
  ViewInAr,
  Euro,
  Schedule,
  Engineering,
  Architecture,
  ArrowForward,
  Refresh,
  CheckCircle,
  Warning,
  Error,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { api } from '../services/api';

interface StatCard {
  title: string;
  value: string | number;
  change?: number;
  icon: React.ReactNode;
  color: string;
}

const Dashboard = () => {
  const theme = useTheme();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<StatCard[]>([]);
  const [recentProjects, setRecentProjects] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [systemHealth, setSystemHealth] = useState<any>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch dashboard data from all APIs
      const [metricsRes, healthRes, projectsRes, materialsRes, reportsRes] = await Promise.all([
        api.get('/v1/analytics/processing-metrics?period=30d'),
        api.get('/v1/health'),
        api.get('/v1/projects').catch(() => ({ data: [] })),
        api.get('/v1/materials/stats/summary').catch(() => ({ data: { total_materials: 0, total_value: 0 } })),
        api.get('/v1/reports/stats/summary').catch(() => ({ data: { total_reports: 0, total_value: 0 } })),
      ]);

      const metrics = metricsRes.data?.data || metricsRes.data || {};
      const projects = projectsRes.data || [];
      const materialsStats = materialsRes.data || {};
      const reportsStats = reportsRes.data || {};

      // Set stats from real data
      setStats([
        {
          title: 'Total Projects',
          value: projects.length,
          change: 0,
          icon: <Construction />,
          color: theme.palette.primary.main,
        },
        {
          title: 'Materials',
          value: materialsStats.total_materials || 0,
          change: 0,
          icon: <Engineering />,
          color: theme.palette.secondary.main,
        },
        {
          title: 'Reports Generated',
          value: reportsStats.total_reports || 0,
          change: 0,
          icon: <Assessment />,
          color: theme.palette.success.main,
        },
        {
          title: 'Total Value',
          value: `€${((materialsStats.total_value || 0) + (reportsStats.total_value || 0)).toLocaleString()}`,
          change: 0,
          icon: <Euro />,
          color: theme.palette.info.main,
        },
      ]);

      // Set recent projects from API
      const recentProjectsList = projects.slice(0, 3).map((p: any) => ({
        id: p.id,
        name: p.name,
        status: p.status,
        progress: p.progress,
        deadline: p.deadline,
        materials: p.materials_count || 0,
      }));
      setRecentProjects(recentProjectsList);

      // Set chart data (placeholder - would need time-series API)
      setChartData([
        { name: 'Mon', projects: projects.length, materials: materialsStats.total_materials || 0, revenue: 2400 },
        { name: 'Tue', projects: 0, materials: 0, revenue: 2210 },
        { name: 'Wed', projects: 0, materials: 0, revenue: 3290 },
        { name: 'Thu', projects: 0, materials: 0, revenue: 4908 },
        { name: 'Fri', projects: 0, materials: 0, revenue: 4800 },
        { name: 'Sat', projects: 0, materials: 0, revenue: 3800 },
        { name: 'Sun', projects: 0, materials: 0, revenue: 2300 },
      ]);

      // Set system health
      setSystemHealth(healthRes.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      // Use default mock data if API fails
    } finally {
      setLoading(false);
    }
  };

  const pieData = [
    { name: 'Concrete', value: 35, color: '#FF6B00' },
    { name: 'Steel', value: 25, color: '#1E3A5F' },
    { name: 'Wood', value: 20, color: '#4CAF50' },
    { name: 'Glass', value: 15, color: '#2196F3' },
    { name: 'Other', value: 5, color: '#9E9E9E' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'pending':
        return 'default';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle sx={{ fontSize: 16 }} />;
      case 'processing':
        return <Warning sx={{ fontSize: 16 }} />;
      case 'error':
        return <Error sx={{ fontSize: 16 }} />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ textAlign: 'center', mt: 4 }}>
          Loading Dashboard...
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Welcome Back! 👋
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Here's what's happening with your construction projects today
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={loadDashboardData}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<CloudUpload />}
            onClick={() => window.location.href = '/upload'}
          >
            New Upload
          </Button>
        </Box>
      </Box>

      {/* System Health Alert */}
      {systemHealth?.status === 'healthy' ? (
        <Alert severity="success" sx={{ mb: 3 }}>
          System is running smoothly - All services operational
        </Alert>
      ) : systemHealth?.status === 'degraded' ? (
        <Alert severity="warning" sx={{ mb: 3 }}>
          System performance degraded - Check services
        </Alert>
      ) : null}

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card
                sx={{
                  height: '100%',
                  background: 'linear-gradient(135deg, #FFFFFF 0%, #F5F7FA 100%)',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    transition: 'transform 0.3s',
                    boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                  },
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Avatar sx={{ bgcolor: `${stat.color}20`, color: stat.color }}>
                      {stat.icon}
                    </Avatar>
                    {stat.change !== undefined && (
                      <Chip
                        size="small"
                        icon={stat.change >= 0 ? <TrendingUp /> : <TrendingDown />}
                        label={`${Math.abs(stat.change)}%`}
                        color={stat.change >= 0 ? 'success' : 'error'}
                        variant="outlined"
                      />
                    )}
                  </Box>
                  <Typography variant="h4" fontWeight={700}>
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {stat.title}
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Weekly Activity
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stackId="1"
                    stroke={theme.palette.primary.main}
                    fill={theme.palette.primary.main}
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="materials"
                    stackId="2"
                    stroke={theme.palette.secondary.main}
                    fill={theme.palette.secondary.main}
                    fillOpacity={0.6}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Material Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Projects */}
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" fontWeight={600}>
              Recent Projects
            </Typography>
            <Button endIcon={<ArrowForward />} onClick={() => window.location.href = '/projects'}>
              View All
            </Button>
          </Box>

          <Grid container spacing={2}>
            {recentProjects.map((project) => (
              <Grid item xs={12} md={4} key={project.id}>
                <Paper
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    '&:hover': {
                      borderColor: 'primary.main',
                      boxShadow: '0 4px 12px rgba(255,107,0,0.15)',
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="subtitle1" fontWeight={600}>
                      {project.name}
                    </Typography>
                    <Chip
                      label={project.status}
                      color={getStatusColor(project.status) as any}
                      size="small"
                      icon={getStatusIcon(project.status) as any}
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {project.materials} materials • Due {project.deadline}
                  </Typography>

                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LinearProgress
                      variant="determinate"
                      value={project.progress}
                      sx={{ flex: 1, height: 8, borderRadius: 4 }}
                    />
                    <Typography variant="body2" fontWeight={600}>
                      {project.progress}%
                    </Typography>
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard;
