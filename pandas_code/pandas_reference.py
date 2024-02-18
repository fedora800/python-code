import pandas as pd
import numpy as np

dataset_file_1="car_data.csv"           # https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho
'''
    Car_Name  Year  Selling_Price  Present_Price  Kms_Driven Fuel_Type Seller_Type Transmission  Owner
0       ritz  2014           3.35           5.59       27000    Petrol      Dealer       Manual      0
1        sx4  2013           4.75           9.54       43000    Diesel      Dealer       Manual      0
'''
AXIS_ROWS=0        # default value of axis
AXIS_COLUMNS=1

# --------------------------------------------------------------------------------
def fn_00_get_dataframe_info(df):
  print('TODO')
  print('**IMP**')
  print('Index of 1st column = 0')
  print('like shape, no cols, no rows, etc etc, column names')
  print(df)
  print(df.describe())  # gives stats like count, mean, std dev etc for each column
  print(df.info())   # num_rows, num_cols, datatypes of each column, memory usage
  print("Total number of rows = ", df.shape[0])
  print("Total number of columns = ", df.shape[1])
  

  if df.empty:
    print("df is EMPTY")
  else
    print("df is NOT empty")

  # To print ALL the rows of the df, instead of the default
  # Save the original setting
  original_max_rows = pd.get_option('display.max_rows')
  # Set option to display all rows
  pd.set_option('display.max_rows', None)
  # Your DataFrame
  print(df)
  # Reset the option to its original value
  pd.reset_option('display.max_rows')


# --------------------------------------------------------------------------------
def fn_01_data_section():

  fn_01_A_load_csv_file()
  fn_01_B_save_as_csv_file()


def  fn_01_A_load_csv_file(csv_fname):
  # check data_set_file_1 
  df = pd.read_csv(csv_fname)
  return df
  
def fn_01_B_save_as_csf_file(df):

  csv_file_path = 'path/to/your/file.csv'
  
  # Write the DataFrame to the CSV file
  #To save the index (like Date is the index for yfinance price data df), we need to explicitly mention like below
  # This will include the "Date" column as the first column in the CSV file
  # df.to_csv(csv_file_path, index=True)
  # else to exclude the index altogether (which is the DEFAULT)
  df.to_csv('your_file.csv', index=False)

  print(f'DataFrame written to file - {csv_file_path}')


# --------------------------------------------------------------------------------
def fn_02_manipulate_rows_and_columns(df):
  print(' --- fn_02 ---')
  print('--before--'); print(df.tail())
  #fn_02_A_delete_rows(df)
  #fn_02_B_delete_columns(df)
  fn_02_C_add_columns(df)
  #fn_02_C_apply_scalar_on_all_items_of_a_column(df)


def fn_02_A_delete_rows(df):
  print('--before--'); print(df.tail())

  print('Deleting rows based on 1 column criteria - method 1')
  # rows where the condition is False will be excluded, effectively deleting them from the DataFrame
  df_tmp1 = df[df['Kms_Driven'] < 20000]
  print('Deleting rows based on 1 column criteria - method 2')
  df_tmp2 = df.query('Kms_Driven < 20000')

def fn_02_B_delete_columns(df, axis=AXIS_COLUMNS):
  print('--before--'); print(df.tail())

  print('Dropping 3 columns by using their COLUMN NAMES ...')
  #df.drop(columns=['Car_Name', 'Year', 'Selling_Price'], inplace=True)
  df_tmp1 = df.drop(columns=['Car_Name', 'Year', 'Selling_Price'])
  print('--after--'); print(df_tmp1.tail())

  print('Dropping 3 columns by using their INDEX ...')
  df_tmp2 = df.drop(columns=df.columns[1:3])    # index of 1st column =0
  print('--after--'); print(df_tmp2.tail())

  print('Dropping 3 columns by only mentioning the ones we want to KEEP (negation) ...')
  df_tmp3 = df[['Present_Price','Kms_Driven','Fuel_Type','Seller_Type','Transmission','Owner']]
  print('--after--'); print(df_tmp3.tail())

  print('Renaming specific column names...')
  df_tmp4 = df.rename(columns={'Car_Name': 'NameOfCar', 'Fuel_Type': 'TypeOfFuel', 'Year': 'YearMade'})
  print('--after--'); print(df_tmp4.tail())

#    Car_Name  Year  Selling_Price  Present_Price  Kms_Driven Fuel_Type Seller_Type Transmission  Owner
#0       ritz  2014           3.35           5.59       27000    Petrol      Dealer       Manual      0


