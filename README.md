# Sistema de Préstamos de Materiales
- Ronald Cruz Chino.
- Denilson Davis Machaca Flores.
- Daniel Wilfredo Pomarez Huaranca

**Materia:** Programación Fundamental

## Descripción
Programa en Python que permite gestionar préstamos de materiales a estudiantes mediante un archivo CSV.

## Características
- Validación del código de estudiante (`SIS-123456`).
- Validación de nombres y títulos.
- Control de días de préstamo (1 a 30 días).
- Detección de préstamos duplicados.
- Lectura y escritura de datos en CSV.
- Ignora registros inválidos o repetidos.
- Protección de errores al leer y guardar archivos.

## Tecnologías utilizadas
- Python 3
- Módulo CSV

## Estructura de datos

El archivo `prestamos.csv` almacena los siguientes campos:

| Campo | Descripción |
|---|---|
| codigo | Código del estudiante |
| nombre | Nombre del estudiante |
| titulo | Material solicitado |
| dias | Días del préstamo |

## Cómo ejecutar

1. Tener Python instalado.
2. Guardar `PFU.py` y `prestamos.csv` en la misma carpeta.
3. Abrir una terminal en esa carpeta.
4. Ejecutar:

```bash
python PFU.py
```

El archivo CSV se crea al guardar los primeros registros.

## Validaciones
El sistema comprueba que los datos ingresados sean correctos antes de almacenarlos, evitando información vacía, formatos incorrectos y préstamos duplicados.


