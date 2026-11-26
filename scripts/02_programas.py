# -*- coding: utf-8 -*-
"""02_programas.py
Figura:    Maestrantes preinscritos por programa de maestría
Tipo:      barras horizontales
Datos:     datos/02_programas.csv
Resultado: resultados/02_programas.png
Uso:       python scripts/02_programas.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "02_programas.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "02_programas.png")

programas = [r["programa"].replace("Maestría en ", "", 1) for r in tabla]
valores = [int(r["maestrantes"]) for r in tabla]
ruta = g.barras_horizontales(programas, valores, salida, eje="Número de maestrantes")

print("listo:", os.path.relpath(ruta, RAIZ))