def fn_02_C_add_columns(df, axis=AXIS_COLUMNS):
  print('--before--'); print(df.tail())

  print('Adding 1 new column with a hardcoded static value (at the end)...')
  df_tmp1 = df
  df_tmp1["Country"] = "India"
  print('--after--'); print(df_tmp1.tail())

  print('Adding 1 new column with column values from another dataframe ...')
  print('*IMP* - the dfs should have matching indices')
  df_tmp2 = df
  df_tmp2["Price_Difference"] = df["Selling_Price"] - df["Present_Price"]
  print('--after--'); print(df_tmp2.tail())

  print("Adding multiple columns at the end of existing df with NaN values")
  # Define the names of the new columns
  new_columns = ['ema_5', 'ema_13', 'sma_50', 'sma_200', 'rsi_14', 'macd_sig_hist', 'dm_dp_adx', 'crs_50']
  # Use df.assign() to add the new columns with NaN values
  df_tmp3 = df.assign(**{col: np.nan for col in new_columns})
  # -- OR --
  # Add new columns with explicit NaN values for all rows
  df_tmp3[new_columns] = np.nan
  print('--after--'); print(df_tmp3.tail())




def fn_02_C_apply_scalar_on_all_items_of_a_column(df):
  # below with multiply each value in the column by 10
  # -- method 1 -- lambda function --
  #df['Present_Price'] = df['Present_Price'].apply(lambda x: x*10)
  # -- method 2 -- operation directly on the dataframe --
  df['Present_Price'] = df['Present_Price']*10
  print('--after--'); print(df.tail())


# --------------------------------------------------------------------------------
def fn_02_D_change_others(df):


  print("---------- to change index -----------")
  print('--before--'); print(df.tail(2))

  '''
  In case data shows like this - 
              Symbol,Open,High,Low,Close,Volume
  Date
  2023-01-03   MSFT,243.0800018310547,245.75,237.39999389648438,239.5800018310547,25740000
  2023-01-04   MSFT,232.27999877929688,232.8699951171875,225.9600067138672,229.10000610351562,50623400
  2023-01-05   MSFT,227.1999969482422,227.5500030517578,221.75999450683594,222.30999755859375,39585600

    where Date is a part of the dataframe INDEX
    we need to convert it to a column of it's own standing if we need to better handling charting Date on the X axis
  '''

  #If you want to reset the index and make the "Date" column a part of the DataFrame itself, you can use the reset_index method and specify drop=False. 
  # After this operation, your DataFrame should have the "Date" column as a regular column rather than an index.
  #df.reset_index(drop=False, inplace=True)

  #If you want to remove the "Date" column from the index and keep it as an index, you can use:
  # This will remove the "Date" column from the index and keep only the default integer index.
  #df.reset_index(drop=True, inplace=True)

  df.reset_index(inplace=True)
  print('--after--'); print(df.tail(2))

  '''
  df becomes like this - 
    Date,Symbol,Open,High,Low,Close,Volume
  0  2023-01-03,MSFT,243.0800018310547,245.75,237.39999389648438,239.5800018310547,25740000
  1  2023-01-04,MSFT,232.27999877929688,232.8699951171875,225.9600067138672,229.10000610351562,50623400
  2  2023-01-05,MSFT,227.1999969482422,227.5500030517578,221.75999450683594,222.30999755859375,39585600
  '''  


  print("---------- to convert all headers fields to lowercase -----------")
  df.columns = df.columns.str.lower()






# --------------------------------------------------------------------------------
def fn_03_find_in_dataframe(df):
  print("----- fn_03_find_in_dataframe -----")
  #find first N columns
  N = 5
  subset = df.iloc[:,0:N]

  # find numeric columns only 
  subset =  df.select_dtypes(include = 'number')

  # find all excluding numeric columns 
  subset =  df.select_dtypes(exclude = 'number')

  # pass a list of columns and keep only those columns which name matches a value in the list:
  subset = df.loc[:,df.columns.isin(['area', 'salary'])]

  # look for a specific string in a column name and retain those columns only
  subset = df.loc[:,df.columns.str.find('addre') > -1]

  # get columns whose name starts with a specific string
  #subset = candidates.loc[:,candidates.columns.str.startswith('addr')]

  #find last row of df as a SERIES
  ps_last_row = df.iloc[-1]   # returns a series

  # find the first and last row of df and return them as a dataframe
  df_head_foot = pd.concat([df.head(1), df.tail(1)])
  print("df with only header and footer rows = ", df_head_foot)

  # find a value of a particular cell (ie row and column)
  # for symbol column from the 1st row of df
  str_symbol = df.iloc[0]["symbol"]

  # find missing (NaN - Not a Number) values in a df
  fn_03_A_find_missing_NAN(df)

# --------------------------------------------------------------------------------
def fn_03_A_find_missing_NAN(df):
  """
  The df.isna() method in pandas is used to check for missing or NaN (Not a Number) values in a DataFrame. 
  It returns a DataFrame of the same shape as the input DataFrame (df), where each element is a boolean value 
  indicating whether the corresponding element in the original DataFrame is missing or not.
  """

  # Create a DataFrame with some missing values
  data = {'A': [1, 2, None, 4], 'B': [5, None, 7, 8]}
  df = pd.DataFrame(data)
  print(df)
  # Output:
  #      A    B
  # 0  1.0  5.0
  # 1  2.0  NaN
  # 2  NaN  7.0
  # 3  4.0  8.0

  # Check for missing values
  df_missing_values = df.isna()
  # In the resulting missing_values DataFrame, True indicates a missing value, while False indicates a non-missing (or present) value.
  # This can be useful for various data cleaning and preprocessing tasks where you need to identify and handle missing values appropriately.

  print(df_missing_values)
  # Output:
  #        A      B
  # 0  False  False
  # 1  False   True
  # 2   True  False
  # 3  False  False

  # Create a boolean mask for the rows you want to update
  mask = df["B"].isna()
  # Set values in column B to 999 where they were NaN before, using the mask
  df.loc[mask, "B"] = 999

  print(df)
  # Output:
  #     A      B
  #0  1.0    5.0
  #1  2.0  999.0
  #2  NaN    7.0
  #3  4.0    8.0





