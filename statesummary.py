#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This routine reads the election results and block group shape files for each state,
then summarizes voting by party and
calculates average votes per precinct.

This serves to test data integrity and confirm that precincts have consistent scope.

The output of this report is available at the end of the README.md
"""

import pandas as pd
import geopandas as gpd
import warnings
warnings.filterwarnings("error")

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

print("State\tRepublican\tDemocrat\tLibertarian\tOther\tPrecincts\tVotes per Precinct\tBlock Groups")
for state in states["Abbreviation"]:
    try:
        state_election = gpd.read_file( \
            "D:/Open Environments/data/electionscience/dataverse_files/" \
            + state.lower() + "_2020/" + state.lower() + "_2020.shp")
        blockgroups = gpd.read_file( \
            datapath + "census/tiger/blockgroups/tl_2021_" + state.lower() + "_bg")
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
        print(state, "\t",  # State abbreviation
              "{:,}".format(state_election[R].sum().sum()), "\t",  # Repoublican votes
              "{:,}".format(state_election[D].sum().sum()), "\t",  # Democrat votes
              "{:,}".format(state_election[L].sum().sum()), "\t",  # Libertarian votes
              "{:,}".format(state_election[O].sum().sum()), "\t",  # Presidential candidates in other parties
              "{:,}".format(state_election.shape[0]), "\t",  # number of precincts
              "{:,.2f}".format( \
                  (state_election[R].sum().sum() + state_election[D].sum().sum() +
                   state_election[L].sum().sum() + state_election[O].sum().sum()) / state_election.shape[0]),
              "{:,}".format(blockgroups.shape[0])  # number of precincts
              )  # print statement

    except:
        missing = missing.append(states[states.Abbreviation == state])

print("Total\t", \
      "{:,}".format(Rtotal), "\t", \
      "{:,}".format(Dtotal), "\t", \
      "{:,}".format(Ltotal), "\t", \
      "{:,}".format(Ototal), "\t", \
      "{:,}".format(Ptotal), "\t", \
      "{:,.2f}".format((Rtotal + Dtotal + Ltotal + Ototal) / Ptotal), "\t", \
      "{:,}".format(Btotal) \
      )
print("\n")
print("Missing:", missing)