import requests
import pandas as pd

cookie = 'udid=e3dca774d4da17d2f11adac1a56a011e; PHPSESSID=uim2tcp1q2hs0ppgfjcgvlqqre'

# 미국 주식 섹터 데이터 (NASDAQ, NYSE)
# NASDAQ
nasdaq = pd.read_csv('stock_codes/nasdaq_list_inv.csv')
# 전체 데이터의 개수 - symbol 열의 개수
print("나스닥 전체 종목 개수 : ", nasdaq['기호'].count())
# 섹터별 데이터의 개수는 3595개
nasdaq_sector_count = 3595
# 섹터가 구분되지 않은 데이터의 개수를 출력
print("나스닥에서 섹터가 구분되지 않은 종목 개수 : ", nasdaq['기호'].count()-nasdaq_sector_count)
# NYSE
nyse = pd.read_csv('stock_codes/nyse_list_inv.csv')
# 전체 데이터의 개수 - symbol 열의 개수
print("뉴욕증권거래소 전체 종목 개수 : ", nyse['기호'].count())
# 섹터별 데이터의 개수는 2978개
nyse_sector_count = 2978
# 섹터가 구분되지 않은 데이터의 개수를 출력
print("뉴욕증권거래소에서 섹터가 구분되지 않은 종목 개수 : ", nyse['기호'].count()-nyse_sector_count)

# NASDAQ
# 나스닥의 각 섹터별 데이터(url) 프레임을 만듬.
nasdaq_sector_url = pd.DataFrame({
    '금융': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=29&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '기술': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=31&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '부동산': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=33&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '산업': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=26&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소비순환재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=27&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=25&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '아카데믹 및 교육 서비스': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=36&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '에너지': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=24&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '유틸리티': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=32&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '정부활동': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=35&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '필수소비재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=28&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '헬스케어': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=2&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview'
}, index=[0])

# 각 섹터별 데이터 개수를 index[1]에 추가.
nasdaq_sector_url.loc[1] = 803, 699, 81, 313, 358, 73, 22, 83, 38, 1, 118, 1006

