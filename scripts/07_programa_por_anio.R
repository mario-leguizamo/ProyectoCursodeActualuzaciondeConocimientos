# 07_programa_por_anio.R
# Mapa de calor: programa de maestria y anio de conclusion de estudios.
# Proyecto del Curso de Actualizacion de Conocimientos, periodo enero-mayo de 2027. Corte: 24 de noviembre de 2026.
# Datos: datos/07_programa_por_anio.csv (si no esta en la carpeta de trabajo, se lee del repositorio de GitHub).
if (!requireNamespace("ggplot2", quietly = TRUE)) install.packages("ggplot2", repos = "https://cloud.r-project.org")
library(ggplot2)

# 1. Datos
local <- "datos/07_programa_por_anio.csv"
github <- "https://raw.githubusercontent.com/mario-leguizamo/ProyectoCursodeActualuzaciondeConocimientos/main/datos/07_programa_por_anio.csv"
tabla <- read.csv(if (file.exists(local)) local else github, fileEncoding = "UTF-8", stringsAsFactors = FALSE)

anios <- sort(unique(tabla$anio))
total <- tapply(tabla$maestrantes, tabla$programa, sum)
programas <- unique(tabla$programa)
programas <- programas[order(-total[programas])]                 # de mayor a menor numero de maestrantes
nf <- length(programas); nc <- length(anios)

# una celda por cada programa y anio (las que no tienen maestrantes quedan en cero)
celdas <- expand.grid(fila = seq_len(nf), col = seq_len(nc))
celdas$valor <- 0
celdas$valor[(match(tabla$anio, anios) - 1) * nf + match(tabla$programa, programas)] <- tabla$maestrantes
celdas$id <- seq_len(nrow(celdas))
vmax <- max(celdas$valor)
tono <- function(v) 0.08 + 0.92 * (v / vmax)^0.55               # escala no lineal: los valores bajos tambien se distinguen
celdas$tono <- tono(celdas$valor)

# 2. Piezas del grafico
# celdas con esquinas redondeadas: cada una es un poligono (la fila 1 va arriba, por eso y = -fila)
redondeada <- function(id, xc, yc, ancho = 0.90, alto = 0.84, r = 0.07, n = 6) {
  ang <- seq(0, pi / 2, length.out = n)
  cx <- c(xc + ancho / 2 - r, xc - ancho / 2 + r, xc - ancho / 2 + r, xc + ancho / 2 - r)
  cy <- c(yc + alto / 2 - r, yc + alto / 2 - r, yc - alto / 2 + r, yc - alto / 2 + r)
  data.frame(id = id, x = unlist(lapply(1:4, function(k) cx[k] + r * cos(ang + (k - 1) * pi / 2))),
             y = unlist(lapply(1:4, function(k) cy[k] + r * sin(ang + (k - 1) * pi / 2))))
}
formas <- do.call(rbind, Map(redondeada, celdas$id, celdas$col, -celdas$fila))
formas$valor <- celdas$valor[formas$id]; formas$tono <- celdas$tono[formas$id]

# nombres, totales y anios: letra negra sobre fondo blanco, con una franja gris clara en filas y columnas alternas
negro <- "#111827"; franja <- "#e9ecf1"; oscuro <- "#0b1020"; gris <- "#aab5d0"
izq <- -7.0; der <- nc + 1.6                                     # borde izquierdo (nombres) y derecho (totales) de la figura
nombres <- data.frame(fila = seq_len(nf), texto = sapply(sub("^Maestr.a en ", "", programas), function(t) paste(strwrap(t, 42), collapse = "\n")))
totales <- data.frame(fila = seq_len(nf), texto = as.character(total[programas]))
cabecera <- data.frame(col = seq_len(nc), texto = as.character(anios))
filas_gris <- data.frame(fila = seq(2, nf, by = 2))
cols_gris <- data.frame(col = seq(2, nc, by = 2))

# escala de color, dibujada con franjas delgadas debajo del mapa (dentro de la zona oscura)
largo <- 2.9; x0 <- 0.6; y_escala <- -(nf + 0.95)
tiras <- data.frame(x = x0 + largo * (seq_len(300) - 1) / 300, tono = seq_len(300) / 300)
marcas <- pretty(c(0, vmax), 4); marcas <- unique(c(marcas[marcas > 0 & tono(marcas) <= tono(vmax) - 0.12], vmax))
rotulos <- data.frame(x = x0 + largo * tono(marcas), texto = as.character(marcas))
rampa <- c("#3d5af1", "#7a5cd6", "#c45aa8", "#ff8a3d", "#ff3b30")

