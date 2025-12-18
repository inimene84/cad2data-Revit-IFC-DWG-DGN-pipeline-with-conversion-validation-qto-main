// Data structure
const appData = {
  categories: [
    {
      id: 'frontend',
      name: 'Frontend/UX Enhancements',
      icon: '🎨',
      improvements: [
        { id: 'f1', name: 'File Management Dashboard', description: 'Drag-and-drop upload with real-time progress tracking', hours: 20, phase: 1 },
        { id: 'f2', name: 'Real-Time Status Panel', description: 'WebSocket-powered live workflow updates', hours: 16, phase: 1 },
        { id: 'f3', name: 'Analytics Dashboard', description: 'Cost trends, material breakdown, processing metrics', hours: 24, phase: 1 },
        { id: 'f4', name: 'Project Workspace', description: 'Multi-project organization with collaboration', hours: 32, phase: 2 },
        { id: 'f5', name: 'Export Functionality', description: 'BOQ, cost reports, compliance documentation', hours: 20, phase: 2 }
      ]
    },
    {
      id: 'api',
      name: 'API Optimization',
      icon: '⚙️',
      improvements: [
        { id: 'a1', name: 'Rate Limiting', description: 'Token bucket algorithm, 100 req/min per user', hours: 12, phase: 2 },
        { id: 'a2', name: 'Cursor-Based Pagination', description: 'Efficient data loading for large datasets', hours: 10, phase: 2 },
        { id: 'a3', name: 'Multi-Layer Caching', description: 'Redis caching for analysis, metadata, projects', hours: 16, phase: 2 },
        { id: 'a4', name: 'Async Workflows', description: 'Celery task queue with progress tracking', hours: 18, phase: 2 },
        { id: 'a5', name: 'Input Validation Layer', description: 'Pydantic models with comprehensive validation', hours: 14, phase: 2 }
      ]
    },
    {
      id: 'n8n',
      name: 'N8N Workflow Refinements',
      icon: '🔄',
      improvements: [
        { id: 'n1', name: 'Workflow Consolidation', description: 'Reduce 50+ workflows to 12-15 core workflows', hours: 40, phase: 2 },
        { id: 'n2', name: 'Performance Optimization', description: 'Timeout handlers, batch processing', hours: 20, phase: 2 },
        { id: 'n3', name: 'Webhook Throttling', description: 'Rate limiting and deduplication', hours: 12, phase: 2 },
        { id: 'n4', name: 'Conditional Execution', description: 'Smart routing based on file type', hours: 16, phase: 2 },
        { id: 'n5', name: 'Testing Framework', description: 'Unit, integration, E2E, and performance tests', hours: 30, phase: 3 }
      ]
    },
    {
      id: 'database',
      name: 'Database Improvements',
      icon: '🗄️',
      improvements: [
        { id: 'd1', name: 'Connection Pooling', description: 'PostgreSQL pool optimization (20 size, 40 overflow)', hours: 8, phase: 2 },
        { id: 'd2', name: 'Index Optimization', description: 'Strategic indexes on key queries', hours: 16, phase: 2 },
        { id: 'd3', name: 'Automated Archival', description: 'Archive old files to S3 Glacier', hours: 20, phase: 3 },
        { id: 'd4', name: 'Vector DB Integration', description: 'Qdrant for similarity search in cost estimates', hours: 24, phase: 3 },
        { id: 'd5', name: 'Query Optimization', description: 'Identify and optimize slow queries', hours: 14, phase: 2 }
      ]
    },
    {
      id: 'errors',
      name: 'Error Handling',
      icon: '⚠️',
      improvements: [
        { id: 'e1', name: 'Circuit Breaker Pattern', description: 'Protect against cascading failures', hours: 14, phase: 2 },
        { id: 'e2', name: 'Graceful Degradation', description: 'Partial processing when services fail', hours: 12, phase: 2 },
        { id: 'e3', name: 'User-Friendly Messages', description: 'Translate technical errors for users', hours: 10, phase: 2 },
        { id: 'e4', name: 'Retry Strategy', description: 'Exponential backoff with jitter', hours: 12, phase: 2 },
        { id: 'e5', name: 'Error Analytics', description: 'Track and analyze error patterns', hours: 16, phase: 3 }
      ]
    },
    {
      id: 'security',
      name: 'Security Hardening',
      icon: '🔒',
      improvements: [
        { id: 's1', name: 'API Key Rotation', description: 'Automated 30-day rotation with grace period', hours: 18, phase: 2 },
        { id: 's2', name: 'CORS Configuration', description: 'Strict CORS policies for production', hours: 8, phase: 2 },
        { id: 's3', name: 'Input Sanitization', description: 'File validation and malware scanning', hours: 16, phase: 2 },
        { id: 's4', name: 'Audit Logging', description: 'Comprehensive event tracking and logging', hours: 20, phase: 3 },
        { id: 's5', name: 'Security Rate Limiting', description: 'Aggressive limits on auth endpoints', hours: 10, phase: 2 }
      ]
    },
    {
      id: 'performance',
      name: 'Performance Optimization',
      icon: '⚡',
      improvements: [
        { id: 'p1', name: 'File Compression', description: 'Gzip compression before processing', hours: 12, phase: 2 },
        { id: 'p2', name: 'Parallel Processing', description: 'Concurrent file processing (batch size 10)', hours: 18, phase: 2 },
        { id: 'p3', name: 'Resource Monitoring', description: 'Monitor memory, CPU, disk usage', hours: 14, phase: 3 },
        { id: 'p4', name: 'Load Testing', description: 'Test with 1000 concurrent users', hours: 24, phase: 3 },
        { id: 'p5', name: 'CDN Integration', description: 'CloudFront for static assets', hours: 16, phase: 3 }
      ]
    },
    {
      id: 'monitoring',
      name: 'Monitoring & Observability',
      icon: '📊',
      improvements: [
        { id: 'm1', name: 'Custom Grafana Dashboards', description: 'Business metrics and KPIs', hours: 20, phase: 2 },
        { id: 'm2', name: 'Prometheus Alerts', description: 'Alert rules for critical metrics', hours: 16, phase: 2 },
        { id: 'm3', name: 'ELK Stack Setup', description: 'Log aggregation and visualization', hours: 24, phase: 3 },
        { id: 'm4', name: 'Distributed Tracing', description: 'OpenTelemetry with Jaeger', hours: 22, phase: 3 },
        { id: 'm5', name: 'Health Checks', description: 'Comprehensive system health endpoints', hours: 12, phase: 2 }
      ]
    },
    {
      id: 'business',
      name: 'Business Features',
      icon: '💼',
      improvements: [
        { id: 'b1', name: 'Multi-Tenancy Support', description: 'Tenant isolation and data separation', hours: 32, phase: 3 },
        { id: 'b2', name: 'Usage Analytics', description: 'Track files, API calls, storage usage', hours: 24, phase: 3 },
        { id: 'b3', name: 'Billing Integration', description: 'Usage-based billing and invoicing', hours: 30, phase: 3 },
        { id: 'b4', name: 'Automation Rules', description: 'User-defined workflow automation', hours: 28, phase: 4 }
      ]
    },
    {
      id: 'roadmap',
      name: 'Implementation Roadmap',
      icon: '🗺️',
      improvements: [
        { id: 'r1', name: 'Phase 1 Planning', description: 'Quick wins, UX improvements', hours: 60, phase: 1 },
        { id: 'r2', name: 'Phase 2 Planning', description: 'Core technical improvements', hours: 120, phase: 2 },
        { id: 'r3', name: 'Phase 3 Planning', description: 'Advanced features and scaling', hours: 160, phase: 3 },
        { id: 'r4', name: 'Phase 4 Planning', description: 'Optimization and enterprise features', hours: 100, phase: 4 }
      ]
    }
  ],
  phases: [
    { id: 1, name: 'Quick Wins', week_start: 1, week_end: 2, total_hours: 60, impact: '40% UX improvement', description: 'WebSocket updates, progress indicators, basic monitoring' },
    { id: 2, name: 'Core Improvements', week_start: 3, week_end: 6, total_hours: 120, impact: '30% performance, 50% error reduction', description: 'API optimization, database improvements, security hardening' },
    { id: 3, name: 'Advanced Features', week_start: 7, week_end: 10, total_hours: 160, impact: 'Enterprise-ready platform', description: 'Multi-tenancy, billing, advanced monitoring' },
    { id: 4, name: 'Optimization & Scaling', week_start: 11, week_end: 15, total_hours: 100, impact: '10x scalability', description: 'Performance optimization, automation rules, load testing' }
  ],
  tools: {
    monitoring: [
      { name: 'Grafana', description: 'Dashboards and visualization', url: 'https://grafana.com' },
      { name: 'Prometheus', description: 'Metrics collection and alerting', url: 'https://prometheus.io' },
      { name: 'ELK Stack', description: 'Elasticsearch, Logstash, Kibana', url: 'https://www.elastic.co/elk-stack' },
      { name: 'Jaeger', description: 'Distributed tracing', url: 'https://www.jaegertracing.io' }
    ],
    testing: [
      { name: 'Locust', description: 'Load testing framework', url: 'https://locust.io' },
      { name: 'pytest', description: 'Python testing framework', url: 'https://pytest.org' },
      { name: 'Postman', description: 'API testing and documentation', url: 'https://www.postman.com' },
      { name: 'Selenium', description: 'UI automation testing', url: 'https://www.selenium.dev' }
    ],
    security: [
      { name: 'OWASP ZAP', description: 'Security scanning tool', url: 'https://www.zaproxy.org' },
      { name: 'Snyk', description: 'Dependency vulnerability scanning', url: 'https://snyk.io' },
      { name: 'SonarQube', description: 'Code quality and security', url: 'https://www.sonarqube.org' }
    ],
    infrastructure: [
      { name: 'Docker', description: 'Containerization', url: 'https://www.docker.com' },
      { name: 'Kubernetes', description: 'Container orchestration', url: 'https://kubernetes.io' },
      { name: 'Terraform', description: 'Infrastructure as Code', url: 'https://www.terraform.io' },
      { name: 'CloudFlare', description: 'CDN and security', url: 'https://www.cloudflare.com' }
    ]
  }
};

