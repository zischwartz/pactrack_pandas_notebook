
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import os.path

import my_keymap


# In[54]:


# Usage, to get the file:
# https://www.fec.gov/files/bulk-downloads/2018/cn18.zip
# as a dataframe
# cands = get_df('cn', [2018])

# accepts: 'cm','oth','pas2','cn','webk','ccl'

# pacs = get_df('webk', [2018], True)
# tra = get_df('webk', [2018], True)
# pacs
# pac_to_cand_transactions =  get_df('pas2', [2018], True)
# pac_to_cand_transactions =  get_df('pas2', [2018], False)
# pac_to_pac_transactions = get_df('oth', [2018])
 


# In[55]:


# This is meant to be imported as a python module, into a notebook, to make it easer to load fec data

# XXX
# XXX WARNING, TO IMPORT THIS, IT NEEDS TO BY A .py FILE, NOT AN .ipynb FILE. 
# Convert it in the container using `yarn run nbconvert`
# XXX


# In[56]:


# XXX there's no header file for webk ! 
# generated via js at: 
# https://www.fec.gov/campaign-finance-data/pac-and-party-summary-file-description/
# js
# Array.from(document.querySelectorAll('tr+ tr td:nth-child(1)')).map( x=> x.innerHTML)
webk_column_names = ["CMTE_ID", "CMTE_NM", "CMTE_TP", "CMTE_DSGN", "CMTE_FILING_FREQ", "TTL_RECEIPTS", "TRANS_FROM_AFF", "INDV_CONTRIB", "OTHER_POL_CMTE_CONTRIB", "CAND_CONTRIB", " CAND_LOANS", "TTL_LOANS_RECEIVED", "TTL_DISB", "TRANF_TO_AFF", "INDV_REFUNDS", "OTHER_POL_CMTE_REFUNDS", "CAND_LOAN_REPAY", "LOAN_REPAY", "COH_BOP", "COH_COP", "DEBTS_OWED_BY", "NONFED_TRANS_RECEIVED", "CONTRIB_TO_OTHER_CMTE", "IND_EXP", "PTY_COORD_EXP", "NONFED_SHARE_EXP", "CVG_END_DT"]


# In[57]:


# download the zip and header files for a type of record, given an array of years
def get_df(name, years=[2018], apply_amendments=False, force_data_download=False):
    # where we'll store the final result
    result_df = pd.DataFrame()
    # get the header file
    header_url = "https://www.fec.gov/data/advanced/files/bulk-downloads/data_dictionaries/{}_header_file.csv".format(name)
    header_file_name = "{}_header_file.csv".format(name)
    if not os.path.isfile(header_file_name):
        get_ipython().system(' curl -L $header_url > $header_file_name')
    head = pd.read_csv(header_file_name, header=None)
    names = head.values.tolist()[0]
    if name is 'webk':
        names = webk_column_names
    # the default
    the_dtypes = {}    
    # is it transactions? if so, make them a string, so we can parse the dates for amendments     
    if name in ['pas2', 'oth']:
        the_dtypes = {'TRANSACTION_DT': 'str'}

    # get the actual data 
    for year in years:
        # get the last two digts
        year_str = str(year)[-2:]
        # zip_file_name = "{}{}.zip".format(name, year%100)
        zip_file_name = "{}{}.zip".format(name, year_str)        
        zip_url = "https://www.fec.gov/files/bulk-downloads/{}/{}".format(year, zip_file_name)
        print('loading:', zip_file_name)
        if not os.path.isfile(zip_file_name) or force_data_download:
            print('downloading from: ', zip_url)
            get_ipython().system(' curl -L $zip_url > $zip_file_name')
        df = pd.read_csv(zip_file_name, compression='zip', sep='|', header=None, names=names, low_memory=False, dtype=the_dtypes, na_values='')

        # combine them
        result_df = pd.concat([df, result_df], ignore_index=True)
    # do we need to deal with dates and amendments, XXX maybe do this above, before combining years, might be more performant?
    if apply_amendments and name in ['pas2', 'oth']:
        # print('before', len(result_df))        
        # parse the dates 
        result_df['TRANSACTION_DT'] = pd.to_datetime(result_df['TRANSACTION_DT'], format='%m%d%Y',  errors = 'coerce') # errors = 'ignore'
        # group them by transaction id and apply the amendment, i.e. use the most recent
        # https://stackoverflow.com/a/41525937/83859
        result_df = result_df.loc[result_df.groupby('TRAN_ID')['TRANSACTION_DT'].idxmax()]
        # print('after', len(result_df))

    return result_df


# In[58]:


#  df = pd.read_csv(zip_file_name, compression='zip', sep='|', header=None, names=names, low_memory=False, date_parser=the_date_parser, parse_dates=date_cols, dtype=the_dtypes)
 
# print('You forgot to comment out your testing in download_data.ipynb. Fix it and run nbconvert')
# 


# In[3]:


# dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
# fec_dateparse = lambda x: pd.datetime.strptime(x, '%m%d%Y')
# fec_dateparse('01011981')

