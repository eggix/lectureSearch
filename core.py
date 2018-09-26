#!/bin/python

import requests
import re, random

BASEURL = 'https://campusonline.uni-bayreuth.de/ubto/'
COURSEURL = BASEURL + 'wbLv.wbShowLVDetail?pStpSpNr='

search = {'pSuchbegriff':'',
          'pTermSerieWochentagNr':'1', # monday:1, tuesday:2, ...
          'pTermSerieZeitVon':'1400',
          'pTermSerieZeitBis':'1600',
          'pSjNr':'1708', # <option value="-1">alle</option>, <option value="1708" selected="">2018/19</option>
          'pSemester':'W'} # all:A, summer:S, winter:W

def getID(data = search, combined = True):
    """Gets list of course IDs.
    Keyword arguments:
    data -- data for HTTP POST request
    combined -- whether lecture+tutorial (VÜ) should also be search for (default True)
    """
    resp = requests.post(BASEURL + 'wbSuche.LVSuche', data=data)
    all = re.findall('(?<=wbLv\.wbShowLVDetail\?pStpSpNr=)[0-9]+', resp.text) # all IDs, more rigid method, but not filtered
    lecture = filterType('V', resp.text)
    if combined:
        combi = filterType('VÜ', resp.text)
        res = combi + lecture
    else:
        res = lecture

    assert len(res)>0, 'Search result empty'
    return res

def filterType(t, text):
    """Filters courses for type, since type can not be searched for (as far as I now).
    Keyword arguments:
    t -- type of course as string 'V','Ü' or 'VÜ' (lecture, tutorial or combination)
    text -- HTML to search
    """
    assert t in ['V','Ü','VÜ'], 'invalid course type'
    return re.findall('(?<=<TD class="C">' + t + '<\/TD>\n<TD class="C"><A HREF="sa\.gruppen_einteilung\?clvnr=)[0-9]+', text) # kind of a hack, hope it does not break

print(COURSEURL + random.choice(getID())) # URL for random lecture
