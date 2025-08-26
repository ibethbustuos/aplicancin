import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  Bell, 
  CheckCircle2, 
  Plus, 
  Settings, 
  BarChart3, 
  BookOpen, 
  User,
  Clock,
  Target,
  TrendingUp,
  Heart,
  Dumbbell,
  Coffee,
  Briefcase,
  Star,
  Droplets,
  Activity,
  AlertTriangle,
  Shield,
  Apple,
  Scale,
  TrendingDown,
  TrendingUp as TrendingUpIcon
} from 'lucide-react';

const LifeOrganizerApp = () => {
  const [currentScreen, setCurrentScreen] = useState('welcome');
  const [user, setUser] = useState(null);
  const [surveys, setSurveys] = useState({});
  const [tasks, setTasks] = useState([]);
  const [healthData, setHealthData] = useState({
    waterIntake: { daily: 0, target: 2000, lastReminder: null },
    bloodPressure: { systolic: 0, diastolic: 0, lastCheck: null, history: [] },
    weight: { current: 0, target: 0, history: [] },
    meals: { breakfast: false, lunch: false, dinner: false, snacks: 0 },
    sleep: { hours: 0, quality: 'good', bedtime: '22:00', wakeup: '07:00' },
    exercise: { minutes: 0, type: '', calories: 0 },
    medications: [],
    riskAlerts: []
  });
  const [notifications, setNotifications] = useState([]);
  const [statistics, setStatistics] = useState({
    completedTasks: 0,
    totalTasks: 0,
    streak: 3,
    healthScore: 85
  });

  // Función para calcular riesgos de salud
  const calculateHealthRisks = () => {
    const risks = [];
    const bp = healthData.bloodPressure;
    
    // Riesgo por presión arterial
    if (bp.systolic > 140 || bp.diastolic > 90) {
      risks.push({
        type: 'high_blood_pressure',
        level: 'high',
        message: 'Tu presión arterial está elevada. Consulta a tu médico.',
        action: 'Reduce el sodio y aumenta la actividad física'
      });
    }
    
    // Riesgo por deshidratación
    if (healthData.waterIntake.daily < healthData.waterIntake.target * 0.6) {
      risks.push({
        type: 'dehydration',
        level: 'medium',
        message: 'Estás bebiendo poca agua hoy.',
        action: 'Bebe al menos 2 vasos de agua ahora'
      });
    }
    
    // Riesgo por falta de ejercicio
    if (healthData.exercise.minutes < 30) {
      risks.push({
        type: 'sedentary',
        level: 'low',
        message: 'No has hecho ejercicio hoy.',
        action: 'Camina al menos 30 minutos'
      });
    }

    setHealthData(prev => ({ ...prev, riskAlerts: risks }));
    return risks;
  };

  // Función para crear notificaciones automáticas
  const createNotification = (type, message, priority = 'normal') => {
    const newNotification = {
      id: Date.now(),
      type,
      message,
      priority,
      timestamp: new Date().toLocaleTimeString(),
      read: false
    };
    setNotifications(prev => [newNotification, ...prev.slice(0, 9)]);
  };

  // Verificar estado de salud cada minuto (simulado)
  useEffect(() => {
    if (user) {
      const interval = setInterval(() => {
        const risks = calculateHealthRisks();
        risks.forEach(risk => {
          if (risk.level === 'high') {
            createNotification('health_alert', risk.message, 'urgent');
          }
        });
        
        // Recordatorio de agua cada 2 horas
        const now = new Date();
        const lastWaterReminder = healthData.waterIntake.lastReminder;
        if (!lastWaterReminder || (now - new Date(lastWaterReminder)) > 2 * 60 * 60 * 1000) {
          createNotification('water_reminder', '💧 Es hora de beber agua', 'normal');
          setHealthData(prev => ({
            ...prev,
            waterIntake: { ...prev.waterIntake, lastReminder: now.toISOString() }
          }));
        }
      }, 60000);
      
      return () => clearInterval(interval);
    }
  }, [user, healthData]);

  // Componente de Bienvenida
  const WelcomeScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-6">
      <div className="bg-white rounded-3xl p-8 max-w-sm w-full text-center shadow-2xl">
        <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <Heart className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-gray-800 mb-4">Life Organizer</h1>
        <p className="text-gray-600 mb-8">Tu compañero digital para una vida más saludable y organizada</p>
        <button
          onClick={() => setCurrentScreen('register')}
          className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-semibold mb-4 hover:opacity-90 transition-opacity"
        >
          Comenzar
        </button>
        <button
          onClick={() => setCurrentScreen('login')}
          className="w-full text-gray-600 py-2 rounded-xl hover:bg-gray-100 transition-colors"
        >
          Ya tengo cuenta
        </button>
      </div>
    </div>
  );

  // Pantalla de Login
  const LoginScreen = () => {
    const [formData, setFormData] = useState({
      email: '',
      password: ''
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      setUser({ 
        name: 'Usuario', 
        email: formData.email,
        age: 30,
        weight: 70,
        height: 170,
        medicalConditions: []
      });
      setCurrentScreen('healthSurvey');
    };

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-6">
        <div className="bg-white rounded-3xl p-8 max-w-sm w-full shadow-2xl">
          <div className="text-center mb-8">
            <User className="w-16 h-16 text-blue-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-800">Iniciar Sesión</h2>
            <p className="text-gray-600">Bienvenido de vuelta</p>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <input
              type="password"
              placeholder="Contraseña"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 rounded-xl font-semibold hover:opacity-90 transition-opacity"
            >
              Iniciar Sesión
            </button>
          </form>
          
          <button
            onClick={() => setCurrentScreen('welcome')}
            className="w-full mt-4 text-gray-600 py-2 rounded-xl hover:bg-gray-100 transition-colors"
          >
            Volver
          </button>
        </div>
      </div>
    );
  };

  // Encuesta de Salud Inicial
  const HealthSurveyScreen = () => {
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState({});

    const healthQuestions = [
      {
        id: 'age',
        question: '¿Cuál es tu edad?',
        type: 'number',
        placeholder: 'Ej: 25'
      },
      {
        id: 'weight',
        question: '¿Cuál es tu peso actual? (kg)',
        type: 'number',
        placeholder: 'Ej: 70'
      },
      {
        id: 'height',
        question: '¿Cuál es tu altura? (cm)',
        type: 'number',
        placeholder: 'Ej: 170'
      },
      {
        id: 'waterTarget',
        question: '¿Cuánta agua quieres beber al día? (ml)',
        type: 'select',
        options: ['1500', '2000', '2500', '3000']
      },
      {
        id: 'exerciseGoal',
        question: '¿Cuántos minutos de ejercicio quieres hacer al día?',
        type: 'select',
        options: ['30', '45', '60', '90']
      },
      {
        id: 'medicalConditions',
        question: '¿Tienes alguna condición médica?',
        type: 'multiselect',
        options: ['Diabetes', 'Hipertensión', 'Colesterol alto', 'Ninguna']
      },
      {
        id: 'medications',
        question: '¿Tomas algún medicamento regularmente?',
        type: 'text',
        placeholder: 'Ej: Aspirina 100mg, Metformina'
      }
    ];

    const handleAnswer = (answer) => {
      const newAnswers = {...answers, [healthQuestions[currentQuestion].id]: answer};
      setAnswers(newAnswers);
      
      if (currentQuestion < healthQuestions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
      } else {
        // Procesar respuestas e inicializar datos de salud
        setHealthData(prev => ({
          ...prev,
          waterIntake: { ...prev.waterIntake, target: parseInt(newAnswers.waterTarget) || 2000 },
          weight: { ...prev.weight, current: parseFloat(newAnswers.weight) || 0 },
        }));
        
        setUser(prevUser => ({
          ...prevUser,
          age: parseInt(newAnswers.age) || 0,
          weight: parseFloat(newAnswers.weight) || 0,
          height: parseInt(newAnswers.height) || 0,
          medicalConditions: newAnswers.medicalConditions || []
        }));
        
        setSurveys(newAnswers);
        setCurrentScreen('dashboard');
      }
    };

    const currentQ = healthQuestions[currentQuestion];

    return (
      <div className="min-h-screen bg-gradient-to-br from-green-500 to-blue-600 flex items-center justify-center p-6">
        <div className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <span className="text-sm text-gray-500">Pregunta {currentQuestion + 1} de {healthQuestions.length}</span>
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <Heart className="w-6 h-6 text-green-500" />
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
              <div 
                className="bg-gradient-to-r from-green-500 to-blue-600 h-2 rounded-full transition-all duration-300"
                style={{width: `${((currentQuestion + 1) / healthQuestions.length) * 100}%`}}
              ></div>
            </div>
            <h2 className="text-xl font-bold text-gray-800 mb-6">
              {currentQ.question}
            </h2>
          </div>
          
          {currentQ.type === 'number' || currentQ.type === 'text' ? (
            <div>
              <input
                type={currentQ.type}
                placeholder={currentQ.placeholder}
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent mb-4"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && e.target.value) {
                    handleAnswer(e.target.value);
                  }
                }}
              />
              <button
                onClick={(e) => {
                  const input = e.target.previousElementSibling;
                  if (input.value) handleAnswer(input.value);
                }}
                className="w-full bg-gradient-to-r from-green-500 to-blue-600 text-white py-3 rounded-xl font-semibold"
              >
                Continuar
              </button>
            </div>
          ) : currentQ.type === 'select' ? (
            <div className="space-y-3">
              {currentQ.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswer(option)}
                  className="w-full p-4 text-left border border-gray-200 rounded-xl hover:bg-green-50 hover:border-green-300 transition-all duration-200"
                >
                  {option} {currentQ.id === 'waterTarget' ? 'ml' : currentQ.id === 'exerciseGoal' ? 'minutos' : ''}
                </button>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    );
  };

  // Dashboard Principal con Salud
  const DashboardScreen = () => {
    const todayTasks = tasks.filter(task => 
      new Date(task.date).toDateString() === new Date().toDateString()
    );

    const waterPercentage = (healthData.waterIntake.daily / healthData.waterIntake.target) * 100;
    const hasHighRisk = healthData.riskAlerts.some(risk => risk.level === 'high');

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header con alertas de salud */}
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-b-3xl">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-2xl font-bold">¡Hola {user?.name}!</h1>
              <p className="opacity-90">Cuidemos tu salud hoy</p>
            </div>
            <div className="relative">
              <button className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                {hasHighRisk ? <AlertTriangle className="w-6 h-6 text-red-300" /> : <Shield className="w-6 h-6" />}
              </button>
              {notifications.filter(n => !n.read).length > 0 && (
                <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-xs">
                  {notifications.filter(n => !n.read).length}
                </div>
              )}
            </div>
          </div>
          
          {/* Stats Cards de Salud */}
          <div className="grid grid-cols-4 gap-3">
            <div className="bg-white bg-opacity-20 rounded-2xl p-3 text-center">
              <Droplets className="w-6 h-6 mx-auto mb-1" />
              <div className="text-sm font-bold">{Math.round(waterPercentage)}%</div>
              <div className="text-xs opacity-90">Agua</div>
            </div>
            <div className="bg-white bg-opacity-20 rounded-2xl p-3 text-center">
              <Activity className="w-6 h-6 mx-auto mb-1" />
              <div className="text-sm font-bold">{healthData.bloodPressure.systolic || '--'}</div>
              <div className="text-xs opacity-90">Presión</div>
            </div>
            <div className="bg-white bg-opacity-20 rounded-2xl p-3 text-center">
              <Dumbbell className="w-6 h-6 mx-auto mb-1" />
              <div className="text-sm font-bold">{healthData.exercise.minutes}</div>
              <div className="text-xs opacity-90">Ejercicio</div>
            </div>
            <div className="bg-white bg-opacity-20 rounded-2xl p-3 text-center">
              <Heart className="w-6 h-6 mx-auto mb-1" />
              <div className="text-sm font-bold">{statistics.healthScore}</div>
              <div className="text-xs opacity-90">Salud</div>
            </div>
          </div>
        </div>

        <div className="p-6 pb-24">
          {/* Alertas de Riesgo */}
          {healthData.riskAlerts.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-bold text-gray-800 mb-3">⚠️ Alertas de Salud</h3>
              {healthData.riskAlerts.map((risk, index) => (
                <div key={index} className={`p-4 rounded-xl mb-3 ${
                  risk.level === 'high' ? 'bg-red-50 border border-red-200' :
                  risk.level === 'medium' ? 'bg-orange-50 border border-orange-200' :
                  'bg-yellow-50 border border-yellow-200'
                }`}>
                  <div className="flex items-start">
                    <AlertTriangle className={`w-5 h-5 mr-3 mt-0.5 ${
                      risk.level === 'high' ? 'text-red-500' :
                      risk.level === 'medium' ? 'text-orange-500' :
                      'text-yellow-500'
                    }`} />
                    <div>
                      <p className="font-semibold text-gray-800">{risk.message}</p>
                      <p className="text-sm text-gray-600 mt-1">{risk.action}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Recordatorios de Salud Rápidos */}
          <div className="bg-white rounded-2xl p-6 mb-6 shadow-sm">
            <h3 className="text-lg font-bold text-gray-800 mb-4">Recordatorios de Salud</h3>
            <div className="grid grid-cols-2 gap-4">
              <button 
                onClick={() => setCurrentScreen('waterTracker')}
                className="flex flex-col items-center p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
              >
                <Droplets className="w-8 h-8 text-blue-500 mb-2" />
                <span className="font-semibold text-blue-700">Agua</span>
                <span className="text-sm text-blue-600">{healthData.waterIntake.daily}ml</span>
              </button>
              
              <button 
                onClick={() => setCurrentScreen('mealTracker')}
                className="flex flex-col items-center p-4 bg-green-50 rounded-xl hover:bg-green-100 transition-colors"
              >
                <Apple className="w-8 h-8 text-green-500 mb-2" />
                <span className="font-semibold text-green-700">Comidas</span>
                <span className="text-sm text-green-600">
                  {Object.values(healthData.meals).filter(Boolean).length}/3
                </span>
              </button>
              
              <button 
                onClick={() => setCurrentScreen('bloodPressure')}
                className="flex flex-col items-center p-4 bg-red-50 rounded-xl hover:bg-red-100 transition-colors"
              >
                <Activity className="w-8 h-8 text-red-500 mb-2" />
                <span className="font-semibold text-red-700">Presión</span>
                <span className="text-sm text-red-600">
                  {healthData.bloodPressure.systolic || '--'}/{healthData.bloodPressure.diastolic || '--'}
                </span>
              </button>
              
              <button 
                onClick={() => setCurrentScreen('weightTracker')}
                className="flex flex-col items-center p-4 bg-purple-50 rounded-xl hover:bg-purple-100 transition-colors"
              >
                <Scale className="w-8 h-8 text-purple-500 mb-2" />
                <span className="font-semibold text-purple-700">Peso</span>
                <span className="text-sm text-purple-600">{healthData.weight.current || '--'}kg</span>
              </button>
            </div>
          </div>

          {/* Tareas del Día */}
          <div className="bg-white rounded-2xl p-6 mb-6 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold text-gray-800">Tareas de Hoy</h3>
              <button 
                onClick={() => setCurrentScreen('addTask')}
                className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center"
              >
                <Plus className="w-5 h-5 text-white" />
              </button>
            </div>
            
            {todayTasks.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Target className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No tienes tareas para hoy</p>
                <p className="text-sm">¡Agrega una nueva tarea!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {todayTasks.map(task => (
                  <TaskItem key={task.id} task={task} onToggle={toggleTask} />
                ))}
              </div>
            )}
          </div>
        </div>

        <BottomNav currentScreen="dashboard" setCurrentScreen={setCurrentScreen} />
      </div>
    );
  };

  // Tracker de Agua
  const WaterTrackerScreen = () => {
    const addWater = (amount) => {
      setHealthData(prev => ({
        ...prev,
        waterIntake: {
          ...prev.waterIntake,
          daily: prev.waterIntake.daily + amount
        }
      }));
      
      if (healthData.waterIntake.daily + amount >= healthData.waterIntake.target) {
        createNotification('achievement', '🎉 ¡Meta de agua alcanzada!', 'normal');
      }
    };

    const waterPercentage = Math.min((healthData.waterIntake.daily / healthData.waterIntake.target) * 100, 100);

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-6">
          <div className="flex items-center mb-4">
            <button 
              onClick={() => setCurrentScreen('dashboard')}
              className="mr-4 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Hidratación Diaria</h1>
          </div>
        </div>

        <div className="p-6">
          {/* Progreso de Agua */}
          <div className="bg-white rounded-2xl p-6 mb-6 text-center shadow-sm">
            <div className="relative w-32 h-32 mx-auto mb-6">
              <div className="w-full h-full rounded-full border-8 border-gray-200">
                <div 
                  className="absolute inset-0 rounded-full border-8 border-blue-500 transition-all duration-500"
                  style={{
                    clipPath: `inset(${100 - waterPercentage}% 0 0 0)`
                  }}
                ></div>
              </div>
              <div className="absolute inset-0 flex items-center justify-center">
                <Droplets className="w-12 h-12 text-blue-500" />
              </div>
            </div>
            
            <h2 className="text-2xl font-bold text-gray-800 mb-2">
              {healthData.waterIntake.daily}ml / {healthData.waterIntake.target}ml
            </h2>
            <p className="text-gray-600">
              {waterPercentage >= 100 ? '¡Meta alcanzada!' : `Te faltan ${healthData.waterIntake.target - healthData.waterIntake.daily}ml`}
            </p>
          </div>

          {/* Botones para agregar agua */}
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <h3 className="font-bold text-gray-800 mb-4">Agregar Agua</h3>
            <div className="grid grid-cols-2 gap-4">
              <button 
                onClick={() => addWater(250)}
                className="p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">🥤</div>
                  <div className="font-semibold">Vaso</div>
                  <div className="text-sm text-gray-600">250ml</div>
                </div>
              </button>
              
              <button 
                onClick={() => addWater(500)}
                className="p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">🍶</div>
                  <div className="font-semibold">Botella</div>
                  <div className="text-sm text-gray-600">500ml</div>
                </div>
              </button>
              
              <button 
                onClick={() => addWater(750)}
                className="p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">🥛</div>
                  <div className="font-semibold">Botella Grande</div>
                  <div className="text-sm text-gray-600">750ml</div>
                </div>
              </button>
              
              <button 
                onClick={() => addWater(1000)}
                className="p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
              >
                <div className="text-center">
                  <div className="text-2xl mb-2">🏺</div>
                  <div className="font-semibold">Litro</div>
                  <div className="text-sm text-gray-600">1000ml</div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Tracker de Presión Arterial
  const BloodPressureScreen = () => {
    const [systolic, setSystolic] = useState('');
    const [diastolic, setDiastolic] = useState('');

    const saveBP = () => {
      if (systolic && diastolic) {
        const newBP = {
          systolic: parseInt(systolic),
          diastolic: parseInt(diastolic),
          timestamp: new Date().toISOString()
        };
        
        setHealthData(prev => ({
          ...prev,
          bloodPressure: {
            ...newBP,
            lastCheck: new Date().toISOString(),
            history: [...prev.bloodPressure.history, newBP].slice(-30)
          }
        }));
        
        // Verificar si está en rango peligroso
        if (parseInt(systolic) > 140 || parseInt(diastolic) > 90) {
          createNotification('health_alert', '⚠️ Presión arterial elevada detectada', 'urgent');
        }
        
        setSystolic('');
        setDiastolic('');
      }
    };

    const getBPStatus = () => {
      const s = healthData.bloodPressure.systolic;
      const d = healthData.bloodPressure.diastolic;
      
      if (!s || !d) return { status: 'Sin datos', color: 'text-gray-500' };
      
      if (s < 120 && d < 80) return { status: 'Normal', color: 'text-green-500' };
      if (s < 130 && d < 80) return { status: 'Elevada', color: 'text-yellow-500' };
      if (s < 140 || d < 90) return { status: 'Etapa 1', color: 'text-orange-500' };
      return { status: 'Etapa 2', color: 'text-red-500' };
    };

    const bpStatus = getBPStatus();

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-red-400 to-pink-600 text-white p-6">
          <div className="flex items-center mb-4">
            <button 
              onClick={() => setCurrentScreen('dashboard')}
              className="mr-4 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Presión Arterial</h1>
          </div>
        </div>

        <div className="p-6">
          {/* Lectura Actual */}
          <div className="bg-white rounded-2xl p-6 mb-6 shadow-sm">
            <div className="text-center mb-6">
              <Activity className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-gray-800">
                {healthData.bloodPressure.systolic || '--'}/{healthData.bloodPressure.diastolic || '--'}
              </h2>
              <p className="text-lg text-gray-600">mmHg</p>
              <p className={`font-semibold mt-2 ${bpStatus.color}`}>{bpStatus.status}</p>
            </div>
          </div>

          {/* Registrar Nueva Lectura */}
          <div className="bg-white rounded-2xl p-6 mb-6 shadow-sm">
            <h3 className="font-bold text-gray-800 mb-4">Nueva Lectura</h3>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sistólica</label>
                <input
                  type="number"
                  value={systolic}
                  onChange={(e) => setSystolic(e.target.value)}
                  placeholder="120"
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Diastólica</label>
                <input
                  type="number"
                  value={diastolic}
                  onChange={(e) => setDiastolic(e.target.value)}
                  placeholder="80"
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
                />
              </div>
            </div>
            <button
              onClick={saveBP}
              className="w-full bg-gradient-to-r from-red-500 to-pink-600 text-white py-3 rounded-xl font-semibold"
            >
              Guardar Lectura
            </button>
          </div>

          {/* Historial Reciente */}
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <h3 className="font-bold text-gray-800 mb-4">Historial Reciente</h3>
            {healthData.bloodPressure.history.length === 0 ? (
              <p className="text-gray-500 text-center py-4">Sin lecturas registradas</p>
            ) : (
              <div className="space-y-3">
                {healthData.bloodPressure.history.slice(-5).reverse().map((reading, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-xl">
                    <div>
                      <span className="font-semibold">{reading.systolic}/{reading.diastolic}</span>
                      <span className="text-sm text-gray-500 ml-2">mmHg</span>
                    </div>
                    <span className="text-sm text-gray-500">
                      {new Date(reading.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Tracker de Comidas
  const MealTrackerScreen = () => {
    const toggleMeal = (mealType) => {
      setHealthData(prev => ({
        ...prev,
        meals: {
          ...prev.meals,
          [mealType]: !prev.meals[mealType]
        }
      }));
    };

    const mealRecommendations = {
      breakfast: ["Avena con frutas", "Huevos revueltos con verduras", "Yogurt con granola"],
      lunch: ["Ensalada con pollo", "Sopa de verduras", "Pescado a la plancha"],
      dinner: ["Verduras al vapor", "Sopa ligera", "Ensalada mixta"]
    };

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-green-400 to-emerald-600 text-white p-6">
          <div className="flex items-center mb-4">
            <button 
              onClick={() => setCurrentScreen('dashboard')}
              className="mr-4 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Seguimiento de Comidas</h1>
          </div>
        </div>

        <div className="p-6">
          {/* Comidas del Día */}
          <div className="bg-white rounded-2xl p-6 mb-6 shadow-sm">
            <h3 className="font-bold text-gray-800 mb-4">Comidas de Hoy</h3>
            
            <div className="space-y-4">
              {/* Desayuno */}
              <div className={`p-4 rounded-xl border-2 transition-all ${
                healthData.meals.breakfast ? 'border-green-500 bg-green-50' : 'border-gray-200'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div className="text-2xl mr-3">🍳</div>
                    <h4 className="font-semibold">Desayuno</h4>
                  </div>
                  <button
                    onClick={() => toggleMeal('breakfast')}
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                      healthData.meals.breakfast
                        ? 'border-green-500 bg-green-500'
                        : 'border-gray-300'
                    }`}
                  >
                    {healthData.meals.breakfast && <CheckCircle2 className="w-4 h-4 text-white" />}
                  </button>
                </div>
                <div className="text-sm text-gray-600">
                  Sugerencias: {mealRecommendations.breakfast.join(', ')}
                </div>
              </div>

              {/* Almuerzo */}
              <div className={`p-4 rounded-xl border-2 transition-all ${
                healthData.meals.lunch ? 'border-green-500 bg-green-50' : 'border-gray-200'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div className="text-2xl mr-3">🥗</div>
                    <h4 className="font-semibold">Almuerzo</h4>
                  </div>
                  <button
                    onClick={() => toggleMeal('lunch')}
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                      healthData.meals.lunch
                        ? 'border-green-500 bg-green-500'
                        : 'border-gray-300'
                    }`}
                  >
                    {healthData.meals.lunch && <CheckCircle2 className="w-4 h-4 text-white" />}
                  </button>
                </div>
                <div className="text-sm text-gray-600">
                  Sugerencias: {mealRecommendations.lunch.join(', ')}
                </div>
              </div>

              {/* Cena */}
              <div className={`p-4 rounded-xl border-2 transition-all ${
                healthData.meals.dinner ? 'border-green-500 bg-green-50' : 'border-gray-200'
              }`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div className="text-2xl mr-3">🍽️</div>
                    <h4 className="font-semibold">Cena</h4>
                  </div>
                  <button
                    onClick={() => toggleMeal('dinner')}
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                      healthData.meals.dinner
                        ? 'border-green-500 bg-green-500'
                        : 'border-gray-300'
                    }`}
                  >
                    {healthData.meals.dinner && <CheckCircle2 className="w-4 h-4 text-white" />}
                  </button>
                </div>
                <div className="text-sm text-gray-600">
                  Sugerencias: {mealRecommendations.dinner.join(', ')}
                </div>
              </div>
            </div>
          </div>

          {/* Consejos Nutricionales */}
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl p-6 text-white">
            <div className="flex items-center mb-4">
              <Apple className="w-8 h-8 mr-3" />
              <h3 className="font-bold text-lg">Consejo Nutricional</h3>
            </div>
            <p className="opacity-95">
              Mantén un horario regular de comidas. Incluye proteínas, carbohidratos complejos y vegetales en cada comida para una nutrición balanceada.
            </p>
          </div>
        </div>
      </div>
    );
  };

  // Función para alternar estado de tarea
  const toggleTask = (taskId) => {
    setTasks(prevTasks => 
      prevTasks.map(task => {
        if (task.id === taskId) {
          const newCompleted = !task.completed;
          
          setStatistics(prev => ({
            ...prev,
            completedTasks: newCompleted 
              ? prev.completedTasks + 1 
              : prev.completedTasks - 1
          }));
          
          return { ...task, completed: newCompleted };
        }
        return task;
      })
    );
  };

  // Componente de Tarea Individual
  const TaskItem = ({ task, onToggle }) => {
    const getTaskIcon = (category) => {
      const icons = {
        exercise: Dumbbell,
        food: Coffee,
        work: Briefcase,
        personal: Heart,
        health: Activity
      };
      const IconComponent = icons[category] || Target;
      return <IconComponent className="w-5 h-5" />;
    };

    return (
      <div className={`flex items-center p-4 rounded-xl border-2 transition-all ${
        task.completed 
          ? 'border-green-200 bg-green-50' 
          : 'border-gray-200 bg-white hover:border-blue-200'
      }`}>
        <button
          onClick={() => onToggle(task.id)}
          className={`w-6 h-6 rounded-full border-2 flex items-center justify-center mr-4 transition-colors ${
            task.completed
              ? 'border-green-500 bg-green-500'
              : 'border-gray-300 hover:border-blue-500'
          }`}
        >
          {task.completed && <CheckCircle2 className="w-4 h-4 text-white" />}
        </button>
        
        <div className="flex-1">
          <div className="flex items-center mb-1">
            <span className="text-blue-500 mr-2">{getTaskIcon(task.category)}</span>
            <h4 className={`font-semibold ${task.completed ? 'text-gray-500 line-through' : 'text-gray-800'}`}>
              {task.title}
            </h4>
          </div>
          <div className="flex items-center text-sm text-gray-500">
            <Clock className="w-4 h-4 mr-1" />
            <span>{task.time}</span>
          </div>
        </div>
      </div>
    );
  };

  // Pantalla para Agregar Tarea (actualizada con categoría de salud)
  const AddTaskScreen = () => {
    const [taskData, setTaskData] = useState({
      title: '',
      category: 'personal',
      date: new Date().toISOString().split('T')[0],
      time: '09:00',
      reminder: true
    });

    const categories = [
      { id: 'personal', name: 'Personal', icon: Heart, color: 'text-pink-500' },
      { id: 'work', name: 'Trabajo', icon: Briefcase, color: 'text-blue-500' },
      { id: 'exercise', name: 'Ejercicio', icon: Dumbbell, color: 'text-green-500' },
      { id: 'food', name: 'Alimentación', icon: Coffee, color: 'text-orange-500' },
      { id: 'health', name: 'Salud', icon: Activity, color: 'text-red-500' }
    ];

    const handleSubmit = (e) => {
      e.preventDefault();
      const newTask = {
        id: Date.now(),
        ...taskData,
        completed: false,
        createdAt: new Date().toISOString()
      };
      
      setTasks([...tasks, newTask]);
      setStatistics(prev => ({
        ...prev,
        totalTasks: prev.totalTasks + 1
      }));
      
      setCurrentScreen('dashboard');
    };

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6">
          <div className="flex items-center mb-4">
            <button 
              onClick={() => setCurrentScreen('dashboard')}
              className="mr-4 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Nueva Tarea</h1>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Título de la tarea</label>
            <input
              type="text"
              value={taskData.title}
              onChange={(e) => setTaskData({...taskData, title: e.target.value})}
              className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Ej. Tomar medicamento"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Categoría</label>
            <div className="grid grid-cols-2 gap-3">
              {categories.map(category => {
                const IconComponent = category.icon;
                return (
                  <button
                    key={category.id}
                    type="button"
                    onClick={() => setTaskData({...taskData, category: category.id})}
                    className={`p-4 rounded-xl border-2 flex flex-col items-center transition-all ${
                      taskData.category === category.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <IconComponent className={`w-6 h-6 mb-2 ${category.color}`} />
                    <span className="text-sm font-medium">{category.name}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Fecha</label>
              <input
                type="date"
                value={taskData.date}
                onChange={(e) => setTaskData({...taskData, date: e.target.value})}
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Hora</label>
              <input
                type="time"
                value={taskData.time}
                onChange={(e) => setTaskData({...taskData, time: e.target.value})}
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 rounded-xl font-semibold hover:opacity-90 transition-opacity"
          >
            Crear Tarea
          </button>
        </form>
      </div>
    );
  };

  // Navegación Inferior
  const BottomNav = ({ currentScreen, setCurrentScreen }) => {
    const navItems = [
      {
        id: 'dashboard',
        name: 'Inicio',
        icon: Heart,
        screen: 'dashboard'
      },
      {
        id: 'stats',
        name: 'Estadísticas',
        icon: BarChart3,
        screen: 'stats'
      },
      {
        id: 'guides',
        name: 'Guías',
        icon: BookOpen,
        screen: 'guides'
      },
      {
        id: 'notifications',
        name: 'Alertas',
        icon: Bell,
        screen: 'notifications'
      }
    ];

    return (
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-2">
        <div className="flex justify-around">
          {navItems.map(item => {
            const IconComponent = item.icon;
            const isActive = currentScreen === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentScreen(item.screen)}
                className={`flex flex-col items-center py-2 px-3 rounded-xl transition-all relative ${
                  isActive 
                    ? 'text-blue-500 bg-blue-50' 
                    : 'text-gray-400 hover:text-gray-600'
                }`}
              >
                <IconComponent className="w-5 h-5 mb-1" />
                <span className="text-xs font-medium">{item.name}</span>
                {item.id === 'notifications' && notifications.filter(n => !n.read).length > 0 && (
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-xs text-white">
                    {notifications.filter(n => !n.read).length}
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  // Pantalla de Notificaciones
  const NotificationsScreen = () => {
    const markAsRead = (notificationId) => {
      setNotifications(prev =>
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      );
    };

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-orange-500 to-red-600 text-white p-6">
          <div className="flex items-center mb-4">
            <button 
              onClick={() => setCurrentScreen('dashboard')}
              className="mr-4 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Notificaciones</h1>
          </div>
        </div>

        <div className="p-6 pb-24">
          {notifications.length === 0 ? (
            <div className="text-center py-12">
              <Bell className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-600">No hay notificaciones</h3>
              <p className="text-gray-500">Todas las alertas aparecerán aquí</p>
            </div>
          ) : (
            <div className="space-y-4">
              {notifications.map(notification => (
                <div
                  key={notification.id}
                  onClick={() => markAsRead(notification.id)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    notification.read 
                      ? 'bg-gray-50 border-gray-200' 
                      : notification.priority === 'urgent'
                      ? 'bg-red-50 border-red-200'
                      : 'bg-blue-50 border-blue-200'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className={`font-medium ${
                        notification.priority === 'urgent' ? 'text-red-800' : 'text-gray-800'
                      }`}>
                        {notification.message}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">{notification.timestamp}</p>
                    </div>
                    {!notification.read && (
                      <div className="w-3 h-3 bg-blue-500 rounded-full ml-4"></div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <BottomNav currentScreen="notifications" setCurrentScreen={setCurrentScreen} />
      </div>
    );
  };

  // Pantalla de Estadísticas actualizada
  const StatsScreen = () => {
    const completionRate = Math.round((statistics.completedTasks / Math.max(statistics.totalTasks, 1)) * 100);
    const waterPercentage = Math.round((healthData.waterIntake.daily / healthData.waterIntake.target) * 100);
    
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white p-6">
          <div className="flex items-center mb-4">
            <button 
              onClick={() => setCurrentScreen('dashboard')}
              className="mr-4 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors"
            >
              ←
            </button>
            <h1 className="text-xl font-bold">Estadísticas de Salud</h1>
          </div>
          <p className="opacity-90">Tu progreso integral</p>
        </div>

        <div className="p-6 pb-24">
          {/* Stats Overview */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <div className="bg-white rounded-2xl p-6 text-center shadow-sm">
              <Heart className="w-8 h-8 text-red-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-red-500 mb-1">{statistics.healthScore}</div>
              <div className="text-sm text-gray-600">Puntuación Salud</div>
            </div>
            <div className="bg-white rounded-2xl p-6 text-center shadow-sm">
              <Droplets className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-500 mb-1">{waterPercentage}%</div>
              <div className="text-sm text-gray-600">Hidratación</div>
            </div>
            <div className="bg-white rounded-2xl p-6 text-center shadow-sm">
              <Activity className="w-8 h-8 text-green-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-green-500 mb-1">{healthData.exercise.minutes}</div>
              <div className="text-sm text-gray-600">Min. Ejercicio</div>
            </div>
            <div className="bg-white rounded-2xl p-6 text-center shadow-sm">
              <Target className="w-8 h-8 text-purple-500 mx-auto mb-2" />
              <div className="text-2xl font-bold text-purple-500 mb-1">{completionRate}%</div>
              <div className="text-sm text-gray-600">Tareas</div>
            </div>
          </div>

          {/* Resumen Semanal de Salud */}
          <div className="bg-white rounded-2xl p-6 shadow-sm mb-6">
            <h3 className="font-bold text-gray-800 mb-4">Resumen Semanal</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Droplets className="w-5 h-5 text-blue-500 mr-3" />
                  <span>Hidratación promedio</span>
                </div>
                <span className="font-semibold">{waterPercentage}%</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Apple className="w-5 h-5 text-green-500 mr-3" />
                  <span>Comidas completadas</span>
                </div>
                <span className="font-semibold">
                  {Object.values(healthData.meals).filter(Boolean).length}/3
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Activity className="w-5 h-5 text-red-500 mr-3" />
                  <span>Última presión arterial</span>
                </div>
                <span className="font-semibold">
                  {healthData.bloodPressure.systolic || '--'}/{healthData.bloodPressure.diastolic || '--'}
                </span>
              </div>
            </div>
          </div>
        </div>

        <BottomNav currentScreen="stats" setCurrentScreen={setCurrentScreen} />
      </div>
    );
  };

  // Renderizado condicional de pantallas
  const renderScreen = () => {
    switch(currentScreen) {
      case 'welcome':
        return <WelcomeScreen />;
      case 'register':
        return <RegisterScreen />;
      case 'login':
        return <LoginScreen />;
      case 'healthSurvey':
        return <HealthSurveyScreen />;
      case 'dashboard':
        return <DashboardScreen />;
      case 'addTask':
        return <AddTaskScreen />;
      case 'waterTracker':
        return <WaterTrackerScreen />;
      case 'bloodPressure':
        return <BloodPressureScreen />;
      case 'mealTracker':
        return <MealTrackerScreen />;
      case 'notifications':
        return <NotificationsScreen />;
      case 'stats':
        return <StatsScreen />;
      default:
        return <DashboardScreen />;
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white min-h-screen relative">
      {renderScreen()}
    </div>
  );
};

export default LifeOrganizerApp;