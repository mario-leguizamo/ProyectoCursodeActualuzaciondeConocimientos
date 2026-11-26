# -*- coding: utf-8 -*-
"""05_distancia_por_aula.py
Figura:    Años transcurridos entre la conclusión de los estudios y la reincorporación con el Curso, por aula virtual
Tipo:      cajas y bigotes
Datos:     datos/05_distancia_por_aula.csv
Resultado: resultados/05_distancia_por_aula.png
Uso:       python scripts/05_distancia_por_aula.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "05_distancia_por_aula.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "05_distancia_por_aula.png")

# una lista de filas por aula virtual, en orden
aulas = {}
for r in tabla:
    aulas.setdefault((int(r["aula"]), r["aula_nombre"]), []).append(r)
aulas = sorted(aulas.items())

grupos = [(f"Aula {n}", nombre, [int(r["anios_desde_conclusion"]) for r in filas]) for (n, nombre), filas in aulas]
ruta = g.cajas(grupos, salida, eje="Años transcurridos desde la conclusión de los estudios", unidad="años")

print("listo:", os.path.relpath(ruta, RAIZ))
