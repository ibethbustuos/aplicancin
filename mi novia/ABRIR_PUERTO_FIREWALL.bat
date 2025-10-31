@echo off
echo ================================================================
echo ABRIENDO PUERTO 5000 EN EL FIREWALL DE WINDOWS
echo ================================================================
echo.
echo Este script necesita permisos de Administrador
echo.
pause

netsh advfirewall firewall add rule name="Flask App Puerto 5000" dir=in action=allow protocol=TCP localport=5000

echo.
echo ================================================================
echo PUERTO 5000 ABIERTO CORRECTAMENTE
echo ================================================================
echo.
echo Ahora puedes acceder desde tu celular usando:
echo http://192.168.20.28:5000
echo.
pause

