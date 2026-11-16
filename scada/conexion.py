"""Lectura de CoppeliaSim por ZeroMQ, independiente de la interfaz gráfica."""

import argparse
from dataclasses import asdict, dataclass
import json
import math
import sys
import time
from typing import Any


@dataclass(frozen=True)
class Telemetria:
    tiempo_simulacion_s: float
    presencia: int | None
    altura_raw: int | None
    estado_faja: Any


def leer_telemetria(sim: Any, conveyor: int) -> Telemetria:
    """Conserva None para señales ausentes; altura conserva el tipo del prototipo."""
    return Telemetria(
        sim.getSimulationTime(),
        sim.getInt32Signal("sensor_presencia"),
        sim.getInt32Signal("sensor_altura"),
        sim.readCustomTableData(conveyor, "__state__"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--puerto", type=int, default=23000)
    parser.add_argument("--faja", default="/conveyor")
    parser.add_argument("--intervalo", type=float, default=0.2)
    parser.add_argument("--timeout", type=float, default=5.0,
                        help="Espera máxima por operación de red, en segundos.")
    parser.add_argument("--muestras", type=int, help="Número de lecturas; omitir para lectura continua.")
    args = parser.parse_args()
    if not 1 <= args.puerto <= 65535:
        parser.error("--puerto debe estar entre 1 y 65535")
    if not math.isfinite(args.intervalo) or args.intervalo <= 0:
        parser.error("--intervalo debe ser positivo y finito")
    if not math.isfinite(args.timeout) or not 0 < args.timeout <= 3600:
        parser.error("--timeout debe ser positivo y como máximo 3600 segundos")
    if args.muestras is not None and args.muestras < 1:
        parser.error("--muestras debe ser mayor que cero")

    # Importar este módulo o pedir ayuda no inicia conexiones.
    import zmq
    from coppeliasim_zmqremoteapi_client import RemoteAPIClient

    client = RemoteAPIClient(host=args.host, port=args.puerto)
    # Cliente 2.0.4: recv() es bloqueante; limitar envío y recepción en el socket.
    client.socket.setsockopt(zmq.RCVTIMEO, max(1, round(args.timeout * 1000)))
    client.socket.setsockopt(zmq.SNDTIMEO, max(1, round(args.timeout * 1000)))
    client.socket.setsockopt(zmq.LINGER, 0)
    try:
        sim = client.require("sim")
        conveyor = sim.getObject(args.faja)
        print("Conexión con CoppeliaSim establecida", file=sys.stderr)
        contador = 0
        while args.muestras is None or contador < args.muestras:
            print(json.dumps(asdict(leer_telemetria(sim, conveyor)), ensure_ascii=False), flush=True)
            contador += 1
            if args.muestras is None or contador < args.muestras:
                time.sleep(args.intervalo)
    except KeyboardInterrupt:
        print("Lectura finalizada", file=sys.stderr)
        return 0
    except zmq.Again:
        print("Tiempo de espera agotado. Verifica CoppeliaSim, el servidor ZeroMQ, host y puerto.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"No se pudo leer CoppeliaSim: {exc}", file=sys.stderr)
        return 1
    finally:
        client.socket.close(linger=0)
        client.context.term()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
