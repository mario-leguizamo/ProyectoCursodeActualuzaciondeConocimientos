# -*- coding: utf-8 -*-
"""07_programa_por_anio.py
Figura:    Programa de maestría y año de conclusión de estudios
Tipo:      mapa de calor
Datos:     datos/07_programa_por_anio.csv
Resultado: resultados/07_programa_por_anio.png
Uso:       python scripts/07_programa_por_anio.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "07_programa_por_anio.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "07_programa_por_anio.png")

anios = sorted({int(r["anio"]) for r in tabla})
valor = {(r["programa"], int(r["anio"])): int(r["maestrantes"]) for r in tabla}

# programas ordenados de mayor a menor número de maestrantes
total = {}
for (p, _), v in valor.items():
    total[p] = total.get(p, 0) + v
programas = sorted(total, key=lambda p: -total[p])

matriz = [[valor.get((p, a), 0) for a in anios] for p in programas]
ruta = g.mapa_calor([p.replace("Maestría en ", "", 1) for p in programas], anios, matriz, salida, eje="Número de maestrantes")

print("listo:", os.path.relpath(ruta, RAIZ))
