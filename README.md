# VoidBoost
VoidBoost es una herramienta desarrollada por v019, principalmente esta herramienta ha sido desarrollada para una práctica de Optimización de un sistema operativo.

## ¿Qué funciones tiene?
1. Crear un plan de energía: Bajo o ahorro de energía, Equilibrado o medio y alto o Alto rendimiento.
2. Borrar archivos temporales: Borra archivos temporales en TEMP y en PREFETCH

## Detalles técnicos
Este proyecto dispone de 1 carpeta en la cual están los módulos almacenados en diferentes archivos con clases y métodos específicos usados en el archivo principal del proyecto `main.py`

El archivo situado en `modules/TempRemover.py` dispone de comentarios para facilitar entender el código.

El resto de archivos he considerado que se entienden bastante bien por lo cual no tienen comentarios.

El único módulo que usa un logger es el `modules/TempRemover.py` por la gran cantidad de archivos que se pueden acumular en las carpetas de archivos temporales.

### Especificaciones extra del TempRemover.py

Este archivo tiene una función interesante, la cual es comprobar si el archivo está siendo usado, usando el modo exclusivo y si el archivo está protegido.

#### Modo exclusivo

En `modules/TempRemover.py` se usa la API de Windows para bloquear el archivo y comprobar si está en uso. El proceso es simple:

1. **Abrir el archivo**: Se abre el archivo en modo binario con `rb`, con un buffer de 0 osea sin buffer.
2. **Obtener el handle del archivo**: Se usa `msvcrt.get_ofshandle()` para pillar el identificador del archivo.
3. **Bloqueo del archivo**: Llamamos a la función Lockfile() de la DLL kernel32 para intentar bloquear el archivo. Si el archivo está bloqueado, la función LockFile() devuelve un valor que es diferente a 0. En caso de que se bloquee correctamente, se desbloquea con UnlockFile()
4. **Excepciones**: En caso de que ocurra un error, se controla con excepciones IOError, OSError entre otras.