// State management
const appState = {
  improvementStatus: {},
  improvementNotes: {},
  currentTheme: 'light',
  selectedCategory: null,
  filters: {
    phase: 'all',
    status: 'all',
    search: ''
  }
};

// Initialize improvement status
function initializeState() {
  appData.categories.forEach(category => {
    category.improvements.forEach(improvement => {
      if (!appState.improvementStatus[improvement.id]) {
        appState.improvementStatus[improvement.id] = 'not-started';
      }
      if (!appState.improvementNotes[improvement.id]) {
        appState.improvementNotes[improvement.id] = '';
      }
    });
  });
}

// Theme toggle
function toggleTheme() {
  const html = document.documentElement;
  const themeIcon = document.getElementById('themeIcon');
  
  if (appState.currentTheme === 'light') {
    html.setAttribute('data-color-scheme', 'dark');
    appState.currentTheme = 'dark';
    themeIcon.textContent = '☀️';
  } else {
    html.setAttribute('data-color-scheme', 'light');
    appState.currentTheme = 'light';
    themeIcon.textContent = '🌙';
  }
}

// Tab navigation
function switchTab(tabName) {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  
  document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
  document.getElementById(`${tabName}-tab`).classList.add('active');
  
  if (tabName === 'progress') {
    setTimeout(renderCharts, 100);
  }
}

