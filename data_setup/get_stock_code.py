import FinanceDataReader as fdr
import requests

# cookie setting
cookie = 'udid=e3dca774d4da17d2f11adac1a56a011e; PHPSESSID=uim2tcp1q2hs0ppgfjcgvlqqre'

# Korea stock list
def get_kr_stock_code():
    
    # Download stock data from FinanceDataReader
    krx = fdr.StockListing('KRX')
    # Exclude KONEX market
    krx = krx[krx['Market'] != 'KONEX']
    # Add '.KS' or '.KQ' to the stock code
    krx['Code'] = krx.apply(lambda x: x['Code'] + '.KS' if x['Market'] == 'KOSPI' else x['Code'] + '.KQ', axis=1)
    # make stocks dataframe as csv
    krx.to_csv('stock_codes/krx_list_fdr.csv', index=False)
    print("krx_list_fdr.csv saved")
    
    # Download stock data from investing.com using Postman
    # KOSPI
    kospi_save_path = "stock_codes/kospi_list_inv.csv"
    
    for i in range(1, 20):
        
        url = f"https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=29%2C34%2C31%2C33%2C26%2C27%2C25%2C36%2C24%2C32%2C35%2C28%2C30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn={i}&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview"
        payload = {}
        headers = {
        'Cookie': cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response_noheader = response.text[response.text.find("\n")+1:]
        with open(kospi_save_path, "a") as f:
            f.write(response_noheader)
        print(f"pn={i} done")
        
    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(kospi_save_path, "r") as f:
        content = f.read()
    with open(kospi_save_path, "w") as f:
        f.write(header + content)
    print("kospi_list_inv.csv saved")
    
    # KOSDAQ
    kosdaq_save_path = "stock_codes/kosdaq_list_inv.csv"
    
    for i in range(1, 36):
        
        url = f"https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=29%2C34%2C31%2C33%2C26%2C27%2C25%2C36%2C24%2C32%2C35%2C28%2C30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn={i}&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview"
        payload = {}
        headers = {
        'Cookie': cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response_noheader = response.text[response.text.find("\n")+1:]
        with open(kosdaq_save_path, "a") as f:
            f.write(response_noheader)
        print(f"pn={i} done")
        
    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(kosdaq_save_path, "r") as f:
        content = f.read()
    with open(kosdaq_save_path, "w") as f:
        f.write(header + content)
    print("kosdaq_list_inv.csv saved")
    
# US stock list
def get_us_stock_code():
    
    # NASDAQ
    nasdaq_save_path = "stock_codes/nasdaq_list_inv.csv"
    
    for i in range(1, 75):
        url = f"https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=29%2C34%2C31%2C33%2C26%2C27%2C25%2C36%2C24%2C32%2C35%2C28%2C30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn={i}&order%5Bcol%5D=viewData.symbol&order%5Bdir%5D=d&tab=overview"
        payload = {}
        headers = {
        'Cookie': cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response_noheader = response.text[response.text.find("\n")+1:]
        with open(nasdaq_save_path, "a") as f:
            f.write(response_noheader)
        print(f"pn={i} done")
        
    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(nasdaq_save_path, "r") as f:
        content = f.read()
    with open(nasdaq_save_path, "w") as f:
        f.write(header + content)
    print("nasdaq_list_inv.csv saved")

    # NYSE
    nyse_save_path = "stock_codes/nyse_list_inv.csv"

    for i in range(1, 62):
        url = f"https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=29%2C34%2C31%2C33%2C26%2C27%2C25%2C36%2C24%2C32%2C35%2C28%2C30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn={i}&order%5Bcol%5D=viewData.symbol&order%5Bdir%5D=a&tab=overview"
        payload = {}
        headers = {
        'Cookie': cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response_noheader = response.text[response.text.find("\n")+1:]
        with open(nyse_save_path, "a") as f:
            f.write(response_noheader)
        print(f"pn={i} done")

    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(nyse_save_path, "r") as f:
        content = f.read()
    with open(nyse_save_path, "w") as f:
        f.write(header + content)
    print("nyse_list_inv.csv saved")
    
if __name__ == '__main__':
    get_kr_stock_code()
    print('KR data is finished.')
    get_us_stock_code()
    print('US data is finished.')