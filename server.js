const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const swaggerUi = require('swagger-ui-express');
const openapiSpec = require('./swagger/openapi.json');
require('dotenv').config();

const app = express();

// Настройка CORS для продакшена
const corsOptions = {
  origin: process.env.FRONTEND_URL || '*',
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(
  helmet({
    contentSecurityPolicy: {
      useDefaults: true,
      directives: {
        'style-src': ["'self'", "'unsafe-inline'"],
        'script-src': ["'self'", "'unsafe-inline'"],
        'img-src': ["'self'", 'data:', 'https:'],
      },
    },
  })
);
app.use(morgan('combined'));
app.use(cors(corsOptions));
app.use(express.json({ limit: '10kb' }));

// Import routes
const authRoutes = require('./routes/authRoutes');
const taskRoutes = require('./routes/taskRoutes');
const userRoutes = require('./routes/userRoutes');

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/tasks', taskRoutes);
app.use('/api/user', userRoutes);

app.get('/api/docs/openapi.json', (req, res) => {
  res.json(openapiSpec);
});

app.use(
  '/api/docs',
  swaggerUi.serve,
  swaggerUi.setup(openapiSpec, {
    customSiteTitle: 'To-Do List API — Swagger',
    swaggerOptions: {
      persistAuthorization: true,
    },
  })
);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'To-Do List API',
    version: '1.0.0',
    status: 'running',
    swagger: '/api/docs',
    openapiJson: '/api/docs/openapi.json',
    endpoints: {
      register: 'POST /api/auth/register',
      login: 'POST /api/auth/login',
      refresh: 'POST /api/auth/refresh',
      tasks: 'GET /api/tasks',
      createTask: 'POST /api/tasks',
      profile: 'GET /api/user/profile'
    }
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    message: 'Route not found' 
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(err.status || 500).json({
    message: process.env.NODE_ENV === 'production' 
      ? 'Internal server error' 
      : err.message
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});