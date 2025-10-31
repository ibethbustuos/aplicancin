from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from app.models import db, User, HealthData, Task, Notification, HealthAlert, Medication
from datetime import datetime, date, timedelta
import json

# Blueprint para rutas principales
main_bp = Blueprint('main', __name__)

# Blueprint para API
api_bp = Blueprint('api', __name__)

# ==================== RUTAS PRINCIPALES ====================

@main_bp.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard principal"""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('main.login'))
    
    # Obtener datos de salud del día actual
    today = date.today()
    health_data = HealthData.query.filter_by(user_id=user.id, date=today).first()
    
    # Obtener tareas del día
    tasks = Task.query.filter_by(user_id=user.id, due_date=today).all()
    
    # Obtener notificaciones no leídas
    notifications = Notification.query.filter_by(user_id=user.id, read=False).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Obtener alertas de salud activas
    health_alerts = HealthAlert.query.filter_by(user_id=user.id, resolved=False).all()
    
    return render_template('dashboard.html', 
                         user=user, 
                         health_data=health_data,
                         tasks=tasks,
                         notifications=notifications,
                         health_alerts=health_alerts)

@main_bp.route('/health-tracker')
def health_tracker():
    """Página de seguimiento de salud"""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    today = date.today()
    health_data = HealthData.query.filter_by(user_id=user.id, date=today).first()
    
    return render_template('health_tracker.html', user=user, health_data=health_data)

@main_bp.route('/analytics')
def analytics():
    """Página de análisis de datos"""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.get(session['user_id'])
    return render_template('analytics.html', user=user)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age', type=int)
        weight = request.form.get('weight', type=float)
        height = request.form.get('height', type=int)
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('register.html')
        
        # Crear nuevo usuario
        user = User(
            name=name,
            email=email,
            age=age,
            weight=weight,
            height=height
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return redirect(url_for('main.dashboard'))
    
    return render_template('register.html')

@main_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.pop('user_id', None)
    return redirect(url_for('main.index'))

# ==================== API ENDPOINTS ====================

@api_bp.route('/health/water', methods=['POST'])
def add_water():
    """Agregar consumo de agua"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    amount = data.get('amount', 0)
    
    user_id = session['user_id']
    today = date.today()
    
    # Obtener o crear datos de salud del día
    health_data = HealthData.query.filter_by(user_id=user_id, date=today).first()
    if not health_data:
        health_data = HealthData(user_id=user_id, date=today)
        db.session.add(health_data)
    
    health_data.water_intake += amount
    db.session.commit()
    
    # Verificar si se alcanzó la meta
    if health_data.water_intake >= health_data.water_target:
        notification = Notification(
            user_id=user_id,
            type='achievement',
            message='🎉 ¡Meta de agua alcanzada!',
            priority='normal'
        )
        db.session.add(notification)
        db.session.commit()
    
    return jsonify({'success': True, 'water_intake': health_data.water_intake})

@api_bp.route('/health/blood-pressure', methods=['POST'])
def add_blood_pressure():
    """Registrar presión arterial"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    systolic = data.get('systolic')
    diastolic = data.get('diastolic')
    
    if not systolic or not diastolic:
        return jsonify({'error': 'Presión sistólica y diastólica requeridas'}), 400
    
    user_id = session['user_id']
    today = date.today()
    
    # Obtener o crear datos de salud del día
    health_data = HealthData.query.filter_by(user_id=user_id, date=today).first()
    if not health_data:
        health_data = HealthData(user_id=user_id, date=today)
        db.session.add(health_data)
    
    health_data.systolic_pressure = systolic
    health_data.diastolic_pressure = diastolic
    db.session.commit()
    
    # Verificar si está en rango peligroso
    if systolic > 140 or diastolic > 90:
        alert = HealthAlert(
            user_id=user_id,
            alert_type='high_blood_pressure',
            level='high',
            message='Tu presión arterial está elevada. Consulta a tu médico.',
            action_recommended='Reduce el sodio y aumenta la actividad física'
        )
        db.session.add(alert)
        
        notification = Notification(
            user_id=user_id,
            type='health_alert',
            message='⚠️ Presión arterial elevada detectada',
            priority='urgent'
        )
        db.session.add(notification)
        db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/health/weight', methods=['POST'])
def add_weight():
    """Registrar peso"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    weight = data.get('weight')
    
    if not weight:
        return jsonify({'error': 'Peso requerido'}), 400
    
    user_id = session['user_id']
    today = date.today()
    
    # Obtener o crear datos de salud del día
    health_data = HealthData.query.filter_by(user_id=user_id, date=today).first()
    if not health_data:
        health_data = HealthData(user_id=user_id, date=today)
        db.session.add(health_data)
    
    health_data.weight = weight
    db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/health/meal', methods=['POST'])
