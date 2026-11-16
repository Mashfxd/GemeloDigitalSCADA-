"""Muestras sintéticas independientes; no representan degradación temporal."""

import argparse
import csv
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random


ESTADOS = ("Normal", "Alerta", "Falla")


@dataclass(frozen=True)
class MuestraSintetica:
    carga_kg: float
    temperatura_c: float
    vibracion_mm_s: float
    corriente_a: float
    velocidad_m_s: float
    estado: str


def generar_muestra(rng: random.Random, estado: str | None = None) -> MuestraSintetica:
    """Genera una muestra según distribuciones ilustrativas, sin calibración física."""
    if estado is None:
        estado = rng.choice(ESTADOS)
    if estado not in ESTADOS:
        raise ValueError(f"Estado desconocido: {estado}")

    if estado == "Normal":
        carga = rng.uniform(0.5, 3.0)
        temperatura = rng.gauss(38, 3)
        vibracion = rng.gauss(1.2, 0.25)
        corriente = 2.0 + 0.35 * carga + rng.gauss(0, 0.15)
        velocidad = rng.uniform(0.4, 0.5)
    elif estado == "Alerta":
        carga = rng.uniform(1.5, 4.0)
        temperatura = rng.gauss(55, 6)
        vibracion = rng.gauss(3.0, 0.9)
        corriente = 2.6 + 0.45 * carga + rng.gauss(0, 0.3)
        velocidad = rng.uniform(0.35, 0.49)
    else:
        carga = rng.uniform(2.0, 5.0)
        temperatura = rng.gauss(72, 9)
        vibracion = rng.gauss(5.0, 1.3)
        corriente = 3.0 + 0.6 * carga + rng.gauss(0, 0.45)
        velocidad = rng.uniform(0.25, 0.43)

    return MuestraSintetica(
        round(carga, 2), round(max(0, temperatura), 2),
        round(max(0, vibracion), 2), round(max(0, corriente), 2),
        round(velocidad, 2), estado,
    )


def exportar_csv(
    ruta: Path, cantidad: int, semilla: int = 42,
    estado: str | None = None, sobrescribir: bool = False,
) -> Path:
    """Exporta sin sobrescribir archivos existentes salvo petición explícita."""
    if cantidad < 1:
        raise ValueError("La cantidad debe ser mayor que cero.")
    if estado is not None and estado not in ESTADOS:
        raise ValueError(f"Estado desconocido: {estado}")
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(semilla)
    campos = ["muestra_id", "origen", *MuestraSintetica.__dataclass_fields__]
    with ruta.open("w" if sobrescribir else "x", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        for indice in range(cantidad):
            writer.writerow({
                "muestra_id": indice, "origen": "sintetico",
                **asdict(generar_muestra(rng, estado)),
            })
    return ruta


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--muestras", type=int, default=1)
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--estado", choices=ESTADOS)
    parser.add_argument("--salida", type=Path, help="Ruta CSV; sin ella imprime las muestras.")
    parser.add_argument("--sobrescribir", action="store_true")
    args = parser.parse_args()
    if args.muestras < 1:
        parser.error("--muestras debe ser mayor que cero")
    if args.sobrescribir and args.salida is None:
        parser.error("--sobrescribir requiere --salida")
    if args.salida:
        try:
            ruta = exportar_csv(args.salida, args.muestras, args.semilla,
                                args.estado, args.sobrescribir)
        except (OSError, ValueError) as exc:
            parser.exit(1, f"No se pudo exportar: {exc}\n")
        print(f"Guardadas {args.muestras} muestras sintéticas en {ruta}")
    else:
        rng = random.Random(args.semilla)
        for _ in range(args.muestras):
            print(json.dumps(asdict(generar_muestra(rng, args.estado)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
