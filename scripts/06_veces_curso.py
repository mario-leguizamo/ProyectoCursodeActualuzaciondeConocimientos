# -*- coding: utf-8 -*-
"""06_veces_curso.py
Figura:    Maestrantes preinscritos según las veces que han realizado el Curso
Tipo:      barras con detalle
Datos:     datos/06_veces_curso.csv
Resultado: resultados/06_veces_curso.png
Uso:       python scripts/06_veces_curso.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "06_veces_curso.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "06_veces_curso.png")

barras = [(r["categoria"], r["detalle"], int(r["maestrantes"])) for r in tabla]
ruta = g.barras_detalle(barras, salida, eje="Número de maestrantes")

print("listo:", os.path.relpath(ruta, RAIZ))
