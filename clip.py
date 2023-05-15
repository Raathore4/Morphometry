import os

# Path of subBasin Vector File which have all the subBasins
pathSub = r'H:\AnkitKailashi\dem\carto10m\hydrology\bqasin\subBasins\subBasins.shp'

#define as vector
v3Man10SubBasin = QgsVectorLayer(pathSub,"subBasin",'ogr')

feat = []


#arrange attribute table of sub-basin according the gridcode (a field in their attribute)
confi = v3Man10SubBasin.attributeTableConfig()
confi.setSortExpression("gridcode")
confi.setSortOrder(1)
v3Man10SubBasin.setAttributeTableConfig(confi)


# Loop through every sub-basin in the vector file
for feature in v3Man10SubBasin.getFeatures():
    #make a sql expression
    exp = "\"Name\"='{}'".format(feature["Name"])
    v3Man10SubBasin.selectByExpression(exp)
    print(feature["Name"])
    try:
        
        os.makedirs(r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM'%(feature['Name'])) #address of our file
    
    
    
        write = QgsVectorFileWriter.writeAsVectorFormat(v3Man10SubBasin,r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\carto10%s.shp'%(feature['Name'],feature['Name']), 'utf-8', driverName='ESRI Shapefile',onlySelected=True)
    
        
        #clip slope and drainage of individual sub-basin
        processing.run("gdal:cliprasterbymasklayer", {'INPUT':r'F:\pythonProject\QGis\basins\carto10\carto10ManSlopDgr.tif','MASK':r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\carto10%s.shp'%(feature['Name'],feature['Name']),'SOURCE_CRS':None,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32643'),'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,'MULTITHREADING':False,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'','OUTPUT':r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\carto10%sSlopeDgr.tif'%(feature['Name'],feature['Name'])})
        processing.run("gdal:clipvectorbypolygon", {'INPUT':'E:/phd/satelite Images/cartoset DEM/v3/mosaic/arcgis work/stream/v3mandrainage.shp','MASK':r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\carto10%s.shp'%(feature['Name'],feature['Name']),'OPTIONS':'','OUTPUT':r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\%sDrainage.shp'%(feature['Name'],feature['Name'])})
        
    #check any exceptional error
    except Exception:
        feat.append(feature['Name'])


print(feat)
