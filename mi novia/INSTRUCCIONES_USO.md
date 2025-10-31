# Instrucciones de Uso - Life Organizer

## ¿Qué tipo de aplicación es esta?

Esta es una **aplicación web** que se ejecuta en un servidor y se accede a través de un navegador web (Chrome, Firefox, Edge, etc.). **NO es una aplicación móvil Android** que puedes instalar directamente.

## Opciones para usar la aplicación

### Opción 1: Usar en tu computadora (Más fácil)

1. **Instalar dependencias** (si aún no lo has hecho):
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python run.py
   ```

3. **Abrir en tu navegador**:
   - Abre tu navegador web
   - Ve a: `http://localhost:5000`
   - ¡Listo! Ya puedes usar la aplicación

### Opción 2: Usar en tu celular Android (Necesitas acceso a la red)

Si quieres usar la aplicación en tu celular:

1. **Ejecuta la aplicación en tu computadora** con:
   ```bash
   python run.py
   ```

2. **Conecta tu celular a la misma red WiFi** que tu computadora

3. **Obtén la dirección IP** de tu computadora:
   - En Windows: Abre PowerShell y ejecuta `ipconfig`
   - Busca "IPv4 Address" (ejemplo: 192.168.1.100)

4. **Abre en tu celular**:
   - Abre tu navegador móvil
   - Ve a: `http://TU_IP:5000` (ejemplo: http://192.168.1.100:5000)

### Opción 3: Desplegar en Internet (Avanzado)

Si quieres que la aplicación esté disponible en internet:

1. **Servicios gratuitos**:
   - Heroku (gratis con limitaciones)
   - PythonAnywhere (gratis con limitaciones)
   - Render (gratis con limitaciones)
   - Railway (gratis con limitaciones)

2. **Servicios de pago**:
   - AWS
   - Google Cloud Platform
   - Azure

## ¿Cómo convertirla en una app móvil Android?

Si realmente necesitas un APK, tendrías que:

### Opción A: Crear una PWA (Progressive Web App)
Convertir la aplicación web en una PWA que se puede instalar como una app:

1. Agregar un archivo `manifest.json`
2. Agregar un Service Worker
3. Configurar HTTPS
4. Los usuarios pueden "instalar" la app desde el navegador

### Opción B: Usar Kivy o BeeWare
Reescribir la aplicación usando herramientas que permiten crear APKs:

1. **Kivy**: Framework Python para apps móviles
2. **BeeWare**: Convierte aplicaciones Python en apps nativas

**Nota**: Esto requiere reescribir gran parte del código.

### Opción C: Usar WebView
Crear una app Android simple que solo muestre tu aplicación web en un WebView.

## Recomendación

**La forma más fácil**: Usa la aplicación en tu computadora o accede a ella desde tu celular usando la misma red WiFi. No necesitas crear un APK para eso.

## ¿Necesitas ayuda con alguna opción?

Si quieres ayuda con alguna de estas opciones, solo dímelo y te ayudo paso a paso.

