subPath = r'F:\pythonProject\QGis\basins\carto10\subBasins\carto10SubBasin.shp'
sub = QgsVectorLayer(subPath,'Stream Length Gradient','ogr')

#l = ['Basin29','Basin30','Basin27','Basin25','Basin22',]

def FieldCalcu():

    for f in sub.getFeatures():
        drainagePath = r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\%sDrainage.shp'%(f['Name'],f['Name'])
        drainage = QgsVectorLayer(drainagePath,'Stream Length Gradient','ogr')
        pathR = r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\carto10%sSlopeDgr.tif'%(f['Name'],f['Name'])
        v3ManSlope = QgsRasterLayer(pathR,'v3ManUTM','GDAL')
        pathRv = r'F:\pythonProject\QGis\basins\carto10\subBasins\%s\DEM\carto10%s.tif'%(f['Name'],f['Name'])
        v3ManUtm = QgsRasterLayer(pathRv,'v3ManUTM','GDAL')
                
        
        featCount = drainage.featureCount()
        total_sum = drainage.aggregate(QgsAggregateCalculator.Sum, "length")
        lengthSum = round(total_sum[0]/1000,2)
        freq = round(featCount/f['Area'],2)
        dens = round(lengthSum/f['Area'],2)
        coM = 1/f['DraDensity']
        loF = 1/(2*f['DraDensity'])
        ReR = f['Relief']/(f['Periferi'])
        Rugd = f['DraDensity']*f['Relief']/1000
        print("\n%s\n"%(f['Name']))
        RR = f['Relief']/(f['BasinLengt'])
        print("\n%s\tRelative %f \tRR %.2f"%(f['Name'],ReR,RR))
        count = 0
        #f['ReliefRati'] = round(RR,3)
        for x in drainage.getFeatures():
            if x['order_']==1:
                count+=1
            else:
                pass
        text = count/f['Periferi']
        #print('\nTexture = ',text)
        
        #slope study
        stats = v3ManUtm.dataProvider().bandStatistics(1)
        #f['FormFact'] = f['Form Facto']
        #f['ShapeFact'] = f['Shape Fact']
        #print("f['FormFact']",f['FormFact'])
        #print("f['ShapeFact']",f['ShapeFact'])
        
        
        cir = (4*(22/7)*f['Area'])/(f['Periferi']**2)
        #print("old cir = %f and New cir %f"%(f['Circularit'],cir))
        #f['Circularit'] = round(cir,2)
        '''
        #print("%s"%(f['Name']))
        #print("Min value: {}".format(stats.minimumValue))
        #print("Max value: {}".format(stats.maximumValue))
        #print("Mean value: {}".format(stats.mean))
        #f['TextureRat'] = text
        #f['MeanEle'] = stats.mean
        #f['MxSlope'] = stats.maximumValue
        #f['MeanSlope'] = stats.mean
        #f['ConChaMant'] = coM
        #f['LenOverLan'] = loF
        #f['RelatiReli'] = RR
        #f['Ruggedness'] = Rugd
        #print("Constant of Channel Maintance",coM,"\nLength of OverlandFlow",loF,"\nRelief Ratio",RR,"\nRuggedness",Rugd)
        #f['DraDensity'] = dens
        #f['DraFrequen'] = freq
        #print("\n\n\n%s \nfeatures = %d \nArea = %.2f \nlength = %.f \nFreq = %.2f and \ndensity = %.2f"%(f['Name'],featCount,f['Area'],lengthSum,freq,dens))
        '''
        #sub.updateFeature(f)

    
#for check editing
if sub.isEditable():
    FieldCalcu()
    print('EditMode')
else:
    with edit(sub):
       FieldCalcu() 
       print('withEdit')
       

iface.showAttributeTable(sub)