def toggle_meal():
    """Alternar estado de comida"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    data = request.get_json()
    meal_type = data.get('meal_type')  # breakfast, lunch, dinner
    
    if meal_type not in ['breakfast', 'lunch', 'dinner']:
        return jsonify({'error': 'Tipo de comida inválido'}), 400
    
    user_id = session['user_id']
    today = date.today()
    
    # Obtener o crear datos de salud del día
    health_data = HealthData.query.filter_by(user_id=user_id, date=today).first()
    if not health_data:
        health_data = HealthData(user_id=user_id, date=today)
        db.session.add(health_data)
    
    # Alternar estado de la comida
    if meal_type == 'breakfast':
        health_data.breakfast_completed = not health_data.breakfast_completed
    elif meal_type == 'lunch':
        health_data.lunch_completed = not health_data.lunch_completed
    elif meal_type == 'dinner':
        health_data.dinner_completed = not health_data.dinner_completed
    
    db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/tasks', methods=['GET', 'POST'])
def tasks():
    """Obtener o crear tareas"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    
    if request.method == 'GET':
        # Obtener tareas del usuario
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.due_date.desc()).all()
        return jsonify([task.to_dict() for task in tasks])
    
    elif request.method == 'POST':
        # Crear nueva tarea
        data = request.get_json()
        
        task = Task(
            user_id=user_id,
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category', 'personal'),
            priority=data.get('priority', 'medium'),
            due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d').date() if data.get('due_date') else None,
            due_time=data.get('due_time'),
            reminder_enabled=data.get('reminder_enabled', True)
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({'success': True, 'task': task.to_dict()})

@api_bp.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def task_detail(task_id):
    """Actualizar o eliminar tarea específica"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    if request.method == 'PUT':
        # Actualizar tarea
        data = request.get_json()
        
        if 'completed' in data:
            task.completed = data['completed']
            if data['completed']:
                task.completed_at = datetime.utcnow()
        
        if 'title' in data:
            task.title = data['title']
        
        if 'description' in data:
            task.description = data['description']
        
        db.session.commit()
        return jsonify({'success': True, 'task': task.to_dict()})
    
    elif request.method == 'DELETE':
        # Eliminar tarea
        db.session.delete(task)
        db.session.commit()
        return jsonify({'success': True})

@api_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Obtener notificaciones del usuario"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(20).all()
    
    return jsonify([notification.to_dict() for notification in notifications])

@api_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    """Marcar notificación como leída"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    
    if not notification:
        return jsonify({'error': 'Notificación no encontrada'}), 404
    
    notification.read = True
    notification.read_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/analytics/health-trends', methods=['GET'])
def health_trends():
    """Obtener tendencias de salud"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    days = request.args.get('days', 30, type=int)
    
    # Obtener datos de salud de los últimos N días
    start_date = date.today() - timedelta(days=days)
    health_data = HealthData.query.filter(
        HealthData.user_id == user_id,
        HealthData.date >= start_date
    ).order_by(HealthData.date).all()
    
    trends = {
        'water_intake': [{'date': hd.date.isoformat(), 'value': hd.water_intake} for hd in health_data if hd.water_intake],
        'weight': [{'date': hd.date.isoformat(), 'value': hd.weight} for hd in health_data if hd.weight],
        'blood_pressure': [{'date': hd.date.isoformat(), 'systolic': hd.systolic_pressure, 'diastolic': hd.diastolic_pressure} for hd in health_data if hd.systolic_pressure and hd.diastolic_pressure],
        'exercise': [{'date': hd.date.isoformat(), 'minutes': hd.exercise_minutes} for hd in health_data if hd.exercise_minutes]
    }
    
    return jsonify(trends)

@api_bp.route('/analytics/task-completion', methods=['GET'])
def task_completion_stats():
    """Obtener estadísticas de completación de tareas"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    
    # Estadísticas generales
    total_tasks = Task.query.filter_by(user_id=user_id).count()
    completed_tasks = Task.query.filter_by(user_id=user_id, completed=True).count()
    
    # Estadísticas por categoría
    categories = ['personal', 'work', 'exercise', 'food', 'health']
    category_stats = {}
    
    for category in categories:
        total = Task.query.filter_by(user_id=user_id, category=category).count()
        completed = Task.query.filter_by(user_id=user_id, category=category, completed=True).count()
        category_stats[category] = {
            'total': total,
            'completed': completed,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'category_stats': category_stats
    })

@api_bp.route('/health/summary', methods=['GET'])
def health_summary():
    """Obtener resumen de salud del día"""
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    user_id = session['user_id']
    today = date.today()
    
    health_data = HealthData.query.filter_by(user_id=user_id, date=today).first()
    
    if not health_data:
        return jsonify({
            'water_intake': 0,
            'water_target': 2000,
            'water_percentage': 0,
            'meals_completed': 0,
            'total_meals': 3,
            'exercise_minutes': 0,
            'blood_pressure': None,
            'weight': None
        })
    
    meals_completed = sum([
        health_data.breakfast_completed,
        health_data.lunch_completed,
        health_data.dinner_completed
    ])
    
    water_percentage = (health_data.water_intake / health_data.water_target * 100) if health_data.water_target > 0 else 0
    
    blood_pressure = None
    if health_data.systolic_pressure and health_data.diastolic_pressure:
        blood_pressure = {
            'systolic': health_data.systolic_pressure,
            'diastolic': health_data.diastolic_pressure
        }
    
    return jsonify({
        'water_intake': health_data.water_intake,
        'water_target': health_data.water_target,
        'water_percentage': round(water_percentage, 1),
        'meals_completed': meals_completed,
        'total_meals': 3,
        'exercise_minutes': health_data.exercise_minutes,
        'blood_pressure': blood_pressure,
        'weight': health_data.weight
    })
