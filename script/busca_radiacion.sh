#!/bin/bash
gribfile='/scratch/Datatemporal/SMN/data/regional/PERU_WRF22/202501/2025010106/WRFPRS_d01.06'
grib_ls -w shortName=ssrd $gridfile
grib_ls -w shortName=dswrf $gribfile
grib_ls -p shortName,name,paramId,typeOfLevel,level,stepType $gribfile | grep -Ei 'ssrd|dswrf|swrad|short|solar'

