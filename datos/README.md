# Datos del proyecto

Los CSV y otros experimentos de esta carpeta se excluyen de Git. Versionar por separado datasets pequeños y autorizados si se decide compartirlos, junto con su procedencia y licencia.

## CSV sintético actual

| Campo | Tipo/unidad | Significado |
| --- | --- | --- |
| muestra_id | entero, desde 0 | Índice dentro de una exportación; no es tiempo |
| origen | texto | Siempre `sintetico` |
| carga_kg | kg | Carga ilustrativa |
| temperatura_c | °C | Temperatura ilustrativa |
| vibracion_mm_s | mm/s | Magnitud ilustrativa, sin adquisición ni banda definidas |
| corriente_a | A | Corriente ilustrativa dependiente de carga y escenario |
| velocidad_m_s | m/s | Velocidad ilustrativa |
| estado | Normal/Alerta/Falla | Escenario elegido antes de generar las variables |

Misma semilla, cantidad, escenario y versión del código reproducen el archivo. Las clases aleatorias no garantizan balance exacto, particularmente con pocas muestras. Las distribuciones pueden solaparse. El generador no simula desgaste progresivo, espectros, ventanas de señal ni el tiempo restante hasta una falla.

La etiqueta es una entrada del generador, no un diagnóstico independiente ni una observación de falla real. Un modelo entrenado aquí puede aprender sus distribuciones artificiales; su resultado no demuestra capacidad predictiva industrial. No usar estos datos para validar inspección de calidad: no hay piezas ni defectos etiquetados.

## Telemetría futura

Antes de capturar datos reales o del simulador, fijar: identificador de activo, sesión y pieza; timestamp UTC y tiempo de simulación; frecuencia; origen; unidades; tipo de sensor; indicador de calidad; calibración; intervención y falla confirmada. Guardar datos brutos separados de variables derivadas y predicciones.

La altura actual se lee como señal entera `sensor_altura` y se expone como `altura_raw`, sin asumir metros o milímetros. Si la escena publica un flotante, cambiar el contrato y la lectura conjuntamente. Presencia ausente (`None`/`null`) significa dato no disponible; `0` significa ausencia observada.
