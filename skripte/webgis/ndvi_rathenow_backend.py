from flask import Flask, request, jsonify
# wir nutzen flask für unser backend

import rasterio 


ndvi_path = r"C:\Users\Daniel Koch\Desktop\Fernerkundung\Daten\WebGIS_Rathenow\NDVI_240925_Rathenow.tif"

app = Flask(__name__)

ndvi = rasterio.open(ndvi_path) 

@app.route("/get_value")
def get_value():
    lon = float(request.args.get("lon"))
    lat = float(request.args.get("lat"))
    for val in ndvi.sample([(lon, lat)]):
        return jsonify({"ndvi": float(val[0])})

app.run(port=5000)
