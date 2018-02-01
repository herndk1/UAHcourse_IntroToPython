#################################
#FILE: takehome1.py
#AUTHOR:Kelsey Herndon
#EMAIL: keh0023@uah.edu 
#MODIFIED BY: N/A
#ORGANIZATION: University of Alabama in Huntsville; Department of Atmospheric Science
#CREATION DATE: 2/22/2017
#LAST MOD DATE: 2/26/2017
#PURPOSE: This script adds a desired suffix to a file name
#DEPENDENCIES: arcpy
#################################

# Import system modules
import arcpy

##Get the variables from ArcMap
#get the workspace location
workspace = arcpy.GetParameterAsText(0) 
#get the original file (to be renamed)
in_data = arcpy.GetParameterAsText(1)
#get the desired suffix for the file (note: this is not the file type, for example .tif, .jpeg, etc.)
suffix = arcpy.GetParameterAsText(2)

##Define the workspace
arcpy.env.workspace = workspace

##Define the new name of the file 
out_data =  in_data[0:-4] + suffix

##Execute Rename
arcpy.Rename_management(in_data, out_data, "raster")
