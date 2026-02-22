# This document outlines he Aquis Python test as part of our interview process. With this
# document there will be an attached file test_data.zip. This file contains details of orders and
# trades on the Aquis platform for 2022-11-24.
# Please note, this is not a complete days’ worth of data.
# Please complete as many of the below tasks within one hour and provide your answers in
# csv form or xls and the version of python used.
# Tasks
# 1. Return the earliest time that an order and trade were made
# 2. Return the latest order and trade
# 3. Total number of trades
# 4. Total number or orders buy , total number of orders sell
# 5. Total value of orders buy/sell per security
# 6. Total Value of Trades by security
# 7. Total volume of trades by security
# 8. Total volume of orders by security for buys , total volume of orders by security for sells
# 9. VWAP by security
# Information:
# The file is tab delimited.
# Trading commences at 08.00 am UK time but times in the file are in UTC.
# Security id’s range between 1 – 9999

import os
import pandas as pd

#F_INPUT = "test_data_SAMPLE.tsv"
F_INPUT = "test_data"
F_4_ORDERADD = "test_data_4_ORDERADD.tsv"
F_7_TRADECOMBINED = "test_data_7_TRADECOMBINED.tsv"
F_11_STOCK = "test_data_11_STOCK.tsv"
F_33_ORDER_ADD_EXTENDED = "test_data_33_ORDERADD_EXTENDED.tsv"
F_50_TRADECOMBINED_EXTENDED = "test_data_50_TRADECOMBINED_EXTENNDED.tsv"
F_TEMP_FILE = "temp.tsv"


