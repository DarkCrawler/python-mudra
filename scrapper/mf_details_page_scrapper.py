import urllib2
from bs4 import BeautifulSoup
import mf_equity_distribution_scrapper as equitycrawler

'''
mfcode -
plan -
plan_option -
plan_type -
nav_change_abs -
nav_change_percent-
riskometer -
fund_family -
fund_class - 

returns (list) -
absolute_returns (list) - 
category_ret_diff -
minimum_investment

equitylist (list)

'''


def _scrap_detail_mf(_mf_object):
    _mf_page = urllib2.urlopen(_mf_object.fund_url)
    _mf_url_split = _mf_object.fund_url.split('/')
    _mf_object.mfcode = _mf_url_split[len(_mf_url_split) - 1]
    soup = BeautifulSoup(_mf_page, 'html.parser')

    # Plan  type details:
    details_split_text = soup.find('div', attrs={'class': 'bsns_pcst FL'}).get_text().split('|')

    for str in details_split_text:
        trim_text = str.strip()
        details_type = trim_text[0]
        details_val = trim_text[1]

        if details_type.lower() == 'plan':
            _mf_object.plan = details_val

        if details_type.lower() == 'option':
            _mf_object.plan_option = details_val

        if details_type.lower() == 'type':
            _mf_object.plan_type = details_val

    # Current nav change and %
    try:
        greenchange = soup.find('span', attrs={'class': 'grnpc1'})
        if greenchange != None:
            # read green change and %
            greenchange = soup.find('span', attrs={'class': 'grnpc1'}).get_text()
            index_brac_open = greenchange.find('(')
            index_percentage = greenchange.find('%')
            percentage_change = greenchange[index_brac_open + 1: index_percentage]
            abs_change = greenchange[0:index_brac_open - 1]
            _mf_object.nav_change_abs = abs_change.strip()
            _mf_object.nav_change_percent = percentage_change.strip()
        else:
            redchange = soup.find('span', attrs={'class': 'redpc1'}).get_text()
            index_brac_open = redchange.find('(')
            index_percentage = redchange.find('%')
            percentage_change = redchange[index_brac_open + 1: index_percentage]
            abs_change = redchange[0:index_brac_open - 1]
            _mf_object.nav_change_abs = abs_change.strip()
            _mf_object.nav_change_percent = percentage_change.strip()
    except Exception as e:
        print "Error in fetching NAV changes for : ", _mf_object.name, ".....", _mf_object.fund_url
        # raise e

    # Riskometer:
    try:
        var_meters = soup.findAll('div', attrs={'class': 'mufndBx'})
        for meters in var_meters:
            meters_text = meters.get_text()
            if meters_text.find('Riskometer') != -1:
                riskometer_text = meters.find('div', attrs={'class': 'muttxtdn'}).get_text()
                space_index = riskometer_text.find('\n')
                _mf_object.riskometer = riskometer_text[0:space_index]

            if meters_text.find('FUND Family') != -1:
                _mf_object.fund_family = meters.find('div', attrs={'class': 'muttxtdn'}).get_text()

            if meters_text.find('FUND Class') != -1:
                _mf_object.fund_class = meters.find('div', attrs={'class': 'muttxtdn'}).get_text()
    except Exception as e:
        print "Error in fetching Riskometer data for : ", _mf_object.name, ".....", _mf_object.fund_url
        # raise e

    # returns - have to find the definition  of this
    try:
        returns_data_rows = \
            soup.findAll('div', attrs={'class': 'clearfix hist_tbl left_align tbl_oddwrp MT2 mb-2'})[0].findAll(
                'tbody')[
                1].findAll('tr')
        returns_data = []
        for row in returns_data_rows:
            cols = row.findAll('td')
            ret_dict = {}
            for index, col in enumerate(cols):
                if index == 0:
                    ret_dict['period'] = col.get_text()
                if index == 1:
                    ret_dict['returns'] = col.get_text()
                if index == 2:
                    ret_dict['rank'] = col.get_text()
            returns_data.append(ret_dict)

        _mf_object.returns = returns_data
    except Exception as e:
        print "Error in fetching returns data for : ", _mf_object.name, ".....", _mf_object.fund_url
        # raise e

    # absolute returns (%)
    try:
        tab_with_abs_ret_class = soup.findAll('div', attrs={'class': 'clearfix hist_tbl tbl_oddwrp MT2'})
        abs_return_data_list = []
        for tab in tab_with_abs_ret_class:
            tab_text = tab.get_text()
            if tab_text.find('Year') != -1:
                returns_tbody = tab.findAll('tbody')[1]
                returns_row = returns_tbody.findAll('tr')

                for row in returns_row:
                    cols = row.findAll('td')
                    abs_ret_dict = {}

                    for index, col in enumerate(cols):
                        if index == 0:
                            abs_ret_dict['year'] = col.get_text()
                        if index == 1:
                            abs_ret_dict['qtr1'] = col.get_text()
                        if index == 2:
                            abs_ret_dict['qtr2'] = col.get_text()
                        if index == 3:
                            abs_ret_dict['qtr3'] = col.get_text()
                        if index == 4:
                            abs_ret_dict['qtr4'] = col.get_text()
                        if index == 5:
                            abs_ret_dict['annual'] = col.get_text()
                    abs_return_data_list.append(abs_ret_dict)

        _mf_object.absolute_returns = abs_return_data_list
    except Exception as e:
        print "Error in fetching absolute returns returns data for : ", _mf_object.name, ".....", _mf_object.fund_url
        # raise e

    # category return diff:::
    try:
        cat_average = {}
        rows = soup.findAll('div', attrs={'class': 'MT30'})[0].findAll('table')[0].findAll('tbody')[1].findAll('tr')
        for row in rows:
            if row.get_text().find('Difference of Fund returns and Category returns') != -1:
                cols = row.findAll('td')
                for index, col in enumerate(cols):
                    if index == 1:
                        cat_average['1 month'] = col.get_text()
                    if index == 2:
                        cat_average['3 month'] = col.get_text()
                    if index == 3:
                        cat_average['6 month'] = col.get_text()
                    if index == 4:
                        cat_average['1 year'] = col.get_text()
                    if index == 5:
                        cat_average['2 year'] = col.get_text()
                    if index == 6:
                        cat_average['3 year'] = col.get_text()
                    if index == 7:
                        cat_average['5 year'] = col.get_text()
        _mf_object.category_ret_diff = cat_average
    except Exception as e:
        print "Error in fetching cateogry returns returns data for : ", _mf_object.name, ".....", _mf_object.fund_url
        # raise e

    # investor level info:
    try:
        investor_info_uls = soup.findAll('ul', attrs={'class': 'investr_info'})
        for ul in investor_info_uls:
            if ul.get_text().find('Minimum Investment') != -1:
                lis = ul.findAll('lis')
            for li in lis:
                if li.get_text().find('Minimum Investment') != -1:
                    _mf_object.minimum_investment = li.get_text().split(":")[1]
    except Exception as e:
        print "Error in fetching investor level data for : ", _mf_object.name, ".....", _mf_object.fund_url
        # raise e

    print "Detials page crawling of constrution of MF :", _mf_object.mfcode, " :: ", _mf_object.name, " completed, moving on to crawl for sector and equity ditribution crawling"

    equitycrawler._crawl_sector_and_equity_distribution(_mf_object)
