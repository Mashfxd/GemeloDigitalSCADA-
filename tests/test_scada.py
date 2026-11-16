"""Pruebas de contratos sin escena ni interfaz gráfica."""

import csv
from dataclasses import asdict
import importlib
import io
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

from scada.conexion import leer_telemetria
from scada.generador import ESTADOS, exportar_csv, generar_muestra


ROOT = Path(__file__).resolve().parents[1]


class PruebasGenerador(unittest.TestCase):
    def test_semilla_reproduce_las_muestras(self):
        uno, dos = random.Random(42), random.Random(42)
        self.assertEqual([generar_muestra(uno) for _ in range(30)],
                         [generar_muestra(dos) for _ in range(30)])

    def test_escenario_solicitado_y_magnitudes_no_negativas(self):
        rng = random.Random(12)
        for estado in ESTADOS:
            for _ in range(100):
                muestra = generar_muestra(rng, estado)
                self.assertEqual(muestra.estado, estado)
                for nombre, valor in asdict(muestra).items():
                    if nombre != "estado":
                        self.assertGreaterEqual(valor, 0)

    def test_estado_invalido(self):
        with self.assertRaises(ValueError):
            generar_muestra(random.Random(1), "desconocido")

    def test_csv_reproducible_con_origen_y_unidades(self):
        with tempfile.TemporaryDirectory() as carpeta:
            primera = exportar_csv(Path(carpeta) / "a.csv", 12, semilla=9)
            segunda = exportar_csv(Path(carpeta) / "b.csv", 12, semilla=9)
            self.assertEqual(primera.read_bytes(), segunda.read_bytes())
            with primera.open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas), 12)
            self.assertEqual([int(f["muestra_id"]) for f in filas], list(range(12)))
            self.assertTrue(all(f["origen"] == "sintetico" for f in filas))
            self.assertIn("temperatura_c", filas[0])

    def test_no_sobrescribe_por_defecto(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.csv"
            ruta.write_text("datos anteriores", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                exportar_csv(ruta, 3)
            self.assertEqual(ruta.read_text(encoding="utf-8"), "datos anteriores")
            exportar_csv(ruta, 3, sobrescribir=True)
            self.assertIn("sintetico", ruta.read_text(encoding="utf-8"))

    def test_cantidad_invalida_no_crea_archivo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.csv"
            with self.assertRaises(ValueError):
                exportar_csv(ruta, 0)
            self.assertFalse(ruta.exists())


class PruebasTelemetria(unittest.TestCase):
    def simulado(self, presencia):
        sim = Mock()
        sim.getSimulationTime.return_value = 3.5
        sim.getInt32Signal.side_effect = lambda nombre: presencia if nombre == "sensor_presencia" else None
        sim.readCustomTableData.return_value = {"vel": 0.4}
        return sim

    def test_no_confunde_ausencia_de_senal_con_cero(self):
        self.assertIsNone(leer_telemetria(self.simulado(None), 5).presencia)
        self.assertEqual(leer_telemetria(self.simulado(0), 5).presencia, 0)
        self.assertEqual(leer_telemetria(self.simulado(1), 5).presencia, 1)

    def test_conserva_tiempo_altura_y_estado_sin_inventar_unidades(self):
        sim = self.simulado(1)
        muestra = leer_telemetria(sim, 5)
        self.assertEqual(muestra.tiempo_simulacion_s, 3.5)
        self.assertIsNone(muestra.altura_raw)
        self.assertEqual(muestra.estado_faja, {"vel": 0.4})
        sim.readCustomTableData.assert_called_once_with(5, "__state__")

    def test_error_remoto_no_se_convierte_en_telemetria_valida(self):
        sim = self.simulado(0)
        sim.getSimulationTime.side_effect = RuntimeError("desconectado")
        with self.assertRaises(RuntimeError):
            leer_telemetria(sim, 5)


class PruebasEntradas(unittest.TestCase):
    def test_importaciones_sin_ventanas_conexiones_o_salida(self):
        codigo = (
            "import sys; import dashboard_scada, conexion_Coppelia, generador_datos; "
            "assert 'customtkinter' not in sys.modules; "
            "assert 'coppeliasim_zmqremoteapi_client' not in sys.modules"
        )
        resultado = subprocess.run([sys.executable, "-c", codigo], cwd=ROOT,
                                   capture_output=True, text=True, timeout=30)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stdout, "")
        self.assertEqual(resultado.stderr, "")

    def test_cli_generador_rechaza_cantidad_invalida(self):
        modulo = importlib.import_module("scada.generador")
        with patch.object(sys, "argv", ["generador", "--muestras", "0"]):
            with patch("sys.stderr", new_callable=io.StringIO):
                with self.assertRaises(SystemExit) as error:
                    modulo.main()
        self.assertEqual(error.exception.code, 2)

    def test_cli_conexion_rechaza_intervalos_invalidos(self):
        modulo = importlib.import_module("scada.conexion")
        for valor in ["0", "-1", "nan", "inf"]:
            with self.subTest(valor=valor):
                with patch.object(sys, "argv", ["conexion", "--intervalo", valor]):
                    with patch("sys.stderr", new_callable=io.StringIO):
                        with self.assertRaises(SystemExit) as error:
                            modulo.main()
                self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
