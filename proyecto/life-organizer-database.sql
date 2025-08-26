-- Base de Datos Life Organizer
-- Sistema integral de organización personal y monitoreo de salud

-- =======================
-- TABLA DE USUARIOS
-- =======================
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    weight DECIMAL(5,2), -- kg
    height INT, -- cm
-- Base de Datos Life Organizer
-- Sistema integral de organización personal y monitoreo de salud

-- =======================
-- TABLA DE USUARIOS
-- =======================
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT,
    weight DECIMAL(5,2), -- kg
    height INT, -- cm
    target_water_intake INT DEFAULT 2000, -- ml
    target_exercise_minutes INT DEFAULT 30,
    target_weight DECIMAL(5,2), -- kg
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =======================
-- TABLA DE CONDICIONES MÉDICAS
-- =======================
CREATE TABLE medical_conditions (
    condition_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    condition_name VARCHAR(100) NOT NULL,
    diagnosed_date DATE,
    severity ENUM('leve', 'moderada', 'severa'),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =======================
-- TABLA DE MEDICAMENTOS
-- =======================
CREATE TABLE medications (
    medication_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    frequency VARCHAR(50), -- "2 veces al día", "cada 8 horas", etc.
    start_date DATE,
    end_date DATE,
    active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =======================
-- TABLA DE TAREAS
-- =======================
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category ENUM('personal', 'work', 'exercise', 'food', 'health') DEFAULT 'personal',
    due_date DATE,
    due_time TIME,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    reminder_enabled BOOLEAN DEFAULT TRUE,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- =======================
-- TABLA DE CONSUMO DE AGUA
-- =======================
CREATE TABLE water_intake (
    intake_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    amount_ml INT NOT NULL,
    recorded_date DATE NOT NULL,
    recorded_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, recorded_date)
);

-- =======================
-- TABLA DE PRESIÓN ARTERIAL
-- =======================
CREATE TABLE blood_pressure (
    bp_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    systolic INT NOT NULL, -- mmHg
    diastolic INT NOT NULL, -- mmHg
    pulse INT, -- pulsaciones por minuto
    measurement_date DATE NOT NULL,
    measurement_time TIME NOT NULL,
    notes TEXT,
    location VARCHAR(50), -- 'casa', 'consultorio', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, measurement_date)
);

-- =======================
-- TABLA DE PESO CORPORAL
-- =======================
CREATE TABLE weight_records (
    weight_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    weight_kg DECIMAL(5,2) NOT NULL,
    measurement_date DATE NOT NULL,
    measurement_time TIME DEFAULT '08:00:00',
    body_fat_percentage DECIMAL(4,2), -- opcional
    muscle_mass DECIMAL(5,2), -- opcional
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, measurement_date)
);

-- =======================
-- TABLA DE EJERCICIOS
-- =======================
CREATE TABLE exercises (
    exercise_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    exercise_type VARCHAR(100) NOT NULL, -- 'caminar', 'correr', 'natación', etc.
    duration_minutes INT NOT NULL,
    calories_burned INT,
    intensity ENUM('baja', 'moderada', 'alta') DEFAULT 'moderada',
    exercise_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, exercise_date)
);

-- =======================
-- TABLA DE COMIDAS
-- =======================
CREATE TABLE meals (
    meal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
    meal_date DATE NOT NULL,
    meal_time TIME,
    calories_estimated INT,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, meal_date)
);

-- =======================
-- TABLA DE PATRONES DE SUEÑO
-- =======================
CREATE TABLE sleep_records (
    sleep_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    sleep_date DATE NOT NULL,
    bedtime TIME,
    wake_time TIME,
    total_hours DECIMAL(3,1), -- calculado automáticamente
    quality ENUM('poor', 'fair', 'good', 'excellent') DEFAULT 'good',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, sleep_date)
);

-- =======================
-- TABLA DE NOTIFICACIONES
-- =======================
CREATE TABLE notifications (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    type VARCHAR(50) NOT NULL, -- 'water_reminder', 'health_alert', 'medication', etc.
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal',
    read_status BOOLEAN DEFAULT FALSE,
    scheduled_time DATETIME,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_read (user_id, read_status)
);

-- =======================
-- TABLA DE ALERTAS DE RIESGO
-- =======================
CREATE TABLE health_risk_alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    risk_type VARCHAR(50) NOT NULL, -- 'high_blood_pressure', 'dehydration', etc.
    risk_level ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    alert_message TEXT NOT NULL,
    recommended_action TEXT,
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_active (user_id, active)
);

-- =======================
-- TABLA DE ENCUESTAS INICIALES
-- =======================
CREATE TABLE user_surveys (
    survey_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    survey_type VARCHAR(50) NOT NULL, -- 'initial_health', 'lifestyle', etc.
    question_id VARCHAR(50) NOT NULL,
    question_text TEXT NOT NULL,
    answer_text TEXT,
    answer_value INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, survey_type)
);

