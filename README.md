# Gemelo Digital SCADA

Prototipo académico en Python para supervisar una faja transportadora en CoppeliaSim, con una línea de investigación en inspección de calidad y mantenimiento predictivo mediante machine learning.

**Estado: desarrollo inicial.** Existe una interfaz de escritorio, un lector de señales por consola y un generador sintético. La adquisición todavía no está integrada al dashboard; no hay modelos ML entrenados, inspección automática ni mantenimiento predictivo implementados.

## Funcionalidades actuales

| Componente | Implementado | Pendiente |
| --- | --- | --- |
| Interfaz CustomTkinter | Panel oscuro, tarjetas, sensor y distribución adaptable | Actualización de valores y navegación |
| CoppeliaSim | Lector ZeroMQ de presencia, altura y estado de faja | Validación con la escena e integración gráfica |
| Datos sintéticos | Normal/Alerta/Falla, semilla y exportación CSV | Calibración y degradación temporal |
| Calidad | Lectura bruta de altura/presencia en consola | Tolerancias, trazabilidad por pieza y decisión |
| Mantenimiento ML | Espacio visual reservado | Dataset, entrenamiento, evaluación e inferencia |

## Requisitos e instalación

- Python 3.12 o superior; comprobación local con Python 3.14.7 en Windows.
- Tkinter para la interfaz. En algunas distribuciones Linux se instala por separado, por ejemplo como `python3-tk`.
- CoppeliaSim con servidor ZeroMQ para el lector. No es necesario para abrir la interfaz o generar datos.

Desde la raíz del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No es necesario activar el entorno. En Linux/macOS utiliza `.venv/bin/python` en lugar de `.\.venv\Scripts\python.exe`.

## Ejecutar

### Dashboard visual

```powershell
.\.venv\Scripts\python.exe dashboard_scada.py
```

Abre la interfaz con indicadores sin datos y conexión inactiva. Ejecutar el lector en otra consola todavía no actualiza el dashboard. Las opciones laterales son secciones previstas, no botones funcionales.

### Lector de CoppeliaSim

Abre tu escena, inicia la simulación y verifica el contrato de [simulacion/README.md](simulacion/README.md). Luego:

```powershell
.\.venv\Scripts\python.exe conexion_Coppelia.py --host localhost --puerto 23000 --intervalo 0.2 --timeout 5
```

`--muestras 10` limita la lectura; `Ctrl+C` termina el modo continuo. El lector no inicia ni detiene la simulación. Emite JSON por línea a stdout y mensajes de conexión a stderr. Si una señal falta, devuelve `null`; no lo convierte en cero. La escena `.ttt` no está incluida, por lo que la lectura real requiere aportarla.

### Datos sintéticos reproducibles

```powershell
.\.venv\Scripts\python.exe generador_datos.py --semilla 42
.\.venv\Scripts\python.exe generador_datos.py --muestras 1000 --semilla 42 --salida datos/sinteticos.csv
.\.venv\Scripts\python.exe generador_datos.py --muestras 100 --estado Alerta --salida datos/alerta.csv
```

No sobrescribe archivos existentes salvo que se añada `--sobrescribir`. Estas muestras son independientes: el índice no representa tiempo ni degradación. Las distribuciones son ilustrativas; no sirven como evidencia de precisión en una planta real. Consulta el [diccionario de datos](datos/README.md).

También se puede ejecutar `python -m scada.dashboard`, `python -m scada.conexion` o `python -m scada.generador`. Opcionalmente, `python -m pip install --no-deps -e .` registra los comandos `scada-dashboard`, `scada-coppelia` y `scada-generar` tras instalar las dependencias.

## Organización

```text
GemeloDigitalSCADA/
├── scada/
│   ├── dashboard.py          # Construcción y ejecución de la interfaz
│   ├── conexion.py           # Lectura de CoppeliaSim
│   └── generador.py          # Generación sintética y CSV
├── dashboard_scada.py        # Entradas compatibles con los nombres originales
├── conexion_Coppelia.py
├── generador_datos.py
├── datos/README.md           # Esquema y límites del dataset
├── simulacion/README.md      # Requisitos de la escena pendiente
├── docs/
│   ├── REVISION_TECNICA.md   # Feedback de software e investigación
│   └── PUBLICAR_GITHUB.md   # Preparación y publicación
├── tests/
├── .github/workflows/ci.yml
├── requirements.txt
└── pyproject.toml
```

## Verificación

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q scada dashboard_scada.py conexion_Coppelia.py generador_datos.py
```

Las pruebas usan señales simuladas y no necesitan una escena ni abrir ventanas. El workflow añade verificaciones automáticas en Windows/Linux y Python 3.12/3.14 al publicar; esa matriz no implica que ya se haya ejecutado.

## Próximas etapas

1. Incorporar la escena y documentar señales, tipos, unidades y versión de CoppeliaSim.
2. Conectar adquisición y dashboard con una cola y `after()`, con estado desconectado/dato obsoleto.
3. Persistir telemetría y decisiones de calidad con identificador de pieza y tiempo.
4. Definir fallas, horizonte predictivo, campañas y protocolo de evaluación ML.

El [informe técnico](docs/REVISION_TECNICA.md) explica las prioridades y los criterios de aceptación. Para publicar, sigue la [guía de GitHub](docs/PUBLICAR_GITHUB.md). No se ha asignado una licencia: el titular debe elegirla antes de distribuir el proyecto bajo términos de código abierto.
