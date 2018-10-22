import scrapper.init_page_scrapper as _init_page_scrapper
import scrapper.mf_details_page_scrapper as _details_page_crawler


def scrap_main_page():
    mf_scan_list = _init_page_scrapper.scanPageAndGetPrimaryMFList()
    print "Initial list of mutual funds contains :: ", mf_scan_list.__len__(), " , nos of scanned Mutual funds"
    for mf in mf_scan_list:
        scrap_details_page(mf)


def scrap_details_page(_mfundObj):
    # scraps details of mutual fund and also build the equity and sector distribution
    print "Scrapping....", _mfundObj.name
    _details_page_crawler._scrap_detail_mf(_mfundObj)


scrap_main_page()