// Calculate metrics
function calculateMetrics() {
  let totalImprovements = 0;
  let completedImprovements = 0;
  let totalHours = 0;
  
  appData.categories.forEach(category => {
    category.improvements.forEach(improvement => {
      totalImprovements++;
      totalHours += improvement.hours;
      if (appState.improvementStatus[improvement.id] === 'completed') {
        completedImprovements++;
      }
    });
  });
  
  const completedPercentage = totalImprovements > 0 
    ? Math.round((completedImprovements / totalImprovements) * 100) 
    : 0;
  
  return { totalImprovements, completedImprovements, completedPercentage, totalHours };
}

// Update dashboard metrics
function updateDashboardMetrics() {
  const metrics = calculateMetrics();
  document.getElementById('totalImprovements').textContent = metrics.totalImprovements;
  document.getElementById('completedPercentage').textContent = `${metrics.completedPercentage}%`;
  document.getElementById('totalHours').textContent = `${metrics.totalHours}h`;
  
  // Determine current phase based on completion
  let currentPhase = 'Phase 1';
  const phase1Complete = checkPhaseCompletion(1);
  const phase2Complete = checkPhaseCompletion(2);
  const phase3Complete = checkPhaseCompletion(3);
  
  if (phase3Complete >= 50) currentPhase = 'Phase 4';
  else if (phase2Complete >= 50) currentPhase = 'Phase 3';
  else if (phase1Complete >= 50) currentPhase = 'Phase 2';
  
  document.getElementById('currentPhase').textContent = currentPhase;
}

