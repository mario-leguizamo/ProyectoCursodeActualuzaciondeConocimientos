# Gráficos del Proyecto del Curso de Actualización de Conocimientos

Figuras del Proyecto del Curso de Actualización de Conocimientos, período enero-mayo de 2027
(GAC-FP-CACFP-2026-0002-INF), Facultad de Posgrado, Universidad Técnica del Norte.

Cada gráfico es independiente: tiene su propia tabla de datos, su propio script y su propio resultado, los tres con el mismo nombre.

```
datos/05_distancia_por_aula.csv  →  scripts/05_distancia_por_aula.py  →  resultados/05_distancia_por_aula.png
```

## Gráficos

| N.º | Nombre | Qué muestra | Tipo de gráfico |
|---|---|---|---|
| 01 | `01_genero_por_campo` | Maestrantes por género y campo del conocimiento | Pirámide |
| 02 | `02_programas` | Maestrantes por programa de maestría | Barras horizontales |
| 03 | `03_provincias` | Maestrantes por provincia de residencia | Barras horizontales |
| 04 | `04_anio_conclusion` | Maestrantes por año de conclusión de estudios | Barras verticales |
| 05 | `05_distancia_por_aula` | Años entre la conclusión de los estudios y la reincorporación con el Curso, por aula virtual | Cajas y bigotes |
| 06 | `06_veces_curso` | Maestrantes según las veces que han realizado el Curso | Barras con detalle |
| 07 | `07_programa_por_anio` | Programa de maestría y año de conclusión | Mapa de calor |
| 08 | `08_aulas_por_campo` | Conformación de las aulas virtuales por campo del conocimiento | Barras apiladas |
| 09 | `09_balance_por_aula` | Ingresos proyectados de cada aula virtual frente al costo de docencia | Barras con línea de referencia |

## Contenido

| Carpeta o archivo | Qué contiene |
|---|---|
| `datos/` | Una tabla por gráfico, con conteos y valores agregados. Corte: 24 de noviembre de 2026 (92 maestrantes preinscritos de 20 programas) |
| `scripts/` | Un script por gráfico. Cada uno lee su tabla y dibuja solo su figura |
| `resultados/` | Las nueve figuras en PNG (15 cm de ancho, 300 ppp) |
| `graficos_base.py` | El estilo común (colores, letra, tamaños) y los tipos de gráfico. Lo usan todos los scripts |

## Cómo volver a generar un gráfico

Requiere Python 3.9 o superior.

```
pip install matplotlib numpy
python scripts/05_distancia_por_aula.py
```

Cada script se ejecuta por separado y vuelve a crear únicamente su figura.
Para usar un gráfico en otro trabajo se copian su script y `graficos_base.py`, y se cambia la tabla de datos.

## Sobre los datos

- Las tablas salen del formulario de preinscripción en línea del Curso. Solo contienen conteos y valores agregados.
- No hay nombres, cédulas, teléfonos ni correos. La hoja de respuestas del formulario y las bases de datos del Curso no se guardan en este repositorio.
- `05_distancia_por_aula.csv` tiene una fila por maestrante, solo con su aula virtual y los años transcurridos desde que concluyó sus estudios.
- Las figuras usan las mismas cifras que el Proyecto. Están dibujadas con `graficos_base.py`, por lo que su disposición puede variar ligeramente respecto de las del documento.
