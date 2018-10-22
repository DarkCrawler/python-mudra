import urllib2
from bs4 import BeautifulSoup
from dbhandler import MFDetailsPersistor as persistor


def _crawl_sector_and_equity_distribution(_mf_object):
    mf_code = _mf_object.mfcode
    allocation_url = 'https://www.moneycontrol.com/india/mutualfunds/mfinfo/sector_allocation/' + mf_code
    _distribution_page = urllib2.urlopen(allocation_url)

    soup = BeautifulSoup(_distribution_page, 'html.parser')
    details_divs = soup.findAll('div', attrs={'class': 'MT10'})

    sector_dist_list = []
    sector_equity_dist_list = []
    current_sector = ''
    for div in details_divs:
        if div.find('table') != None:
            info_table = div.find('table')
            rows = info_table.findAll('tr')

            for index, row in enumerate(rows):

                if index > 0:
                    if row.find('strong') != None:
                        # logic to extract sector
                        sector_info = {}
                        cols = row.findAll('td')
                        for colindex, col in enumerate(cols):
                            if colindex == 0:
                                sector_info['sector_name'] = col.get_text()
                                if current_sector != col.get_text():
                                    current_sector = col.get_text()

                            if colindex == 1:
                                sector_info['sector_investment_value'] = col.get_text()

                            if colindex == 3:
                                sector_info['sector_investment_percentage'] = col.get_text()

                        sector_dist_list.append(sector_info)

                    else:
                        # logic to extract equity
                        equity_info = {}
                        cols = row.findAll('td')
                        for colindex, col in enumerate(cols):
                            if colindex == 0:
                                equity_info['equity_name'] = col.get_text()

                                equity_info['equity_link'] = col.find('a')['href']
                                equity_info['equity_sector'] = current_sector

                            if colindex == 1:
                                equity_info['equity_investment_value'] = col.get_text()

                            if colindex == 2:
                                equity_info['equity_qtty'] = col.get_text()

                            if colindex == 3:
                                equity_info['equity_percentage_investment'] = col.get_text()

                        sector_equity_dist_list.append(equity_info)

    _mf_object.sector_distribution = sector_dist_list
    _mf_object.sector_equity_distribution = sector_equity_dist_list

    print "Completed scanning sector and equity distribution for MF:: ", _mf_object.name, ":: moving to crete model and commiting to database"
    persistor.transformAndInsert(_mf_object)
