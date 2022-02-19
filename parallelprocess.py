import argparse

parser = argparse.ArgumentParser(description='Allocating voting results by block group')
parser.add_argument('-t','--thread', help='Which thread is this?', required=True)
parser.add_argument('-o','--ofthreads', help='Of how many threads?', required=True)
args = vars(parser.parse_args())

# copy from above EXCEPT the get data functions
# major imports
import os
import pandas as pd
import wget
from zipfile import ZipFile
import geopandas as gpd
import datetime
import logging
import numpy as np
import sqlalchemy as sql
# import geoplot as gpt
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("error")

# global variables

datapath = "/data/disk2/update/"
votingvintage = "2020"
shapefilevintage = "2019"

# Create the states control dataframe

sdata = \
"""Alabama,AL,01,COUNTYFP20
Alaska,AK,02,none
Arizona,AZ,04,CDE_COUNTY
Arkansas,AR,05,COUNTY_FIP
California,CA,06,CNTY_CODE
Colorado,CO,08,COUNTYFP
Connecticut,CT,09,COUNTYFP20
Delaware,DE,10,none
District of Columbia,DC,11,none
Florida,FL,12,county
Georgia,GA,13,CTYNUMBER
Hawaii,HI,15,COUNTYFP
Idaho,ID,16,COUNTYFP
Illinois,IL,17,COUNTYFP20
Indiana,IN,18,COUNTYFP20
Iowa,IA,19,COUNTY
Kansas,KS,20,COUNTYFP
Louisiana,LA,22,COUNTYFP
Maine,ME,23,COUNTY20
Maryland,MD,24,JURSCODE
Massachusetts,MA,25,none
Michigan,MI,26,COUNTYFIPS
Minnesota,MN,27,COUNTYFIPS
Mississippi,MS,28,COUNTYFP20
Missouri,MO,29,COUNTYFP
Montana,MT,30,COUNTYFP10
Nebraska,NE,31,COUNTY
Nevada,NV,32,COUNTYFP
New Hampshire,NH,33,COUNTYFP20
New Jersey,NJ,34,COUNTY
New Mexico,NM,35,COUNTYFP
New York,NY,36,COUNTYFP
North Carolina,NC,37,COUNTY_ID
North Dakota,ND,38,COUNTYFP
Ohio,OH,39,COUNTYFP20
Oklahoma,OK,40,COUNTYFP
Oregon,OR,41,COUNTY
Pennsylvania,PA,42,COUNTYFP
Rhode Island,RI,44,COUNTYFP20
South Carolina,SC,45,COUNTY
Tennessee,TN,47,COUNTY
Texas,TX,48,CNTY
Utah,UT,49,CountyID
Vermont,VT,50,COUNTYFP20
Virginia,VA,51,COUNTYFP
Washington,WA,53,COUNTY
Wisconsin,WI,55,CNTY_FIPS
Wyoming,WY,56,COUNTYFP20
"""

statedict = [{ \
    "Possession":state.split(",")[0],
    "Abbreviation":state.split(",")[1],
    "StateFIPS":state.split(",")[2],
    "CountyField":state.split(",")[3]
             } for state in sdata.splitlines()]

states = pd.DataFrame.from_dict(statedict)

# Main processing function to be called for each state

def process_state(state):
    """
    Main function accpets a tuple representing one state and its properties
    """
    print("Processing state", state["Abbreviation"])
    # read in the corresponding shape files for voting results and block groups
    precincts = gpd.read_file( \
        datapath + "/voting/" \
            + state["Abbreviation"].lower() + "_" + votingvintage + "/" + state["Abbreviation"].lower() + "_2020.shp")
    precincts = precincts.to_crs("EPSG:3395")
    #The precinct set may not have a key.  Intersection calcs will then lose track of which pr caused the intersection.
    precincts["prindex"] = precincts.index
    blockgroups = gpd.read_file( \
            datapath + "shapefiles/" + "tl_" + shapefilevintage + "_" + state["StateFIPS"] + "_bg")
    blockgroups = blockgroups.to_crs("EPSG:3395")
    # Calculate the party summary
    R = [c for c in precincts.columns.to_list() if c[0:7] == "G20PRER"][0]
    precincts["REP"] = precincts[R]
    D = [c for c in precincts.columns.to_list() if c[0:7] == "G20PRED"][0]
    precincts["DEM"] = precincts[D]
    L = [c for c in precincts.columns.to_list() if c[0:7] == "G20PREL"][0]
    precincts["LIB"] = precincts[L]
    O = [c for c in precincts.columns.to_list() if c[0:6] == "G20PRE" and c[6] not in ['R','D','L'] ]
    precincts["OTH"] = precincts[O].sum(axis=1)
    # Initialize summary objects for block groups and precincts
    bgaccumulate = list()
    prlist = {}   # a list of dict to track precinct results remaining to be allocated
                  # initialized with one entry per precinct value set to 100 pct remaining
                  # in many cases, precincts do not have identifiers so we will use the pr dataframe's indexes
    for pre in list(precincts.index.values):
        prlist[pre] = 100  # initialize the precinct list has having 100 percent left to allocate

    bgwith = 0
    bgwithout = 0

    for i,b in blockgroups.iterrows():
        print(state["Abbreviation"],"processing",i,"of",blockgroups.shape[0],"block groups")
        bgresults = dict.fromkeys(['GEOID', 'REP', 'DEM', 'LIB','OTH','area','gap','precincts'], 0)
        bgresults['GEOID'] = b.GEOID
        bgresults['REP'] = 0
        bgresults['DEM'] = 0
        bgresults['LIB'] = 0
        bgresults['OTH'] = 0
        intersections = blockgroups.loc[blockgroups.index == i].overlay( \
             precincts, how='intersection', keep_geom_type=False)
        if intersections.shape[0] > 0:
            bgwith += 1
            for j,p in intersections.iterrows():
                # what is the proportion area of overlay
                prproportion = intersections.area[j]/(precincts.loc[precincts.index == p.prindex].area)[p.prindex]
                # allocate this precincts voting to the block group using that proportion
                bgresults['REP'] += prproportion * precincts['REP'].loc[p.prindex]
                bgresults['DEM'] += prproportion * precincts['DEM'].loc[p.prindex]
                bgresults['LIB'] += prproportion * precincts['LIB'].loc[p.prindex]
                bgresults['OTH'] += prproportion * precincts['OTH'].loc[p.prindex]
                # decrement the precinct allocation tracking data
                prlist[p.prindex] -= prproportion * 100
        else:
                bgwithout += 1
        bgresults['area'] = blockgroups.loc[blockgroups.index == i].area.sum()
        bgresults['gap'] = blockgroups.loc[blockgroups.index == i].area.sum() - intersections.area.sum()
        bgresults['precincts'] = intersections.shape[0]
        #area of intersections should equal area of block group
        bgaccumulate.append(bgresults)
    # write the state result to csv
    pd.DataFrame(bgaccumulate).to_csv(datapath + "results/" + state["Abbreviation"] + 'bg.csv')
    pd.DataFrame.from_dict(prlist,orient='index').to_csv(datapath + "results/" + state["Abbreviation"] + 'pr.csv')

if __name__ == "__main__":
    print(">>>",args['ofthreads'],"threads<<<>>>running #", args['thread'])
    for i, state in states.iterrows():
        if (i % int(args['ofthreads'])) ==  int(args['thread']):
            print("Launching",state.Possession)
            if os.path.exists(datapath + "results/" + state["Abbreviation"] + 'bg.csv'):
                print("Already finished ",datapath + "results/" + state["Abbreviation"] + 'bg.csv')
            else:
                process_state(state)
