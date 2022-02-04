# blockgroupvoting
This repository shares the programming needed to project U.S. election results from state based voting precincts onto U.S. Census block group geographies. 

## Problem and Opportunity
In the United States, voting is largely a private matter. A registered voter is given a randomized ballot form or machine to prevent linkage between their voting choices and their identity. This disconnect supports confidence in the election process, but it provides obstacles to an election's analysis. A common solution is to field exit polls, interviewing voters immediately after leaving the polling location. This method is rife with bias, however, and functionally limited in direct demographics data collected. 

For the 2020 general election, most states published their election results for each voting location. These publications were additionally supported by the geographical areas assigned to each location, the voting precincts. While precinct have few demographic traits directly, their geographies have characteristics that make them projectable onto U.S. Census geographies. Both state voting precincts and Census block groups:
* are exclusive, and do not overlap
* are adjacent, fully covering their corresponding state and potentially county
* have roughly the same size in area, population and voter presence

Analytically, a projection of local demographics does not allow conclusions about voters themselves. However, the dataset does allow statements related to the geographies that yield voting behavior. One could say that an area dominated by a particular voting pattern would have mean traits of age, race, income or household structure, for example.

## Data Sources
The state election results and geographies have been compiled by [Voting and Election Science team](https://dataverse.harvard.edu/dataverse/electionscience "Voting and Election Science team") on Harvard's dataverse. State voting precincts lie within state and county boundaries.

The Census Bureau, on the other hand, publishes its estimates across a variety of geographic definitions including a hierarchy of states, counties, census tracts and block groups. [Their definitions can be found here](https://www.census.gov/programs-surveys/geography/about/glossary.html#par_textimage_4).  The geometric shapefiles for each block group [are available here](https://www2.census.gov/geo/tiger/TIGER2021/BG/).

The lowest level of this geography changes often and can obsolesce before the next census survey (Decennial or American Community Survey programs). The second to lowest census level, block groups, have the benefit of both granularity and stability however. The 2020 Decennial survey details US demographics into 217,740 block groups with between a few hundred and a few thousand people.

## Dataset Structure
The dataset's columns include:

    |Column|Definition
----|------|--------------------------------------
    |GEOID|12 digit primary key. Census GEOID of the block group row. This code concatenates 
||    2 digit state
||    3 digit county within state
||    6 digit Census Tract identifier
||    1 digit Census Block Group identifier within tract
|REP|Votes for Republican party candidate for president
|DEM|Votes for Democratic party candidate for president
|LIB|Votes for Libertarian party candidate for president
|OTH|Votes for presidential candidates other than Republican, Democratic or Libertarian
|area|square kilometers of area associated with this block group 
|gap|total area of the block group, net of area attributed to voting precincts


Additional notes and concerns:
* Votes are attributed based upon the proportion of the precinct's area that intersects the corresponding block group. Alternative methods are left to the analyst's initiative. 
* 50 states and the District of Columbia are in scope as those U.S. possessions voting in the general election for the U.S. Presidency.
* Three states did not report their results at the precinct level: South Dakota, Kentucky and West Virginia. A dummy block group is added for each of these states to maintain national totals. These states represent 2.1% of all votes cast. 
* Counties are commonly coded using FIPS codes. However, each election result file may have the county field named differently. Also, three states do not share county definitions - Delaware, Massachusetts, Alaska and the District of Columbia.
* Block groups may be used to capture geographies that do not have population like bodies of water. As a result, block groups without intersection voting precincts are not uncommon.
* In the U.S., elections are administered at a state level with the Federal Elections Commission compiling state totals against the Electoral College weights.  The states have liberty, though, to define and change their own voting precincts https://en.wikipedia.org/wiki/Electoral_precinct.

Special thanks to the meticulous efforts of 

[MIT's Election Data and Science Lab MEDSL](https://dataverse.harvard.edu/dataverse/medsl
[Voting and Election Science Team](University of Florida, Wichita State University) (https://dataverse.harvard.edu/dataverse/electionscience)

@data{DVN/K7760H_2020,
author = {Voting and Election Science Team},
publisher = {Harvard Dataverse},
title = {{2020 Precinct-Level Election Results}},
year = {2020},
version = {V29},
doi = {10.7910/DVN/K7760H},
url = {https://doi.org/10.7910/DVN/K7760H}
}
