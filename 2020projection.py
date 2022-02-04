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

    Block groups include area covered by water.
        Block Groups with BLKGRPCE = '0' are entirely water.
        Those partially covered by water are not identified.
        As a result, Block Group geometry looks like a superset of voting precincts.
        
    Some states dont have counties and some states do not have a county identifer in the dataset  (DC, AK. MA, DE)
"""

import os
import sqlalchemy as sql
import pandas as pd
import geopandas as gpd
import geoplot as gpt


import logging
logging.basicConfig(level=logging.INFO)
logging.debug('Initializing debug logging')
logging.info('Initializing info logging')
logging.warning('Initializing warning logging')
logging.error('Initializing error logging')
logging.critical('Initializing critical logging')

import datetime
start = datetime.datetime.now()
logging.info("Starting",start)
stop = datetime.datetime.now()
logging.info("Step 1 finished. Duration:",stop - start)

datapath = "D:/Open Environments/data/"


for state in states:



def main():
    initialize()
    for state in states["Abbreviation"]:
        loadelection(state)
        loadbcg(state)
        if county_field[state] == 'None':
            # process the entire state
            allocateprecinct(bg,pr)
        else:
            # loop over counties
            for county in state_election[county_field[state]].unique():
                print(county)
              allocateprecinct(bg, pr)
    tests()..

# if __name__ == "__main__":
#   main()

def initialize():

    # Get the list of state abbreviations and state fips codes from USPS

    engine = sql.create_engine("postgresql://" +
                               os.environ.get("OEuser") +
                               ":" + os.environ.get("OEpassword") +
                               "@" + os.environ.get("OEhost") +
                               ":" + os.environ.get("OEport") +
                               "/" + os.environ.get("OEdatabase"))
    connection = engine.connect();

    states = pd.read_sql("select * from usps.states", connection)

    #########################################################################
    # State based voting files record the county name in a variety of fields

    county_field = {
    'AL':'COUNTYFP20',    'AK':'none',    'AZ':'CDE_COUNTY',    'AR':'COUNTY_FIP',
    'CA':'CNTY_CODE',    'CO':'COUNTYFP',    'CT':'COUNTYFP20',    'DE':'none',
    'DC':'none',    'FL':'county',    'GA':'CTYNUMBER',    'HI':'COUNTYFP',
    'ID':'COUNTYFP',    'IL':'COUNTYFP20',    'IN':'COUNTYFP20',    'IA':'COUNTY',
    'KS':'COUNTYFP',    'LA':'COUNTYFP',    'ME':'COUNTY20',    'MD':'JURSCODE',
    'MA':'none',    'MI':'COUNTYFIPS',    'MN':'COUNTYFIPS',    'MS':'COUNTYFP20',
    'MO':'COUNTYFP',    'MT':'COUNTYFP10',    'NE':'COUNTY',    'NV':'COUNTYFP',
    'NH':'COUNTYFP20',    'NJ':'COUNTY',    'NM':'COUNTYFP',    'NY':'COUNTYFP',
    'NC':'COUNTY_ID',    'ND':'COUNTYFP',    'OH':'COUNTYFP20',    'OK':'COUNTYFP',
    'OR':'COUNTY',    'PA':'COUNTYFP',    'RI':'COUNTYFP20',    'SC':'COUNTY',
    'TN':'COUNTY',    'TX':'CNTY',    'UT':'CountyID',    'VT':'COUNTYFP20',
    'VA':'COUNTYFP',    'WA':'COUNTY',    'WI':'CNTY_FIPS'    }




#################################################################################
#
#################################################################################


def loadbcg:
    # wget https://www2.census.gov/geo/tiger/TGRGDB21/tlgdb_2021_a_01_al.gdb.zip  --  all files like this



###############################################################33
# last good idea  -  looping over one bg and one pr at a time
############################################################
    ####################################################################
    # Attribute precinct voting results only census block groups
    ####################################################################

    # THIS WILL PROB BE A PROCEDURE, SO GENERALIZE THESE NAMES

    # blockgroups = pd.merge(bgshapes, bgpop, on='GEOID', how='inner')
    blockgroups = bgpop[bgpop.COUNTYFP10 == "115"]
    precincts = precincts[precincts.COUNTYFIPS == '115']

    # Initialize voting fields in the underlying block group dataframe

    # outer loop over bcg

    # def allocateprecinct(blockgroups, precincts):
    """
    For a geography that bounds both precincts and blockgroups (county, eg),
    loop over its block groups
    find any precincts that overlap each
    accumulate the overlapping precincts' voting proportioned by the

    Inputs:
        blockgroups - geometries with blockgroup identifiers
        precincts - geometries with voting results 
    Results:
        bockgroupvoting - a dataframe with
            GEOID - census block group id with state(2), county(3), tract(),blockgroup(1)
            REP - Votes for Republican party candidate
            DEM - Votes for Democrat party candidate
            LIB - Votes for Libertary party candidate
            OTH - Votes for any other parties' candidates
    """

    bglist = []  # a list of dict to accumulate block group results
    # initialized as empty, to be progressively built
    prlist = {}  # a list of dict to track precinct results remaining to be allocated
    # initialized with one entry per precinct value set to 100 pct remaining
    # in many cases, precincts do not have identifiers so we will use the pr dataframe's indexes
    for p in list(precincts.index.values):
        prlist[p] = 100

    for i, b in blockgroups.iterrows():
        print("Processing block group index", i)
        found = False
        intersectioncounter = 0
        bgresults = dict.fromkeys(['GEOID', 'REP', 'DEM', 'LIB', 'OTH', 'area', 'gap', 'precincts'], 0)
        bgresults['GEOID'] = b.GEOID
        for j, p in precincts.iterrows():
            # find the intersection of this precinct with this block group
            # it may return points or edges which should be ignored, area = 0
            # inter = blockgroups[blockgroups.index == i].overlay( \
            #    precincts[precincts.index == j], how='intersection', keep_geom_type=False)
            # inter = blockgroups.iloc[[i]].overlay( \
            #     precincts.iloc[[j]], how='intersection', keep_geom_type=False)
            # also consider type(gpd.GeoDataFrame(b))
            inter = blockgroups.loc[blockgroups.index == i].overlay( \
                precincts, how='intersection', keep_geom_type=False)
            if inter.shape[0] > 0:
                print("    precinct intersections found: ", inter.shape[0])
                if inter.area[0] > 0:
                    if not found:
                        intersections = inter
                        found = True
                    else:
                        intersections = intersections.append(inter)
                    intersectioncounter += 1
        #    bgresults['REP'] +=
        #    bgresults['DEM'] +=
        #    bgresults['LIB'] +=
        #    bgresults['OTH'] +=
        bgresults['area'] = blockgroups.where(blockgroups.index == i).area.sum()
        bgresults['gap'] = (blockgroups.where(blockgroups.index == i).area.sum() - intersections.area.sum())
        bgresults['precincts'] = intersectioncounter
        bgresults['population'] = bgpop.B01001e1
        if bgresults['gap'] > 4046.86:
            # There are 4046.86 square meters in an acre.
            # The mean area of a block group is 2m square meters.
            # This alerts when more than an acre of the block group is unrepresented by a voting precinct
            print(b.GEOID, blockgroups[blockgroups.index == i].area.sum(), bgresults['gap'])
        # area of intersections should equal area of block group
        bglist.append(bgresults)    