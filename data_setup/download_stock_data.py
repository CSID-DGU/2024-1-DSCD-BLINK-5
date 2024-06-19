# Download stock data from yfinance, using the extracted stock code above
import pandas as pd
import yfinance as yf
import pytz

def get_us_stock_data():
    # Check the data & extract symbols
    # NASDAQ
    df_nas = pd.read_csv("stock_codes/nasdaq_list.csv")
    print(df_nas.shape)
    print("중복 기호 개수 : ", df_nas["기호"].duplicated().sum())
    nas_symbols = df_nas["기호"].tolist()
    print(len(nas_symbols))
    # NYSE
    df_nyse = pd.read_csv("stock_codes/nyse_list.csv")
    print(df_nyse.shape)
    print("중복 기호 개수 : ", df_nyse["기호"].duplicated().sum())
    nyse_symbols = df_nyse["기호"].tolist()
    print(len(nyse_symbols))
    
    # Float error check & fixed
    # NASDAQ
    print([s for s in nas_symbols if isinstance(s, float)]) 
    print(df_nas[df_nas['기호'].apply(lambda x: isinstance(x, float))])
    df_nas['기호'] = df_nas['기호'].apply(lambda x: str(x))
    nas_symbols = df_nas['기호'].tolist()
    print([s for s in nas_symbols if isinstance(s, float)])
    # NYSE
    print([s for s in nyse_symbols if isinstance(s, float)])

    # Timezone setting
    dt = pd.Timestamp
    tz_us = pytz.timezone("America/New_York")
    # start_us = tz_us.localize(dt(2010,1,1))
    end_us = tz_us.localize(dt(2023,12,31))

    # download data
    nas = yf.download(nas_symbols, end=end_us)
    nyse = yf.download(nyse_symbols, end=end_us)

    nas.to_csv('stock_data/nas.csv')
    nyse.to_csv('stock_data/nyse.csv')

    # Exclude the data with download failed error
    '''
    fail_nas = ['OPHV', 'ELEP', 'HWEP', 'PRSRW', 'OXACW', 'TEDU', 'BTWNW', 'BIOS', 'TDTH', 'LFAC', 'VACC', 'RLND', 'TMKRU', 'ZBAO', 'SMXT', 'GUTS', 'SUGP', 'WETH', 'YIBO', 'ALAB', 'DYCQU', 'ZOOZ', 'UBXG', 'AFJK', 'TELO', 'ANSC', 'BCG', 'ROMA', 'CGON', 'AMIX', 'MGX', 'KYTX', 'BKHAU', 'LGCL', 'LOBO', 'BTSG', 'SUUN', 'JVSAU', 'ZPTA', 'JVSA', 'INTJ', 'KSPI', 'BTSGU', 'HAO', 'GRDI', 'IROH', 'AITR', 'CORZ', 'JL', 'PLMJU', 'DHAI', 'CCTG', 'EPRX', 'IBACU', 'FBLG', 'AVBP', 'MAMO', 'BOLD', 'CTNM', 'HLXB', 'MNDR', 'CLBTW', 'HTZWW', 'EVLVW', 'XOSWW', 'KPLTW', 'CXAIW', 'RUMBW', 'DWACW', 'GGROW', 'OXBRW', 'CSSEL', 'NTHI', 'NVNIW', 'SYTAW', 'ORGNW', 'MTRS']
    tickers = [t for t in nas_symbols if t not in fail_nas]
    nas = yf.download(tickers, start=start, end=end)

    fail_nyse = ['GS_PC', 'WEL_U', 'PHYT_U', 'PEB_PH', 'SITC_PA', 'RCFA_U', 'MNTN_U', 'EBRB', 'PEB_PE', 'PCG_PH', 'MAA_PI', 'WSOB', 'MS_PE', 'EFC_PC', 'CADE_PA', 'LGFA', 'AHL_PD', 'ACP_PA', 'GUT_PC', 'AKOA', 'WRB_PF', 'BML_PH', 'IVR_PB', 'KIM_PL', 'USB_PA', 'SCE_PJ', 'ABR_PD', 'ATH_PE', 'NCV_PA', 'PSFE_T', 'AMH_PG', 'ECC_PD', 'PHGE_U', 'APCA_U', 'SB_PC', 'PRIF_PK', 'EPR_PE', 'GS_PK', 'RRAC_U', 'AGM_PG', 'GEHI', 'C_PJ', 'JPM_PJ', 'CWENA', 'HYAC_U', 'BFAC_U', 'TNP_PE', 'SRG_PA', 'PMT_PC', 'EFC_PE', 'ALL_PB', 'UWMC_T', 'CNDA_U', 'MITT_PB', 'GNL_PB', 'BML_PJ', 'ACHR_T', 'SCE_PM', 'MS_PA', 'GE_W', 'RWT_PA', 'PCG_PD', 'TY_P', 'PCG_PI', 'ECF_PA', 'CMRE_PD', 'MS_PF', 'HEIA', 'AMH_PH', 'AKOB', 'EQC_PD', 'SBXC_U', 'RF_PC', 'AGMA', 'INN_PE', 'GMRE_PA', 'GLOG_PA', 'BRKB', 'DBRG_PI', 'PGSS_U', 'CMS_PB', 'TWO_PC', 'APO_PA', 'BHR_PD', 'DSAQ_U', 'GNL_PA', 'RF_PB', 'MET_PA', 'PW_PA', 'NLY_PF', 'MITT_PA', 'O_P', 'CIM_PA', 'ACR_PD', 'GLU_PB', 'TRTN_PE', 'OPP_PB', 'PSEC_PA', 'LAC_W', 'AHT_PD', 'GNL_PD', 'BLUA_U', 'RITM_PB', 'CSR_PC', 'IVR_PC', 'PRIF_PH', 'PSA_PG', 'PRIF_PD', 'CHMI_PA', 'AXS_PE', 'PRIF_PG', 'TRTN_PB', 'DLR_PK', 'EFC_PA', 'SCE_PL', 'CLDT_PA', 'RJF_PB', 'SNV_PE', 'PBRA', 'GEFB', 'RC_PC', 'NYCB_PU', 'CHMI_PB', 'PEB_PF', 'DX_PC', 'GAB_PK', 'OAK_PA', 'GGT_PE', 'XFLT_PA', 'GAQ_U', 'MTB_PH', 'SNV_PD', 'NGL_PB', 'CTA_PB', 'SEDA_U', 'AL_PA', 'MFA_PB', 'NFYS_U', 'PRIF_PJ', 'AULT_PD', 'BW_PA', 'SEAL_PA', 'OPP_PA', 'AGM_PD', 'ADRT_U', 'GTNA', 'PCG_PB', 'MS_PK', 'SCE_PG', 'CIM_PB', 'TRIS_U', 'BML_PL', 'DLNG_PB', 'BFB', 'TRTX_PC', 'PRIF_PF', 'ARR_PC', 'TRTN_PD', 'UHALB', 'EP_PC', 'KREF_PA', 'GNT_PA', 'TCOA_U', 'LEGT_U', 'TWO_PA', 'GLOP_PA', 'JPM_PC', 'EFC_PB', 'NXDT_PA', 'GLOP_PB', 'NGL_PC', 'BRKA', 'CIM_PC', 'NS_PB', 'ICR_PA', 'REXR_PC', 'GGN_PB', 'WNNR_U', 'BAC_PE', 'BAC_PM', 'GPMT_PA', 'DLNG_PA', 'AGM_PF', 'BNREA', 'NCZ_PA', 'VCXB_U', 'PRE_PJ', 'GDV_PH', 'PEB_PG', 'GDV_PK', 'UMH_PD', 'EVE_U', 'SHO_PH', 'NLY_PI', 'DRH_PA', 'CTA_PA', 'RITM_PD', 'SACH_PA', 'GGT_PG', 'SHO_PI', 'EPR_PG', 'YCBD_PA', 'JOBY_T', 'DBRG_PJ', 'CODI_PB', 'CDR_PB', 'PRIF_PI', 'ATCO_PH', 'AHH_PA', 'CUBI_PE', 'CTO_PA', 'F_PC', 'WFC_PL', 'LEV_T', 'IIPR_PA', 'SEAL_PB', 'ABR_PF', 'PBI_PB', 'TRTN_PC', 'SPLP_PA', 'BML_PG', 'HPP_PC', 'AHL_PC', 'SCE_PH', 'RLJ_PA', 'SB_PD', 'BIOB', 'OSI_U', 'AEVA_T', 'BIP_PA', 'WFC_PY', 'LGFB', 'ABR_PE', 'BEP_PA', 'RHE_PA', 'FRT_PC', 'VNO_PM', 'NS_PA', 'GDL_PC', 'DSX_PB', 'BC_PB', 'GTLS_PB', 'WCC_PA', 'VNO_PL', 'PCG_PE', 'PMT_PA', 'MKCV', 'AGM_PE', 'BAC_PL', 'STT_PG', 'ATEK_U', 'RC_PE', 'CMRE_PC', 'SLG_PI', 'EFC_PD', 'INN_PF', 'BCV_PA', 'MER_PK', 'GAB_PG', 'KCGI_U', 'C_PN', 'BIP_PB', 'NEE_PN', 'OAK_PB', 'GNL_PE', 'CODI_PC', 'AHT_PF', 'PSA_PF', 'CMRE_PB', 'EPR_PC', 'MDV_PA', 'DMYY_U', 'REXR_PB', 'CIO_PA', 'AHT_PI', 'GRP_U', 'SCE_PK', 'HFRO_PA', 'GLTA', 'DLR_PL', 'AGM_PC', 'MFA_PC', 'NREF_PA', 'PCG_PA', 'LFT_PA', 'NLY_PG', 'ATCO_PD', 'TNP_PF', 'GLU_PA', 'F_PB', 'NSA_PA', 'BFA', 'PMT_PB', 'HVTA', 'GLOP_PC', 'LCW_U', 'HWM_P', 'CLBR_U', 'BC_PA', 'ET_PE', 'KEY_PI', 'RITM_PC', 'GLP_PB', 'CODI_PA', 'PRIF_PL', 'FBRT_PE', 'TRTL_U', 'TWO_PB', 'AHT_PG', 'LENB', 'WRB_PE', 'CORR_PA', 'DLR_PJ', 'GS_PD', 'BITE_U', 'BC_PC', 'CUBI_PF', 'PCG_PC', 'MS_PI', 'HL_PB', 'RITM_PA', 'QBTS_T', 'MITT_PC', 'SPNT_PB', 'TRTN_PA', 'MOGB', 'CDR_PC', 'IFIN_U', 'ACR_PC', 'VNO_PN', 'CIGC', 'DBRG_PH', 'GSL_PB', 'VNO_PO', 'HIPO_T', 'AHT_PH', 'MOGA', 'GAB_PH', 'AACT_U', 'GAM_PB', 'GS_PA', 'GLP_PA', 'USB_PH', 'EQH_PC', 'RMPL_P', 'RIV_PA', 'NS_PC', 'PCG_PG', 'CIM_PD', 'OXY_T', 'CMRE_PE', 'JWSM_U', 'ET_PI', 'ETI_P', 'LPA', 'OBDE', 'AHR', 'RYDE', 'RDDT', 'MSDL', 'LEGT', 'SOLV', 'CHRO', 'MMA', 'ANRO', 'ECCF', 'TBBB', 'NCDL', 'SYNX', 'DXYZ', 'UMAC', 'CLBR', 'AUNA', 'AXIL', 'SDHC', 'GEV', 'PMNT', 'AS', 'PSBD', 'SING', 'CRDB', 'LXP_PC', 'TAPA', 'EAI', 'CRDA', 'ULS', 'BHA', 'IBTA', 'SPG_PJ', 'EMP', 'PACS']
    tickers = [t for t in nyse_symbols if t not in fail_nyse]
    nyse = yf.download(tickers, start=start, end=end)
    '''
    
    
def get_kr_stock_data():
    # Load stock list
    stocks = pd.read_csv('stock_codes/krx_stocklist.csv')
    kr_symbols = stocks['Code'].tolist()

    # Timezone setting
    dt = pd.Timestamp
    tz_kr = pytz.timezone("Asia/Seoul")
    # start_kr = tz_kr.localize(dt(2010,1,1))
    end_kr = tz_kr.localize(dt(2023,12,31))

    # download data
    krx = yf.download(kr_symbols, end=end_kr)
    krx.to_csv('stock_data/krx.csv')
    

if __name__ == '__main__':
    get_kr_stock_data()
    print('kr data is downloaded.')
    
    get_us_stock_data()
    print('us data is downloaded.')