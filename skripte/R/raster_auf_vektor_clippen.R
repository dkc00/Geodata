library(sf)
library(terra)


# RASTER AUF VEKTORRÄNDER CLIPPEN 


tif_path <- "..."   # pfad des rasters
shp_path <- "..."    # pfad des vektorlayers


raster <- rast(tif_path)
shp <- st_read(shp_path)

if (!st_crs(shp) == crs(raster)) {
  shp <- st_transform(shp, crs(raster)) #crs transformieren wenn erforderlich (if abfrage)
}

# Ist die Gesamt-Vektordatei deutlich größer als das Raster, und die TIF-Datei (z.B. Flurabstandskarte) soll lediglich auf den relevanten Ausschnitt der Vektordatei (z.B. Landesgrenzen Niedersachsens) zugeschnitten werden? 
# Dann die drei folgenden Zeilen aktivieren, diese clippen das eingeladene Shapefile auf die Intersection von Shape und Raster-Ausdehnung. 

# raster_extent <- st_as_sfc(st_bbox(raster))
 
# st_crs(raster_extent) <- st_crs(shp)
 
# shp_clip <- st_intersection(shp, raster_extent)


shp_vect <- vect(shp)

raster_clipped <- mask(crop(raster, shp_vect), shp_vect) # die logik ist: mask(crop(raster, vektor), vektor)

writeRaster(raster_clipped, "...", overwrite=TRUE) # output path angeben
