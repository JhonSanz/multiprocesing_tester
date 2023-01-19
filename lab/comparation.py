import pandas as pd
import datetime

def read_report(report_mt5_file):
    df = pd.read_excel( report_mt5_file, sheet_name="Sheet1", 
    names = ["Time", "Deal", "Symbol", "Type", "Direction", "Volume", "Price", 
            "Order", "Commission", "Swap", "Profit", "Balance", "Comment"])
    index_deals = df[df["Time"] == "Time"].index.values
    df_report = df[ index_deals[0]+2: len(df.index)-1 ].reset_index(drop=True)
    df_report["Time"] = pd.to_datetime(df_report["Time"].astype(str), format="%Y/%m/%d")
    df_report["Time"] = df_report["Time"] - pd.DateOffset(minutes=1) - pd.to_timedelta(df_report["Time"].dt.second, unit='S')
    return df_report

def format_report(df):
    dff = df.groupby("Direction")
    df_in = dff.get_group("in").reset_index()
    df_out = dff.get_group("out").reset_index()
    df_report_format = pd.DataFrame()  
    df_report_format["price_open_report"]  = df_in["Price"]
    df_report_format["date_open_report"]   = df_in["Time"]
    df_report_format["type_report"]        = df_in["Type"]
    df_report_format["date_close_report"]  = df_out["Time"]
    df_report_format["price_close_report"] = df_out["Price"]
    df_report_format["comment_report"]     = df_in["Comment"]
    df_report_format["swap_report"]        = df_out["Swap"]
    df_report_format["total_report"]       = df_out["Profit"]
    df_report_format["diff_report"]        = df_out["Profit"] + df_out["Swap"]  
    return df_report_format

def read_total(ma_total_file):
    return pd.read_csv( ma_total_file, usecols = range(1, 11))
                    

def drop_excess_items(df_total, df_report):
    date_to_search = df_total.loc[0, ["date_open"]].values
    if any(df_report[df_report["date_open_report"] == date_to_search[0]]) == True:
        index_match =  df_report[df_report["date_open_report"] == date_to_search[0]].index 
        df_report.drop(range(0, index_match[0]), axis= 0, inplace= True)
        df_report = df_report.reset_index(drop=True)
        df_report.drop(range(len(df_total), len(df_report)), axis= 0, inplace= True)
        df_report = df_report.reset_index(drop=True)
        return df_report
    else:
        return "No se encontró la fecha"


def generate_not_matches(df_total, df_report, tolencia=2):
    df = pd.DataFrame()

    for i in df_total.index:
        
        if df_total.loc[ i, ["date_open"]].values != df_report.loc[ i, ["date_open_report"]].values.astype(str) \
        or (df_report.loc[ i, ["diff_report"]].values < df_total.loc[ i, ["diff"]].values - tolencia \
            or df_report.loc[ i, ["diff_report"]].values > df_total.loc[ i, ["diff"]].values + tolencia):

            value_df_total = pd.DataFrame(df_total.loc[i]).T
            value_df_report = pd.DataFrame(df_report.loc[i]).T
            values = pd.concat([value_df_total, value_df_report], axis=1, join='inner')
            df = pd.concat([df, values])

    return df.to_csv("not_matches_operations.csv")


if __name__ == "__main__":
    

    report_mt5_file = "data/asd.xlsx"
    ma_total_file = "data/4000_4000_10_totals.csv"

    df_report = format_report(read_report(report_mt5_file))
    df_total = read_total(ma_total_file)
    df_report = drop_excess_items(df_total, df_report)
    

    generate_not_matches(df_total, df_report, tolencia=2)
