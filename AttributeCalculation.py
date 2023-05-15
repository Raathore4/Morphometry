#call sub-basin file
subPath = r'F:\pythonProject\QGis\basins\carto10\subBasins\carto10SubBasin.shp'
sub = QgsVectorLayer(subPath,'Stream Length Gradient','ogr')



def FieldCalcu():

    for f in sub.getFeatures():
        drainagePath = r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\%sDrainage.shp'%(f['Name'],f['Name'])
        drainage = QgsVectorLayer(drainagePath,'Stream Length Gradient','ogr')
        pathR = r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\carto10%sSlopeDgr.tif'%(f['Name'],f['Name'])
        v3ManSlope = QgsRasterLayer(pathR,'v3ManUTM','GDAL')
        pathRv = r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\carto10%s.tif'%(f['Name'],f['Name'])
        v3ManUtm = QgsRasterLayer(pathRv,'v3ManUTM','GDAL')
        print("\n%s\n"%(f['Name']))   
        statsDEM = v3ManUtm.dataProvider().bandStatistics(1)
        statsSlope = v3ManSlope.dataProvider().bandStatistics(1)
        f['Relief'] = statsDEM.maximumValue-statsDEM.minimumValue
        featCount = drainage.featureCount()
        total_sum = drainage.aggregate(QgsAggregateCalculator.Sum, "length")
        lengthSum = round(total_sum[0]/1000,2)
        freq = round(featCount/f['Area'],2)
        dens = round(lengthSum/f['Area'],2)
        coM = 1/f['DraDensity']
        loF = 1/(2*f['DraDensity'])
        ReR = f['Relief']/(f['Periferi'])
        Rugd = f['DraDensity']*f['Relief']/1000
        
        RR = f['Relief']/(f['BasinLengt'])
        print("\n%s\tRelative %f \tRR %.2f"%(f['Name'],ReR,RR))
        count = 0
        
        for x in drainage.getFeatures():
            if x['order_']==1:
                count+=1
            else:
                pass
        text = count/f['Periferi']       
        cir = (4*(22/7)*f['Area'])/(f['Periferi']**2)        
        f['MinEle'] = statsDEM.minimumValue
        f['MaxEle'] = statsDEM.maximumValue
        f['MeanEle'] = statsDEM.mean
        f['TextureRat'] = text
        f['MxSlope'] = statsSlope.maximumValue
        f['MeanSlope'] = statsSlope.mean
        f['ConChaMant'] = coM
        f['LenOverLan'] = loF
        f['RelatiReli'] = RR
        f['Ruggedness'] = Rugd
        f['Circularit'] = round(cir,2)
        f['DraDensity'] = dens
        f['DraFrequen'] = freq
        f['FormFact'] = f['Form Facto']
        f['ShapeFact'] = f['Shape Fact']
        f['ReliefRati'] = round(RR,3)
        
        
        sub.updateFeature(f)

    
#for check editing
if sub.isEditable():
    FieldCalcu()
    print('EditMode')
else:
    with edit(sub):
       FieldCalcu() 
       print('withEdit')
       

iface.showAttributeTable(sub)
