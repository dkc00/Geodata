library(terra)

# Simples Skript, um eine Differenzenkarte von zwei Flurabstandsszenarien zu berechnen. 
# Im gegebenen Fall wurden die zugrunde liegenden Rasterdateien von unterschiedlichen
# Bearbeitern erstellt, mit unterschiedlichem extent und KBS. Außerdem lagen die 
# Rasterzellen nicht direkt übereinander, weshalb sie mit der project-Methode von terra 
# interpoliert wurden. 

sep_path <- "..." # Flurabstände z.B. september 
mar_path <- "..." # Flurabstände z.B. März

output_path <-"..." # Diffkarte

sep <- rast(sep_path)
mar <- rast(mar_path)

mar_neu <- project(mar, sep, method = "bilinear")

compareGeom(mar_neu, sep) # Wenn TRUE erscheint, stimmt die Geometrie überein


diff_ms <- mar_neu - sep

writeRaster(diff_ms, output_path, overwrite = TRUE)
