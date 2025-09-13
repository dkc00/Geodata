
install.packages("terra")
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

shp_vect <- vect(shp)

raster_clipped <- mask(crop(raster, shp_vect), shp_vect) # die logik ist: mask(crop(raster, vektor), vektor)

writeRaster(raster_clipped, "...", overwrite=TRUE) # output path angeben