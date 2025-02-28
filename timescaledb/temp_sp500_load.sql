
\copy tbl_price_data_1day (pd_time,pd_symbol,open,high,low,close,volume) FROM '~/git-projects/python-code/timescaledb/data/sp500symbols/AAPL.csv' DELIMITER ',' CSV HEADER;


$ head -n2 symbols_insert.csv
^ABNB
^APO

$ grep -f symbols_insert.csv sp500_companies_list.csv
Symbol,Security,GICS Sector,GICS Sub-Industry,Headquarters Location,Date added,CIK,Founded
ABNB,Airbnb,Consumer Discretionary,"Hotels, Resorts & Cruise Lines","San Francisco, California",2023-09-18,1559720,2008
APO,Apollo Global Management,Financials,Asset Management & Custody Banks,"New York City, New York",2024-12-23,1858681,1990

$ grep -f symbols_insert.csv sp500_companies_list.csv |  sed 's/"//g' | awk -F',' '{print $1, ", \"" $2 "\""}'
Symbol, "Security"
ABNB, "Airbnb"
APO, "Apollo Global Management"
BRK.B, "Berkshire Hathaway"
BX, "Blackstone Inc."


$ grep -f symbols_insert.csv sp500_companies_list.csv |  sed 's/"//g' | awk -F',' '{print $1, ",\"" $2 "\""}' > to_load.csv
$ sed -i 's/BRK.B/BRK-B/' to_load.csv
$ sed -i 's/BF.B/BF-B/' to_load.csv



-- Step 1: Create a temporary table to load CSV data
CREATE TEMP TABLE temp_instrument (
    symbol TEXT,
    name TEXT
);

-- Step 2: Copy data into the temporary table
COPY temp_instrument (symbol, name)
FROM 'C:\mytmp\downloads\scratch\to_load.csv'
DELIMITER ',' CSV HEADER;

select * from temp_instrument;

-- Step 3: Insert data into tbl_instrument with 'STOCK' as asset_type
INSERT INTO tbl_instrument (symbol, name, asset_type, note_1)
SELECT symbol, name, 'STOCK', 'SP500' FROM temp_instrument;
