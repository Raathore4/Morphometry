import os

pathSub = r'H:\AnkitKailashi\dem\carto10m\hydrology\bqasin\subBasins\subBasins.shp'
v3Man10SubBasin = QgsVectorLayer(pathSub,"subBasin",'ogr')

selectedFeat = []

#v3ManLayer = iface.activeLayer()
print("Qgs ", v3Man10SubBasin.type())

count =0

confi = v3Man10SubBasin.attributeTableConfig()
confi.setSortExpression("gridcode")
confi.setSortOrder(1)
v3Man10SubBasin.setAttributeTableConfig(confi)

progressMessageBar = iface.messageBar().createMessage("Doing something boring...")
progress = QProgressBar()
progress.setMaximum(100)
progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
progressMessageBar.layout().addWidget(progress)


for feature in v3Man10SubBasin.getFeatures():
    iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
    iface.statusBarIface().showMessage("Processind")
    exp = "\"Name\"='{}'".format(feature["Name"])
    v3Man10SubBasin.selectByExpression(exp)
    print(feature["Name"])
    
    os.makedirs(r'H:\AnkitKailashi\withCode\Analysis\hypsometric\subBasins\%s'%(feature['Name']))
    processing.run("native:clip", {'INPUT':'H:/AnkitKailashi/withCode/Analysis/hypsometric/v3Man10ContourPoly20m.shp','OVERLAY':r'H:\AnkitKailashi\withCode\subBasins\%s\%s.shp'%(feature['Name'],feature['Name']),'OUTPUT':'H:/AnkitKailashi/withCode/Analysis/hypsometric/subBasins/%s/v3%shypsometric.shp'%(feature["Name"],feature["Name"])})
    print("%s is created"%(feature["Name"]))
    
    
    
    #processing.run("native:clip", {'INPUT':'H:/AnkitKailashi/withCode/Analysis/hypsometric/v3Man10ContourPoly20m.shp','OVERLAY':QgsProcessingFeatureSourceDefinition('H:/AnkitKailashi/dem/carto10m/hydrology/bqasin/subBasins/subBasins.shp', selectedFeaturesOnly=True, featureLimit=-1, geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid),'OUTPUT':'H:/AnkitKailashi/withCode/Analysis/hypsometric/subBasins/Basin1/v3Basin1hypsometric.shp'})
    # v3Man10SubBasin.removeSelection()
    #break
    #print('H:/AnkitKailashi/withCode/Analysis/hypsometric/subBasins/%s/v3%shypsometric.shp'%(feature["Name"],feature["Name"]))
    #
iface.messageBar().clearWidgets()

iface.showAttributeTable(v3Man10SubBasin)