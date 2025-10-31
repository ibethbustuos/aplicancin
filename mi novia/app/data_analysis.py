"""
Módulo de Análisis de Datos para Life Organizer
Incluye análisis estadísticos y visualizaciones de datos de salud
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, text
import os
from io import BytesIO
import base64

# Configuración de matplotlib para mejor calidad
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except OSError:
        plt.style.use('seaborn-darkgrid')
sns.set_palette("husl")

class HealthDataAnalyzer:
    """Clase para análisis de datos de salud"""
    
    def __init__(self, db_path='life_organizer.db'):
        """Inicializar con conexión a base de datos"""
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        
    def get_user_health_data(self, user_id, days=30):
        """Obtener datos de salud de un usuario"""
        query = """
        SELECT * FROM health_data 
        WHERE user_id = :user_id 
        AND date >= date('now', '-' || :days || ' days')
        ORDER BY date
        """
        
        df = pd.read_sql_query(query, self.engine, params={'user_id': user_id, 'days': days})
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
        return df
    
    def get_user_tasks(self, user_id, days=30):
        """Obtener tareas de un usuario"""
        query = """
        SELECT * FROM tasks 
        WHERE user_id = :user_id 
        AND created_at >= datetime('now', '-' || :days || ' days')
        ORDER BY created_at
        """
        
        df = pd.read_sql_query(query, self.engine, params={'user_id': user_id, 'days': days})
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['due_date'] = pd.to_datetime(df['due_date'])
        return df
    
    def analyze_water_intake_trends(self, user_id, days=30):
        """Analizar tendencias de consumo de agua"""
        df = self.get_user_health_data(user_id, days)
        
        if df.empty:
            return None
        
        # Filtrar datos con consumo de agua
        water_data = df[df['water_intake'] > 0].copy()
        
        if water_data.empty:
            return None
        
        # Calcular estadísticas
        stats = {
            'average_daily': water_data['water_intake'].mean(),
            'median_daily': water_data['water_intake'].median(),
            'max_daily': water_data['water_intake'].max(),
            'min_daily': water_data['water_intake'].min(),
            'std_daily': water_data['water_intake'].std(),
            'target_achievement_rate': (water_data['water_intake'] >= water_data['water_target']).mean() * 100
        }
        
        return {
            'data': water_data[['date', 'water_intake', 'water_target']].to_dict('records'),
            'stats': stats
        }
    
    def analyze_blood_pressure_trends(self, user_id, days=30):
        """Analizar tendencias de presión arterial"""
        df = self.get_user_health_data(user_id, days)
        
        if df.empty:
            return None
        
        # Filtrar datos con presión arterial
        bp_data = df[(df['systolic_pressure'].notna()) & (df['diastolic_pressure'].notna())].copy()
        
        if bp_data.empty:
            return None
        
        # Calcular estadísticas
        stats = {
            'avg_systolic': bp_data['systolic_pressure'].mean(),
            'avg_diastolic': bp_data['diastolic_pressure'].mean(),
            'max_systolic': bp_data['systolic_pressure'].max(),
            'max_diastolic': bp_data['diastolic_pressure'].max(),
            'min_systolic': bp_data['systolic_pressure'].min(),
            'min_diastolic': bp_data['diastolic_pressure'].min(),
            'high_bp_readings': ((bp_data['systolic_pressure'] > 140) | (bp_data['diastolic_pressure'] > 90)).sum(),
            'total_readings': len(bp_data)
        }
        
        return {
            'data': bp_data[['date', 'systolic_pressure', 'diastolic_pressure']].to_dict('records'),
            'stats': stats
        }
    
    def analyze_weight_trends(self, user_id, days=30):
        """Analizar tendencias de peso"""
        df = self.get_user_health_data(user_id, days)
        
        if df.empty:
            return None
        
        # Filtrar datos con peso
        weight_data = df[df['weight'].notna()].copy()
        
        if weight_data.empty:
            return None
        
        # Calcular estadísticas
        weight_change = weight_data['weight'].iloc[-1] - weight_data['weight'].iloc[0] if len(weight_data) > 1 else 0
        
        stats = {
            'current_weight': weight_data['weight'].iloc[-1],
            'starting_weight': weight_data['weight'].iloc[0],
            'weight_change': weight_change,
            'avg_weight': weight_data['weight'].mean(),
            'max_weight': weight_data['weight'].max(),
            'min_weight': weight_data['weight'].min(),
            'weight_variance': weight_data['weight'].var()
        }
        
        return {
            'data': weight_data[['date', 'weight']].to_dict('records'),
            'stats': stats
        }
    
    def analyze_task_completion_patterns(self, user_id, days=30):
        """Analizar patrones de completación de tareas"""
        df = self.get_user_tasks(user_id, days)
        
        if df.empty:
            return None
        
        # Estadísticas generales
        total_tasks = len(df)
        completed_tasks = df['completed'].sum()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Análisis por categoría
        category_stats = df.groupby('category').agg({
            'completed': ['count', 'sum'],
            'id': 'count'
        }).round(2)
        
        category_stats.columns = ['total', 'completed', 'total_count']
        category_stats['completion_rate'] = (category_stats['completed'] / category_stats['total'] * 100).round(1)
        
        # Análisis por prioridad
        priority_stats = df.groupby('priority').agg({
            'completed': ['count', 'sum'],
            'id': 'count'
        }).round(2)
        
        priority_stats.columns = ['total', 'completed', 'total_count']
        priority_stats['completion_rate'] = (priority_stats['completed'] / priority_stats['total'] * 100).round(1)
        
        return {
            'overall': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': completion_rate
            },
            'by_category': category_stats.to_dict('index'),
            'by_priority': priority_stats.to_dict('index')
        }
    
    def create_water_intake_chart(self, user_id, days=30):
        """Crear gráfico de consumo de agua"""
        df = self.get_user_health_data(user_id, days)
        
        if df.empty or df['water_intake'].sum() == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Filtrar datos con consumo de agua
        water_data = df[df['water_intake'] > 0].copy()
        
        if water_data.empty:
            return None
        
        # Crear gráfico de barras
        ax.bar(water_data['date'], water_data['water_intake'], 
               alpha=0.7, color='skyblue', label='Consumo diario')
        
        # Línea de meta
        if 'water_target' in water_data.columns:
            ax.axhline(y=water_data['water_target'].iloc[0], 
                      color='red', linestyle='--', alpha=0.8, label='Meta diaria')
        
        ax.set_title('Consumo de Agua Diario', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Consumo (ml)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotar etiquetas de fecha
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def create_blood_pressure_chart(self, user_id, days=30):
        """Crear gráfico de presión arterial"""
        df = self.get_user_health_data(user_id, days)
        
        if df.empty:
            return None
        
        # Filtrar datos con presión arterial
        bp_data = df[(df['systolic_pressure'].notna()) & (df['diastolic_pressure'].notna())].copy()
        
        if bp_data.empty:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Gráfico de líneas para presión sistólica y diastólica
        ax.plot(bp_data['date'], bp_data['systolic_pressure'], 
                marker='o', linewidth=2, label='Sistólica', color='red')
        ax.plot(bp_data['date'], bp_data['diastolic_pressure'], 
                marker='s', linewidth=2, label='Diastólica', color='blue')
        
        # Líneas de referencia para presión normal
        ax.axhline(y=120, color='green', linestyle='--', alpha=0.7, label='Normal Sistólica')
        ax.axhline(y=80, color='orange', linestyle='--', alpha=0.7, label='Normal Diastólica')
        
        ax.set_title('Presión Arterial', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Presión (mmHg)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def create_weight_trend_chart(self, user_id, days=30):
        """Crear gráfico de tendencia de peso"""
        df = self.get_user_health_data(user_id, days)
        
        if df.empty:
            return None
        
        # Filtrar datos con peso
        weight_data = df[df['weight'].notna()].copy()
        
        if weight_data.empty:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Gráfico de línea para peso
        ax.plot(weight_data['date'], weight_data['weight'], 
                marker='o', linewidth=2, markersize=6, color='purple')
        
        # Línea de tendencia
        if len(weight_data) > 1:
            z = np.polyfit(range(len(weight_data)), weight_data['weight'], 1)
            p = np.poly1d(z)
            ax.plot(weight_data['date'], p(range(len(weight_data))), 
                    "r--", alpha=0.8, label='Tendencia')
        
        ax.set_title('Tendencia de Peso', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Peso (kg)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def create_task_completion_chart(self, user_id, days=30):
        """Crear gráfico de completación de tareas"""
        df = self.get_user_tasks(user_id, days)
        
        if df.empty:
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de completación por categoría
        category_completion = df.groupby('category')['completed'].agg(['count', 'sum']).reset_index()
        category_completion['completion_rate'] = (category_completion['sum'] / category_completion['count'] * 100)
        
        bars1 = ax1.bar(category_completion['category'], category_completion['completion_rate'], 
                       color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        ax1.set_title('Tasa de Completación por Categoría', fontweight='bold')
        ax1.set_ylabel('Porcentaje de Completación')
        ax1.set_ylim(0, 100)
        
        # Agregar valores en las barras
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # Gráfico de completación por prioridad
        priority_completion = df.groupby('priority')['completed'].agg(['count', 'sum']).reset_index()
        priority_completion['completion_rate'] = (priority_completion['sum'] / priority_completion['count'] * 100)
        
        bars2 = ax2.bar(priority_completion['priority'], priority_completion['completion_rate'],
                       color=['#FF9999', '#66B2FF', '#99FF99'])
        ax2.set_title('Tasa de Completación por Prioridad', fontweight='bold')
        ax2.set_ylabel('Porcentaje de Completación')
        ax2.set_ylim(0, 100)
        
        # Agregar valores en las barras
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def create_health_summary_dashboard(self, user_id, days=30):
        """Crear dashboard completo de salud"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Consumo de agua
        water_data = self.get_user_health_data(user_id, days)
        if not water_data.empty and water_data['water_intake'].sum() > 0:
            water_daily = water_data[water_data['water_intake'] > 0]
            ax1.bar(water_daily['date'], water_daily['water_intake'], alpha=0.7, color='skyblue')
            if 'water_target' in water_daily.columns:
                ax1.axhline(y=water_daily['water_target'].iloc[0], color='red', linestyle='--', alpha=0.8)
            ax1.set_title('Consumo de Agua Diario', fontweight='bold')
            ax1.set_ylabel('ml')
            ax1.tick_params(axis='x', rotation=45)
        
        # 2. Presión arterial
        bp_data = water_data[(water_data['systolic_pressure'].notna()) & (water_data['diastolic_pressure'].notna())]
        if not bp_data.empty:
            ax2.plot(bp_data['date'], bp_data['systolic_pressure'], marker='o', label='Sistólica', color='red')
            ax2.plot(bp_data['date'], bp_data['diastolic_pressure'], marker='s', label='Diastólica', color='blue')
            ax2.axhline(y=120, color='green', linestyle='--', alpha=0.7)
            ax2.axhline(y=80, color='orange', linestyle='--', alpha=0.7)
            ax2.set_title('Presión Arterial', fontweight='bold')
            ax2.set_ylabel('mmHg')
            ax2.legend()
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Peso
        weight_data = water_data[water_data['weight'].notna()]
        if not weight_data.empty:
            ax3.plot(weight_data['date'], weight_data['weight'], marker='o', linewidth=2, color='purple')
            ax3.set_title('Tendencia de Peso', fontweight='bold')
            ax3.set_ylabel('kg')
            ax3.tick_params(axis='x', rotation=45)
        
        # 4. Completación de tareas
        task_data = self.get_user_tasks(user_id, days)
        if not task_data.empty:
            daily_completion = task_data.groupby(task_data['created_at'].dt.date)['completed'].mean() * 100
            ax4.plot(daily_completion.index, daily_completion.values, marker='o', linewidth=2, color='green')
            ax4.set_title('Completación Diaria de Tareas', fontweight='bold')
            ax4.set_ylabel('Porcentaje')
            ax4.tick_params(axis='x', rotation=45)
        
        plt.suptitle(f'Dashboard de Salud - Últimos {days} días', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return self._fig_to_base64(fig)
    
    def generate_health_report(self, user_id, days=30):
        """Generar reporte completo de salud"""
        report = {
            'user_id': user_id,
            'period_days': days,
            'generated_at': datetime.now().isoformat(),
            'water_analysis': self.analyze_water_intake_trends(user_id, days),
            'blood_pressure_analysis': self.analyze_blood_pressure_trends(user_id, days),
            'weight_analysis': self.analyze_weight_trends(user_id, days),
            'task_analysis': self.analyze_task_completion_patterns(user_id, days),
            'charts': {
                'water_intake': self.create_water_intake_chart(user_id, days),
                'blood_pressure': self.create_blood_pressure_chart(user_id, days),
                'weight_trend': self.create_weight_trend_chart(user_id, days),
                'task_completion': self.create_task_completion_chart(user_id, days),
                'dashboard': self.create_health_summary_dashboard(user_id, days)
            }
        }
        
        return report
    
    def _fig_to_base64(self, fig):
        """Convertir figura de matplotlib a base64 para mostrar en web"""
        if fig is None:
            return None
        
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{image_base64}"

# Función de utilidad para crear datos de muestra
def create_sample_data():
    """Crear datos de muestra para testing"""
    import random
    from datetime import datetime, timedelta
    
    # Datos de muestra para análisis
    sample_data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        sample_data.append({
            'date': date.date(),
            'water_intake': random.randint(800, 3000),
            'water_target': 2000,
            'systolic_pressure': random.randint(110, 150),
            'diastolic_pressure': random.randint(70, 95),
            'weight': 70 + random.uniform(-2, 2),
            'exercise_minutes': random.randint(0, 90),
            'breakfast_completed': random.choice([True, False]),
            'lunch_completed': random.choice([True, False]),
            'dinner_completed': random.choice([True, False])
        })
    
    return pd.DataFrame(sample_data)

if __name__ == "__main__":
    # Ejemplo de uso
    analyzer = HealthDataAnalyzer()
    
    # Crear datos de muestra
    sample_df = create_sample_data()
    print("Datos de muestra creados:")
    print(sample_df.head())
    
    # Análisis de ejemplo
    print("\nAnálisis de consumo de agua:")
    water_stats = analyzer.analyze_water_intake_trends(1, 30)
    if water_stats:
        print(f"Promedio diario: {water_stats['stats']['average_daily']:.1f} ml")
        print(f"Tasa de logro de meta: {water_stats['stats']['target_achievement_rate']:.1f}%")
