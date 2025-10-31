# Life Organizer - Proyecto de Salud y Productividad

## Descripción del Proyecto

Life Organizer es una aplicación web integral que combina gestión de tareas con monitoreo de salud personal. El proyecto está diseñado para ayudar a los usuarios a mantener un estilo de vida saludable mientras organizan sus actividades diarias.

## Estructura del Proyecto

```
life-organizer/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── data_analysis.py
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── health_tracker.html
│       └── analytics.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── data/
│   └── sample_data.csv
├── requirements.txt
├── README.md
└── run.py
```

## Tecnologías Utilizadas

### Backend
- **Python 3.9+**: Lenguaje principal
- **Flask**: Framework web ligero
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos local

### Análisis de Datos
- **Pandas**: Manipulación y análisis de datos
- **Matplotlib**: Visualizaciones básicas
- **Seaborn**: Visualizaciones estadísticas avanzadas
- **Plotly**: Gráficos interactivos

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript**: Interactividad
- **Bootstrap**: Framework CSS
- **Chart.js**: Gráficos en el frontend

## Instalación y Configuración

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno virtual: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Ejecutar aplicación: `python run.py`

## Características Principales

### 1. Gestión de Usuarios
- Registro e inicio de sesión
- Perfil de usuario con información de salud
- Encuesta inicial de salud

### 2. Monitoreo de Salud
- Seguimiento de hidratación diaria
- Registro de presión arterial
- Control de peso
- Seguimiento de comidas
- Recordatorios de medicamentos

### 3. Gestión de Tareas
- Creación y organización de tareas
- Categorización por tipo (salud, trabajo, personal)
- Recordatorios y notificaciones
- Seguimiento de progreso

### 4. Análisis y Reportes
- Estadísticas de salud personalizadas
- Gráficos de tendencias
- Alertas de salud automáticas
- Reportes semanales y mensuales

## Base de Datos

### Tablas Principales
- **users**: Información de usuarios
- **health_data**: Datos de salud (presión, peso, hidratación)
- **tasks**: Tareas y actividades
- **notifications**: Sistema de alertas
- **health_alerts**: Alertas de salud automáticas

## API Endpoints

### Usuarios
- `POST /api/register` - Registro de usuario
- `POST /api/login` - Inicio de sesión
- `GET /api/user/profile` - Obtener perfil

### Salud
- `POST /api/health/water` - Registrar consumo de agua
- `POST /api/health/blood-pressure` - Registrar presión arterial
- `GET /api/health/summary` - Resumen de salud

### Tareas
- `GET /api/tasks` - Obtener tareas
- `POST /api/tasks` - Crear tarea
- `PUT /api/tasks/<id>` - Actualizar tarea

### Análisis
- `GET /api/analytics/health-trends` - Tendencias de salud
- `GET /api/analytics/task-completion` - Estadísticas de tareas

## Contribución

1. Fork del proyecto
2. Crear rama para feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o sugerencias, contactar a través de los issues del repositorio.
