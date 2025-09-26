library(terra)

# GENERELLES VEKTORISIEREN MIT TERRA


raster_path <- "M:/DBU Ueckermünder Heide/QGIS/Karten/PrognoseTool/NEU_Projektbereich_Schlosssee_KOSKA_Diff_recl.tif"
output_path <- "M:/DBU Ueckermünder Heide/QGIS/Karten/PrognoseTool/NEU_Projektbereich_Schlosssee_KOSKA_Diff_recl_vect.shp"


raster <- rast(raster_path)


# Ohne dissolve = FALSE exportiert er hier einfach ein großes Polygon mit allen 
# Zellen, die denselben Wert tragen. So bekommt jede Zelle mit einem Wert
# ein eigenes Polygon. 
vector <- as.polygons(raster, dissolve = FALSE)

writeVector(vector, output_path)

# ________________________________________________________________---

# Ich möchte jetzt zuerst mein Raster auf 20x20m hochskalieren 
# (aktuell 1x1m) und dann mit dissolve = FALSE vektorisieren. 
# Siehe für diesen Code das Skript "rasterisieren_und_hochskalieren"

# Schritt 1:
raster_path <- "M:/DBU Ueckermünder Heide/QGIS/Karten/PrognoseTool/NEU_Projektbereich_Schlosssee_KOSKA_Diff_recl.tif"
output_path <- "M:/DBU Ueckermünder Heide/QGIS/Karten/PrognoseTool/NEU_Projektbereich_Schlosssee_KOSKA_Diff_recl_vect.shp"


raster <- rast(raster_path)

orig_res <- res(raster) # originale Auflösung

factor <- 20  # um faktor 20 hochskalieren

raster_upscaled <- disagg(raster, fact = factor, method = "near")
plot(raster_upscaled) # neues raster zur kontrolle plotten 

# Wenn wir jetzt vektorisieren, kommt bei sehr großen Rastern der Fehler
# Fehler: [as.polygons] the raster is too large
# Also clippen wir das Raster auf eine bbox und vektorisieren dann

# Schritt 2: raster auf bbox clippen

# Der Code hier basiert auf dem Skript "Resampling_Rasterdaten"

# 454290.7525713772047311,5934435.8579823439940810 : 455010.6223939021583647,5935854.8240607017651200

xmin <- 454290.7525713772047311
ymin <- 5934435.8579823439940810
xmax <- 455010.6223939021583647
ymax <- 5935854.8240607017651200

extent_poly <- vect(rbind(
  c(xmin, ymin),
  c(xmin, ymax),
  c(xmax, ymax),
  c(xmax, ymin),
  c(xmin, ymin)
), type = "polygons", crs = crs(raster_upscaled))

raster_cropped <- crop(raster_upscaled, extent_poly)

ncell(raster_upscaled) # Anzahl der Zellen ausgeben
ncell(raster_cropped) # Anzahl der Zellen ausgeben

# In meinem akuten Fall ist das Raster immer noch zu groß und lediglich 
# von 4020328000 auf 408600842 Zellen runtergegangen. Das Skript funktioniert 
# aber und ist gut auf kleinere Raster anwendbar. 



# Schritt 3: vektorisieren 

vector <- as.polygons(raster_cropped, dissolve = FALSE)

writeVector(vector, output_path)