// Check phase completion
function checkPhaseCompletion(phaseId) {
  let total = 0;
  let completed = 0;
  
  appData.categories.forEach(category => {
    category.improvements.forEach(improvement => {
      if (improvement.phase === phaseId) {
        total++;
        if (appState.improvementStatus[improvement.id] === 'completed') {
          completed++;
        }
      }
    });
  });
  
  return total > 0 ? Math.round((completed / total) * 100) : 0;
}

// Render categories grid
function renderCategoriesGrid() {
  const grid = document.getElementById('categoriesGrid');
  grid.innerHTML = '';
  
  appData.categories.forEach(category => {
    const filteredImprovements = filterImprovements(category.improvements);
    if (filteredImprovements.length === 0 && appState.filters.search) return;
    
    const total = filteredImprovements.length;
    const completed = filteredImprovements.filter(imp => 
      appState.improvementStatus[imp.id] === 'completed'
    ).length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    
    const card = document.createElement('div');
    card.className = 'category-card';
    card.innerHTML = `
      <div class="category-header">
        <span class="category-icon">${category.icon}</span>
        <h3 class="category-title">${category.name}</h3>
      </div>
      <div class="category-stats">
        <div class="stat-item">
          <span class="stat-value">${total}</span>
          <span class="stat-label">Items</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">${percentage}%</span>
          <span class="stat-label">Complete</span>
        </div>
      </div>
      <div class="progress-bar-container">
        <div class="progress-bar" style="width: ${percentage}%"></div>
      </div>
    `;
    
    card.addEventListener('click', () => {
      appState.selectedCategory = category;
      showImprovementsList(category);
    });
    
    grid.appendChild(card);
  });
}

// Filter improvements
function filterImprovements(improvements) {
  return improvements.filter(imp => {
    const phaseMatch = appState.filters.phase === 'all' || imp.phase === parseInt(appState.filters.phase);
    const statusMatch = appState.filters.status === 'all' || appState.improvementStatus[imp.id] === appState.filters.status;
    const searchMatch = !appState.filters.search || 
      imp.name.toLowerCase().includes(appState.filters.search.toLowerCase()) ||
      imp.description.toLowerCase().includes(appState.filters.search.toLowerCase());
    
    return phaseMatch && statusMatch && searchMatch;
  });
}

