# Contrato de CoppeliaSim

La escena `.ttt` y los scripts Lua no estaban presentes en el proyecto revisado. Esta carpeta documenta los requisitos del lector; no proporciona una escena ejecutable.

| Elemento | Valor esperado actualmente |
| --- | --- |
| Transporte | ZeroMQ Remote API, protocolo compatible con cliente Python 2.0.4 |
| Host/puerto por defecto | `localhost:23000`, configurables por CLI |
| Objeto de faja | `/conveyor`, configurable mediante `--faja` |
| Presencia | Señal int32 `sensor_presencia`; 0/1 o ausente |
| Altura | Señal int32 `sensor_altura`; unidad y escala pendientes de definir |
| Estado de faja | Tabla personalizada `__state__`; esquema depende de la escena |
| Reloj | `getSimulationTime()` en segundos |

El lector observa una simulación que ya está en ejecución; no modifica el movimiento de la faja. Los campos se consultan secuencialmente y no constituyen una captura atómica ni un muestreo de tiempo real garantizado. El intervalo por defecto de 0.2 s es una pausa entre ciclos, a la que se suma la latencia de las consultas.

Para reproducibilidad, añadir aquí la escena y sus scripts propios junto con la versión exacta de CoppeliaSim, pasos de arranque, parámetros físicos, escala/unidades, escenarios de falla y condiciones iniciales. Comprobar permisos/licencias de modelos de terceros antes de incluirlos.

El timeout de CLI limita la espera de envío/recepción de cada operación; una lectura contiene varias operaciones. Tras una interrupción de red, el comando finaliza con error y puede reiniciarse. Reconexión automática e historial persistente siguen pendientes.

Referencia: [ZeroMQ Remote API oficial](https://manual.coppeliarobotics.com/en/zmqRemoteApiOverview.htm).
