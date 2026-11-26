# -*- coding: utf-8 -*-
"""graficos_base.py: gráficos estadísticos con un solo estilo, listos para reutilizar.

Origen: son los gráficos del Proyecto del Curso de Actualización de Conocimientos (UTN, Facultad de Posgrado,
noviembre de 2026), pasados a funciones generales: reciben los datos ya contados y devuelven un PNG.

Estilo: ggplot2 sobre fondo oscuro, degradado azul-violeta-rosa-naranja-rojo, 15 cm de ancho y 300 ppp
(tamaño real para una hoja A4 vertical), letra de 9 a 12 puntos, decimales con coma.

Tipos de gráfico (una función por tipo):
    barras_horizontales   ranking de categorías con valor y porcentaje
    barras_verticales     serie corta (años, niveles, etapas)
    barras_detalle        pocas barras, cada una con título y una línea de detalle
    barras_apiladas       composición de cada grupo por categorías, con leyenda
    barras_referencia     valores con degradado frente a una línea de referencia (meta, costo)
    piramide              dos series enfrentadas (mujeres y hombres, antes y después) por categoría
    cajas                 cajas y bigotes por grupo, con cada observación como punto
    mapa_calor            cruce de dos variables; el color y el número de cada celda son el valor

Todas aceptan, de forma opcional: titulo, subtitulo y fuente (se escriben dentro de la imagen) y alto (en cm).
En un documento con normas APA el título y la nota van fuera de la imagen: en ese caso no se pasan.

Uso rápido:
    import graficos_base as g
    g.barras_horizontales(["Imbabura", "Carchi", "Pichincha"], [61, 14, 9], "provincias.png", eje="Número de personas")

Ver todos los tipos con datos de ejemplo:
    python graficos_base.py            (crea la carpeta "ejemplos")

Requiere: Python 3.9 o superior, matplotlib y numpy  (pip install matplotlib numpy)
"""
import os, textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, PowerNorm, to_rgb
from matplotlib.ticker import MaxNLocator, FuncFormatter
from matplotlib.patches import Patch, FancyBboxPatch

# ------------------------------------------------------------------------------------------------ estilo
# Para cambiar la apariencia de TODOS los gráficos se cambian solo estas líneas.
FONDO, PANEL, REJA, TXT, SUB = "#0b1020", "#121a30", "#2a3759", "#f2f4f8", "#aab5d0"
TXT2 = "#8fd0ff"                   # celeste: segundo color de texto, para alternar filas y columnas en el mapa de calor
RAMPA = LinearSegmentedColormap.from_list("base", ["#3d5af1", "#7a5cd6", "#c45aa8", "#ff8a3d", "#ff3b30"])   # degradado principal
RAMPA_A = LinearSegmentedColormap.from_list("a", ["#c45aa8", "#ff8a3d", "#ffb347"])                          # serie izquierda de la pirámide
RAMPA_B = LinearSegmentedColormap.from_list("b", ["#7a5cd6", "#3d5af1", "#39a0f2"])                          # serie derecha de la pirámide
PALETA = ["#3d5af1", "#ff8a3d", "#2ec4b6", "#39d5f2", "#7a5cd6", "#ff3b30", "#c45aa8", "#f6c945", "#8bd450", "#6b7690"]   # categorías
ANCHO = 15.0                       # cm: ancho útil de una hoja A4 vertical con márgenes de 4 y 3 cm
PPP = 300                          # puntos por pulgada del PNG
CM = 1 / 2.54
DECIMALES = 1                      # decimales de los valores que no son enteros

_disp = {f.name for f in font_manager.fontManager.ttflist}
LETRA = next((f for f in ("Arial", "Liberation Sans", "DejaVu Sans") if f in _disp), "DejaVu Sans")
plt.rcParams.update({"font.family": LETRA, "font.size": 9.5, "text.color": TXT,
                     "axes.labelcolor": SUB, "xtick.color": SUB, "ytick.color": SUB})


# ------------------------------------------------------------------------------------------------ utilidades
def num(v, k=None):
    """Número con formato en español: 1.234 y 3,5."""
    k = DECIMALES if k is None else k
    if abs(v - round(v)) < 1e-9: return f"{int(round(v)):,}".replace(",", ".")
    return f"{v:,.{k}f}".replace(",", "§").replace(".", ",").replace("§", ".")

def pct(n, d):
    return (f"{100 * n / d:.1f}".replace(".", ",") + " %") if d else "0 %"

