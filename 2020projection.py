#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code allocates voting data from the state precinct geography onto the Census block group geography.
The geopandas package is used for most processing:
    inputs as
        state shapefiles with dbf columns for voting results against precinct shapes
        a python dictionary identifying the county field within each state dataset
        blockgroup shapefiles from TIGER/Line with selected demographic data
    outputs as GeoDataFrame with precinct results reallocated to block group shapes

The process includes tests that:
    All votes are allocated. BCG results equal elections results at State & County level
    No BCG shapes overlap (show how much)
    No Precinct shapes overlap (show how much)
            cartesian join - every shape overlapping with every shape should only show self
    State & County is fully covered by BCGs (no gaps)
    State & County is fully covered by Precincts (no gaps)
            sum of shapes' areas = aggregate area (assuming the non-overlapping test succeeds)
    Converse operation - bcg votes could be realoocated back to overlapping precincts -
        should return the same county/state totals.

Note:
    The election dataset has 166,419 precincts (3 states missing)
    The Census Bureau publishes 220,333 block groups

    Both of these geographies are bounded
        within state (of 59 US possessions) and within county (3220 of them)

    Some states dont have counties and some states do not have a county identifer in the dataset  (DC, MA, DE)
"""

import os
import sqlalchemy as sql
import pandas as pd
import geopandas as gpd
import geoplot as gpt

def main():
    initialize()
    loadelection()
    loadbcg()
    precinct_to_bcg()
    tests()..

# if __name__ == "__main__":
#   main()



# Get the list of state abbreviations from USPS and county geocodes from NIST

engine = sql.create_engine("postgresql://" +
                       os.environ.get("OEuser") +
                       ":" + os.environ.get("OEpassword") +
                       "@" + os.environ.get("OEhost") +
                       ":" + os.environ.get("OEport") +
                       "/" + os.environ.get("OEdatabase"))
connection    = engine.connect();

states = pd.read_sql("select * from usps.states", connection)

counties = pd.read_sql("select * from nist.geocodes_2019 where summary=50", connection)

# State based voting files record the county name in a variety of fields

county_field = {
'AL':'COUNTYFP20',
'AK':'none',
'AZ':'CDE_COUNTY',
'AR':'COUNTY_FIP',
'CA':'CNTY_CODE',
'CO':'COUNTYFP',
'CT':'COUNTYFP20',
'DE':'none',
'DC':'none',
'FL':'county',
'GA':'CTYNUMBER',
'HI':'COUNTYFP',
'ID':'COUNTYFP',
'IL':'COUNTYFP20',
'IN':'COUNTYFP20',
'IA':'COUNTY',
'KS':'COUNTYFP',
'LA':'COUNTYFP',
'ME':'COUNTY20',
'MD':'JURSCODE',
'MA':'none',
'MI':'COUNTYFIPS',
'MN':'COUNTYFIPS',
'MS':'COUNTYFP20',
'MO':'COUNTYFP',
'MT':'COUNTYFP10',
'NE':'COUNTY',
'NV':'COUNTYFP',
'NH':'COUNTYFP20',
'NJ':'COUNTY',
'NM':'COUNTYFP',
'NY':'COUNTYFP',
'NC':'COUNTY_ID',
'ND':'COUNTYFP',
'OH':'COUNTYFP20',
'OK':'COUNTYFP',
'OR':'COUNTY',
'PA':'COUNTYFP',
'RI':'COUNTYFP20',
'SC':'COUNTY',
'TN':'COUNTY',
'TX':'CNTY',
'UT':'CountyID',
'VT':'COUNTYFP20',
'VA':'COUNTYFP',
'WA':'COUNTY',
'WI':'CNTY_FIPS'
}

#################################################################################
#
#################################################################################
