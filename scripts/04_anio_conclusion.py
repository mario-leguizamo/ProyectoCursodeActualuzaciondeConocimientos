# -*- coding: utf-8 -*-
"""04_anio_conclusion.py
Figura:    Maestrantes preinscritos por año de conclusión de estudios
Tipo:      barras verticales
Datos:     datos/04_anio_conclusion.csv
Resultado: resultados/04_anio_conclusion.png
Uso:       python scripts/04_anio_conclusion.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "04_anio_conclusion.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "04_anio_conclusion.png")

anios = [r["anio"] for r in tabla]
valores = [int(r["maestrantes"]) for r in tabla]
ruta = g.barras_verticales(anios, valores, salida, eje="Número de maestrantes")

print("listo:", os.path.relpath(ruta, RAIZ))
