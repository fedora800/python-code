import pandas as pd
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
  print(df.tail())
  print(df.describe())
  print(df.info())   # num_rows, num_cols, datatypes of each column, memory usage

# --------------------------------------------------------------------------------
def fn_01_load_data_section():

  fn_01_A_load_csv_file()


def  fn_01_A_load_csv_file(csv_fname):
  df = pd.read_csv(csv_fname)
  return df
  

# --------------------------------------------------------------------------------
def fn_02_manipulate_rows_and_columns(df):
  fn_02_A_delete_rows(df)
  fn_02_B_delete_columns(df)

def fn_02_A_delete_rows(df):
  print('')

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

#    Car_Name  Year  Selling_Price  Present_Price  Kms_Driven Fuel_Type Seller_Type Transmission  Owner
#0       ritz  2014           3.35           5.59       27000    Petrol      Dealer       Manual      0

# --------------------------------------------------------------------------------
def fn_03_find_in_dataframe(df):

  '''
  #find first N columns
  subset = candidates.iloc[:,0:N]

  # find numeric columns only 
  subset =  candidates.select_dtypes(include = 'number')

  # find all excluding numeric columns 
  subset =  candidates.select_dtypes(exclude = 'number')

  # pass a list of columns and keep only those columns which name matches a value in the list:
  subset = candidates.loc[:,candidates.columns.isin(['area', 'salary'])]

  # look for a specific string in a column name and retain those columns only
  subset = candidates.loc[:,candidates.columns.str.find('addre') > -1]

  # get columns whose name starts with a specific string
  #subset = candidates.loc[:,candidates.columns.str.startswith('addr')]

  ''' 

# --------------------------------------------------------------------------------
def main():

  df_cars = fn_01_A_load_csv_file(dataset_file_1)
  fn_00_get_dataframe_info(df_cars)
  #fn_02_manipulate_rows_and_columns(df_cars)
  #fn_03_find_in_dataframe(df_cars)


# --------------------------------------------------------------------------------
# --- main ---
if __name__ == '__main__':
  main()