# --------------------------------------------------------------------------------
def fn_04_date_related(df):

  df_sym['Date'] = pd.to_datetime(df_sym['Date'])     # convert Date to a datetime object

def fn_05_lambda_functions(df):
  # multiplies each value in the COLUMN by 2.5
  # note - lambda function WILL CHANGE the values directly in the df
  df['Present_Price'] = df['Present_Price'].apply(lambda x: x*2.5)


# --------------------------------------------------------------------------------
def fn_06_pandas_series(df_cars):

  ps_lastrow = df_return.iloc[-1]   # returns a series
  print(ps_lastrow["Car_Name"])  # by index label
  print(ps_lastrow.iloc[0])  # by position

  ps_subset = ps_lastrow[1:3]  # gets elements from position 1 to 3
  ps_filtered = ps_lastrow[ps_lastrow > 15]   # it will compare each element for this condition and only those elements that satisfy will be picked


# --------------------------------------------------------------------------------
def fn_07_pandas_df_referencing(df):
  # THIS IS VERY IMPORTANT TO UNDERSTAND 
  # by default, when we assign a df to another, it will create a REFERENCE to the original DataFrame,
  # NOT a new copy. Therefore, changes made to one DataFrame WILL affect the other.
  
  print("----- fn_07_pandas_df_referencing -----")
  print('--before--'); print(df.tail())

  # changes the original df
  print('Changing the original df when changing another df assigned to it ...')
  # this will change the original df
  df_tmp1 = df
  df_tmp1["newcol_1"] = "AAA"
  print(df_tmp1)
  print('--after   original df = '); print(df.tail())

  # create independent copy of the df
  print('Creating an independent seperate copy of the original df ...')
  df_tmp2 = df.copy()
  df_tmp2["newcol_2"] = "BBB"
  print(df_tmp2)
  print('--after   original df = '); print(df.tail())

  # for loop
  print('Going through the entire df in a loop and using the columns ...')
  for index, row in df.iterrows():
    print(f"Car Name: {row['Car_Name']}, Selling Price: {row['Selling_Price']}")


# --------------------------------------------------------------------------------

def fn_08_using_multiple_dataframes(df1, df2):
  '''
In pandas, you can combine two DataFrames in several ways depending on your requirements. Here are some common methods:

    Concatenation (Stacking):
    You can concatenate two DataFrames along rows (axis=0) or columns (axis=1) using the concat function:

    python

import pandas as pd

df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

# Concatenate along rows (axis=0)
result = pd.concat([df1, df2])

# Concatenate along columns (axis=1)
result = pd.concat([df1, df2], axis=1)

Merging:
If you have common columns in both DataFrames and you want to merge them based on these columns, you can use the merge function:

python

import pandas as pd

df1 = pd.DataFrame({'key': ['A', 'B'], 'value': [1, 2]})
df2 = pd.DataFrame({'key': ['A', 'B'], 'value': [3, 4]})

result = pd.merge(df1, df2, on='key')

This is similar to SQL-style joins.

Appending:
If you want to append one DataFrame to another, you can use the append method:

python

    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

    result = df1.append(df2, ignore_index=True)

    The ignore_index=True parameter resets the index.

Choose the method that best fits your use case based on whether you want to concatenate, merge, or append the DataFrames.  
  '''

# --------------------------------------------------------------------------------
def main():

  df_cars = fn_01_A_load_csv_file(dataset_file_1)
  fn_00_get_dataframe_info(df_cars)
  #fn_02_manipulate_rows_and_columns(df_cars)
  #fn_03_find_in_dataframe(df_cars)
  #fn_04_date_related(df_cars)
  #fn_05_lambda_functions(df_cars)
  #fn_06_pandas_series(df_cars)
  fn_07_pandas_df_referencing(df_cars)
  fn_08_using_multiple_dataframes(df_cars, df_xxxx_todo)



# --------------------------------------------------------------------------------
# --- main ---
if __name__ == '__main__':
  main()

# --- todo ---
#https://saturncloud.io/blog/converting-object-column-in-pandas-dataframe-to-datetime-a-data-scientists-guide/    datetime conversion


'''
https://linuxhint.com/pandas-pct-change/
# Percentage change across columns
print(stocks.pct_change(axis=0),"\n")

# Percentage change across rows
print(stocks.pct_change(axis=1),"\n")

'''




