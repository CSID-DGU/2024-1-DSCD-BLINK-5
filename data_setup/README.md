# DB Construction
- 1, 2번은 온라인 데이터를 가져오는 과정이므로 실행하지 않아도 됩니다. (2024.04.18 기준으로 실행하여 데이터 다운로드 완료.)
- 3번 부터 차례대로 실행하면 됩니다.

## 1. get_sotck_code.py
### get csv files :
- kosdaq_list_inv.csv
- kospi_list_inv.csv
- krx_list_fdr.csv
- nasdaq_list_inv.csv
- nyse_list_inv.csv

## 2. get_sector_data.py
### get csv files :
- kosdaq_sector.csv
- kospi_sector.csv
- nasdaq_sector.csv
- nyse_sector.csv

## 3. cleaning_for_listup.ipynb
### get csv files :
- krx_list_inv.csv
- kr_list_final.csv
- kr_list_final.csv

## 4. get_each_stock_data.py
### get csv files in each folder :
- us_db folder
- kr_db folder
