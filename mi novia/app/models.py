from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """Modelo de Usuario"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Integer)
    medical_conditions = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relaciones
    health_data = db.relationship('HealthData', backref='user', lazy=True, cascade='all, delete-orphan')
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'weight': self.weight,
            'height': self.height,
            'medical_conditions': self.medical_conditions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class HealthData(db.Model):
    """Modelo de Datos de Salud"""
    __tablename__ = 'health_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    
    # Datos de hidratación
    water_intake = db.Column(db.Integer, default=0)  # ml
    water_target = db.Column(db.Integer, default=2000)  # ml
    
    # Presión arterial
    systolic_pressure = db.Column(db.Integer)
    diastolic_pressure = db.Column(db.Integer)
    
    # Peso
    weight = db.Column(db.Float)
    
    # Comidas
    breakfast_completed = db.Column(db.Boolean, default=False)
    lunch_completed = db.Column(db.Boolean, default=False)
    dinner_completed = db.Column(db.Boolean, default=False)
    snacks_count = db.Column(db.Integer, default=0)
    
    # Ejercicio
    exercise_minutes = db.Column(db.Integer, default=0)
    exercise_type = db.Column(db.String(100))
    calories_burned = db.Column(db.Integer, default=0)
    
    # Sueño
    sleep_hours = db.Column(db.Float)
    sleep_quality = db.Column(db.String(20))  # poor, fair, good, excellent
    bedtime = db.Column(db.String(10))  # HH:MM format
    wakeup_time = db.Column(db.String(10))  # HH:MM format
    
    # Medicamentos
    medications_taken = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'water_intake': self.water_intake,
            'water_target': self.water_target,
            'systolic_pressure': self.systolic_pressure,
            'diastolic_pressure': self.diastolic_pressure,
            'weight': self.weight,
            'breakfast_completed': self.breakfast_completed,
            'lunch_completed': self.lunch_completed,
            'dinner_completed': self.dinner_completed,
            'snacks_count': self.snacks_count,
            'exercise_minutes': self.exercise_minutes,
            'exercise_type': self.exercise_type,
            'calories_burned': self.calories_burned,
            'sleep_hours': self.sleep_hours,
            'sleep_quality': self.sleep_quality,
            'bedtime': self.bedtime,
            'wakeup_time': self.wakeup_time,
            'medications_taken': self.medications_taken,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Task(db.Model):
    """Modelo de Tareas"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # personal, work, exercise, food, health
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    due_time = db.Column(db.String(10))  # HH:MM format
    reminder_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'completed': self.completed,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'due_time': self.due_time,
            'reminder_enabled': self.reminder_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Notification(db.Model):
    """Modelo de Notificaciones"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # health_alert, water_reminder, task_reminder, achievement
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'message': self.message,
            'priority': self.priority,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

class HealthAlert(db.Model):
    """Modelo de Alertas de Salud"""
    __tablename__ = 'health_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # high_blood_pressure, dehydration, sedentary, etc.
    level = db.Column(db.String(20), nullable=False)  # low, medium, high
    message = db.Column(db.Text, nullable=False)
    action_recommended = db.Column(db.Text)
    resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'alert_type': self.alert_type,
            'level': self.level,
            'message': self.message,
            'action_recommended': self.action_recommended,
            'resolved': self.resolved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

class Medication(db.Model):
    """Modelo de Medicamentos"""
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))  # daily, twice_daily, etc.
    time_of_day = db.Column(db.String(20))  # morning, afternoon, evening
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'time_of_day': self.time_of_day,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
