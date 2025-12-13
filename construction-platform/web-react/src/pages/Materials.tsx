import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  InputAdornment,
  LinearProgress,
  Alert,
  Button,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Search, Refresh, Add, Edit, Delete } from '@mui/icons-material';
import { api } from '../services/api';

interface Material {
  id: number;
  name: string;
  quantity: number;
  unit: string;
  price: number;
  supplier: string | null;
  category: string;
  project_id: number | null;
  created_at: string;
  updated_at: string;
}

const Materials = () => {
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingMaterial, setEditingMaterial] = useState<Material | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    quantity: 0,
    unit: 'unit',
    price: 0,
    supplier: '',
    category: 'construction',
  });

  const fetchMaterials = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = searchQuery ? { search: searchQuery } : {};
      const response = await api.get('/v1/materials', { params });
      setMaterials(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load materials');
      console.error('Error fetching materials:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMaterials();
  }, []);

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (searchQuery.length >= 2 || searchQuery.length === 0) {
        fetchMaterials();
      }
    }, 300);
    return () => clearTimeout(debounce);
  }, [searchQuery]);

  const handleOpenDialog = (material?: Material) => {
    if (material) {
      setEditingMaterial(material);
      setFormData({
        name: material.name,
        quantity: material.quantity,
        unit: material.unit,
        price: material.price,
        supplier: material.supplier || '',
        category: material.category,
      });
    } else {
      setEditingMaterial(null);
      setFormData({
        name: '',
        quantity: 0,
        unit: 'unit',
        price: 0,
        supplier: '',
        category: 'construction',
      });
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingMaterial(null);
  };

  const handleSave = async () => {
    try {
      if (editingMaterial) {
        await api.put(`/v1/materials/${editingMaterial.id}`, formData);
      } else {
        await api.post('/v1/materials', formData);
      }
      handleCloseDialog();
      fetchMaterials();
    } catch (err: any) {
      setError(err.message || 'Failed to save material');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this material?')) {
      try {
        await api.delete(`/v1/materials/${id}`);
        fetchMaterials();
      } catch (err: any) {
        setError(err.message || 'Failed to delete material');
      }
    }
  };

  const totalValue = materials.reduce((sum, m) => sum + m.price * m.quantity, 0);

  if (loading && materials.length === 0) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ textAlign: 'center', mt: 4 }}>
          Loading Materials...
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Materials Database
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {materials.length} materials • Total value: €{totalValue.toLocaleString('et-EE', { minimumFractionDigits: 2 })}
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" startIcon={<Refresh />} onClick={fetchMaterials}>
            Refresh
          </Button>
          <Button variant="contained" startIcon={<Add />} onClick={() => handleOpenDialog()}>
            Add Material
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent sx={{ py: 2 }}>
          <TextField
            placeholder="Search materials..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
            fullWidth
            size="small"
          />
        </CardContent>
      </Card>

      <Card>
        <CardContent sx={{ p: 0 }}>
          <TableContainer component={Paper} elevation={0}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell><strong>ID</strong></TableCell>
                  <TableCell><strong>Material</strong></TableCell>
                  <TableCell><strong>Category</strong></TableCell>
                  <TableCell align="right"><strong>Quantity</strong></TableCell>
                  <TableCell><strong>Unit</strong></TableCell>
                  <TableCell align="right"><strong>Price (€)</strong></TableCell>
                  <TableCell align="right"><strong>Total (€)</strong></TableCell>
                  <TableCell><strong>Supplier</strong></TableCell>
                  <TableCell align="center"><strong>Actions</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {materials.map((material) => (
                  <TableRow key={material.id} hover>
                    <TableCell>{material.id}</TableCell>
                    <TableCell><strong>{material.name}</strong></TableCell>
                    <TableCell>
                      <Chip label={material.category} size="small" variant="outlined" />
                    </TableCell>
                    <TableCell align="right">{material.quantity.toLocaleString()}</TableCell>
                    <TableCell>{material.unit}</TableCell>
                    <TableCell align="right">€{material.price.toFixed(2)}</TableCell>
                    <TableCell align="right">
                      <strong>€{(material.price * material.quantity).toFixed(2)}</strong>
                    </TableCell>
                    <TableCell>{material.supplier || '-'}</TableCell>
                    <TableCell align="center">
                      <IconButton size="small" onClick={() => handleOpenDialog(material)}>
                        <Edit fontSize="small" />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleDelete(material.id)} color="error">
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

      {/* Create/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingMaterial ? 'Edit Material' : 'Add New Material'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
            <TextField
              label="Material Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              fullWidth
              required
            />
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                label="Quantity"
                type="number"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: parseFloat(e.target.value) || 0 })}
                fullWidth
              />
              <TextField
                label="Unit"
                value={formData.unit}
                onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                fullWidth
              />
            </Box>
            <TextField
              label="Price per Unit (€)"
              type="number"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
              fullWidth
            />
            <TextField
              label="Supplier"
              value={formData.supplier}
              onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
              fullWidth
            />
            <TextField
              label="Category"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSave} variant="contained" disabled={!formData.name}>
            {editingMaterial ? 'Save Changes' : 'Add Material'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Materials;
