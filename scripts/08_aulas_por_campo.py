# -*- coding: utf-8 -*-
"""08_aulas_por_campo.py
Figura:    Conformación de las aulas virtuales por campo del conocimiento
Tipo:      barras apiladas
Datos:     datos/08_aulas_por_campo.csv
Resultado: resultados/08_aulas_por_campo.png
Uso:       python scripts/08_aulas_por_campo.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "08_aulas_por_campo.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "08_aulas_por_campo.png")

# una lista de filas por aula virtual, en orden
aulas = {}
for r in tabla:
    aulas.setdefault((int(r["aula"]), r["aula_nombre"]), []).append(r)
aulas = sorted(aulas.items())

COLOR_CAMPO = {"Servicios": "#3d5af1", "Educación": "#ff8a3d", "Salud": "#2ec4b6",
               "Tecnologías de la Información y la Comunicación": "#39d5f2", "Administración de Empresas y Derecho": "#7a5cd6",
               "Ingeniería, Industria y Construcción": "#ff3b30", "Ciencias Sociales, Periodismo e Información": "#c45aa8",
               "Artes y Humanidades": "#f6c945", "Investigación": "#8bd450"}

filas = [(f"Aula {n}", nombre, {r["campo"]: int(r["maestrantes"]) for r in fs}) for (n, nombre), fs in aulas]
ruta = g.barras_apiladas(filas, salida, eje="Número de maestrantes", colores=COLOR_CAMPO)

print("listo:", os.path.relpath(ruta, RAIZ))
