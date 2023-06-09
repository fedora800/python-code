# this is to handle the swiss NCARes file for compliance
#from datetime import datetime
import datetime
import jaydebeapi
import pandas as pd

DB_HOST="VAPLEAP.liquidnet.biz"
DB_SERVICE_NAME = "njpleap"
DB_USERID = "sshinde"
DB_PASSWORD = "01feb22#"
DB_CONN_JDBC_URL = "jdbc:oracle:thin:@VAPLEAP.liquidnet.biz:1521/njpleap"
JAR_FILE = "C:/myapps/dbeaver/plugins/ojdbc6.jar"
DRIVER = "oracle.jdbc.OracleDriver"
SQL_QUERY_1 = "SELECT COUNT(*) FROM REG_PROD.REG_MIFID2_RESPONSE WHERE CREATE_DATE_TIME > SYSDATE-1"
SQL_QUERY_2 = "SELECT * FROM REG_PROD.TRANSACTION_REPORTING_RESPONSE WHERE FILE_SUBMISSION_DATE = TO_NUMBER(TO_CHAR(SYSDATE-1, 'YYYYMMDD')) AND RESPONSE_FILE_NAME LIKE '%FinFrag%NCARes%'"
# SQL_QUERY_3 = """SELECT MIC_CODE, ISIN, FILE_SUBMISSION_DATE, ERROR_ID, ERROR_MSG, TRUNC(create_date_time) RESPONSE_DATE, 
# RECORD_STATUS, FILE_SEQ_NUM, RESPONSE_FILE_NAME, REPORT_NAME, FILE_STATUS
# FROM REG_PROD.REG_MIFID2_RESPONSE WHERE CREATE_DATE_TIME > SYSDATE-1 AND RECORD_STATUS='RJCT' AND ISIN LIKE 'FR0000%' """
 


url = 'jdbc:oracle:thin:@192.168.0.13:1521:JGD'
user = 'aaaaa'
password = 'xxxxx'
dirver = 'oracle.jdbc.OracleDriver'
jarFile = '/Users/warrior/Code/project/builder/ojdbc6-11.2.0.1.0.jar'
sqlStr = 'select * from T_ERP_MAT_IMGEXG'

def connect_to_database():
    # https://pypi.org/project/JayDeBeApi/
    #jdbc_conn = jaydebeapi.connect("jdbc:oracle:thin:.", {'user': DB_USERID, 'password': DB_PASSWORD, 'other_property': "foobar"}, "/path/to/hsqldb.jar",)
    print(datetime.datetime.now(), ' - Connecting to DB : ', DB_CONN_JDBC_URL)
    jdbc_conn = jaydebeapi.connect(DRIVER, DB_CONN_JDBC_URL, [DB_USERID, DB_PASSWORD], JAR_FILE)
    #jdbc_conn = jaydebeapi.connect(dirver, url, [user, password], jarFile)
    #jdbc_conn = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver', 'jdbc:oracle:thin:sshinde/01feb22#@//DB_HOST_IP:1521/DB_NAME')
    return jdbc_conn

def get_db_rows(conn, sql_query):
    print(datetime.datetime.now(), ' - Running SQL Query : ', sql_query)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    print('Rows returned = ', len(results))
    for x in results:
        print(x)
    cursor.close()
    conn.close()
    print(datetime.datetime.now(), ' - Completed SQL query')

    print('\nConverting results to pandas dataframe ...')
    df = pd.DataFrame(results)
    print(df)

    print('\Writing to Excel file ...')
    workbook_fd = pd.ExcelWriter('test_file_excel.xlsx')
    df.to_excel(workbook_fd, sheet_name='tab1', index=False)
    workbook_fd.save()


# Step 2: Insert a row into Oracle table

# Here's a simple example of how to execute an insert statement to test the connection to the database. The script inserts a new record to the EMP table.

# cursor = cnxn.cursor()
# cursor.execute("INSERT INTO EMP (EMPNO, ENAME, JOB, MGR) VALUES (535, 'Scott', 'Manager', 545)") 
# Step 3: Retrieve data from Oracle table

# The cursor.execute() function retrieves rows from the select query on a dataset. The cursor.fetchone() function iterates over the result set returned by cursor.execute() while the print() function prints out all records from the table to the console.

# cursor = cnxn.cursor()	
# cursor.execute("SELECT * FROM EMP") 
# row = cursor.fetchone() 
# while row:
#     print (row) 
#     row = cursor.fetchone()


def main():
    db_conn = connect_to_database()
    get_db_rows(db_conn, SQL_QUERY_2)

if __name__ == '__main__':
    main()

print('Exiting..')

