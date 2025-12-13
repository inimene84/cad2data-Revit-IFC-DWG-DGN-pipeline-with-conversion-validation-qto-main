import React, { useState, useRef, Suspense } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import {
  OrbitControls,
  PerspectiveCamera,
  Environment,
  Grid,
  Box as ThreeBox,
  Text,
  Html,
  useGLTF,
  Stage,
  Center,
  Bounds,
  useBounds,
  Sky,
  Stats,
} from '@react-three/drei';
import * as THREE from 'three';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Slider,
  Switch,
  FormControlLabel,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Chip,
  Tooltip,
  Grid as MuiGrid,
  ToggleButton,
  ToggleButtonGroup,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Fullscreen,
  FullscreenExit,
  CameraAlt,
  Visibility,
  VisibilityOff,
  Layers,
  ZoomIn,
  ZoomOut,
  RestartAlt,
  GetApp,
  ViewInAr,
  Architecture,
  Construction,
  Settings,
  PlayArrow,
  Pause,
  Timeline,
  LocationOn,
  Info,
  Warning,
  CheckCircle,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

// Sample 3D Building Component
function Building({ position, scale, color, onClick, selected }: any) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  useFrame((state, delta) => {
    if (meshRef.current && hovered) {
      meshRef.current.rotation.y += delta * 0.5;
    }
  });

  return (
    <ThreeBox
      ref={meshRef}
      position={position}
      scale={selected ? [scale[0] * 1.1, scale[1] * 1.1, scale[2] * 1.1] : scale}
      onClick={onClick}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <meshStandardMaterial
        color={selected ? '#FF6B00' : hovered ? '#FF8A33' : color}
        emissive={selected ? '#FF6B00' : undefined}
        emissiveIntensity={selected ? 0.2 : 0}
      />
      {selected && (
        <Html position={[0, scale[1] / 2 + 0.5, 0]}>
          <div style={{
            background: 'rgba(0,0,0,0.8)',
            color: 'white',
            padding: '4px 8px',
            borderRadius: '4px',
            fontSize: '12px',
            whiteSpace: 'nowrap',
          }}>
            Selected Building
          </div>
        </Html>
      )}
    </ThreeBox>
  );
}

// Construction Site Component
function ConstructionSite() {
  const [selectedBuilding, setSelectedBuilding] = useState<number | null>(null);
  const [animationSpeed, setAnimationSpeed] = useState(1);

  const buildings = [
    { id: 1, position: [0, 1, 0], scale: [2, 2, 2], color: '#1E3A5F', name: 'Main Building' },
    { id: 2, position: [-4, 0.75, 2], scale: [1.5, 1.5, 1.5], color: '#4CAF50', name: 'Office Block' },
    { id: 3, position: [3, 0.5, -2], scale: [1, 1, 2], color: '#2196F3', name: 'Storage Facility' },
    { id: 4, position: [-2, 1.25, -3], scale: [2.5, 2.5, 1], color: '#9E9E9E', name: 'Workshop' },
  ];

  // Animated Crane
  const CraneArm = () => {
    const groupRef = useRef<THREE.Group>(null);
    
    useFrame((state) => {
      if (groupRef.current) {
        groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * animationSpeed * 0.2) * 0.5;
      }
    });

    return (
      <group ref={groupRef} position={[5, 0, 5]}>
        <ThreeBox position={[0, 2, 0]} scale={[0.2, 4, 0.2]}>
          <meshStandardMaterial color="#FFD700" />
        </ThreeBox>
        <ThreeBox position={[0, 4, 0]} scale={[3, 0.2, 0.2]}>
          <meshStandardMaterial color="#FFD700" />
        </ThreeBox>
        <Text
          position={[0, 5, 0]}
          fontSize={0.3}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          CRANE-01
        </Text>
      </group>
    );
  };

  return (
    <>
      {buildings.map((building) => (
        <Building
          key={building.id}
          position={building.position}
          scale={building.scale}
          color={building.color}
          onClick={() => setSelectedBuilding(building.id)}
          selected={selectedBuilding === building.id}
        />
      ))}
      <CraneArm />
      <Grid
        args={[20, 20]}
        cellSize={1}
        cellThickness={1}
        cellColor="#6f6f6f"
        sectionSize={5}
        sectionThickness={1.5}
        sectionColor="#FF6B00"
        fadeDistance={30}
        fadeStrength={1}
        followCamera={false}
        infiniteGrid={true}
      />
    </>
  );
}

