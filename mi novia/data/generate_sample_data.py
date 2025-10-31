import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generar datos de muestra para testing y demostración"""
    
    # Configuración de datos
    num_users = 10
    num_days = 30
    base_date = datetime.now() - timedelta(days=num_days)
    
    # Datos de usuarios
    users_data = []
    for i in range(num_users):
        users_data.append({
            'id': i + 1,
            'name': f'Usuario {i + 1}',
            'email': f'user{i + 1}@example.com',
            'age': random.randint(25, 65),
            'weight': random.uniform(60, 100),
            'height': random.randint(150, 190),
            'created_at': base_date - timedelta(days=random.randint(1, 10))
        })
    
    # Datos de salud diarios
    health_data = []
    for user_id in range(1, num_users + 1):
        for day in range(num_days):
            date = base_date + timedelta(days=day)
            
            # Consumo de agua (tendencia hacia la meta)
            water_target = 2000
            water_intake = random.randint(800, 3000)
            if random.random() < 0.3:  # 30% de probabilidad de alcanzar la meta
                water_intake = random.randint(water_target, 3000)
            
            # Presión arterial (mayoría normal, algunas elevadas)
            systolic = random.randint(110, 150)
            diastolic = random.randint(70, 95)
            if random.random() < 0.1:  # 10% de probabilidad de presión alta
                systolic = random.randint(140, 160)
                diastolic = random.randint(90, 105)
            
            # Peso (ligera variación diaria)
            base_weight = users_data[user_id - 1]['weight']
            weight_variation = random.uniform(-0.5, 0.5)
            weight = max(50, base_weight + weight_variation)
            
            # Ejercicio (algunos días sin ejercicio)
            exercise_minutes = 0
            if random.random() < 0.7:  # 70% de probabilidad de hacer ejercicio
                exercise_minutes = random.randint(15, 90)
            
            # Comidas (mayoría completadas)
            breakfast = random.random() < 0.8
            lunch = random.random() < 0.9
            dinner = random.random() < 0.85
            
            health_data.append({
                'user_id': user_id,
                'date': date.date(),
                'water_intake': water_intake,
                'water_target': water_target,
                'systolic_pressure': systolic if random.random() < 0.3 else None,  # Solo 30% registra presión
                'diastolic_pressure': diastolic if random.random() < 0.3 else None,
                'weight': weight if random.random() < 0.2 else None,  # Solo 20% registra peso diario
                'breakfast_completed': breakfast,
                'lunch_completed': lunch,
                'dinner_completed': dinner,
                'exercise_minutes': exercise_minutes,
                'exercise_type': random.choice(['cardio', 'strength', 'yoga', 'walking']) if exercise_minutes > 0 else None,
                'sleep_hours': random.uniform(6, 9),
                'sleep_quality': random.choice(['poor', 'fair', 'good', 'excellent'])
            })
    
    # Datos de tareas
    tasks_data = []
    categories = ['personal', 'work', 'exercise', 'food', 'health']
    priorities = ['low', 'medium', 'high']
    
    for user_id in range(1, num_users + 1):
        num_tasks = random.randint(20, 50)
        for task_id in range(num_tasks):
            created_date = base_date + timedelta(days=random.randint(0, num_days - 1))
            due_date = created_date + timedelta(days=random.randint(0, 7))
            
            tasks_data.append({
                'id': len(tasks_data) + 1,
                'user_id': user_id,
                'title': f'Tarea {task_id + 1} del Usuario {user_id}',
                'description': f'Descripción de la tarea {task_id + 1}',
                'category': random.choice(categories),
                'priority': random.choice(priorities),
                'completed': random.random() < 0.7,  # 70% de tareas completadas
                'due_date': due_date.date(),
                'due_time': f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}",
                'reminder_enabled': random.random() < 0.8,
                'created_at': created_date,
                'completed_at': created_date + timedelta(hours=random.randint(1, 24)) if random.random() < 0.7 else None
            })
    
    # Datos de notificaciones
    notifications_data = []
    notification_types = ['water_reminder', 'health_alert', 'task_reminder', 'achievement']
    priorities = ['low', 'normal', 'high', 'urgent']
    
    for user_id in range(1, num_users + 1):
        num_notifications = random.randint(10, 30)
        for notif_id in range(num_notifications):
            created_date = base_date + timedelta(days=random.randint(0, num_days - 1))
            
            notifications_data.append({
                'id': len(notifications_data) + 1,
                'user_id': user_id,
                'type': random.choice(notification_types),
                'message': f'Notificación {notif_id + 1} para Usuario {user_id}',
                'priority': random.choice(priorities),
                'read': random.random() < 0.6,  # 60% de notificaciones leídas
                'created_at': created_date,
                'read_at': created_date + timedelta(hours=random.randint(1, 12)) if random.random() < 0.6 else None
            })
    
    # Crear DataFrames
    users_df = pd.DataFrame(users_data)
    health_df = pd.DataFrame(health_data)
    tasks_df = pd.DataFrame(tasks_data)
    notifications_df = pd.DataFrame(notifications_data)
    
    return {
        'users': users_df,
        'health_data': health_df,
        'tasks': tasks_df,
        'notifications': notifications_df
    }

def save_sample_data_to_csv():
    """Guardar datos de muestra en archivos CSV"""
    data = generate_sample_data()
    
    # Guardar cada DataFrame en un archivo CSV
    data['users'].to_csv('data/sample_users.csv', index=False)
    data['health_data'].to_csv('data/sample_health_data.csv', index=False)
    data['tasks'].to_csv('data/sample_tasks.csv', index=False)
    data['notifications'].to_csv('data/sample_notifications.csv', index=False)
    
    print("Datos de muestra guardados en archivos CSV:")
    print(f"- Usuarios: {len(data['users'])} registros")
    print(f"- Datos de salud: {len(data['health_data'])} registros")
    print(f"- Tareas: {len(data['tasks'])} registros")
    print(f"- Notificaciones: {len(data['notifications'])} registros")

def generate_analytics_summary():
    """Generar resumen de análisis de los datos de muestra"""
    data = generate_sample_data()
    
    print("\n=== RESUMEN DE ANÁLISIS DE DATOS DE MUESTRA ===")
    
    # Análisis de usuarios
    print(f"\n👥 USUARIOS ({len(data['users'])} registros):")
    print(f"- Edad promedio: {data['users']['age'].mean():.1f} años")
    print(f"- Peso promedio: {data['users']['weight'].mean():.1f} kg")
    print(f"- Altura promedio: {data['users']['height'].mean():.1f} cm")
    
    # Análisis de salud
    health_df = data['health_data']
    print(f"\n🏥 DATOS DE SALUD ({len(health_df)} registros):")
    print(f"- Consumo promedio de agua: {health_df['water_intake'].mean():.0f} ml")
    print(f"- Meta de agua alcanzada: {(health_df['water_intake'] >= health_df['water_target']).mean() * 100:.1f}% de los días")
    
    # Presión arterial
    bp_data = health_df.dropna(subset=['systolic_pressure', 'diastolic_pressure'])
    if len(bp_data) > 0:
        print(f"- Presión sistólica promedio: {bp_data['systolic_pressure'].mean():.1f} mmHg")
        print(f"- Presión diastólica promedio: {bp_data['diastolic_pressure'].mean():.1f} mmHg")
        high_bp = ((bp_data['systolic_pressure'] > 140) | (bp_data['diastolic_pressure'] > 90)).sum()
        print(f"- Lecturas de presión alta: {high_bp} ({high_bp/len(bp_data)*100:.1f}%)")
    
    # Ejercicio
    exercise_data = health_df[health_df['exercise_minutes'] > 0]
    if len(exercise_data) > 0:
        print(f"- Días con ejercicio: {len(exercise_data)} ({len(exercise_data)/len(health_df)*100:.1f}%)")
        print(f"- Minutos promedio de ejercicio: {exercise_data['exercise_minutes'].mean():.1f}")
    
    # Comidas
    meals_completed = health_df[['breakfast_completed', 'lunch_completed', 'dinner_completed']].sum().sum()
    total_meals = len(health_df) * 3
    print(f"- Comidas completadas: {meals_completed}/{total_meals} ({meals_completed/total_meals*100:.1f}%)")
    
    # Análisis de tareas
    tasks_df = data['tasks']
    print(f"\n📋 TAREAS ({len(tasks_df)} registros):")
    print(f"- Tareas completadas: {tasks_df['completed'].sum()} ({tasks_df['completed'].mean()*100:.1f}%)")
    print(f"- Por categoría:")
    for category in tasks_df['category'].unique():
        cat_tasks = tasks_df[tasks_df['category'] == category]
        completion_rate = cat_tasks['completed'].mean() * 100
        print(f"  * {category}: {completion_rate:.1f}% completadas")
    
    # Análisis de notificaciones
    notifications_df = data['notifications']
    print(f"\n🔔 NOTIFICACIONES ({len(notifications_df)} registros):")
    print(f"- Notificaciones leídas: {notifications_df['read'].sum()} ({notifications_df['read'].mean()*100:.1f}%)")
    print(f"- Por tipo:")
    for notif_type in notifications_df['type'].unique():
        type_count = (notifications_df['type'] == notif_type).sum()
        print(f"  * {notif_type}: {type_count} notificaciones")

if __name__ == "__main__":
    # Generar y guardar datos de muestra
    save_sample_data_to_csv()
    
    # Generar resumen de análisis
    generate_analytics_summary()
    
    print("\n✅ Datos de muestra generados exitosamente!")
    print("📁 Archivos guardados en el directorio 'data/'")
    print("🚀 Listo para usar en la aplicación Life Organizer")
