# Life Organizer - Guía de Instalación y Configuración

## Requisitos del Sistema

### Software Requerido
- **Python 3.9+**: Lenguaje de programación principal
- **pip**: Gestor de paquetes de Python
- **Git**: Control de versiones (opcional)

### Sistema Operativo
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, CentOS 8+)

## Instalación Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/life-organizer.git
cd life-organizer
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///life_organizer.db
```

### 5. Inicializar Base de Datos
```bash
python run.py
```
La base de datos se creará automáticamente en el primer inicio.

### 6. Ejecutar la Aplicación
```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Estructura del Proyecto

```
life-organizer/
├── app/                    # Aplicación principal
│   ├── __init__.py        # Configuración de Flask
│   ├── models.py          # Modelos de base de datos
│   ├── routes.py          # Rutas y endpoints
│   └── data_analysis.py  # Análisis de datos
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── dashboard.html    # Dashboard principal
│   ├── analytics.html    # Página de análisis
│   ├── health_tracker.html # Seguimiento de salud
│   ├── login.html        # Página de login
│   └── register.html     # Página de registro
├── static/               # Archivos estáticos
│   ├── css/             # Estilos CSS
│   ├── js/              # JavaScript
│   └── images/          # Imágenes
├── data/                # Datos de muestra
├── requirements.txt      # Dependencias Python
├── run.py               # Archivo principal
├── README.md            # Documentación principal
└── DOCUMENTACION_TECNICA.md # Documentación técnica
```

## Configuración de Base de Datos

### SQLite (Por Defecto)
La aplicación usa SQLite por defecto, que se crea automáticamente como `life_organizer.db`.

### PostgreSQL (Producción)
Para usar PostgreSQL en producción:

1. Instalar PostgreSQL
2. Crear base de datos:
```sql
CREATE DATABASE life_organizer;
CREATE USER life_organizer_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE life_organizer TO life_organizer_user;
```

3. Actualizar `.env`:
```env
DATABASE_URL=postgresql://life_organizer_user:tu_password@localhost/life_organizer
```

4. Instalar dependencia adicional:
```bash
pip install psycopg2-binary
```

## Configuración de Desarrollo

### Modo Debug
```bash
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
```

### Recarga Automática
La aplicación se recarga automáticamente cuando se modifican los archivos.

### Logs de Desarrollo
Los logs se muestran en la consola con información detallada.

## Configuración de Producción

### Variables de Entorno
```env
FLASK_ENV=production
SECRET_KEY=clave-super-secreta-para-produccion
DATABASE_URL=postgresql://usuario:password@host:puerto/database
```

### Servidor WSGI
Para producción, usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Proxy Reverso con Nginx
Configuración de ejemplo para Nginx:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /ruta/a/tu/proyecto/static;
    }
}
```

## Solución de Problemas

### Error: "Module not found"
```bash
# Verificar que el entorno virtual esté activado
which python  # Linux/macOS
where python  # Windows

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "Database is locked"
```bash
# Cerrar todas las conexiones a la base de datos
# Reiniciar la aplicación
```

### Error: "Port already in use"
```bash
# Cambiar puerto en run.py
app.run(port=5001)
```

### Error: "Permission denied"
```bash
# Linux/macOS: Dar permisos de ejecución
chmod +x run.py

# Windows: Ejecutar como administrador
```

## Datos de Prueba

### Usuario de Prueba
- **Email**: test@example.com
- **Contraseña**: test123
- **Datos**: Incluye datos de muestra para testing

### Generar Datos de Prueba
```python
# Ejecutar en consola Python
from app.data_analysis import create_sample_data
import pandas as pd

# Crear datos de muestra
sample_data = create_sample_data()
print("Datos de muestra creados:", len(sample_data), "registros")
```

## Monitoreo y Logs

### Logs de Aplicación
Los logs se escriben en la consola por defecto. Para archivos de log:

```python
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

### Métricas de Rendimiento
- Tiempo de respuesta de APIs
- Uso de memoria
- Consultas de base de datos

## Backup y Restauración

### Backup de Base de Datos SQLite
```bash
cp life_organizer.db life_organizer_backup.db
```

### Backup de Base de Datos PostgreSQL
```bash
pg_dump life_organizer > backup.sql
```

### Restauración
```bash
# SQLite
cp life_organizer_backup.db life_organizer.db

# PostgreSQL
psql life_organizer < backup.sql
```

## Actualizaciones

### Actualizar Dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Migraciones de Base de Datos
```python
# Las migraciones se manejan automáticamente con SQLAlchemy
# Para cambios manuales, usar Flask-Migrate
pip install Flask-Migrate
flask db init
flask db migrate -m "Descripción del cambio"
flask db upgrade
```

## Soporte y Contribución

### Reportar Bugs
1. Crear issue en GitHub
2. Incluir logs de error
3. Describir pasos para reproducir

### Contribuir
1. Fork del repositorio
2. Crear rama para feature
3. Hacer commit de cambios
4. Crear Pull Request

### Contacto
- **Email**: soporte@lifeorganizer.com
- **GitHub**: https://github.com/tu-usuario/life-organizer
- **Documentación**: https://lifeorganizer.readthedocs.io