def _env(texto, n):
    return "\n".join(textwrap.wrap(str(texto), n)) or str(texto)

def _largo(textos):
    return max((len(l) for t in textos for l in str(t).split("\n")), default=0)

def _enteros(valores):
    return all(abs(v - round(v)) < 1e-9 for v in valores)

def _colores(n, inv=False):
    if n == 1: return [RAMPA(0.9)]
    cs = [RAMPA(i / (n - 1)) for i in range(n)]
    return cs[::-1] if inv else cs

def _lienzo(alto, izq, der=0.45, inf=1.15, sup=0.40, titulo=None, subtitulo=None, fuente=None):
    """Figura de ANCHO cm; el panel mide `alto` cm con sus márgenes (izq, der, inf, sup) en centímetros.
    Si hay título, subtítulo o fuente, la imagen crece lo necesario: el panel no se achica."""
    lt = textwrap.wrap(titulo, 62) if titulo else []
    ls = textwrap.wrap(subtitulo, 88) if subtitulo else []
    ex_s = (0.52 * len(lt) + 0.42 if lt else 0) + (0.43 * len(ls) + (0.12 if lt else 0.42) if ls else 0)
    ex_i = 0.55 if fuente else 0
    H = alto + ex_s + ex_i
    fig = plt.figure(figsize=(ANCHO * CM, H * CM), facecolor=FONDO)
    ax = fig.add_axes([izq / ANCHO, (inf + ex_i) / H, (ANCHO - izq - der) / ANCHO, (alto - inf - sup) / H], facecolor=PANEL)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0, labelsize=9, colors=SUB, pad=5)
    ax.set_axisbelow(True)
    y = 0.62
    for l in lt:
        fig.text(0.45 / ANCHO, 1 - y / H, l, fontsize=12.5, fontweight="bold", color=TXT, ha="left", va="baseline"); y += 0.52
    if lt: y += 0.02
    for l in ls:
        fig.text(0.45 / ANCHO, 1 - y / H, l, fontsize=9.5, color=SUB, ha="left", va="baseline"); y += 0.43
    if fuente: fig.text(0.45 / ANCHO, 0.24 / H, fuente, fontsize=8, color=SUB, ha="left", va="bottom")
    fig._geo = dict(H=H, ex_s=ex_s, ex_i=ex_i)                      # para ubicar elementos fuera del panel
    return fig, ax

def _guardar(fig, ruta):
    carpeta = os.path.dirname(os.path.abspath(ruta))
    os.makedirs(carpeta, exist_ok=True)
    fig.savefig(ruta, dpi=PPP, facecolor=FONDO); plt.close(fig)
    return ruta

def _degradado(ax, x0, x1, y, grosor, cmap, vmax, z=3):
    """Barra horizontal con relleno continuo: el color avanza con el valor (como scale_fill_gradient de ggplot2)."""
    if x0 == x1: return
    g = np.linspace(0, abs(x1 - x0) / vmax, 256).reshape(1, -1)
    if x1 < x0: g = g[:, ::-1]; x0, x1 = x1, x0
    ax.imshow(g, extent=[x0, x1, y + grosor / 2, y - grosor / 2], aspect="auto", cmap=cmap, vmin=0, vmax=1, zorder=z, interpolation="bilinear")

def _eje_x(ax, valores, eje, holgura):
    ax.set_xlim(0, max(valores) * holgura)
    ax.grid(axis="x", color=REJA, lw=0.7); ax.grid(axis="y", visible=False)
    ax.xaxis.set_major_locator(MaxNLocator(integer=_enteros(valores), nbins=6))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: num(v)))
    ax.set_xlabel(eje, fontsize=9, labelpad=6)

def _rotulos(ax, filas, tr, ancho=28):
    """Nombre en negrita y, debajo, una línea de detalle, a la izquierda de cada fila."""
    for i, (nombre, detalle) in enumerate(filas):
        d = _env(detalle, ancho) if detalle else ""; dos = "\n" in d
        if not d:
            ax.text(-0.035, i, nombre, transform=tr, ha="right", va="center", fontsize=10.5, fontweight="bold", color=TXT); continue
        ax.text(-0.035, i - (0.27 if dos else 0.15), nombre, transform=tr, ha="right", va="center", fontsize=10.5, fontweight="bold", color=TXT)
        ax.text(-0.035, i + (0.15 if dos else 0.17), d, transform=tr, ha="right", va="center", fontsize=8.8, color=SUB, linespacing=1.0)