# 3. Grafico
grafico <- ggplot() +
  # franjas grises: filas alternas (nombres y totales) y columnas alternas (anios)
  geom_rect(data = filas_gris, aes(xmin = izq, xmax = 0.5, ymin = -fila - 0.5, ymax = -fila + 0.5), fill = franja) +
  geom_rect(data = filas_gris, aes(xmin = nc + 0.5, xmax = der, ymin = -fila - 0.5, ymax = -fila + 0.5), fill = franja) +
  geom_rect(data = cols_gris, aes(xmin = col - 0.5, xmax = col + 0.5, ymin = -0.5, ymax = 0.35), fill = franja) +
  # zona oscura: el mapa de calor y, debajo, su escala de color
  annotate("rect", xmin = 0.5, xmax = nc + 0.5, ymin = -(nf + 2.0), ymax = -0.5, fill = oscuro) +
  geom_polygon(data = formas[formas$valor == 0, ], aes(x = x, y = y, group = id), fill = "#1a2440") +
  geom_polygon(data = formas[formas$valor > 0, ], aes(x = x, y = y, group = id, fill = tono)) +
  geom_text(data = celdas[celdas$valor > 0, ], aes(x = col, y = -fila, label = valor), colour = "white", fontface = "bold", size = 3.5) +
  geom_text(data = nombres, aes(x = 0.30, y = -fila, label = texto), colour = negro, size = 2.85, hjust = 1, lineheight = 0.82) +
  geom_text(data = totales, aes(x = nc + 1.05, y = -fila, label = texto), colour = negro, fontface = "bold", size = 3.7) +
  geom_text(data = cabecera, aes(x = col, y = -0.08, label = texto), colour = negro, size = 2.95) +
  annotate("text", x = nc + 1.05, y = -0.08, label = "Total", colour = negro, size = 2.95) +
  geom_rect(data = tiras, aes(xmin = x, xmax = x + largo / 300 + 0.01, ymin = y_escala - 0.13, ymax = y_escala + 0.13, fill = tono)) +
  geom_text(data = rotulos, aes(x = x, y = y_escala - 0.50, label = texto), colour = gris, size = 3.0) +
  annotate("text", x = x0 + largo + 0.25, y = y_escala, label = "N\u00famero de maestrantes", colour = gris, size = 3.2, hjust = 0) +
  scale_fill_gradientn(colours = rampa, limits = c(0, 1)) +
  scale_x_continuous(expand = c(0, 0)) +
  scale_y_continuous(expand = c(0, 0)) +
  coord_cartesian(xlim = c(izq, der), ylim = c(-(nf + 2.0), 0.35)) +
  labs(x = NULL, y = NULL) +
  theme_minimal(base_size = 9) +
  theme(plot.background = element_rect(fill = "white", colour = NA),
        panel.background = element_rect(fill = "white", colour = NA),
        panel.grid = element_blank(),
        axis.text = element_blank(),
        legend.position = "none",
        plot.margin = margin(6, 6, 6, 6))

# 4. Guardarlo y mostrarlo
carpeta <- if (dir.exists("resultados")) "resultados" else path.expand("~")
archivo <- file.path(carpeta, "07_programa_por_anio_R.png")
ggsave(archivo, grafico, width = 15, height = 19, units = "cm", dpi = 300)

# En RStudio el grafico se dibuja dentro de un marco que conserva la proporcion de la hoja (15 x 19):
# no se estira con la ventana y la letra sale nitida. Para verlo bien: pestana Plots, Zoom y maximizar.
grid::grid.newpage()
grid::grid.rect(gp = grid::gpar(fill = "white", col = NA))
grid::pushViewport(grid::viewport(layout = grid::grid.layout(1, 1, widths = grid::unit(15, "null"),
                                                             heights = grid::unit(19, "null"), respect = TRUE)))
print(grafico, vp = grid::viewport(layout.pos.row = 1, layout.pos.col = 1))
grid::popViewport()
cat("Listo. El grafico se guardo en:", archivo, "\n")