// Show improvements list
function showImprovementsList(category) {
  const listContainer = document.getElementById('improvementsList');
  const grid = document.getElementById('categoriesGrid');
  
  grid.style.display = 'none';
  listContainer.style.display = 'block';
  
  const filteredImprovements = filterImprovements(category.improvements);
  
  listContainer.innerHTML = `
    <div class="list-header">
      <h2>${category.icon} ${category.name}</h2>
      <button class="btn btn--secondary" onclick="showCategoriesGrid()">← Back to Categories</button>
    </div>
  `;
  
  filteredImprovements.forEach(improvement => {
    const status = appState.improvementStatus[improvement.id];
    const item = document.createElement('div');
    item.className = 'improvement-item';
    item.innerHTML = `
      <input type="checkbox" class="improvement-checkbox" 
        ${status === 'completed' ? 'checked' : ''} 
        onchange="toggleImprovementStatus('${improvement.id}')">
      <div class="improvement-content">
        <h4 class="improvement-name">${improvement.name}</h4>
        <p class="improvement-description">${improvement.description}</p>
        <div class="improvement-meta">
          <span class="meta-item">⏱️ ${improvement.hours}h</span>
          <span class="meta-item">📋 Phase ${improvement.phase}</span>
          <span class="status-badge status-${status}">${status.replace('-', ' ')}</span>
        </div>
      </div>
    `;
    
    item.addEventListener('click', (e) => {
      if (e.target.type !== 'checkbox') {
        showImprovementDetail(improvement, category);
      }
    });
    
    listContainer.appendChild(item);
  });
}

// Show categories grid
function showCategoriesGrid() {
  document.getElementById('categoriesGrid').style.display = 'grid';
  document.getElementById('improvementsList').style.display = 'none';
  appState.selectedCategory = null;
}

// Toggle improvement status
function toggleImprovementStatus(improvementId) {
  const currentStatus = appState.improvementStatus[improvementId];
  appState.improvementStatus[improvementId] = currentStatus === 'completed' ? 'not-started' : 'completed';
  updateDashboardMetrics();
  
  if (appState.selectedCategory) {
    showImprovementsList(appState.selectedCategory);
  } else {
    renderCategoriesGrid();
  }
}

// Show improvement detail modal
function showImprovementDetail(improvement, category) {
  const modal = document.getElementById('improvementModal');
  const status = appState.improvementStatus[improvement.id];
  const notes = appState.improvementNotes[improvement.id];
  const phase = appData.phases.find(p => p.id === improvement.phase);
  
  document.getElementById('modalTitle').textContent = improvement.name;
  document.getElementById('modalDescription').textContent = improvement.description;
  document.getElementById('modalHours').textContent = `${improvement.hours} hours`;
  document.getElementById('modalPhase').textContent = phase ? phase.name : `Phase ${improvement.phase}`;
  document.getElementById('modalCategory').textContent = category.name;
  document.getElementById('modalStatus').value = status;
  document.getElementById('modalNotes').value = notes;
  
  modal.classList.add('active');
  modal.dataset.improvementId = improvement.id;
}

// Close modal
function closeModal() {
  document.getElementById('improvementModal').classList.remove('active');
}

// Save improvement changes
function saveImprovementChanges() {
  const modal = document.getElementById('improvementModal');
  const improvementId = modal.dataset.improvementId;
  const newStatus = document.getElementById('modalStatus').value;
  const newNotes = document.getElementById('modalNotes').value;
  
  appState.improvementStatus[improvementId] = newStatus;
  appState.improvementNotes[improvementId] = newNotes;
  
  updateDashboardMetrics();
  if (appState.selectedCategory) {
    showImprovementsList(appState.selectedCategory);
  } else {
    renderCategoriesGrid();
  }
  
  closeModal();
}

