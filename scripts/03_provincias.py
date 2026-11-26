# -*- coding: utf-8 -*-
"""03_provincias.py
Figura:    Maestrantes preinscritos por provincia de residencia
Tipo:      barras horizontales
Datos:     datos/03_provincias.csv
Resultado: resultados/03_provincias.png
Uso:       python scripts/03_provincias.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "03_provincias.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "03_provincias.png")

filas = [(r["provincia"], int(r["maestrantes"])) for r in tabla]

# las provincias con un solo maestrante se agrupan en una barra
LETRAS = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve"}
unas = [p for p, v in filas if v == 1]
if len(unas) >= 3:
    filas = [x for x in filas if x[1] > 1] + [(f"Otras {LETRAS.get(len(unas), len(unas))} provincias", len(unas))]

ruta = g.barras_horizontales([p for p, _ in filas], [v for _, v in filas], salida, eje="Número de maestrantes", ordenar=False)

print("listo:", os.path.relpath(ruta, RAIZ))
