# Check the data & extract symbols
import pandas as pd
import yfinance as yf
import pytz
import os

# US
df_us = pd.read_csv("stock_codes/us_list_final.csv")
us_symbols = df_us["기호"].tolist()
# KR
df_kr = pd.read_csv("stock_codes/kr_list_final.csv")
kr_symbols = df_kr["기호"].tolist()

# duplicate error check function
def duplicate_error_check(df):
    if df["기호"].duplicated().sum()==0:
        print("No duplicate data error :)")
    else:
            print("Error Detected: Duplicate data exists!")
            print("중복 기호 개수 : ", df["기호"].duplicated().sum())

duplicate_error_check(df_us)
duplicate_error_check(df_kr)

# Float error check & fixed
def float_error_check(symbols, df):
    if [s for s in symbols if isinstance(s, float)]==[]:
        print("No float data error :)")
    else:
        print("Error Detected: Float data exists!")
        print(df[df['기호'].apply(lambda x: isinstance(x, float))])
        df['기호'] = df['기호'].apply(lambda x: str(x))
        symbols = df['기호'].tolist()
        if [s for s in symbols if isinstance(s, float)]==[]:
            print("Fixed! No float data error anymore :)")
        else:
            print("Error still exists.")
            
float_error_check(us_symbols, df_us)
float_error_check(kr_symbols, df_kr)

# directory setting
os.makedirs("us_db", exist_ok=True)
os.makedirs("kr_db", exist_ok=True)
os.makedirs("us_db/NASDAQ", exist_ok=True)
os.makedirs("us_db/NYSE", exist_ok=True)
os.makedirs("kr_db/KOSPI", exist_ok=True)
os.makedirs("kr_db/KOSDAQ", exist_ok=True)

dt = pd.Timestamp

# Timezone for US
tz_us = pytz.timezone("America/New_York")
end_us = tz_us.localize(dt(2023,12,31))

# Timezone for Korea
tz_kr = pytz.timezone("Asia/Seoul")
start_kr = tz_kr.localize(dt(1960,1,1))
end_kr = tz_kr.localize(dt(2023,12,31))

# 미국 주식 데이터를 yahoo finance로 다운로드 하는 함수를 만드는데, us_symbols 리스트에 들어있는 미국 주식 종목 코드를 돌려가면서 다운로드를 시도하며, df_us에서 각 종목별 거래소 정보를 이용하여 해당 종목이 NASDAQ인지 NYSE인지에 따라 다운로드 폴더를 나누어 저장한다.
def download_us_yf(symbols, df, end_date):
    for symbol in symbols:
        try:
            exchange = df[df["기호"]==symbol]["거래소"].values[0]
            data = yf.download(symbol, end=end_date)
            data.to_csv(f"us_db/{exchange}/{symbol}.csv")
            print(f"{symbol} done")
        except Exception as e:
            print(f"{symbol} error")

# TO DO: 한국 주식 데이터는 야후 파이낸스로 다운로드 시 2000년 부터 다운로드 가능하므로 1900년대 데이터를 얻기 위해서는 다른 방법을 찾아야함.

# 대신증권 Cybos Plus가 좋아보이나, 윈도우 환경에서만 사용 가능하다. (윈도우 컴에서 아나콘다 환경 만들어서 사용해야함 - python3.8)
# import platform
# assert platform.architecture()[0] == '32bit'
# from koapy import CybosPlusEntrypoint

# 그 대안으로 pykrx 사용한다.
# https://github.com/sharebook-kr/pykrx
from pykrx import stock
from pykrx import bond

# 한국 주식 데이터를 pykrx로 다운로드 하는 함수를 만드는데, kr_symbols 리스트에 들어있는 한국 주식 종목 코드를 돌려가면서 다운로드를 시도하며, df_kr에서 각 종목별 거래소 정보를 이용하여 해당 종목이 KOSPI인지 KOSPDAQ인지에 따라 다운로드 폴더를 나누어 저장한다.
def download_kr_pykrx(start_date, end_date, symbols, df):
    for symbol in symbols:
        try:
            market = df[df["기호"]==symbol]["거래소"].values[0]
            data = stock.get_market_ohlcv(start_date, end_date, symbol)
            data.to_csv(f"kr_db/{market}/{symbol}.csv")
            print(f"{symbol} done")
        except Exception as e:
            print(f"{symbol} error")

# Run function
download_us_yf(us_symbols, df_us, end_us)
download_kr_pykrx(start_kr, end_kr, kr_symbols, df_kr)