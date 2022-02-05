#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

These functions download and unzip the state based files needed for blockgroupvoting allocations.

https://www2.census.gov/geo/tiger/TIGER2021/BG/    get the file lists

"""
import wget
from zipfile import ZipFile

def get_blockgroups():
    """
    Downloads the state based files that have shapes for Census block groups
    :return: null
    """
    statefips = ['01','02','04','05','06','08','09','10','11','12','13', \
                 '15','16','17','18','19','20','21','22','23','24','25', \
                 '26','27','28','29','30','31','32','33','34','35','36', \
                 '37','38','39','40','41','42','44','45','46','47','48', \
                 '49','50','51','53','54','55','56','60','66','69','72','78']

    datapath = "D:/Open Environments/data/census/tiger/getdata/"

    for s in statefips:
        fn = 'tl_2021_' + s + '_bg.zip'
        url = 'https://www2.census.gov/geo/tiger/TIGER2021/BG/' + fn
        wget.download(url, out=datapath)
        with ZipFile(datapath + fn, 'r') as Z:
           Z.extractall(datapath + fn[:-4])

def get_electionresults():
    """
    Download the 2020 dataset from here, unzip its main file then unzip state files
    https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/K7760H
    """

def get_ACS5YR():
    """
    D:\Open Environments\data\census\tiger\ACS_2019_5YR_BG\ACS_2019_5YR_BG.gdb    
    """"""