-- =======================
-- TABLA DE ESTADÍSTICAS DIARIAS
-- =======================
CREATE TABLE daily_stats (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    stat_date DATE NOT NULL,
    tasks_completed INT DEFAULT 0,
    tasks_total INT DEFAULT 0,
    water_intake_ml INT DEFAULT 0,
    exercise_minutes INT DEFAULT 0,
    meals_completed INT DEFAULT 0,
    health_score INT DEFAULT 0, -- puntuación calculada del 0-100
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, stat_date)
);

-- =======================
-- TABLA DE CONFIGURACIONES DE USUARIO
-- =======================
CREATE TABLE user_settings (
    setting_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    setting_key VARCHAR(50) NOT NULL,
    setting_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_setting (user_id, setting_key)
);

-- =======================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- =======================
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_category ON tasks(category);
CREATE INDEX idx_bp_measurement_date ON blood_pressure(measurement_date);
CREATE INDEX idx_water_recorded_date ON water_intake(recorded_date);
CREATE INDEX idx_exercises_date ON exercises(exercise_date);
CREATE INDEX idx_notifications_scheduled ON notifications(scheduled_time);

-- =======================
-- TRIGGERS PARA CÁLCULOS AUTOMÁTICOS
-- =======================

-- Trigger para calcular horas de sueño
DELIMITER //
CREATE TRIGGER calculate_sleep_hours 
BEFORE INSERT ON sleep_records
FOR EACH ROW
BEGIN
    IF NEW.bedtime IS NOT NULL AND NEW.wake_time IS NOT NULL THEN
        -- Calcula las horas considerando que puede cruzar medianoche
        SET NEW.total_hours = 
            CASE 
                WHEN NEW.wake_time >= NEW.bedtime THEN 
                    TIME_TO_SEC(TIMEDIFF(NEW.wake_time, NEW.bedtime)) / 3600
                ELSE 
                    (TIME_TO_SEC(TIMEDIFF('24:00:00', NEW.bedtime)) + TIME_TO_SEC(NEW.wake_time)) / 3600
            END;
    END IF;
END //
DELIMITER ;

-- Trigger para actualizar estadísticas diarias
DELIMITER //
CREATE TRIGGER update_daily_stats_water
AFTER INSERT ON water_intake
FOR EACH ROW
BEGIN
    INSERT INTO daily_stats (user_id, stat_date, water_intake_ml)
    VALUES (NEW.user_id, NEW.recorded_date, NEW.amount_ml)
    ON DUPLICATE KEY UPDATE 
        water_intake_ml = water_intake_ml + NEW.amount_ml,
        updated_at = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- =======================
-- PROCEDIMIENTOS ALMACENADOS
-- =======================

-- Procedimiento para calcular puntuación de salud
DELIMITER //
CREATE PROCEDURE CalculateHealthScore(IN p_user_id INT, IN p_date DATE)
BEGIN
    DECLARE v_health_score INT DEFAULT 0;
    DECLARE v_water_score INT DEFAULT 0;
    DECLARE v_exercise_score INT DEFAULT 0;
    DECLARE v_meals_score INT DEFAULT 0;
    DECLARE v_bp_score INT DEFAULT 0;
    
    -- Puntuación de agua (30 puntos máximo)
    SELECT LEAST(30, (SUM(amount_ml) * 30 / 2000)) INTO v_water_score
    FROM water_intake 
    WHERE user_id = p_user_id AND recorded_date = p_date;
    
    -- Puntuación de ejercicio (25 puntos máximo)
    SELECT LEAST(25, (SUM(duration_minutes) * 25 / 30)) INTO v_exercise_score
    FROM exercises 
    WHERE user_id = p_user_id AND exercise_date = p_date;
    
    -- Puntuación de comidas (25 puntos máximo)
    SELECT (COUNT(*) * 25 / 3) INTO v_meals_score
    FROM meals 
    WHERE user_id = p_user_id AND meal_date = p_date AND completed = TRUE;
    
    -- Puntuación de presión arterial (20 puntos máximo)
    SELECT 
        CASE 
            WHEN systolic BETWEEN 90 AND 120 AND diastolic BETWEEN 60 AND 80 THEN 20
            WHEN systolic BETWEEN 120 AND 139 OR diastolic BETWEEN 80 AND 89 THEN 15
            WHEN systolic BETWEEN 140 AND 159 OR diastolic BETWEEN 90 AND 99 THEN 10
            ELSE 5
        END INTO v_bp_score
    FROM blood_pressure 
    WHERE user_id = p_user_id AND measurement_date = p_date
    ORDER BY measurement_date DESC, measurement_time DESC
    LIMIT 1;
    
    SET v_health_score = COALESCE(v_water_score, 0) + COALESCE(v_exercise_score, 0) + 
                        COALESCE(v_meals_score, 0) + COALESCE(v_bp_score, 0);
    
    -- Actualizar estadísticas diarias
    INSERT INTO daily_stats (user_id, stat_date, health_score)
    VALUES (p_user_id, p_date, v_health_score)
    ON DUPLICATE KEY UPDATE 
        health_score = v_health_score,
        updated_at = CURRENT_TIMESTAMP;
        
    SELECT v_health_score as health_score;
