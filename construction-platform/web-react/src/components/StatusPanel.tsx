import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Chip, LinearProgress, List, ListItem } from '@mui/material';
import { CheckCircle, Error, Warning, Refresh } from '@mui/icons-material';
import websocketService from '../services/websocket';

interface WorkflowStatus {
  id: string;
  name: string;
  status: 'running' | 'completed' | 'error' | 'pending';
  progress: number;
  message?: string;
}

const StatusPanel: React.FC = () => {
  const [workflows, setWorkflows] = useState<WorkflowStatus[]>([]);
  
  useEffect(() => {
    const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';
    websocketService.connect(wsUrl);
    
    const handleWorkflowUpdate = (data: WorkflowStatus) => {
      setWorkflows(prev => {
        const existing = prev.find(w => w.id === data.id);
        if (existing) {
          return prev.map(w => w.id === data.id ? data : w);
        }
        return [...prev, data];
      });
    };
    
    websocketService.on('workflow_update', handleWorkflowUpdate);
    
    return () => {
      websocketService.off('workflow_update', handleWorkflowUpdate);
      websocketService.disconnect();
    };
  }, []);
  
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle color="success" />;
      case 'error': return <Error color="error" />;
      case 'running': return <Refresh className="spinning" />;
      default: return <Warning color="warning" />;
    }
  };
  
  if (workflows.length === 0) {
    return (
      <Card>
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            No active workflows
          </Typography>
        </CardContent>
      </Card>
    );
  }
  
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Real-Time Workflow Status
        </Typography>
        <List>
          {workflows.map(workflow => (
            <ListItem key={workflow.id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', mb: 1 }}>
                <Typography variant="body2">{workflow.name}</Typography>
                <Chip 
                  icon={getStatusIcon(workflow.status) as any}
                  label={workflow.status}
                  size="small"
                />
              </Box>
              <LinearProgress variant="determinate" value={workflow.progress} sx={{ width: '100%' }} />
              {workflow.message && (
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  {workflow.message}
                </Typography>
              )}
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default StatusPanel;
