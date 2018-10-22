import urllib2
from bs4 import BeautifulSoup
from models.layer1 import Layer1MFModel

# from ..models import Layer1MFModel

_parentURL = 'http://www.moneycontrol.com'
_pageURL = 'http://www.moneycontrol.com/mutual-funds/top-rated-funds'


def scanPageAndGetPrimaryMFList():
    _mf_scanned_list = []
    print("Scanning main page and getting primary list of Mutual funds data::::")
    page = urllib2.urlopen(_pageURL)
    soup = BeautifulSoup(page, 'html.parser')
    _mf_tables = soup.findAll('table', attrs={'class': 'tblfund'})

    try:
        for tableData in _mf_tables:
            rows = tableData.findAll('tr')

            for row in rows:
                mf_main_model = Layer1MFModel.Layer1MFModelClass()
                colsinrow = row.findAll('td')
                if len(colsinrow) > 0:
                    for num, cols in enumerate(colsinrow):
                        if num == 0:
                            atag = cols.find('a')
                            mf_main_model.name = atag.get_text()
                            mf_main_model.fund_url = _parentURL + atag['href']

                        if num == 1:
                            mf_main_model.crisil_ranking = cols.get_text()

                        if num == 2:
                            mf_main_model.nav = cols.get_text()

                        if num == 3:
                            mf_main_model.yearly_return = cols.get_text()

                        if num == 4:
                            mf_main_model.aum = cols.get_text()
                            _mf_scanned_list.append(mf_main_model)
                else:
                    mf_main_model.fund_type = row.findAll('th')[0].get_text()


    except Exception as e:
        print "Error in scanning in main.py::", type(e)
        raise

    print "Main page scan result ::: Scanned a total of :: ", _mf_scanned_list.__len__(), " Mutual Fund records for url ::", _pageURL
    return _mf_scanned_list


scanPageAndGetPrimaryMFList()