// Render implementation phases
function renderImplementationPhases() {
  const container = document.getElementById('phasesContainer');
  container.innerHTML = '';
  
  appData.phases.forEach(phase => {
    const phaseImprovements = [];
    appData.categories.forEach(category => {
      category.improvements.forEach(improvement => {
        if (improvement.phase === phase.id) {
          phaseImprovements.push({ ...improvement, categoryName: category.name });
        }
      });
    });
    
    const completion = checkPhaseCompletion(phase.id);
    
    const card = document.createElement('div');
    card.className = 'phase-card';
    card.innerHTML = `
      <div class="phase-header">
        <div class="phase-info">
          <h3>Phase ${phase.id}: ${phase.name}</h3>
          <p class="phase-timeline">Week ${phase.week_start}-${phase.week_end}</p>
          <p class="phase-impact">${phase.impact}</p>
        </div>
        <div class="phase-stats">
          <div class="phase-hours">${phase.total_hours}h</div>
          <div class="phase-completion">${completion}% Complete</div>
        </div>
      </div>
      <p class="phase-description">${phase.description}</p>
      <div class="progress-bar-container" style="margin-bottom: 20px;">
        <div class="progress-bar" style="width: ${completion}%"></div>
      </div>
      <div class="phase-improvements">
        ${phaseImprovements.map(imp => `
          <div class="phase-improvement">
            <div>
              <div class="phase-improvement-name">${imp.name}</div>
              <div class="phase-improvement-hours" style="font-size: 12px; color: var(--color-text-secondary);">${imp.categoryName}</div>
            </div>
            <div>
              <span class="status-badge status-${appState.improvementStatus[imp.id]}">
                ${appState.improvementStatus[imp.id].replace('-', ' ')}
              </span>
            </div>
          </div>
        `).join('')}
      </div>
    `;
    
    container.appendChild(card);
  });
}

