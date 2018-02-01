###########
#FILE: hmk_new_3.py
#AUTHOR(S): Kelsey Herndon & Rebekke Muench
#EMAIL: keh0023@uah.edu
#ORGANIZATION: UAH
#CREATION DATE: March 22, 2017
#LAST MOD DATE: March 29, 2017
#PURPOSE: Compare the relationship between NDVI and three census variables for 2006 and 2016
#DEPENDENCIES: arcpy, numpy
###########


#Import packages
import arcpy
from arcpy.sa import *
import numpy as np
arcpy.env.overwriteOutput = 'True'
arcpy.CheckOutExtension('Spatial')

# Import variables 
ndvi06 = r'\\Mac\Home\Documents\UAH\ESS308\ndvi\modis_conus_ndvi2006_int.tif'
ndvi16 = r'\\Mac\Home\Documents\UAH\ESS308\ndvi\modis_conus_ndvi2016_int.tif'
census = r'\\Mac\Home\Documents\UAH\ESS308\CONUS_County_Census\County_2010Census_CONUS.shp'

# Put the NDVI for the two years into an array
files = np.array([ndvi06, ndvi16])

# Run the sam process for each part of the given array (for both NDVIs) 
for x in files:
    # Obtain year from filepath to be used in naming later saved images
    y = x[-10] + x[-9]
    # Designate that the file is a raster
    ras = arcpy.Raster(x)
    # Rename the census file so fields are not added to same file
    census_n = census[:-4] + y +'.shp'
    arcpy.CopyFeatures_management(census, census_n)
    #Define out_table variable which will be used in the zonal statistics
    out_table = r'\\Mac\Home\Documents\UAH\ESS308\out_table' + y + '.dbf'
    # Conduct zonal statistics
    stats = arcpy.sa.ZonalStatisticsAsTable(census_n, 'FID', ras, out_table, ignore_nodata = 'DATA', statistics_type = 'ALL')
    
    # Join the statistics output to the new census file
    joinshp = arcpy.JoinField_management(census_n, 'FID', stats, 'OID')
    census_join = r'\\Mac\Home\Documents\UAH\ESS308\join' + y + '.dbf'
    arcpy.CopyFeatures_management(joinshp, census_join)
    
    # Project the census file so it represents the true area of the counties
    census_prj = census_join[:-4] + '_prj.shp'
    arcpy.Project_management(census_join, census_prj, arcpy.SpatialReference('North America Albers Equal Area Conic'))
 
    # Add field and calculate it for the true area of the counties
    arcpy.AddField_management(census_prj, field_name = 'area_true', field_type = 'FLOAT')
    arcpy.CalculateField_management(census_prj, 'area_true', "float(!SHAPE.AREA!)/1E6", "PYTHON")
    #Add field and calculate it for the population density
    arcpy.AddField_management(census_prj, 'pop_den', field_type = 'FLOAT')
    arcpy.CalculateField_management(census_prj, 'pop_den', "float(!DP0010001! /!area_true!)", "PYTHON")
    #Add field and calculate so FID reads as an integer 
    arcpy.AddField_management(census_prj, field_name = 'FID_real', field_type = 'INTEGER')
    arcpy.CalculateField_management(census_prj, 'FID_real', "int(!FID!)", "PYTHON")
    #Add field and calculate percent institutionalized
    arcpy.AddField_management(census_prj, field_name = 'perc_inst', field_type = 'FLOAT')
    arcpy.CalculateField_management (census_prj, 'perc_inst', "(float(!DP0120015!)/float(!DP0010001!))*1000", "PYTHON")
    # Add field and calculate
    arcpy.AddField_management(census_prj, field_name = 'male', field_type = 'FLOAT')
    arcpy.CalculateField_management(census_prj, 'male', "(float(!DP0040002!)/float(!DP0010001!))*100", "PYTHON")
    
    # Perform Ordinary Least Squares stats with Mean and population density
    ols_results = r'\\Mac\Home\Documents\UAH\ESS308\ols_popden' + y + '.shp'
    outpdf = r'\\Mac\Home\Documents\UAH\ESS308\ols_popden' + y + '.pdf'
    arcpy.OrdinaryLeastSquares_stats(census_prj, 'FID_real', ols_results, 'MEAN', 'pop_den', '#', '#', outpdf)
    # Perform Ordinary Least Squares stats with Mean and {ercent Institutionalized Population
    ols_results2 = r'\\Mac\Home\Documents\UAH\ESS308\ols_inst' + y + '.shp'
    outpdf2 = r'\\Mac\Home\Documents\UAH\ESS308\ols_inst' + y + '.pdf'
    # Perform Ordinary Least Squares stats with Mean and Percent Male (18+) Population
    arcpy.OrdinaryLeastSquares_stats(census_prj, 'FID_real', ols_results2, 'MEAN', 'perc_inst', '#', '#', outpdf2)
    ols_results3 = r'\\Mac\Home\Documents\UAH\ESS308\ols_male' + y + '.shp'
    outpdf3 = r'\\Mac\Home\Documents\UAH\ESS308\ols_male' + y + '.pdf'
    arcpy.OrdinaryLeastSquares_stats(census_prj, 'FID_real', ols_results3, 'MEAN', 'male', '#', '#', outpdf3)


    
    