END //
DELIMITER ;

-- =======================
-- VISTAS ÚTILES
-- =======================

-- Vista para estadísticas semanales de usuario
CREATE VIEW weekly_user_stats AS
SELECT 
    u.user_id,
    u.name,
    YEARWEEK(ds.stat_date) as week_year,
    AVG(ds.health_score) as avg_health_score,
    AVG(ds.water_intake_ml) as avg_water_intake,
    AVG(ds.exercise_minutes) as avg_exercise_minutes,
    AVG(ds.tasks_completed / NULLIF(ds.tasks_total, 0) * 100) as avg_task_completion_rate
FROM users u
LEFT JOIN daily_stats ds ON u.user_id = ds.user_id
GROUP BY u.user_id, YEARWEEK(ds.stat_date);

-- Vista para alertas activas de usuario
CREATE VIEW active_user_alerts AS
SELECT 
    u.name,
    hra.risk_type,
    hra.risk_level,
    hra.alert_message,
    hra.recommended_action,
    hra.triggered_at
FROM users u
JOIN health_risk_alerts hra ON u.user_id = hra.user_id
WHERE hra.active = TRUE
ORDER BY hra.risk_level DESC, hra.triggered_at DESC;

-- =======================
-- DATOS DE EJEMPLO
-- =======================

-- Usuario de ejemplo
INSERT INTO users (name, email, password_hash, age, weight, height, target_water_intake, target_exercise_minutes) 
VALUES ('Juan Pérez', 'juan@example.com', 'hash123', 30, 75.5, 175, 2500, 45);

-- Condiciones médicas de ejemplo
INSERT INTO medical_conditions (user_id, condition_name, diagnosed_date, severity) 
VALUES (1, 'Hipertensión', '2023-01-15', 'leve');

-- Medicamentos de ejemplo
INSERT INTO medications (user_id, medication_name, dosage, frequency, start_date) 
VALUES (1, 'Losartán', '50mg', '1 vez al día', '2023-01-15');

-- Tareas de ejemplo
INSERT INTO tasks (user_id, title, category, due_date, due_time) VALUES
(1, 'Tomar medicamento matutino', 'health', CURDATE(), '08:00:00'),
(1, 'Caminar 30 minutos', 'exercise', CURDATE(), '18:00:00'),
(1, 'Beber 2 litros de agua', 'health', CURDATE(), '20:00:00');

-- Registros de agua de ejemplo
INSERT INTO water_intake (user_id, amount_ml, recorded_date, recorded_time) VALUES
(1, 250, CURDATE(), '08:30:00'),
(1, 500, CURDATE(), '12:00:00'),
(1, 250, CURDATE(), '15:30:00');

-- Presión arterial de ejemplo
INSERT INTO blood_pressure (user_id, systolic, diastolic, pulse, measurement_date, measurement_time) 
VALUES (1, 125, 82, 72, CURDATE(), '09:00:00');

-- =======================
-- CONSULTAS ÚTILES DE EJEMPLO
-- =======================

/*
-- Obtener resumen diario de usuario
SELECT 
    ds.*,
    (SELECT COUNT(*) FROM tasks WHERE user_id = ds.user_id AND due_date = ds.stat_date AND completed = TRUE) as completed_tasks,
    (SELECT COUNT(*) FROM tasks WHERE user_id = ds.user_id AND due_date = ds.stat_date) as total_tasks
FROM daily_stats ds 
WHERE user_id = 1 AND stat_date = CURDATE();

-- Obtener alertas activas
SELECT * FROM active_user_alerts WHERE name = 'Juan Pérez';

-- Historial de presión arterial última semana
SELECT * FROM blood_pressure 
WHERE user_id = 1 AND measurement_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY measurement_date DESC, measurement_time DESC;

-- Progreso de hidratación semanal
SELECT 
    recorded_date,
    SUM(amount_ml) as total_water,
    (SELECT target_water_intake FROM users WHERE user_id = 1) as target,
    (SUM(amount_ml) / (SELECT target_water_intake FROM users WHERE user_id = 1) * 100) as percentage
FROM water_intake 
WHERE user_id = 1 AND recorded_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY recorded_date
ORDER BY recorded_date;
*/