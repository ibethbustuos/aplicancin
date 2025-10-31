# Life Organizer - Guía de Ejecución

## Instrucciones Rápidas

### 1. Instalación
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/life-organizer.git
cd life-organizer

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecución
```bash
# Ejecutar la aplicación
python run.py
```

### 3. Acceso
- **URL**: http://localhost:5000
- **Usuario Demo**: demo@lifeorganizer.com
- **Contraseña**: demo123

## Estructura del Proyecto

```
life-organizer/
├── app/                    # Aplicación principal
│   ├── __init__.py        # Configuración Flask
│   ├── models.py          # Modelos de BD
│   ├── routes.py          # Rutas y API
│   └── data_analysis.py  # Análisis de datos
├── templates/             # Templates HTML
├── static/               # Archivos estáticos
├── data/                 # Datos de muestra
├── requirements.txt      # Dependencias
├── run.py               # Archivo principal
└── README.md            # Documentación
```

## Funcionalidades Principales

### 1. Gestión de Usuarios
- Registro e inicio de sesión
- Perfil de usuario con datos de salud
- Autenticación segura

### 2. Monitoreo de Salud
- Seguimiento de hidratación diaria
- Registro de presión arterial
- Control de peso y ejercicio
- Seguimiento de comidas

### 3. Gestión de Tareas
- Creación y organización de tareas
- Categorización por tipo
- Recordatorios y notificaciones
- Seguimiento de progreso

### 4. Análisis de Datos
- Estadísticas de salud personalizadas
- Gráficos de tendencias temporales
- Alertas de salud automáticas
- Reportes visuales

## API Endpoints

### Salud
- `POST /api/health/water` - Agregar agua
- `POST /api/health/blood-pressure` - Registrar presión
- `POST /api/health/weight` - Registrar peso
- `GET /api/health/summary` - Resumen de salud

### Tareas
- `GET /api/tasks` - Obtener tareas
- `POST /api/tasks` - Crear tarea
- `PUT /api/tasks/<id>` - Actualizar tarea

### Análisis
- `GET /api/analytics/health-trends` - Tendencias
- `GET /api/analytics/task-completion` - Estadísticas

## Base de Datos

### Tablas Principales
- **users**: Información de usuarios
- **health_data**: Datos de salud diarios
- **tasks**: Tareas y actividades
- **notifications**: Sistema de alertas
- **health_alerts**: Alertas automáticas

### Generar Datos de Muestra
```bash
cd data
python generate_sample_data.py
```

## Tecnologías Utilizadas

### Backend
- **Python 3.9+**: Lenguaje principal
- **Flask 2.3.3**: Framework web
- **SQLAlchemy 3.0.5**: ORM
- **SQLite**: Base de datos

### Análisis de Datos
- **Pandas 2.1.1**: Manipulación de datos
- **Matplotlib 3.7.2**: Visualizaciones
- **Seaborn 0.12.2**: Gráficos estadísticos

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **Bootstrap 5**: Framework CSS
- **JavaScript**: Interactividad
- **Chart.js**: Gráficos interactivos

## Solución de Problemas

### Error: "Module not found"
```bash
# Verificar entorno virtual
which python  # Linux/macOS
where python  # Windows

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "Port already in use"
```bash
# Cambiar puerto en run.py
app.run(port=5001)
```

### Error: "Database is locked"
```bash
# Cerrar aplicación y reiniciar
# Verificar que no hay otras instancias ejecutándose
```

## Desarrollo

### Estructura de Código
- **Models**: Definición de entidades
- **Routes**: Lógica de endpoints
- **Templates**: Vistas HTML
- **Static**: Assets estáticos

### Testing
```bash
# Ejecutar tests (si están implementados)
python -m pytest tests/
```

### Debugging
```bash
# Modo debug
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development      # Windows
```

## Despliegue

### Producción con Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Docker (Opcional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

## Documentación Adicional

- **README.md**: Documentación principal
- **DOCUMENTACION_TECNICA.md**: Detalles técnicos
- **INSTALACION.md**: Guía de instalación completa
- **INFORME_MODULOS_FRAMEWORKS.md**: Análisis de tecnologías
- **PRESENTACION.md**: Diapositivas del proyecto

## Contacto y Soporte

- **GitHub**: https://github.com/tu-usuario/life-organizer
- **Issues**: Reportar bugs y solicitar features
- **Documentación**: Ver archivos .md en el repositorio

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