# url을 이용하여 각 섹터별 데이터를 가져오는 함수
def get_nasdaq_sector():

    # NASDAQ
    nasdaq_sector_save_path = "stock_codes/nasdaq_sector.csv"
    
    for i in range (len(nasdaq_sector_url.columns)):
        url = nasdaq_sector_url.iloc[0, i]
        sector = nasdaq_sector_url.columns[i]
        print(f'NASDAQ {sector} sector data is being downloaded...')
        # pn의 range의 마지막 값은 index[1]에 저장된 각 섹터별 데이터 개수를 50으로 나누었을 때 나머지가 있으면 몫에 2를 더한 값이고 나머지가 없으면 몫이다.
        if nasdaq_sector_url.iloc[1, i] % 50 == 0:
            end_range = nasdaq_sector_url.iloc[1, i] // 50 + 1
        else:
            end_range = nasdaq_sector_url.iloc[1, i] // 50 + 2
        # pn 값을 1부터 end_range까지 바꿔가며 데이터를 가져온다.
        for pn in range(1, end_range):
            url = url.replace('pn='+str(pn-1), 'pn='+str(pn))
            # postman으로 가져온 데이터를 csv로 저장한다.
            payload = {}
            headers = {
            'Cookie': cookie
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            response_noheader = response.text[response.text.find("\n")+1:]
            with open(nasdaq_sector_save_path, 'a') as f:
                f.write(response_noheader)
        print(f'NASDAQ {sector} sector data is finished.')

    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(nasdaq_sector_save_path, "r") as f:
        content = f.read()
    with open(nasdaq_sector_save_path, "w") as f:
        f.write(header + content)
    print("nasdaq_sector.csv saved")
    
    nasdaq_sector = pd.read_csv('stock_codes/nasdaq_sector.csv')
    if len(nasdaq_sector["종목명"])==nasdaq_sector_count:
        print("NASDAQ sector data is successfully downloaded.")
        nasdaq_sector['섹터'] = ''
        nasdaq_sector.loc[:802, '섹터'] = '금융'
        nasdaq_sector.loc[803:1501, '섹터'] = '기술'
        nasdaq_sector.loc[1502:1582, '섹터'] = '부동산'
        nasdaq_sector.loc[1583:1895, '섹터'] = '산업'
        nasdaq_sector.loc[1896:2253, '섹터'] = '소비순환재'
        nasdaq_sector.loc[2254:2326, '섹터'] = '소재'
        nasdaq_sector.loc[2327:2348, '섹터'] = '아카데믹 및 교육 서비스'
        nasdaq_sector.loc[2349:2431, '섹터'] = '에너지'
        nasdaq_sector.loc[2432:2469, '섹터'] = '유틸리티'
        nasdaq_sector.loc[2470:2470, '섹터'] = '정부활동'
        nasdaq_sector.loc[2471:2588, '섹터'] = '필수소비재'
        nasdaq_sector.loc[2589:, '섹터'] = '헬스케어'
        print("NASDAQ sector data is successfully categorized.")
        # 이것을 nasdaq_sector.csv로 저장한다.
        nasdaq_sector.to_csv('stock_codes/nasdaq_sector.csv', index=False)
        print("NASDAQ sector data is successfully saved.")
    else:
        print("NASDAQ sector data has error.")

# NYSE
# 뉴욕증권거래소의 각 섹터별 데이터(url) 프레임을 만듬. (정부 활동 섹터는 없음)
nyse_sector_url = pd.DataFrame({
    '금융': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=29&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '기술': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=31&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '부동산': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=33&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '산업': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=26&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소비순환재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=27&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=25&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '아카데믹 및 교육 서비스': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=36&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '에너지': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=24&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '유틸리티': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=32&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '필수소비재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=28&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '헬스케어':'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=5&sector=30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=1&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview'
}, index=[0])

# 각 섹터별 데이터 개수를 index[1]에 추가.
nyse_sector_url.loc[1] = 867, 291, 313, 340, 300, 226, 17, 240, 109, 116, 159

def get_nyse_sector():
    
    # NYSE
    nyse_sector_save_path = "stock_codes/nyse_sector.csv"
    
    for i in range (len(nyse_sector_url.columns)):
        url = nyse_sector_url.iloc[0, i]
        sector = nyse_sector_url.columns[i]
        print(f'NYSE {sector} sector data is being downloaded...')
        # pn의 range의 마지막 값은 index[1]에 저장된 각 섹터별 데이터 개수를 50으로 나누었을 때 나머지가 있으면 몫에 2를 더한 값이고 나머지가 없으면 몫이다.
        if nyse_sector_url.iloc[1, i] % 50 == 0:
            end_range = nyse_sector_url.iloc[1, i] // 50 + 1
        else:
            end_range = nyse_sector_url.iloc[1, i] // 50 + 2
        # pn 값을 1부터 end_range까지 바꿔가며 데이터를 가져온다.
        for pn in range(1, end_range):
            url = url.replace('pn='+str(pn-1), 'pn='+str(pn))
            # postman으로 가져온 데이터를 csv로 저장한다.
            payload = {}
            headers = {
            'Cookie': cookie
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            response_noheader = response.text[response.text.find("\n")+1:]
            with open(nyse_sector_save_path, 'a') as f:
                f.write(response_noheader)
        print(f'NYSE {sector} sector data is finished.')

    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(nyse_sector_save_path, "r") as f:
        content = f.read()
    with open(nyse_sector_save_path, "w") as f:
        f.write(header + content)
    print("nyse_sector.csv saved")
    
    nyse_sector = pd.read_csv('stock_codes/nyse_sector.csv')
    if len(nyse_sector["종목명"])==nyse_sector_count:
        print("NYSE sector data is successfully downloaded.")
        nyse_sector['섹터'] = ''
        nyse_sector.loc[:866, '섹터'] = '금융'
        nyse_sector.loc[867:1157, '섹터'] = '기술'
        nyse_sector.loc[1158:1470, '섹터'] = '부동산'
        nyse_sector.loc[1471:1810, '섹터'] = '산업'
        nyse_sector.loc[1811:2110, '섹터'] = '소비순환재'
        nyse_sector.loc[2111:2336, '섹터'] = '소재'
        nyse_sector.loc[2337:2353, '섹터'] = '아카데믹 및 교육 서비스'
        nyse_sector.loc[2354:2593, '섹터'] = '에너지'
        nyse_sector.loc[2594:2702, '섹터'] = '유틸리티'
        nyse_sector.loc[2703:2818, '섹터'] = '필수소비재'
        nyse_sector.loc[2819:, '섹터'] = '헬스케어'
        print("NYSE sector data is successfully categorized.")
        # 이것을 nyse_sector.csv로 저장한다.
        nyse_sector.to_csv('stock_codes/nyse_sector.csv', index=False)
        print("NYSE sector data is successfully saved.")
    else:
        print("NYSE sector data has error.")

# 한국 주식 섹터 데이터 (KOSPI, KOSDAQ)
# KOSPI
kospi = pd.read_csv('stock_codes/kospi_list_inv.csv')
# 전체 데이터 개수 - 기호 열의 개수
print("코스피 전체 종목 개수 : ", kospi['기호'].count())
# 섹터별 데이터의 개수는 937
kospi_sector_count = 937
# 섹터가 구분되지 않은 데이터의 개수를 출력
print("코스피에서 섹터가 구분되지 않은 종목 개수 : ", kospi['기호'].count()-kospi_sector_count)
# KOSDAQ
kosdaq = pd.read_csv('stock_codes/kosdaq_list_inv.csv')
# 전체 데이터의 개수 - symbol 열의 개수
print("코스닥 전체 종목 개수 : ", kosdaq['기호'].count())
# 섹터별 데이터의 개수는  1610
kosdaq_sector_count = 1610
# 섹터가 구분되지 않은 데이터의 개수를 출력
print("코스닥에서 섹터가 구분되지 않은 종목 개수 : ", kosdaq['기호'].count()-kosdaq_sector_count)

# KOSPI
# 코스피의 각 섹터별 데이터(url) 프레임을 만듬.
kospi_sector_url = pd.DataFrame({
    '금융': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=29&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '기술': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=31&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '부동산': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=33&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '산업': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=26&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소비순환재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=27&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=25&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '에너지': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=24&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '유틸리티': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=32&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '필수소비재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=28&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '헬스케어': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=60&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview'
}, index=[0])

# 각 섹터별 데이터 개수를 index[1]에 추가.
kospi_sector_url.loc[1] = 72, 83, 29, 171, 188, 187, 24, 14, 102, 67

# url을 이용하여 각 섹터별 데이터를 가져오는 함수
def get_kospi_sector():
    # KOSPI
    kospi_sector_save_path = "stock_codes/kospi_sector.csv"
    
    for i in range (len(kospi_sector_url.columns)):
        url = kospi_sector_url.iloc[0, i]
        sector = kospi_sector_url.columns[i]
        print(f'KOSPI {sector} sector data is being downloaded...')
        # pn의 range의 마지막 값은 index[1]에 저장된 각 섹터별 데이터 개수를 50으로 나누었을 때 나머지가 있으면 몫에 2를 더한 값이고 나머지가 없으면 몫이다.
        if kospi_sector_url.iloc[1, i] % 50 == 0:
            end_range = kospi_sector_url.iloc[1, i] // 50 + 1
        else:
            end_range = kospi_sector_url.iloc[1, i] // 50 + 2
        # pn 값을 1부터 end_range까지 바꿔가며 데이터를 가져온다.
        for pn in range(1, end_range):
            url = url.replace('pn='+str(pn-1), 'pn='+str(pn))
            # postman으로 가져온 데이터를 csv로 저장한다.
            payload = {}
            headers = {
            'Cookie': cookie
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            response_noheader = response.text[response.text.find("\n")+1:]
            with open(kospi_sector_save_path, 'a') as f:
                f.write(response_noheader)
        print(f'KOSPI {sector} sector data is finished.')

    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(kospi_sector_save_path, "r") as f:
        content = f.read()
    with open(kospi_sector_save_path, "w") as f:
        f.write(header + content)
    print("kospi_sector.csv saved")
    
    kospi_sector = pd.read_csv('stock_codes/kospi_sector.csv')
    if len(kospi_sector["종목명"])==kospi_sector_count:
        print("KOSPI sector data is successfully downloaded.")
        kospi_sector['섹터'] = ''
        kospi_sector.loc[:71, '섹터'] = '금융'
        kospi_sector.loc[72:154, '섹터'] = '기술'
        kospi_sector.loc[155:183, '섹터'] = '부동산'
        kospi_sector.loc[184:354, '섹터'] = '산업'
        kospi_sector.loc[355:542, '섹터'] = '소비순환재'
        kospi_sector.loc[543:730, '섹터'] = '소재'
        kospi_sector.loc[731:754, '섹터'] = '에너지'
        kospi_sector.loc[755:768, '섹터'] = '유틸리티'
        kospi_sector.loc[769:870, '섹터'] = '필수소비재'
        kospi_sector.loc[871:, '섹터'] = '헬스케어'
        print("KOSPI sector data is successfully categorized.")
        # 이것을 kospi_sector.csv로 저장한다.
        kospi_sector.to_csv('stock_codes/kospi_sector.csv', index=False)
        print("KOSPI sector data is successfully saved.")
    else:
        print("KOSPI sector data has error.")

# KOSDAQ
# 코스닥의 각 섹터별 데이터(url) 프레임을 만듬.
kosdaq_sector_url = pd.DataFrame({
    '금융': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=29&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '기술': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=31&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '부동산': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=33&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '산업': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=26&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소비순환재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=27&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '소재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=25&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '아카데믹 및 교육 서비스': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=36&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '에너지': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=24&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '유틸리티': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=32&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '필수소비재': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=28&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview',
    '헬스케어': 'https://kr.investing.com/stock-screener/Service/downloadData?download=1&country%5B%5D=11&sector=30&industry=173%2C201%2C184%2C179%2C178%2C220%2C183%2C228%2C230%2C185%2C197%2C225%2C194%2C196%2C213%2C206%2C226%2C216%2C212%2C193%2C174%2C172%2C191%2C203%2C219%2C224%2C200%2C202%2C188%2C176%2C189%2C204%2C199%2C210%2C190%2C175%2C222%2C232%2C198%2C186%2C215%2C229%2C211%2C180%2C227%2C192%2C207%2C223%2C181%2C217%2C214%2C221%2C218%2C205%2C208%2C231%2C182%2C209%2C195%2C187%2C177&equityType=ORD%2CDRC%2CPreferred%2CUnit%2CClosedEnd%2CREIT%2CELKS%2COpenEnd%2CRight%2CParticipationShare%2CCapitalSecurity%2CPerpetualCapitalSecurity%2CGuaranteeCertificate%2CIGC%2CWarrant%2CSeniorNote%2CDebenture%2CETF%2CADR%2CETC&exchange%5B%5D=110&pn=1&order%5Bcol%5D=eq_market_cap&order%5Bdir%5D=d&tab=overview'
}, index=[0])

# 각 섹터별 데이터 개수를 index[1]에 추가.
kosdaq_sector_url.loc[1] = 79, 560, 3, 255, 227, 128, 13, 14, 4, 92, 235

def get_kosdaq_sector():
    # KOSDAQ
    kosdaq_sector_save_path = "stock_codes/kosdaq_sector.csv"
    
    for i in range (len(kosdaq_sector_url.columns)):
        url = kosdaq_sector_url.iloc[0, i]
        sector = kosdaq_sector_url.columns[i]
        print(f'KOSDAQ {sector} sector data is being downloaded...')
        # pn의 range의 마지막 값은 index[1]에 저장된 각 섹터별 데이터 개수를 50으로 나누었을 때 나머지가 있으면 몫에 2를 더한 값이고 나머지가 없으면 몫이다.
        if kosdaq_sector_url.iloc[1, i] % 50 == 0:
            end_range = kosdaq_sector_url.iloc[1, i] // 50 + 1
        else:
            end_range = kosdaq_sector_url.iloc[1, i] // 50 + 2
        # pn 값을 1부터 end_range까지 바꿔가며 데이터를 가져온다.
        for pn in range(1, end_range):
            url = url.replace('pn='+str(pn-1), 'pn='+str(pn))
            # postman으로 가져온 데이터를 csv로 저장한다.
            payload = {}
            headers = {
            'Cookie': cookie
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            response_noheader = response.text[response.text.find("\n")+1:]
            with open(kosdaq_sector_save_path, 'a') as f:
                f.write(response_noheader)
        print(f'KOSDAQ {sector} sector data is finished.')

    header = "종목명,기호,종가,변동 %,시가 총액,거래량\n"
    with open(kosdaq_sector_save_path, "r") as f:
        content = f.read()
    with open(kosdaq_sector_save_path, "w") as f:
        f.write(header + content)
    print("kosdaq_sector.csv saved")
    
    kosdaq_sector = pd.read_csv('stock_codes/kosdaq_sector.csv')
    if len(kosdaq_sector["종목명"])==kosdaq_sector_count:
        print("KOSDAQ sector data is successfully downloaded.")
        kosdaq_sector['섹터'] = ''
        kosdaq_sector.loc[:78, '섹터'] = '금융'
        kosdaq_sector.loc[79:638, '섹터'] = '기술'
        kosdaq_sector.loc[639:641, '섹터'] = '부동산'
        kosdaq_sector.loc[642:896, '섹터'] = '산업'
        kosdaq_sector.loc[897:1123, '섹터'] = '소비순환재'
        kosdaq_sector.loc[1124:1251, '섹터'] = '소재'
        kosdaq_sector.loc[1252:1264, '섹터'] = '아카데믹 및 교육 서비스'
        kosdaq_sector.loc[1265:1278, '섹터'] = '에너지'
        kosdaq_sector.loc[1279:1282, '섹터'] = '유틸리티'
        kosdaq_sector.loc[1283:1374, '섹터'] = '필수소비재'
        kosdaq_sector.loc[1375:, '섹터'] = '헬스케어'
        print("KOSDAQ sector data is successfully categorized.")
        # 이것을 kosdaq_sector.csv로 저장한다.
        kosdaq_sector.to_csv('stock_codes/kosdaq_sector.csv', index=False)
        print("KOSDAQ sector data is successfully saved.")
    else:
        print("KOSDAQ sector data has error.")

if __name__ == "__main__":
    get_nasdaq_sector()
    get_nyse_sector()
    print('US (NASDAQ + NYSE) data is finished.')
    get_kospi_sector()
    get_kosdaq_sector()
    print('KR (KOSPI + KOSDAQ) data is finished.')