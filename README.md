# blockgroupvoting
This repository holds programming needed to projecting U.S. election results from state based voting precincts onto U.S. Census block group geographies.

The Census Bureau, of course, publishes its estimates across a variety of geographic definitions.  One most familiar includes a hierarchy of census tracts within counties, block groups within tracks and blocks themselves.  The lowest level of this geography changes often and can obsolesce before the next census survey (Decennial or American Community Survey programs). The second to lowest census level, block groups, have the benefit of both granularity and stability however. The 2020 Decennial survey details US demographics into 217,740 block groups with between a few hundred and a few thousand people.

     https://www.census.gov/programs-surveys/geography/about/glossary.html#par_textimage_4
     Note: block groups may also be used to capture geographies that do not have population like bodies of water.
     
The Census provides various dimensions of people and households, it does not survey peoples' opinions or behavior.
The most public of these resides in voting results.  U.S. elections are administered at a state level with the Federal Elections Commission compiling totals against the Electoral College weights.  The states have liberty, though, to define their own voting geographies called precincts https://en.wikipedia.org/wiki/Electoral_precinct.  Collecting these state based geographies is painstakingly done by academics including 

      MIT's Election Data and Science Lab (MEDSL) https://dataverse.harvard.edu/dataverse/medsl
      The Voting and Election Science Team (University of Florida, Wichita State University) https://dataverse.harvard.edu/dataverse/electionscience

@data{DVN/K7760H_2020,
author = {Voting and Election Science Team},
publisher = {Harvard Dataverse},
title = {{2020 Precinct-Level Election Results}},
year = {2020},
version = {V29},
doi = {10.7910/DVN/K7760H},
url = {https://doi.org/10.7910/DVN/K7760H}
}