const Visualization3D = () => {
  const [fullscreen, setFullscreen] = useState(false);
  const [viewMode, setViewMode] = useState<'perspective' | 'top' | 'side'>('perspective');
  const [showGrid, setShowGrid] = useState(true);
  const [showLabels, setShowLabels] = useState(true);
  const [showMeasurements, setShowMeasurements] = useState(false);
  const [playing, setPlaying] = useState(true);
  const [selectedLayer, setSelectedLayer] = useState('all');
  const [modelLoaded, setModelLoaded] = useState(false);

  const canvasRef = useRef<HTMLCanvasElement>(null);

  const handleScreenshot = () => {
    if (canvasRef.current) {
      const link = document.createElement('a');
      link.download = 'construction-3d-view.png';
      link.href = canvasRef.current.toDataURL();
      link.click();
    }
  };

  const layers = [
    { id: 'all', name: 'All Layers', icon: <Layers />, count: 4 },
    { id: 'structure', name: 'Structure', icon: <Architecture />, count: 2 },
    { id: 'mep', name: 'MEP Systems', icon: <Construction />, count: 1 },
    { id: 'finishes', name: 'Finishes', icon: <ViewInAr />, count: 1 },
  ];

  const projectInfo = {
    name: 'Office Complex Tartu',
    status: 'In Progress',
    completion: 65,
    area: '12,500 m²',
    floors: 5,
    materials: 234,
  };

  return (
    <Box sx={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            3D Visualization
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Interactive 3D view of construction project
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="outlined" startIcon={<GetApp />}>
            Export Model
          </Button>
          <Button variant="contained" startIcon={<ViewInAr />}>
            Open in AR
          </Button>
        </Box>
      </Box>

      {/* Main Content */}
      <MuiGrid container spacing={2} sx={{ flex: 1, overflow: 'hidden' }}>
        {/* 3D Viewer */}
        <MuiGrid item xs={12} md={9}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Toolbar */}
            <Box
              sx={{
                p: 1,
                borderBottom: '1px solid',
                borderColor: 'divider',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <Box sx={{ display: 'flex', gap: 1 }}>
                <ToggleButtonGroup
                  value={viewMode}
                  exclusive
                  onChange={(e, newMode) => newMode && setViewMode(newMode)}
                  size="small"
                >
                  <ToggleButton value="perspective">
                    <Tooltip title="Perspective View">
                      <ViewInAr />
                    </Tooltip>
                  </ToggleButton>
                  <ToggleButton value="top">
                    <Tooltip title="Top View">
                      <Architecture />
                    </Tooltip>
                  </ToggleButton>
                  <ToggleButton value="side">
                    <Tooltip title="Side View">
                      <Construction />
                    </Tooltip>
                  </ToggleButton>
                </ToggleButtonGroup>
                
                <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />
                
                <IconButton size="small" onClick={() => setPlaying(!playing)}>
                  {playing ? <Pause /> : <PlayArrow />}
                </IconButton>
                <IconButton size="small">
                  <RestartAlt />
                </IconButton>
                <IconButton size="small" onClick={handleScreenshot}>
                  <CameraAlt />
                </IconButton>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 1 }}>
                <FormControlLabel
                  control={<Switch checked={showGrid} onChange={(e) => setShowGrid(e.target.checked)} />}
                  label="Grid"
                />
                <FormControlLabel
                  control={<Switch checked={showLabels} onChange={(e) => setShowLabels(e.target.checked)} />}
                  label="Labels"
                />
                <IconButton
                  size="small"
                  onClick={() => setFullscreen(!fullscreen)}
                >
                  {fullscreen ? <FullscreenExit /> : <Fullscreen />}
                </IconButton>
              </Box>
            </Box>

            {/* 3D Canvas */}
            <Box sx={{ flex: 1, position: 'relative', bgcolor: '#f0f0f0' }}>
              {!modelLoaded && (
                <Alert severity="info" sx={{ m: 2 }}>
                  <Typography variant="subtitle2">
                    Loading 3D model... This is a demo visualization.
                  </Typography>
                  <Typography variant="caption">
                    Upload an IFC/DWG file to view your actual project
                  </Typography>
                </Alert>
              )}
              
              <Canvas
                ref={canvasRef}
                shadows
                camera={{ position: [10, 10, 10], fov: 50 }}
                style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }}
                onCreated={() => setModelLoaded(true)}
              >
                <Suspense fallback={null}>
                  <Sky sunPosition={[100, 20, 100]} />
                  <ambientLight intensity={0.5} />
                  <directionalLight
                    castShadow
                    position={[10, 10, 5]}
                    intensity={1}
                    shadow-mapSize={[2048, 2048]}
                  />
                  <pointLight position={[-10, -10, -10]} intensity={0.5} />
                  
                  <ConstructionSite />
                  
                  <OrbitControls
                    enablePan={true}
                    enableZoom={true}
                    enableRotate={true}
                    minDistance={5}
                    maxDistance={50}
                  />
                  
                  {/* <Stats /> */}
                </Suspense>
              </Canvas>
              
              {/* Overlays */}
              <Box
                sx={{
                  position: 'absolute',
                  top: 16,
                  left: 16,
                  bgcolor: 'rgba(255,255,255,0.9)',
                  p: 2,
                  borderRadius: 2,
                  minWidth: 200,
                }}
              >
                <Typography variant="subtitle2" fontWeight={600}>
                  {projectInfo.name}
                </Typography>
                <Chip
                  label={projectInfo.status}
                  color="warning"
                  size="small"
                  sx={{ mt: 1 }}
                />
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Area: {projectInfo.area}
                </Typography>
                <Typography variant="caption" display="block">
                  Progress: {projectInfo.completion}%
                </Typography>
              </Box>
            </Box>
          </Card>
        </MuiGrid>

        {/* Side Panel */}
        <MuiGrid item xs={12} md={3}>
          <Card sx={{ height: '100%', overflow: 'auto' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Layers & Elements
              </Typography>
              
              <List dense>
                {layers.map((layer) => (
                  <ListItem
                    key={layer.id}
                    button
                    selected={selectedLayer === layer.id}
                    onClick={() => setSelectedLayer(layer.id)}
                    sx={{
                      borderRadius: 1,
                      mb: 0.5,
                      '&.Mui-selected': {
                        bgcolor: 'primary.light',
                        color: 'white',
                        '& .MuiListItemIcon-root': {
                          color: 'white',
                        },
                      },
                    }}
                  >
                    <ListItemIcon>{layer.icon}</ListItemIcon>
                    <ListItemText
                      primary={layer.name}
                      secondary={`${layer.count} elements`}
                    />
                    <IconButton size="small">
                      {selectedLayer === layer.id ? <Visibility /> : <VisibilityOff />}
                    </IconButton>
                  </ListItem>
                ))}
              </List>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="h6" gutterBottom>
                View Settings
              </Typography>
              
              <Box sx={{ px: 1 }}>
                <Typography variant="body2" gutterBottom>
                  Animation Speed
                </Typography>
                <Slider
                  defaultValue={1}
                  min={0}
                  max={2}
                  step={0.1}
                  marks
                  valueLabelDisplay="auto"
                  sx={{ mb: 2 }}
                />
                
                <Typography variant="body2" gutterBottom>
                  Transparency
                </Typography>
                <Slider
                  defaultValue={100}
                  min={0}
                  max={100}
                  marks
                  valueLabelDisplay="auto"
                  sx={{ mb: 2 }}
                />
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="h6" gutterBottom>
                Annotations
              </Typography>
              
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <LocationOn color="error" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Issue #1"
                    secondary="Structural conflict - Floor 3"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <Warning color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Pending Review"
                    secondary="MEP coordination needed"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Approved"
                    secondary="Foundation complete"
                  />
                </ListItem>
              </List>
              
              <Box sx={{ mt: 2 }}>
                <Button fullWidth variant="outlined" startIcon={<Timeline />}>
                  Show Timeline
                </Button>
              </Box>
            </CardContent>
          </Card>
        </MuiGrid>
      </MuiGrid>
    </Box>
  );
};

export default Visualization3D;