def fn_extract_order_related_info():

  df = pd.read_csv("test_data_4_ORDERADD.tsv", sep="\t")
  df = df[df["timestamp"] != "timestamp"]   # remove duplicate header row if it exists
  # generate and add a field with a utc python datetime data type from the timestamp field in the file
  df["timestamp"] = df["timestamp"].astype("int64")     # convert timestamp to int
  df["dt_timestamp"] = pd.to_datetime(df["timestamp"] // 1000, unit="us", utc=True)   # convert long number nanos to micros
  df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
  df["limitPrice"] = pd.to_numeric(df["limitPrice"], errors="coerce")
  df["side"] = pd.to_numeric(df["side"], errors="coerce")
  #print(df.columns)
  #print(df.head())

  timestamp_earliest_order = df["dt_timestamp"].min()
  print("\n1A - Timestamp of the Earliest Order : ")
  print(timestamp_earliest_order)
  timestamp_latest_order = df["dt_timestamp"].max()
  print("\n2A - Timestamp of the Latest Order :")
  print(timestamp_latest_order)
  num_buy_orders = (df["side"] == 1).sum()
  num_sell_orders = (df["side"] == 2).sum()
  print("\n4 - Total number or orders buy and Total number of orders sell : ")
  print( num_buy_orders, '\t', num_sell_orders)

  df["order_value"] = df["quantity"] * df["limitPrice"]
  # group by securityId
  df_total_order_value_per_security = df.groupby(["securityId"])["order_value"].sum().reset_index()
  print("\n5 - Total value of orders buy/sell per security : ")
  print(df_total_order_value_per_security)

  # 8. Total volume of orders by security for buys, total volume of orders by security for sells
  df_buy_orders = df[df["side"] == 1]
  df_sell_orders = df[df["side"] == 2]
  df_buy_volume_per_security = df_buy_orders.groupby("securityId")["quantity"].sum().reset_index()
  df_sell_volume_per_security = df_sell_orders.groupby("securityId")["quantity"].sum().reset_index()
  # Rename columns as it's now sum of the quantity per symbol and not just quantity
  df_buy_volume_per_security.rename(columns={"quantity": "buy_volume"}, inplace=True)
  df_sell_volume_per_security.rename(columns={"quantity": "sell_volume"}, inplace=True)
  print("\n8 - Total volume of orders per security (buys & sells) =")
  print(df_buy_volume_per_security)
  print(df_sell_volume_per_security)




def fn_extract_trade_related_info():

  df = pd.read_csv("test_data_7_TRADECOMBINED.tsv", sep="\t")
  df = df[df["timestamp"] != "timestamp"]   # remove duplicate header row if it exists
  # generate and add a field with a utc python datetime data type from the timestamp field in the file
  df["timestamp"] = df["timestamp"].astype("int64")     # convert timestamp to int
  df["dt_timestamp"] = pd.to_datetime(df["timestamp"] // 1000, unit="us", utc=True)   # convert long number nanos to micros
  df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
  df["price"] = pd.to_numeric(df["price"], errors="coerce")
  df["side"] = pd.to_numeric(df["side"], errors="coerce")
  #print(df.columns)
  #print(df.head())

  timestamp_earliest_trade = df["dt_timestamp"].min()
  print("\n1B - Timestamp of the Earliest Trade : ")
  print(timestamp_earliest_trade)
  timestamp_latest_trade = df["dt_timestamp"].max()
  print("\n2B - Timestamp of the Latest Trade : ")
  print(timestamp_latest_trade)

  # Total number of trades
  total_trades = len(df)
  print("\n3 - Total number of trades : ")
  print(total_trades)
  df_trades = df[df["quantity"] > 0]
  #print("Number of trades where executed quantity > 0 = ", len(df_trades))

  # 6. Total Value of Trades by security
  df["trade_value"] = df["quantity"] * df["price"]
  # group by securityId and sum trade_value
  df_total_trade_value_per_security = df.groupby("securityId")["trade_value"].sum().reset_index()
  print("\n6 - Total Value of Trades by security : ")
  print(df_total_trade_value_per_security)

  # 7. Total volume of trades by security
  # Step 1: Group by securityId and sum the quantity (trade volume)
  df_total_trade_volume_per_security = df.groupby("securityId")["quantity"].sum().reset_index()
  # Rename column as it's now sum of the quantity per symbol and not just quantity
  df_total_trade_volume_per_security.rename(columns={"quantity": "trade_volume"}, inplace=True)
  print("\n7 - Total volume of trades per security : ")
  print(df_total_trade_volume_per_security)

  # 9. VWAP by security
  # group by securityId and get for each security the sum of trade_value column and the sum of quantity column
  # trade_value was computed earlier as quantity * price for each trade
  #print(df[["quantity", "price", "trade_value"]].head(5))
  df_vwap = df.groupby("securityId").agg({"trade_value": "sum", "quantity": "sum"}).reset_index()
  # now calculate VWAP
  # ie total trade_value / total quantity
  df_vwap["vwap"] = df_vwap["trade_value"] / df_vwap["quantity"]
  print("\n9 - VWAP by security : ")
  print(df_vwap[["securityId", "vwap"]])


def fn_split_tsv_file_into_multiple_files():
  
  with open(F_INPUT, 'r') as fh_inpfile, \
    open(F_4_ORDERADD, 'w') as fh_4_orderadd, \
    open(F_7_TRADECOMBINED, 'w') as fh_7_tradecombined, \
    open(F_11_STOCK, 'w') as fh_11_stock:

    for line in fh_inpfile:
      if line.startswith("4") or line.startswith("33\t"):   # for 33, ignore the headers and append  into the orderadd file
        fh_4_orderadd.write(line)
      elif line.startswith("7") or line.startswith("50\t"):   # for 50, ignore the headers and append into the tradecombined file
        fh_7_tradecombined.write(line)
      elif line.startswith("11"):
        fh_11_stock.write(line)

  # keep only required columns
  orders_columns_to_keep = ["timestamp", "securityId", "side", "quantity", "limitPrice"]
  with open(F_4_ORDERADD, "r") as infile, open(F_TEMP_FILE, "w") as outfile:
    # write header first
    outfile.write("\t".join(orders_columns_to_keep) + "\n")
    for line in infile:
      line_cols = line.rstrip("\n").split("\t")
      required_cols = [line_cols[5], line_cols[8], line_cols[11], line_cols[12], line_cols[13]]
      outfile.write("\t".join(required_cols) + "\n")
  # overwrite original file with this specific columns file
  os.replace(F_TEMP_FILE, F_4_ORDERADD)

  trades_columns_to_keep = ["timestamp", "securityId", "side", "quantity", "price"]
  with open(F_7_TRADECOMBINED, "r") as infile, open(F_TEMP_FILE, "w") as outfile:
    # write header first
    outfile.write("\t".join(trades_columns_to_keep) + "\n")
    for line in infile:
      line_cols = line.rstrip("\n").split("\t")
      required_cols = [line_cols[5], line_cols[17], line_cols[21], line_cols[14], line_cols[15]]
      outfile.write("\t".join(required_cols) + "\n")
  # overwrite original file with this specific columns file
  os.replace(F_TEMP_FILE, F_7_TRADECOMBINED)


def main():
  pd.set_option("display.max_rows", None)
  fn_split_tsv_file_into_multiple_files()
  fn_extract_order_related_info()
  fn_extract_trade_related_info()


# --- main ---
if __name__ == '__main__':
  # main(sys.argv)
  main()

#     need to print all rows of df not just their default
