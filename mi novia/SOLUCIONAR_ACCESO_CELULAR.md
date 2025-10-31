# 🔧 Solución de Problemas - Acceso desde el Celular

## Problema: No puedo acceder desde mi celular

### Solución 1: Abrir el Puerto en el Firewall (IMPORTANTE)

**Opción A: Usando el script proporcionado**

1. Haz clic derecho en `ABRIR_PUERTO_FIREWALL.bat`
2. Selecciona **"Ejecutar como administrador"**
3. Confirma cuando Windows te pregunte
4. Espera a que termine
5. Intenta acceder desde tu celular nuevamente

**Opción B: Manualmente**

1. Presiona `Windows + R`
2. Escribe: `wf.msc` y presiona Enter
3. En el panel izquierdo, haz clic en **"Reglas de entrada"**
4. En el panel derecho, haz clic en **"Nueva regla..."**
5. Selecciona **"Puerto"** y haz clic en **Siguiente**
6. Selecciona **"TCP"** y escribe **5000** en puertos específicos locales
7. Haz clic en **Siguiente**
8. Selecciona **"Permitir la conexión"**
9. Haz clic en **Siguiente**
10. Marca todas las casillas (Dominio, Privada, Pública)
11. Haz clic en **Siguiente**
12. Ponle un nombre: **"Flask App Puerto 5000"**
13. Haz clic en **Finalizar**

### Solución 2: Verificar que estén en la misma red WiFi

1. **En tu computadora:**
   - Abre PowerShell o CMD
   - Escribe: `ipconfig` y presiona Enter
   - Busca "IPv4" y anota la dirección (ejemplo: 192.168.1.100)

2. **En tu celular:**
   - Ve a Configuración > WiFi
   - Busca la red actual
   - El nombre DEBE ser el mismo que en tu computadora

3. **Verifica la IP:**
   - Si tu computadora está en 192.168.1.x, tu celular debe estar en 192.168.1.x
   - Si son diferentes (ej: 192.168.1.x vs 192.168.0.x), NO están en la misma red

### Solución 3: Deshabilitar temporalmente el Firewall (Solo para probar)

⚠️ **ADVERTENCIA**: Esto desactiva tu firewall. Solo úsalo para probar.

1. Presiona `Windows + R`
2. Escribe: `firewall.cpl` y presiona Enter
3. Haz clic en **"Desactivar o activar Firewall de Windows"**
4. Desactiva temporalmente el firewall para redes privadas
5. Intenta acceder desde tu celular
6. **IMPORTANTE**: Vuelve a activar el firewall después

### Solución 4: Usar tu IP local en lugar de localhost

En el archivo `run.py`, asegúrate de que esté configurado así:

```python
app.run(
    host='0.0.0.0',  # ← Esto permite acceso desde otros dispositivos
    port=5000,
    debug=True
)
```

### Solución 5: Verificar que la aplicación esté corriendo

1. Abre PowerShell o CMD
2. Escribe: `netstat -ano | findstr :5000`
3. Deberías ver algo como:
   ```
   TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING
   ```

Si no ves nada, la aplicación no está corriendo.

### Solución 6: Usar HTTPS en lugar de HTTP (si tienes problemas)

Si sigues teniendo problemas, puedes intentar usar HTTPS:

1. Instala `mkcert` para crear certificados SSL locales
2. Configura Flask para usar HTTPS

## 🔍 Checklist de Diagnóstico

Usa esta lista para identificar el problema:

- [ ] ¿La aplicación está corriendo en tu computadora?
- [ ] ¿Están en la misma red WiFi?
- [ ] ¿El firewall de Windows está bloqueando el puerto?
- [ ] ¿Estás usando la IP correcta? (no uses localhost desde el celular)
- [ ] ¿El puerto 5000 está abierto en el firewall?

## 📱 Prueba desde tu PC primero

Antes de intentar desde el celular, prueba desde tu computadora:

1. Abre tu navegador en la PC
2. Ve a: `http://localhost:5000`
3. Si funciona aquí, el problema es el firewall o la red WiFi

## 🆘 Si nada funciona

**Alternativa**: Usa un servicio de túnel como ngrok para exponer tu aplicación localmente:

1. Descarga ngrok: https://ngrok.com/download
2. Instala ngrok
3. Ejecuta: `ngrok http 5000`
4. ngrok te dará una URL pública (ej: https://abc123.ngrok.io)
5. Usa esa URL desde cualquier dispositivo

## 📞 Más ayuda

Si sigues teniendo problemas, comparte:
- ¿Qué error ves en tu celular?
- ¿La aplicación se abre en tu computadora?
- ¿Qué IP estás usando?