def _margen_rotulos(filas, ancho=28):
    nombres = [n for n, _ in filas]; detalles = [_env(d, ancho) for _, d in filas if d]
    return min(7.0, max(2.6, 0.75 + max(0.205 * _largo(nombres), 0.158 * _largo(detalles))))

def _texto_sobre(color):
    r, g, b = to_rgb(color)
    return "#10131c" if 0.299 * r + 0.587 * g + 0.114 * b > 0.62 else "white"


# ------------------------------------------------------------------------------------------------ gráficos
def barras_horizontales(etiquetas, valores, ruta, eje="Cantidad", porcentaje=True, ordenar=True, envolver=40, alto=None,
                        titulo=None, subtitulo=None, fuente=None):
    """Ranking de categorías. etiquetas y valores van en el mismo orden; si ordenar=True, la mayor queda arriba."""
    pares = list(zip(etiquetas, valores))
    if ordenar: pares.sort(key=lambda x: -x[1])
    et = [_env(e, envolver) for e, _ in pares]; v = [x for _, x in pares]; total = sum(v); n = len(v)
    paso = max(0.74, 0.31 * max(e.count("\n") + 1 for e in et))                    # filas más altas si la etiqueta ocupa tres líneas o más
    alto = alto or min(17.5, max(4.6, paso * n + 1.7))
    fig, ax = _lienzo(alto, izq=min(7.0, max(2.2, 0.6 + 0.158 * _largo(et))), titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    y = list(range(n))
    ax.barh(y, v, color=_colores(n, inv=True), height=0.62, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(et, color=TXT, fontsize=8.8 if _largo(et) > 26 else 9.5, linespacing=1.0)
    ax.set_ylim(n - 0.42, -0.58)
    for i, x in enumerate(v):
        ax.annotate(num(x), (x, i), xytext=(5, 0), textcoords="offset points", va="center", ha="left", fontsize=10.5, fontweight="bold", color=TXT)
        if porcentaje:
            ax.annotate(f"({pct(x, total)})", (x, i), xytext=(5 + 7.5 * len(num(x)) + 3, 0), textcoords="offset points", va="center", ha="left", fontsize=9, color=SUB)
    _eje_x(ax, v, eje, 1.34 if porcentaje else 1.16)
    return _guardar(fig, ruta)


def barras_verticales(etiquetas, valores, ruta, eje="Cantidad", eje_x=None, porcentaje=True, alto=7.4,
                      titulo=None, subtitulo=None, fuente=None):
    """Serie corta en su orden natural (años, niveles, etapas). El color avanza de izquierda a derecha."""
    et = [str(e) for e in etiquetas]; v = list(valores); total = sum(v); n = len(v)
    fig, ax = _lienzo(alto, izq=1.75, inf=1.30 if eje_x else 1.15, titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    x = list(range(n)); tam = 10 if n <= 10 else 8.6
    ax.bar(x, v, color=_colores(n), width=0.60, zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(et, color=TXT, fontsize=tam, linespacing=1.05)
    if not any("\n" in e for e in et):                                  # etiquetas de una línea: todas sobre la misma línea base
        ax.tick_params(axis="x", pad=5 + 0.74 * tam)
        for t in ax.get_xticklabels(): t.set_va("baseline")
    ax.set_xlim(-0.65, n - 0.35)
    ax.grid(axis="y", color=REJA, lw=0.7); ax.grid(axis="x", visible=False)
    for i, y in enumerate(v):
        ax.annotate(num(y), (i, y), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=12, fontweight="bold", color=TXT)
        if porcentaje:
            ax.annotate(pct(y, total), (i, y), xytext=(0, 18), textcoords="offset points", ha="center", va="bottom", fontsize=9, color=SUB)
    ax.set_ylim(0, max(v) * (1.24 if porcentaje else 1.14))
    ax.yaxis.set_major_locator(MaxNLocator(integer=_enteros(v), nbins=6)); ax.yaxis.set_major_formatter(FuncFormatter(lambda t, _: num(t)))
    ax.set_ylabel(eje, fontsize=9, labelpad=6)
    if eje_x: ax.set_xlabel(eje_x, fontsize=9, labelpad=6)
    return _guardar(fig, ruta)


def barras_detalle(barras, ruta, eje="Cantidad", porcentaje=True, alto=None, titulo=None, subtitulo=None, fuente=None):
    """Pocas barras con explicación. barras = [(nombre, detalle, valor), ...]; el detalle puede ser ""."""
    filas = [(b[0], b[1]) for b in barras]; v = [b[2] for b in barras]; total = sum(v); n = len(v)
    alto = alto or 1.55 * n + 1.55
    fig, ax = _lienzo(alto, izq=_margen_rotulos(filas, 36), titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    col = _colores(n)
    for i, x in enumerate(v):
        ax.barh(i, x, color=col[i], height=0.54, zorder=3)
        ax.annotate(num(x), (x, i), xytext=(6, 0), textcoords="offset points", va="center", ha="left", fontsize=12, fontweight="bold", color=TXT)
        if porcentaje:
            ax.annotate(f"({pct(x, total)})", (x, i), xytext=(6 + 8.6 * len(num(x)) + 3, 0), textcoords="offset points", va="center", ha="left", fontsize=9.5, color=SUB)
    _rotulos(ax, filas, ax.get_yaxis_transform(), 36)
    ax.set_yticks([]); ax.set_ylim(n - 0.45, -0.55)
    _eje_x(ax, v, eje, 1.42 if porcentaje else 1.18)
    return _guardar(fig, ruta)


def barras_apiladas(filas, ruta, eje="Cantidad", colores=None, alto=None, titulo=None, subtitulo=None, fuente=None):
    """Composición de cada grupo. filas = [(nombre, detalle, {categoria: valor, ...}), ...].
    colores (opcional) = {categoria: "#rrggbb"}; si no se indica, se toman de PALETA en orden de aparición."""
    cats = []
    for _, _, d in filas:
        for c in d:
            if c not in cats: cats.append(c)
    col = dict(colores or {})
    for i, c in enumerate(c for c in cats if c not in col): col[c] = PALETA[i % len(PALETA)]
    rot = [(f[0], f[1]) for f in filas]; n = len(filas)
    inf = 1.45 + 0.47 * (-(-len(cats) // 2))
    alto = alto or 1.35 * n + inf + 0.4
    fig, ax = _lienzo(alto, izq=_margen_rotulos(rot), inf=inf, titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    tot = [sum(d.values()) for _, _, d in filas]; mx = max(tot)
    for i, (_, _, d) in enumerate(filas):
        x0 = 0
        for c, v in d.items():
            ax.barh(i, v, left=x0, height=0.56, color=col[c], edgecolor=PANEL, linewidth=1.2, zorder=3)
            if v >= mx * 0.07:
                ax.text(x0 + v / 2, i, num(v), ha="center", va="center_baseline", fontsize=9.5, fontweight="bold", color=_texto_sobre(col[c]), zorder=4)
            x0 += v
        ax.annotate(num(x0), (x0, i), xytext=(6, 0), textcoords="offset points", va="center", fontsize=11, fontweight="bold", color=TXT)
    _rotulos(ax, rot, ax.get_yaxis_transform())
    ax.set_yticks([]); ax.set_ylim(n - 0.45, -0.55)
    _eje_x(ax, tot, eje, 1.16)
    g = fig._geo
    fig.legend(handles=[Patch(facecolor=col[c], edgecolor="none", label=c) for c in cats], loc="lower center",
               bbox_to_anchor=(0.5, (0.05 + g["ex_i"]) / g["H"]), ncol=2, frameon=False, fontsize=8.6, labelcolor=TXT,
               handlelength=1.1, handleheight=0.9, columnspacing=1.6, labelspacing=0.55)
    return _guardar(fig, ruta)


def barras_referencia(filas, ruta, referencia, etiqueta_referencia="Referencia", eje="Valor", diferencia=None, notas=None, alto=None,
                      titulo=None, subtitulo=None, fuente=None):
    """Valores (barras con degradado) frente a una línea de referencia (meta, costo, promedio).
    filas = [(nombre, detalle, valor), ...]. Si diferencia="Saldo", escribe dentro de la barra el tramo que supera la referencia.
    notas (opcional) = un texto corto por fila, que se escribe debajo del valor."""
    rot = [(f[0], f[1]) for f in filas]; v = [f[2] for f in filas]; n = len(v)
    alto = alto or 1.38 * n + 2.35
    fig, ax = _lienzo(alto, izq=_margen_rotulos(rot, 24), der=0.5, inf=1.15, sup=0.95, titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    mx = max(max(v), referencia); tope = mx * (1.50 if notas else 1.32)
    for i, x in enumerate(v):
        _degradado(ax, 0, x, i, 0.56, RAMPA, mx)
        ax.annotate(num(x), (x, i), xytext=(6, 5.5 if notas else 0), textcoords="offset points", va="center", ha="left", fontsize=11, fontweight="bold", color=TXT)
        if notas: ax.annotate(notas[i], (x, i), xytext=(6, -7), textcoords="offset points", va="center", ha="left", fontsize=8.4, color=SUB)
        tramo = x - referencia
        if diferencia and tramo > tope * 0.21:
            ax.text(referencia + tramo / 2, i, f"{diferencia} {num(tramo)}", ha="center", va="center_baseline", fontsize=9, fontweight="bold", color="white", zorder=6)
    ax.set_xlim(0, tope); ax.set_ylim(n - 0.45, -0.55); ax.set_aspect("auto")
    _rotulos(ax, rot, ax.get_yaxis_transform(), 24)
    ax.axvline(referencia, color="white", lw=1.3, zorder=5)
    ax.annotate(f"{etiqueta_referencia}: {num(referencia)}", (referencia, -0.55), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                fontsize=9, color=TXT, annotation_clip=False)
    ax.set_yticks([]); ax.grid(axis="x", color=REJA, lw=0.7)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda t, _: num(t))); ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.set_xlabel(eje, fontsize=9, labelpad=6)
    return _guardar(fig, ruta)


def piramide(filas, ruta, nombres=("mujeres", "hombres"), eje="Cantidad", alto=None, titulo=None, subtitulo=None, fuente=None):
    """Dos series enfrentadas por categoría, con los totales arriba. filas = [(categoria, valor_izquierda, valor_derecha), ...]."""
    n = len(filas); ta = sum(f[1] for f in filas); tb = sum(f[2] for f in filas); tot = ta + tb
    alto = alto or 0.95 * n + 3.4
    izq, der, inf, sup = 0.5, 0.5, 1.15, 2.25
    fig, ax = _lienzo(alto, izq=izq, der=der, inf=inf, sup=sup, titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    g = fig._geo; H = g["H"]
    vmax = max(max(a, b) for _, a, b in filas)
    L = 1.26 * vmax / (1 - 5.5 / (ANCHO - izq - der)); hueco = L - 1.26 * vmax        # hueco central (5,5 cm) para el nombre de la categoría
    marcas = [t for t in MaxNLocator(integer=True, nbins=4).tick_values(0, vmax) if 0 <= t <= vmax * 1.2]
    for t in marcas:
        for s in (-1, 1): ax.axvline(s * (hueco + t), color=REJA, lw=0.7, zorder=1)
    for i, (k, a, b) in enumerate(filas):
        _degradado(ax, -hueco, -hueco - a, i, 0.58, RAMPA_A, vmax); _degradado(ax, hueco, hueco + b, i, 0.58, RAMPA_B, vmax)
        ax.text(0, i, _env(k, 34), ha="center", va="center", fontsize=8.8, color=TXT, linespacing=1.0)
        ax.annotate(num(a), (-hueco - a, i), xytext=(-5, 0), textcoords="offset points", ha="right", va="center", fontsize=10.5, fontweight="bold", color=TXT if a else SUB)
        ax.annotate(num(b), (hueco + b, i), xytext=(5, 0), textcoords="offset points", ha="left", va="center", fontsize=10.5, fontweight="bold", color=TXT if b else SUB)
    ax.set_xlim(-L, L); ax.set_ylim(n - 0.42, -0.58); ax.set_yticks([]); ax.set_aspect("auto")
    ax.set_xticks([s * (hueco + t) for s in (-1, 1) for t in marcas]); ax.set_xticklabels([num(t) for _ in (-1, 1) for t in marcas])
    fig.text(0.5, (0.26 + g["ex_i"]) / H, eje, ha="center", va="bottom", fontsize=9, color=SUB)
    yb = 1 - (1.02 + g["ex_s"]) / H                                                    # banda superior: totales y barra de proporción
    t1 = fig.text(izq / ANCHO, yb, num(ta), ha="left", va="baseline", fontsize=25, fontweight="bold", color="#ff9a52")
    t2 = fig.text(1 - der / ANCHO, yb, num(tb), ha="right", va="baseline", fontsize=25, fontweight="bold", color="#6b86ff")
    fig.canvas.draw(); px = fig.bbox.width
    fig.text(t1.get_window_extent().x1 / px + 0.012, yb, f"{nombres[0]} ({pct(ta, tot)})", ha="left", va="baseline", fontsize=11.5, color=TXT)
    fig.text(t2.get_window_extent().x0 / px - 0.012, yb, f"{nombres[1]} ({pct(tb, tot)})", ha="right", va="baseline", fontsize=11.5, color=TXT)
    ap = fig.add_axes([izq / ANCHO, 1 - (1.72 + g["ex_s"]) / H, (ANCHO - izq - der) / ANCHO, 0.34 / H]); ap.axis("off")
    if ta: _degradado(ap, ta - 0.004 * tot, 0, 0, 1, RAMPA_A, ta * 1.0)
    if tb: _degradado(ap, ta + 0.004 * tot, tot, 0, 1, RAMPA_B, tb * 1.0)
    ap.set_xlim(0, tot); ap.set_ylim(0.5, -0.5); ap.set_aspect("auto")
    return _guardar(fig, ruta)


def cajas(grupos, ruta, eje="Valor", unidad="", tope=None, mediana_general=True, alto=None, titulo=None, subtitulo=None, fuente=None):
    """Cajas y bigotes por grupo. grupos = [(nombre, detalle, [valores]), ...].
    La caja abarca el 50 % central; la línea blanca y el número son la mediana; los bigotes llegan a los valores extremos que no
    son atípicos (1,5 veces el rango intercuartílico); cada punto es una observación. Si se indica tope, los valores mayores
    se señalan con una flecha en lugar de alargar la escala."""
    rot = [(f"{g_[0]} (n = {len(g_[2])})", g_[1]) for g_ in grupos]; n = len(grupos)
    todos = [x for g_ in grupos for x in g_[2]]; ent = _enteros(todos)
    cj = []
    for _, _, vals in grupos:
        v = sorted(vals); q1, me, q3 = (float(x) for x in np.percentile(v, [25, 50, 75])); ric = q3 - q1
        cj.append(dict(v=v, q1=q1, me=me, q3=q3, bajo=min(x for x in v if x >= q1 - 1.5 * ric), alto=max(x for x in v if x <= q3 + 1.5 * ric)))
    mn, mx = min(todos), max(todos); x1 = tope if tope else mx + 0.07 * (mx - mn or 1)
    x0 = 0 if 0 <= mn <= 0.4 * mx else mn - 0.07 * (mx - mn or 1)
    alto = alto or 1.45 * n + 2.25
    fig, ax = _lienzo(alto, izq=_margen_rotulos(rot, 24), der=0.5, inf=1.2, sup=0.95, titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    azar = np.random.default_rng(7); mes = [c["me"] for c in cj]; lo, hi = min(mes), max(mes); u = f" {unidad}" if unidad else ""
    for i, c in enumerate(cj):
        col = RAMPA(0.12 + 0.76 * ((c["me"] - lo) / (hi - lo) if hi > lo else 0.5))       # el color avanza con la mediana del grupo
        ax.plot([c["bajo"], c["alto"]], [i, i], color=SUB, lw=1.3, zorder=3)
        for x in (c["bajo"], c["alto"]): ax.plot([x, x], [i - 0.13, i + 0.13], color=SUB, lw=1.3, zorder=3)
        ax.add_patch(FancyBboxPatch((c["q1"], i - 0.25), max(c["q3"] - c["q1"], 1e-6), 0.50, boxstyle="round,pad=0,rounding_size=0.04",
                                    mutation_aspect=1, facecolor=col, edgecolor="none", alpha=0.92, zorder=4))
        if c["q3"] - c["q1"] < 0.01 * (x1 - x0): ax.plot([c["q1"], c["q1"]], [i - 0.25, i + 0.25], color=col, lw=3, zorder=4)
        ax.plot([c["me"], c["me"]], [i - 0.25, i + 0.25], color="white", lw=2.4, zorder=6, solid_capstyle="butt")
        dentro = [x for x in c["v"] if x <= x1]; dx = 0.16 if ent else 0
        ax.scatter([x + azar.uniform(-dx, dx) for x in dentro], [i + azar.uniform(-0.19, 0.19) for _ in dentro], s=13, color="white", alpha=0.62,
                   edgecolor=FONDO, linewidth=0.4, zorder=7)
        for x in [x for x in c["v"] if x > x1]:
            pos = x1 - 0.012 * (x1 - x0)
            ax.annotate(f"{num(x)}{u}", (pos, i), xytext=(-9, 0), textcoords="offset points", ha="right", va="center", fontsize=8.6, color=TXT, zorder=7)
            ax.scatter([pos], [i], marker=">", s=42, color="white", zorder=7)
        ax.annotate(num(c["me"]), (c["me"], i - 0.25), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=TXT, zorder=8)
    _rotulos(ax, rot, ax.get_yaxis_transform(), 24)
    if mediana_general:
        meg = float(np.median(todos))
        ax.axvline(meg, color="white", lw=0.9, ls=(0, (4, 3)), alpha=0.8, zorder=2)
        ax.annotate(f"Mediana general: {num(meg)}{u}", (meg, -0.55), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom", fontsize=9, color=TXT, annotation_clip=False)
    ax.set_yticks([]); ax.set_ylim(n - 0.45, -0.55); ax.set_xlim(x0, x1); ax.grid(axis="x", color=REJA, lw=0.7)
    ax.xaxis.set_major_locator(MaxNLocator(integer=ent, nbins=9)); ax.xaxis.set_major_formatter(FuncFormatter(lambda t, _: num(t)))
    ax.set_xlabel(eje, fontsize=9, labelpad=6)
    return _guardar(fig, ruta)


def mapa_calor(filas, columnas, matriz, ruta, eje="Cantidad", total=True, alto=None, titulo=None, subtitulo=None, fuente=None):
    """Cruce de dos variables. filas y columnas son las etiquetas; matriz[i][j] es el valor de la fila i en la columna j.
    El color y el número de cada celda son el valor; las celdas en cero quedan sin número. total=True añade la suma de cada fila.
    Los nombres de las filas, sus totales y los encabezados de las columnas alternan entre blanco y celeste."""
    et = [_env(f, 40) for f in filas]; nf, nc = len(filas), len(columnas)
    vmax = max(max(r) for r in matriz); norma = PowerNorm(0.55, vmin=0, vmax=vmax)       # escala no lineal: los valores bajos también se distinguen
    tono = lambda v: 0.08 + 0.92 * float(norma(v))
    alto = alto or min(19.5, max(0.78, 0.31 * max(e.count("\n") + 1 for e in et)) * nf + 2.0)
    izq = min(7.0, max(2.2, 0.6 + 0.158 * _largo(et)))
    fig, ax = _lienzo(alto, izq=izq, der=1.6 if total else 0.5, inf=1.25, sup=0.75, titulo=titulo, subtitulo=subtitulo, fuente=fuente)
    g = fig._geo; H = g["H"]
    ax.set_facecolor(FONDO); ax.grid(False)
    for i in range(nf):
        for j in range(nc):
            v = matriz[i][j]
            ax.add_patch(FancyBboxPatch((j - 0.45, i - 0.42), 0.90, 0.84, boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor=RAMPA(tono(v)) if v else "#1a2440", edgecolor="none", zorder=3))
            if v: ax.text(j, i, num(v), ha="center", va="center_baseline", fontsize=10, fontweight="bold", color="white", zorder=4)
        if total: ax.text(nc - 0.30, i, num(sum(matriz[i])), ha="left", va="center_baseline", fontsize=10.5, fontweight="bold", color=TXT2 if i % 2 else TXT, clip_on=False)
    ax.set_yticks(range(nf)); ax.set_yticklabels(et, color=TXT, fontsize=8.8, linespacing=1.0)
    ax.set_xticks(range(nc)); ax.set_xticklabels([_env(c, 12) for c in columnas], color=TXT, fontsize=8.4, linespacing=1.0)
    ax.xaxis.tick_top(); ax.tick_params(length=0, pad=4)
    for k, t in enumerate(ax.get_yticklabels()): t.set_color(TXT2 if k % 2 else TXT)          # filas y columnas alternan entre blanco y celeste,
    for k, t in enumerate(ax.get_xticklabels()): t.set_color(TXT2 if k % 2 else TXT)          # para seguir cada una con la vista
    ax.set_xlim(-0.55, nc - 0.45); ax.set_ylim(nf - 0.5, -0.5)
    if total: ax.annotate("Total", (1, 1), xycoords="axes fraction", xytext=(5, 6), textcoords="offset points", ha="left", va="bottom", fontsize=8.6, color=SUB, annotation_clip=False)
    cax = fig.add_axes([izq / ANCHO, (0.62 + g["ex_i"]) / H, 4.2 / ANCHO, 0.22 / H])                    # escala de color
    cax.imshow(np.linspace(0, 1, 256).reshape(1, -1), aspect="auto", cmap=RAMPA, extent=[0, 1, 0, 1]); cax.set_yticks([])
    marcas = sorted({t for t in MaxNLocator(integer=_enteros([vmax]), nbins=4).tick_values(0, vmax) if 0 < t and tono(t) <= tono(vmax) - 0.12} | {vmax})
    cax.set_xticks([tono(m) for m in marcas]); cax.set_xticklabels([num(m) for m in marcas], color=SUB, fontsize=8.5); cax.tick_params(length=0, pad=3)
    for s in cax.spines.values(): s.set_visible(False)
    fig.text((izq + 4.45) / ANCHO, (0.73 + g["ex_i"]) / H, eje, ha="left", va="center", fontsize=9, color=SUB)
    return _guardar(fig, ruta)


# ------------------------------------------------------------------------------------------------ ejemplos
def ejemplos(carpeta="ejemplos"):
    """Dibuja un ejemplo de cada tipo con DATOS INVENTADOS, solo para ver cómo queda cada gráfico."""
    f = "Datos de ejemplo, inventados para mostrar el tipo de gráfico."
    azar = np.random.default_rng(21)
    r = lambda nombre: os.path.join(carpeta, nombre)
    hechos = [
        barras_horizontales(["Cantón A", "Cantón B", "Cantón C", "Cantón D", "Cantón E", "Cantón F"], [48, 31, 22, 14, 9, 4], r("1_barras_horizontales.png"),
                            eje="Número de emprendimientos", titulo="barras_horizontales", subtitulo="Ranking de categorías con valor y porcentaje", fuente=f),
        barras_verticales([2020, 2021, 2022, 2023, 2024, 2025], [6, 11, 15, 24, 19, 27], r("2_barras_verticales.png"), eje="Número de proyectos",
                          titulo="barras_verticales", subtitulo="Serie corta en su orden natural", fuente=f),
        barras_detalle([("Grupo nuevo", "participa por primera vez", 47), ("Grupo que repite", "participó una vez antes", 39),
                        ("Grupo recurrente", "participó dos o más veces", 6)], r("3_barras_detalle.png"), eje="Número de personas",
                       titulo="barras_detalle", subtitulo="Pocas barras, cada una con su línea de explicación", fuente=f),
        barras_apiladas([("Zona 1", "sierra norte", {"Agricultura": 18, "Artesanía": 9, "Turismo": 6}),
                         ("Zona 2", "valle", {"Agricultura": 11, "Artesanía": 14, "Turismo": 3, "Servicios": 5}),
                         ("Zona 3", "frontera", {"Agricultura": 7, "Turismo": 12, "Servicios": 8})], r("4_barras_apiladas.png"),
                        eje="Número de organizaciones", titulo="barras_apiladas", subtitulo="Composición de cada grupo por categorías", fuente=f),
        barras_referencia([("Proyecto 1", "primer año", 18400), ("Proyecto 2", "primer año", 12750), ("Proyecto 3", "primer año", 9300), ("Proyecto 4", "primer año", 6100)],
                          r("5_barras_referencia.png"), referencia=5000, etiqueta_referencia="Costo de operación", eje="Dólares", diferencia="Saldo",
                          titulo="barras_referencia", subtitulo="Valores frente a una línea de referencia", fuente=f),
        piramide([("Educación", 14, 9), ("Salud", 11, 6), ("Administración", 8, 13), ("Ingeniería", 4, 15), ("Artes", 6, 6)], r("6_piramide.png"),
                 eje="Número de personas", titulo="piramide", subtitulo="Dos series enfrentadas por categoría, con los totales arriba", fuente=f),
        cajas([("T1", "testigo", list(np.round(azar.normal(38, 4.0, 18), 1))), ("T2", "dosis baja", list(np.round(azar.normal(43, 3.5, 18), 1))),
               ("T3", "dosis media", list(np.round(azar.normal(49, 5.0, 18), 1))), ("T4", "dosis alta", list(np.round(azar.normal(46, 6.0, 18), 1)))],
              r("7_cajas.png"), eje="Altura de la planta (cm)", unidad="cm", titulo="cajas", subtitulo="Cajas y bigotes por grupo; cada punto es una observación", fuente=f),
        mapa_calor(["Programa A", "Programa B", "Programa C", "Programa D", "Programa E"], [2021, 2022, 2023, 2024, 2025],
                   [[0, 2, 5, 12, 7], [1, 0, 3, 6, 9], [0, 1, 1, 4, 2], [2, 2, 0, 1, 3], [0, 0, 1, 0, 2]], r("8_mapa_calor.png"),
                   eje="Número de personas", titulo="mapa_calor", subtitulo="Cruce de dos variables: el color y el número son el valor", fuente=f),
    ]
    return hechos


if __name__ == "__main__":
    for ruta in ejemplos():
        print("listo:", ruta)