// Render charts
function renderCharts() {
  const metrics = calculateMetrics();
  
  // Overall Progress Chart (Doughnut)
  const overallCtx = document.getElementById('overallProgressChart');
  if (overallCtx) {
    new Chart(overallCtx, {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'In Progress', 'Not Started'],
        datasets: [{
          data: [
            Object.values(appState.improvementStatus).filter(s => s === 'completed').length,
            Object.values(appState.improvementStatus).filter(s => s === 'in-progress').length,
            Object.values(appState.improvementStatus).filter(s => s === 'not-started').length
          ],
          backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { position: 'bottom' }
        }
      }
    });
  }
  
  // Progress by Phase (Bar)
  const phaseCtx = document.getElementById('phaseProgressChart');
  if (phaseCtx) {
    new Chart(phaseCtx, {
      type: 'bar',
      data: {
        labels: appData.phases.map(p => `Phase ${p.id}`),
        datasets: [{
          label: 'Completion %',
          data: appData.phases.map(p => checkPhaseCompletion(p.id)),
          backgroundColor: '#1FB8CD'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: { beginAtZero: true, max: 100 }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
  
  // Progress by Category (Horizontal Bar)
  const categoryCtx = document.getElementById('categoryProgressChart');
  if (categoryCtx) {
    new Chart(categoryCtx, {
      type: 'bar',
      data: {
        labels: appData.categories.map(c => c.name),
        datasets: [{
          label: 'Completion %',
          data: appData.categories.map(c => {
            const total = c.improvements.length;
            const completed = c.improvements.filter(imp => 
              appState.improvementStatus[imp.id] === 'completed'
            ).length;
            return total > 0 ? Math.round((completed / total) * 100) : 0;
          }),
          backgroundColor: '#FFC185'
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          x: { beginAtZero: true, max: 100 }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
  
  // Time Tracking (Line)
  const timeCtx = document.getElementById('timeTrackingChart');
  if (timeCtx) {
    const phaseHours = appData.phases.map(phase => {
      let completed = 0;
      appData.categories.forEach(category => {
        category.improvements.forEach(improvement => {
          if (improvement.phase === phase.id && 
              appState.improvementStatus[improvement.id] === 'completed') {
            completed += improvement.hours;
          }
        });
      });
      return completed;
    });
    
    new Chart(timeCtx, {
      type: 'line',
      data: {
        labels: appData.phases.map(p => `Phase ${p.id}`),
        datasets: [
          {
            label: 'Hours Completed',
            data: phaseHours,
            borderColor: '#1FB8CD',
            backgroundColor: 'rgba(31, 184, 205, 0.1)',
            fill: true
          },
          {
            label: 'Total Hours',
            data: appData.phases.map(p => p.total_hours),
            borderColor: '#B4413C',
            backgroundColor: 'rgba(180, 65, 60, 0.1)',
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
}

// Render resources
function renderResources() {
  const container = document.getElementById('resourcesContent');
  container.innerHTML = '';
  
  const categories = [
    { key: 'monitoring', title: 'Monitoring Tools', icon: '📊' },
    { key: 'testing', title: 'Testing Tools', icon: '🧪' },
    { key: 'security', title: 'Security Tools', icon: '🔒' },
    { key: 'infrastructure', title: 'Infrastructure Tools', icon: '🏗️' }
  ];
  
  categories.forEach(cat => {
    const section = document.createElement('div');
    section.className = 'resource-category';
    section.innerHTML = `
      <h3>${cat.icon} ${cat.title}</h3>
      <div class="resource-grid">
        ${appData.tools[cat.key].map(tool => `
          <div class="resource-item">
            <div class="resource-name">${tool.name}</div>
            <div class="resource-description">${tool.description}</div>
            <a href="${tool.url}" target="_blank" class="resource-link">Learn more →</a>
          </div>
        `).join('')}
      </div>
    `;
    container.appendChild(section);
  });
}

// Export report
function exportReport() {
  const metrics = calculateMetrics();
  const report = [
    'Construction AI Platform - Improvements Report',
    '='.repeat(50),
    '',
    `Generated: ${new Date().toLocaleString()}`,
    '',
    'OVERVIEW',
    '-'.repeat(50),
    `Total Improvements: ${metrics.totalImprovements}`,
    `Completed: ${metrics.completedImprovements} (${metrics.completedPercentage}%)`,
    `Total Hours: ${metrics.totalHours}`,
    '',
    'PHASE COMPLETION',
    '-'.repeat(50)
  ];
  
  appData.phases.forEach(phase => {
    const completion = checkPhaseCompletion(phase.id);
    report.push(`Phase ${phase.id} (${phase.name}): ${completion}%`);
  });
  
  report.push('', 'CATEGORY BREAKDOWN', '-'.repeat(50));
  
  appData.categories.forEach(category => {
    const total = category.improvements.length;
    const completed = category.improvements.filter(imp => 
      appState.improvementStatus[imp.id] === 'completed'
    ).length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    report.push(`${category.name}: ${completed}/${total} (${percentage}%)`);
  });
  
  const blob = new Blob([report.join('\n')], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'improvements-report.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
  initializeState();
  updateDashboardMetrics();
  renderCategoriesGrid();
  renderImplementationPhases();
  renderResources();
  
  // Tab navigation
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      switchTab(btn.dataset.tab);
    });
  });
  
  // Theme toggle
  document.getElementById('themeToggle').addEventListener('click', toggleTheme);
  
  // Export button
  document.getElementById('exportBtn').addEventListener('click', exportReport);
  
  // Filters
  document.getElementById('filterPhase').addEventListener('change', (e) => {
    appState.filters.phase = e.target.value;
    if (appState.selectedCategory) {
      showImprovementsList(appState.selectedCategory);
    } else {
      renderCategoriesGrid();
    }
  });
  
  document.getElementById('filterStatus').addEventListener('change', (e) => {
    appState.filters.status = e.target.value;
    if (appState.selectedCategory) {
      showImprovementsList(appState.selectedCategory);
    } else {
      renderCategoriesGrid();
    }
  });
  
  document.getElementById('searchInput').addEventListener('input', (e) => {
    appState.filters.search = e.target.value;
    if (appState.selectedCategory) {
      showImprovementsList(appState.selectedCategory);
    } else {
      renderCategoriesGrid();
    }
  });
  
  // Modal controls
  document.getElementById('modalClose').addEventListener('click', closeModal);
  document.getElementById('modalCancel').addEventListener('click', closeModal);
  document.getElementById('modalSave').addEventListener('click', saveImprovementChanges);
  
  // Close modal on background click
  document.getElementById('improvementModal').addEventListener('click', (e) => {
    if (e.target.id === 'improvementModal') {
      closeModal();
    }
  });
});