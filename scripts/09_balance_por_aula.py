# -*- coding: utf-8 -*-
"""09_balance_por_aula.py
Figura:    Ingresos proyectados de cada aula virtual frente al costo de docencia
Tipo:      barras con línea de referencia
Datos:     datos/09_balance_por_aula.csv
Resultado: resultados/09_balance_por_aula.png
Uso:       python scripts/09_balance_por_aula.py

Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027. Corte: 24 de noviembre de 2026.
"""
import csv, os, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
import graficos_base as g

with open(os.path.join(RAIZ, "datos", "09_balance_por_aula.csv"), encoding="utf-8", newline="") as f:
    tabla = list(csv.DictReader(f))
salida = os.path.join(RAIZ, "resultados", "09_balance_por_aula.png")

costo = float(tabla[0]["costo_docencia"])                       # el costo de docencia es el mismo en todas las aulas
filas = [(f"Aula {r['aula']}", r["aula_nombre"], round(float(r["ingreso_proyectado"]))) for r in tabla]          # redondeado al dólar
notas = [f"beneficio-costo {g.num(float(r['ingreso_proyectado']) / costo, 2)}" for r in tabla]
ruta = g.barras_referencia(filas, salida, referencia=costo, etiqueta_referencia="Costo de docencia por aula", eje="Dólares",
                           diferencia="Saldo", notas=notas)

print("listo:", os.path.relpath(ruta, RAIZ))
