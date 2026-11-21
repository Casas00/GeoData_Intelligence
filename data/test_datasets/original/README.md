# Datasets originales de prueba

Estos archivos son datos sintéticos diseñados para probar el flujo de adaptación e ingesta.

- `buildings_original.geojson`: 12 huellas Polygon en coordenadas GeoJSON WGS84 (EPSG:4326). Los atributos de origen tienen nombres distintos a los del modelo lógico `vector_buildings.json`. `alcada_aprox` mezcla punto y coma decimal en valores numéricos y `data_registre` contiene un nulo.
- `population_original.csv`: 18 registros tabulares. Los campos difieren de `tabular_population.json`; los valores numéricos llegan como texto, la densidad mezcla punto y coma decimal, y hay nulos/campos vacíos. El valor `no disponible` en `hab_km2` es un caso deliberadamente no convertible que debe detectarse y no convertirse silenciosamente.

Los datos son ficticios. No representan estadísticas oficiales ni inventario real de edificios.
