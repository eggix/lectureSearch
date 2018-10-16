#!/bin/python

import requests
import re, random

BASEURL = 'https://campusonline.uni-bayreuth.de/ubto/'
COURSEURL = BASEURL + 'wbLv.wbShowLVDetail?pStpSpNr='

search = {'pSuchbegriff':'',
          'pTermSerieWochentagNr':'1', # monday:1, tuesday:2, ...
          'pTermSerieZeitVon':'1400',
          'pTermSerieZeitBis':'1600',
          'pSjNr':'1708', # <option value="-1">alle</option>, <option value="1708">2018/19</option>
          'pSemester':'W'} # all:A, summer:S, winter:W

def getID(data = search, ctype = ['V','VÜ']):
    """Gets list of course IDs.
    Keyword arguments:
    data -- data for HTTP POST request
    ctype -- type of course as list of strings; 'V','Ü' or 'VÜ' (lecture, tutorial or combination) (default ['V','VÜ'])
    """
    resp = requests.post(BASEURL + 'wbSuche.LVSuche', data=data)
    all = re.findall('(?<=wbLv\.wbShowLVDetail\?pStpSpNr=)[0-9]+', resp.text) # all IDs, more rigid method, but not filtered

    res = []
    for t in ctype:
        res = res + filterType(t, resp.text)

    assert len(res)>0, 'Search result empty'
    return res

def filterType(ctype, text):
    """Filters courses for type, since type can not be searched for (as far as I now).
    Keyword arguments:
    ctype -- type of course as string 'V','Ü' or 'VÜ' (lecture, tutorial or combination)
    text -- HTML to search
    """
    assert ctype in ['V','Ü','VÜ'], 'invalid course type'
    return re.findall('(?<=<TD class="C">' + ctype + '<\/TD>\n<TD class="C"><A HREF="sa\.gruppen_einteilung\?clvnr=)[0-9]+', text) # kind of a hack, hope it does not break

print(COURSEURL + random.choice(getID())) # URL for random lecture
