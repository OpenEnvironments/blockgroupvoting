#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This routine reads the election results and block group shape files for each state,
then summarizes voting by party with counts for precincts and block groups.

This serves to test data integrity and confirm that precincts have consistent scope.

The output of this report is available at the end of the README.md
"""

import pandas as pd
import geopandas as gpd

# Get the list of state abbreviations

states = pd.read_csv("C:/Users/micha/Documents/pycharm/openenvironments/blockgroupvoting/states.csv")

datapath = "D:/Open Environments/data/"

missing = states[states.Abbreviation == "XX"]  # brute force way to make a blank state list
Rtotal = 0
Dtotal = 0
Ltotal = 0
Ototal = 0
Ptotal = 0
Btotal = 0

print("State\tRepublican\tDemocrat\tLibertarian\tOther\tPrecincts\tBlock Groups")
for i, state in states[~states.Abbreviation.isin(["KY","SD","WV"])].iterrows():
    try:
        state_election = gpd.read_file( \
            datapath + "electionscience/dataverse_files/" \
            + state["Abbreviation"].lower() + "_2020/" + state["Abbreviation"].lower() + "_2020.shp")
        blockgroups = gpd.read_file( \
            datapath + "census/tiger/blockgroups/tl_2021_" + "{:02d}".format(state["StateFIPS"]) + "_bg")
        # Get the presidential race column names for Republican, Democrate & Other
        R = [c for c in state_election.columns.to_list() if c[0:7] == "G20PRER"][0]
        D = [c for c in state_election.columns.to_list() if c[0:7] == "G20PRED"][0]
        L = [c for c in state_election.columns.to_list() if c[0:7] == "G20PREL"][0]
        O = [c for c in state_election.columns.to_list() if c[0:6] == "G20PRE" and c[6] not in ['R', 'D', 'L']]
        Rtotal += state_election[R].sum().sum()
        Dtotal += state_election[D].sum().sum()
        Ototal += state_election[O].sum().sum()
        Ltotal += state_election[L].sum().sum()
        Ptotal += state_election.shape[0]
        Btotal += blockgroups.shape[0]
        # state_election.plot()  # generates a map of precincts within states
        print(state["Abbreviation"], "\t",  # State abbreviation
              "{:,}".format(state_election[R].sum().sum()), "\t",  # Repoublican votes
              "{:,}".format(state_election[D].sum().sum()), "\t",  # Democrat votes
              "{:,}".format(state_election[L].sum().sum()), "\t",  # Libertarian votes
              "{:,}".format(state_election[O].sum().sum()), "\t",  # Presidential candidates in other parties
              "{:,}".format(state_election.shape[0]), "\t",        # number of precincts
              "{:,}".format(blockgroups.shape[0])                  # number of block groups
              )  # print statement
    except:
        missing = missing.append(states[states.Abbreviation == state])

print("Total\t", \
      "{:,}".format(Rtotal), "\t", \
      "{:,}".format(Dtotal), "\t", \
      "{:,}".format(Ltotal), "\t", \
      "{:,}".format(Ototal), "\t", \
      "{:,}".format(Ptotal), "\t", \
      "{:,}".format(Btotal) \
      )
print("\n")
print("Missing:", missing)