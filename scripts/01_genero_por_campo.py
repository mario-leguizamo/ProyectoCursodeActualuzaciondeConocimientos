# -*- coding: utf-8 -*-
"""01_genero_por_campo.py
Figura:    Maestrantes preinscritos por género y campo del conocimiento
Tipo:      pirámide
Datos:     datos/01_genero_por_campo.csv
Resultado: resultados/01_genero_por_campo.png
Uso:       python scripts/01_genero_por_campo.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "01_genero_por_campo.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "01_genero_por_campo.png")

filas = [(r["campo"], int(r["mujeres"]), int(r["hombres"])) for r in tabla]
ruta = g.piramide(filas, salida, nombres=("mujeres", "hombres"), eje="Número de maestrantes")

print("listo:", os.path.relpath(ruta, RAIZ))
