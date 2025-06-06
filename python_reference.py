"""
 Imports should be grouped in the following order:

Standard library imports.
Related third party imports.
Local application/library specific imports.
You should put a blank line between each group of imports.
"""

import sys
import inspect
#import logging
from loguru import logger
import pandas as pd
from utils import connect_to_db_using_sqlalchemy
#import utils

def get_arguments_info():

  """Gives understanding about the arguments passed at command line
  needs sys module

  Parameters:
  aaaa

  Returns:
  bbbb
  """

  print("list of command-line arguments (including scriptname) = ", sys.argv)
  print("number of command-line arguments (including scriptname) = ", len(sys.argv))
  print("this scriptname that was run =  ", sys.argv[0])
  '''
  eg - 
  $ python python_reference.py aaa bbb ccc 123 "hello world"
  list of command-line arguments (including scriptname) =  ['python_reference.py', 'aaa', 'bbb', 'ccc', '123', 'hello world']
  number of command-line arguments (including scriptname) =  6
  this scriptname that was run =   python_reference.py
  '''

  # also refer to getopt and argparse modules - https://www.tutorialspoint.com/python/python_command_line_arguments.htm


def use_environment_variables_linux():
  import os
  home_dir = os.environ.get("HOME")
  app_version = os.getenv('APP_VERSION', '0.0.1')  # Default to '0.0.1' if not set

  print(home_dir)
  print(f"Starting application version: {app_version}")

  if home_dir:
   sys.path.append(os.path.join(home_dir, "git-projects/python-code"))
   sys.path.append(f"{home_dir}/git-projects/python-code/pkg_common")

  # will print all env variables
  for data in os.environ:
    #print(f"--------data={data}-------value={os.environ[data]}----------")
    print(f"{data}={os.environ[data]}")

  # prints the dictionary of all env variables 
  print(os.environ)

  for key, value in os.environ.items():
    print(f'{key}: {value}')


  # sorted
  for name, value in sorted(os.environ.items()):
     print("   " + name + "=" + value)

  print(os.environ.get('APPENV', 'staging'))    # only returns value of staging if the env variable APPENV does not exist, does NOT set APPENV variable

  try:                                        # to check if the key exists 
    os.environ["APPENV"]
  except KeyError: 
    print("Please set the environment variable APPENV")
    #sys.exit(1)
  
  os.environ['APPENV'] = 'uat'             # SETS env variable
  print(os.environ.get('APPENV'))
  



def use_environment_variables_created_from_my_special_file():
  # we can store seperate our required variables in .env file and using the below module to load and access them as regular env variables
  # pip install python-dotenv
  # https://ioflood.com/blog/python-dotenv-guide-how-to-use-environment-variables-in-python/

  import os
  from dotenv import load_dotenv, dotenv_values

  load_dotenv()                      # Load environment variables from the .env file (if present) into the current environment
  # eg .env file -
  # ENV=staging
  # DB_USER=prod_support
  # # DB_PASSWORD=secret123!

  # Access environment variables as if they came from the actual environment
  DB_USER = os.getenv('DB_USER')
  DB_PASSWORD = os.getenv('DB_PASSWORD')

  # Example usage
  print(f'DB_USER: {DB_USER}')
  print(f'DB_PASSWORD: {DB_PASSWORD}')

  # We can also put ALL the variables from the file into a dictionary
  my_env_config = dotenv_values(".env")
  print(my_env_config)
  # OrderedDict([('DB_USER', 'prod_support'), ('DB_PASSWORD', 'secret123!')])
  db_user = my_env_config['DB_USER']    # will get the value of this env variable 

  # we can also make use of multiple .env files like .env.shared, .env.dev, .env.prod, .env.stage and use accordingly based off the APPENV env variable seperately set and access via os.getenv()
  appenv = os.getenv('APPENV') 
  load_dotenv(f'.env.{appenv}')

  # we can also use shell commands to access/update this .env file, like such -
  # $ dotenv -f .env.dev list
  # DB_PASSWORD=secret123!
  # DB_USER=prod_support
  # $ dotenv get DB_USER
  # prod_support
  # $ dotenv set DB_PORT 3000
  # DB_PORT=3000
  # $ dotenv set DB_PASSWORD changed456!
  # DB_PASSWORD=changed456!
  # $ dotenv list
  # DB_PASSWORD=changed456!
  # DB_PORT=3000
  # DB_USER=prod_support
  # $ dotenv unset DB_PORT



def dictionary_sorted()

  import numpy as np
  
  my_dict = {'yash': 2, 'rajnish': 9,
          'sanjeev': 15, 'chanda': 10, 'suraj': 32}
  
  
  print("-----sorting by key-----")
  my_keys = list(my_dict.keys())
  my_keys.sort()
  sorted_dict_by_key = {i: my_dict[i] for i in my_keys}
  
  print(sorted_dict_by_key)
  
  print("-----sorting by values-----")
  sorted_list_by_value = sorted(my_dict.items(), key=lambda x:x[1])
  sorted_dict_by_value = dict(sorted_list_by_value)
  
  print(sorted_dict_by_value)
  
  #-----sorting by key-----
  #{'chanda': 10, 'rajnish': 9, 'sanjeev': 15, 'suraj': 32, 'yash': 2}
  #-----sorting by values-----
  #{'yash': 2, 'rajnish': 9, 'chanda': 10, 'sanjeev': 15, 'suraj': 32}



def your_function_name(data_venue: str, symbol: str, start_date: datetime, end_date: datetime, optional_parameter3=None) -> pd.DataFrame:
    """
    Brief description of your function.

    Parameters:
    - parameter1 (type): Description of parameter1.
    - parameter2 (type): Description of parameter2.
    - optional_parameter3 (type, optional): Description of optional_parameter3.
      Defaults to None.

    Returns:
    type: Description of the return value.

    Raises:
    SpecificException: Description of when this exception is raised.
    AnotherException: Description of another possible exception.

    Example:
    >>> get_historical_data_symbol("YFINANCE", "AAPL", datetime(2022, 1, 1), datetime(2022, 12, 31))
    """
    print(f"Received arguments : dbconn={dbconn} symbol={symbol} df={df_head_foot} tbl_name={table_name}")
    logger.debug("Received arguments : dbconn={} symbol={} df={} tbl_name={}", dbconn, symbol, df_head_foot, table_name)
   
   # Your function code here

#    Brief description: A concise one-line summary of what the function does.
#    Parameters: List each parameter with its type and a brief description. Specify whether a parameter is optional and provide its default value if applicable.
#    Returns: Describe the type of value the function returns.
#    Raises: List any exceptions that the function might raise, along with a description of the circumstances under which they occur. Omit if there are no exceptions.


from datetime import datetime, Optional

def fn_get_table_data_for_symbol(dbconn, symbol: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    # Your function code here
    pass
In this modification:

I imported the datetime class from the datetime module.
I imported the Optional type from the typing module, and I used it to specify that the start_date and end_date parameters are optional and can be either datetime objects or None.
If the optional parameters are not provided when calling the function, they default to None.
You can then use the start_date and end_date parameters within your function as needed. If they are not provided, you can handle the case where they are None accordingly.



def read_csv_into_list(file_path, has_header=True):
    """
    Read a CSV file and store its contents in a list.

    Parameters:
    - file_path (str): The path to the CSV file.
    - has_header (bool, optional): Specify if the CSV file has a header row. Defaults to True.

    Returns:
    list: A list containing rows from the CSV file.
    """
    import csv

    data_list = []

    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip the header row if present
        if has_header:
            next(csvreader)

        # Iterate over rows and append them to the list
        for row in csvreader:
            data_list.append(row)

        # If the csv is a SINGLE column file, then EXTEND the list using below, else it will become a list of lists
        for row in csvreader:
            data_list.append(row)

    return data_list

    # Example usage:
    csv_file_path = 'your_file.csv'  # Replace with the actual path to your CSV file
    csv_data = read_csv_into_list(csv_file_path, has_header=False)
    
    # Display the data
    for row in csv_data:
        print(row)

def explain_about_module_and_package():
  print("Module -  is a single Python file containing Python code, functions, and variables.")
  print("Save your functions or code into a .py file. For example, common_functions.py. Define functions and variables within this file.")
  print("In another Python script, you can import the module using the import statement")  
  print("To access functions or variables from the module, use the module_name.function_name syntax eg - ")
  print("common_functions.read_csv_into_list('your_file.csv', has_header=False)")

  print("Package - a way of organizing related modules into a directory hierarchy.")
  print("A package is a directory that contains an __init__.py file (can be empty) and other Python files (modules).")
  print("Create a directory to serve as the package, and include an empty __init__.py file within the directory. This makes the directory a package.")
  print("Place your modules (Python files) inside this directory.")
  print("To use a package (ie import one of its module), use the import statement with the package name and module name. eg -")
  print("from my_package import common_functions")
  print("Now you can use functions like common_functions.read_csv_into_list(...) ")
  print("Also, similar to modules, use the package_name.module_name.function_name syntax to access functions or variables. eg -")
  print("my_package.common_functions.read_csv_into_list('your_file.csv', has_header=False) ")

  print("Package Initialization - The __init__.py file can be used to initialize the package. It can be empty or contain code that runs when the package is imported")
  print("__init__ is strictly not required, but is good practice")
  '''
  example dir structure - 
  project_root/
│
├── my_package/
│   ├── __init__.py
│   ├── common_functions.py
│   └── other_module.py
│
├── main_script.py
└── another_script.py

  In this structure, my_package is a package containing common_functions.py and other_module.py. main_script.py and another_script.py are scripts
  that can import modules from the package.

  to import a module in a subfolder, do below (where  technical_analysis is a folders and mod_technical_indicators.py is the file)
  from technical_analysis import mod_technical_indicators as m_ti

  ----------------------------------------------------------------------------------------------------
  RELATIVE PACKAGE IMPORT - 
  In Python, relative imports only work within a package. To use relative imports, you need to organize your project as a package by 
  including an __init__.py file in each directory that you want to be part of the package.

  Here's a brief explanation:
  1
    Create a Package Structure:
    Suppose you have the following directory structure:
    plaintext

  2
my_project/
├── main_module/
│   ├── __init__.py
│   └── streamlit_2_with_timescaledb.py
└── technical_analysis/
    ├── __init__.py
    └── mod_technical_indicators.py

Add __init__.py Files:
Make sure each directory contains an __init__.py file (can be empty). This file signals to Python that the directory should be treated as a package.

3
Use Relative Imports:
Now, in streamlit_2_with_timescaledb.py, you can use a relative import like this:
python
    from main_module.technical_analysis import mod_technical_indicators as m_ti
    This assumes that your main_module is the top-level package.
Remember that if you're running the script directly (streamlit_2_with_timescaledb.py), you may encounter issues with relative imports. In such cases, it's often better to run your code as part of a package or use absolute imports.
----------------------------------------------------------------------------------------------------

  '''

def common_and_utilities_files():
  '''
  --- common.py ---
  Purpose:
  Use common.py for functions and code that are widely shared and applicable across different parts of your application.
  Functions in common.py are typically used in various modules and components of your project.

  Content:
  Functions that provide common functionality needed across different parts of your application.
  Code that is central to the overall logic of your project.
  Constants and configurations shared throughout your application.

  Examples:
  Functions for handling configuration settings.
  Helper functions that perform common tasks used across different modules.
  Constants that are shared across multiple parts of your application.   

  --- utils.py ---
  Purpose:
  Use utils.py for utility functions that may not have a direct connection to the overall logic of your application but are still useful in various scenarios.
  Functions in utils.py are often more specialized and may not be needed by every part of your application.

  Content:
  Helper functions that perform specific, standalone tasks.
  Functions that provide utility or convenience but are not central to the application's core logic.
  Tools and functions that may be useful in different projects, not just the current one.

  Examples:
  Date and time utility functions.
  String manipulation functions.
  File I/O utilities.
  Mathematical or statistical helper functions.

  --- Decision Factors ---
  Reusability:
  If a function is likely to be reused in different projects or contexts, consider placing it in a utils.py file.

  Project-Specific:
  If a function is closely tied to the specific logic of your project and is used across multiple modules, consider placing it in a common.py file.

  Complexity:
  More complex and central functions might find a home in common.py, while simpler and more specialized functions could go in utils.py.
  Organization:

  Use these files to improve the organization of your code. If a function fits naturally into one of these categories, it can make your codebase more readable and maintainable.

  --- Example Directory Structure ---

  project_root/
  │
  ├── common.py
  ├── utils.py
  ├── module1/
  │   ├── __init__.py
  │   ├── module1_file1.py
  │   └── module1_file2.py
  │
  ├── module2/
  │   ├── __init__.py
  │   ├── module2_file1.py
  │   └── module2_file2.py
  │
  └── main_script.py

  --- Example Usage in Scripts or Modules ---

  # main_script.py

  from common import common_function
  from utils import utility_function

  # Use functions from common.py and utils.py
  common_function()
  utility_function()

  '''

def connect_to_DB_using_SQLAlchemy_and_get_results():

  from sqlalchemy import text

  my_db_uri = "postgresql://postgres:postgres@localhost:5432/dbs_invest"
  #my_sql_query = """SELECT * FROM tbl_instrument;"""   # use it in this fashion so that it does not mess when '%ET%' types are used. use as below using patterns search
  # Replace the '%' character with ':wildcard' and bind the actual value
  # from sqlalchemy import text           # needs this module
  wildcard_value_1 = 'UN%'
  wildcard_value_2 = 'TA%'

  # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_using_textual_sql.htm
  # https://docs.sqlalchemy.org/en/20/core/sqlelement.html
  #sql_query = text("""SELECT symbol FROM tbl_instrument WHERE exchange_code LIKE 'NY%' AND symbol LIKE 'A%' ORDER BY symbol""")  # wildcards in the string
  sql_query = text("""
      SELECT symbol FROM tbl_instrument 
      WHERE exchange_code NOT LIKE :wildcard_1 AND symbol LIKE :wildcard_2
      ORDER BY symbol
  """).bindparams(wildcard_1=wildcard_value_1, wildcard_2=wildcard_value_2)     # wildcards taken from variables

  db_conn = connect_to_db_using_sqlalchemy(my_db_uri)
  df = pd.read_sql_query(my_sql_query, db_conn)
  print(df)


def difference_between_import_and_from_module_import():
   '''
   from psycopg2 import Error

This imports the Error class specifically from the psycopg2 module.
With this import, you can use Error directly in your code without needing to reference psycopg2 every time.
Example:

python
Copy code
from psycopg2 import Error

try:
    # Your code...
except Error as e:
    print(f"Error: {e}")
import psycopg2

This imports the entire psycopg2 module.
You need to reference the psycopg2 module when using its contents, such as psycopg2.Error for the Error class.
Example:

python
Copy code
import psycopg2

try:
    # Your code...
except psycopg2.Error as e:
    print(f"Error: {e}")
In most cases, using from psycopg2 import Error is more convenient because it allows you to use Error directly in your code without having to reference psycopg2. However, if you need multiple components from psycopg2, you might prefer the second form (import psycopg2) to have access to all elements in the module without additional imports.

Choose the form that suits your coding style and requirements.
   '''


def different_data_types():
   
   print(" ---------------------- LISTS ---------------")
   lst_tmp = []   # intiate a list with null values
   lst_symbols = ['CSPX.L', 'EQQQ.L', 'IITU.L', 'ISF.L', 'SWDA.L', 'VHVG.L', 'VUAG.L', 'VUSA.L', 'VWRL.L', 'VWRP.L']
   for symbol in lst_symbols:
    print(symbol)


def how_to_use_logger_module():
  '''
  Using the Python logging module in a professional way involves setting up a structured logging system that allows you to control log levels, 
  format log messages consistently, and configure different output handlers. Here's a guide to using the logging module professionally:
  '''

  # https://docs.python.org/3/library/logging.html

  # 1. Import the logging module:
  import logging

  # 2. Configure the Logging System:
  # Configure the logging system based on your needs. This configuration is usually done at the beginning of your script or application.

  # Configure the root logger
  #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
  #LOGGING_FORMAT = '%(asctime)s - [%(levelname)s] - [%(process)d:%(thread)d] - %(name)s:%(filename)s:%(funcName)s:%(lineno)d — %(message)s'
  LOGGING_FORMAT = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"

  # logging.basicConfig(filename='example.log', filemode='w', format=LOGGING_FORMAT, level=logging.DEBUG)
  #logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
  logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)

  # Optionally, disable log messages from other libraries
  logging.getLogger("requests").setLevel(logging.WARNING)
  logging.getLogger("urllib3").setLevel(logging.WARNING)
  #Adjust the log level and format according to your requirements.

  #3. Create a Logger for Your Module:
  #Create a logger instance for each module or script. This allows you to control logging settings for specific parts of your application.
  logger = logging.getLogger(__name__)

  #4. Use the Logger:
  #Use the logger to output log messages at different levels.

  logger.debug("This is a debug message")
  logger.info("This is an info message")
  logger.warning("This is a warning message")
  logger.error("This is an error message")
  logger.critical("This is a critical message")

  #5. Add File Handler (Optional):
  #You may want to log messages to a file in addition to the console. This is useful for keeping a record of logs.

  file_handler = logging.FileHandler('logfile.log')
  file_handler.setLevel(logging.DEBUG)  # Adjust the level as needed
  file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
  logger.addHandler(file_handler)

  #6. Use Exception Logging:
  #When catching exceptions, use the logger to log the exception information.
  try:
      # Some code that may raise an exception
      result = 1 / 0
  except Exception as e:
      logger.exception("An error occurred: %s", str(e))

  '''
  7. Consider Using a Configuration File (Advanced):
  For more complex setups, consider using a configuration file to configure the logging system. 
  This allows you to configure different loggers, handlers, and formatters based on your application's needs.

  Example Configuration File (logging.conf):
  ini format

  [loggers]
  keys=root,sampleLogger

  [handlers]
  keys=consoleHandler,fileHandler

  [formatters]
  keys=sampleFormatter

  [logger_root]
  level=DEBUG
  handlers=consoleHandler,fileHandler

  [logger_sampleLogger]
  level=DEBUG
  handlers=consoleHandler,fileHandler
  qualname=sampleLogger

  [handler_consoleHandler]
  class=StreamHandler
  level=DEBUG
  formatter=sampleFormatter
  args=(sys.stdout,)

  [handler_fileHandler]
  class=FileHandler
  level=DEBUG
  formatter=sampleFormatter
  args=('logfile.log',)

  [formatter_sampleFormatter]
  format=%(asctime)s - %(levelname)s - %(message)s
  datefmt=%Y-%m-%d %H:%M:%S

  Usage of Configuration File in Your Python Script:
  import logging.config

  logging.config.fileConfig('logging.conf')
  This is a more advanced setup, and you can customize it based on your application's logging needs.
  '''

def how_to_use_loguru_module_for_logging():
  '''
  quite straightforward to use
  gives nice colourized and well formatted logging output
  https://betterstack.com/community/guides/logging/loguru/        (has mention of how to do filtering)
  https://medium.com/analytics-vidhya/a-quick-guide-to-using-loguru-4042dc5437a5
  https://loguru.readthedocs.io/en/stable/api/logger.html

  +----------------------+------------------------+------------------------+
  | Level name           | Severity value         | Logger method          |
  +======================+========================+========================+
  | ``TRACE``            | 5                      | |logger.trace|         |
  +----------------------+------------------------+------------------------+
  | ``DEBUG``            | 10                     | |logger.debug|         |
  +----------------------+------------------------+------------------------+
  | ``INFO``             | 20                     | |logger.info|          |
  +----------------------+------------------------+------------------------+
  | ``SUCCESS``          | 25                     | |logger.success|       |
  +----------------------+------------------------+------------------------+
  | ``WARNING``          | 30                     | |logger.warning|       |
  +----------------------+------------------------+------------------------+
  | ``ERROR``            | 40                     | |logger.error|         |
  +----------------------+------------------------+------------------------+
  | ``CRITICAL``         | 50                     | |logger.critical|      |
  +----------------------+------------------------+------------------------+  

  some files to check :
  _defaults.py
  _colorizer.py
  
   31 LOGURU_FORMAT = env(
 32     "LOGURU_FORMAT",
 33     str,
 34     "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
 35     "<level>{level: <8}</level> | "
 36     "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
 37 )

  '''
  from loguru import logger

  # Logging levels are defined by their ``name`` to which a severity ``no``, an ansi ``color`` tag 
  # and an ``icon`` are associated and possibly modified at run-time. 


  logger.trace("Executing program")
  # default level is debug, so above won't print
  logger.debug("Processing data...")
  logger.info("Server started successfully.")
  logger.success("Data processing completed successfully.")
  logger.warning("Invalid configuration detected.")
  logger.error("Failed to connect to the database.")
  logger.critical("Unexpected system error occurred. Shutting down.")
  var1 = 'hello 123'
  logger.info("Printing a variable value using logger : {}", var1)

  # to show what setting we have for that particular logger level
  level = logger.level("ERROR")   # returns A |namedtuple| containing information about the level.
  print(level)    # => Level(name='ERROR', no=40, color='<red><bold>', icon='❌')


  # To |log| to a custom level, you should necessarily use its name
  # the severity number is not linked back to levels name (this implies that several levels can share the same severity).
  # To add a new level, its ``name`` and its ``no`` are required.
  # A ``color`` and an ``icon`` can also be specified or will be empty by default.
  logger.level("CUSTOM", no=45, color="<red>", icon="🚨")  # add/SETS a new custom level for logger
  logger.level("CUSTOM")   # => (name='CUSTOM', no=33, color="<red>", icon="🚨")      # shows/GETS the settings that are defined for this level
  logger.log("CUSTOM", "logging hello world in my CUSTOM logger style")   # => 33 @ logging hello world in my CUSTOM logger style

  logger.add(sys.stderr, format = "<red>[{level}]</red> Message : <green>{message}</green> @ {time}", colorize=True)    # to change the format
  logger.success("Successfully changed format")

  logger.remove()  # All configured handlers are removed
  #logger.remove(0) # remove the default handler configuration, else the old one will work along with the new one
  #logger.add(sys.stdout, level="INFO")
  logger.add(sys.stdout, level="INFO", serialize=True)  # adds a new handler and only records logs with INFO severity or greater and prints in JSON format

  # set our customized logging level named NOTICE
  logger.level("NOTICE", no=15, color="<light-magenta>", icon="@")
  notice_level = logger.level("NOTICE")
  logger.log("NOTICE", "New logging level set with values {}", notice_level)

  logger.trace("Executing program")
  # default level is debug, so above won't print
  logger.debug("Processing data...")
  logger.info("Server started successfully.")
  logger.success("Data processing completed successfully.")
  logger.warning("Invalid configuration detected.")
  logger.error("Failed to connect to the database.")
  logger.critical("Unexpected system error occurred. Shutting down.")
  logger.info("Printing a variable value using logger : {}", var1)

  # go to the end of this url to see how we can elevate logging from command line arguments
  https://github.com/Delgan/loguru/issues/402

  is_debug_enabled = logger.is_enabled("DEBUG")   # If need to check if DEBUG level is enabled
  logger.warning("Is DEBUG level enabled? {}", is_debug_enabled)

  # to add context information to log messages for better troubleshooting.
  # from here on, every log message will automatically include user information.
  logger.bind(user="admin")   

  logger.add(sys.stderr, level="INFO")  # sets the logging level
  current_logging_level = logger.level   # get the current logging level
  logger.info("Logging level set to {} ", current_logging_level)
  # compares the current logger level "name" with "DEBUG"
  # The result will be True if it matches and False otherwise.
  is_debug_enabled = logger.level == "DEBUG"
  logger.warning("Is DEBUG level enabled? {}", is_debug_enabled)


  '''
  logger.remove(0): This line removes the default (0ᵗʰ) handler. This needs to be done otherwise we would receive multiple log messages for the same log statement. 
  Passing None deletes all the handlers.
  logger.add(…): This line adds the new handler. The only mandatory parameter is the sink, which is an object that receives the log messages. 
  The format parameter specifies the custom format of our log. We can take advantage of keys (such as level, time, message) that give more contextual information. 
  Setting colorize to true allow for colouring texts using markup tags. Colouring is not limited to font colours, you can set background and text styles as well.

  # adding extra information
  logger.remove(0)
  logger.add(sys.stderr, format="{time:HH:mm:ss.SS} | {level} | {extra[ip]} | {message}")
  context_logger = logger.bind(ip="192.168.0.1")
  context_logger.info("Pinging IP")

  logger.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file
  logger.add("file_2.log", rotation="12:00")     # New file is created each day at noon
  logger.add("file_3.log", rotation="1 week")    # Once the file is too old, it's rotated
  logger.add("file_X.log", retention="10 days")  # Cleanup after some time
  logger.add("file_Y.log", compression="zip")    # Save some loved space

  try:
      func(5, c)
  except ZeroDivisionError:
      logger.exception("Division by zero error!")  

  '''

# ----------  this code works perfectly -------------------start-----

from loguru import logger
import sys

logger.remove()  # All configured handlers are removed

LOGGING_LEVEL = 'DEBUG'  # this is the loguru default
#LOGGING_LEVEL = "INFO"  # our default logging level

logger.add(sys.stderr, level=LOGGING_LEVEL)  # sets the logging level

curr_level = logger.level(LOGGING_LEVEL)     # get the current logging level
logger.info("Logging level set to {} ", curr_level)  # Level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞')
logger.debug("Setting for loguru logger level {} : level.name={} level.no={}  level.color={} level.icon={}", LOGGING_LEVEL, curr_level.name, curr_level.no, curr_level.color, curr_level.icon)

# set our customized logging level named MYACTION with a new severity number
MYACTION=11
#logger.level("MYACTION", no=MYACTION, color="<reverse>", icon="@")         # creates this new logger level
logger.level("MYACTION", no=MYACTION, color="<light-red><reverse>", icon="@")
this_level = logger.level("MYACTION")
logger.log("MYACTION", "New logging level set with values {}", this_level)
logger.debug("Setting for loguru logger level MYACTION : level.name={} level.no={}  level.color={} level.icon={}", this_level.name, this_level.no, this_level.color, this_level.icon)


# set another customized logging level
# but first check if the "MYNOTICE" level already exists
try:
  str_level_name="MYNOTICE"
  my_level = logger.level(str_level_name)
  print("MYNOTICE level already exists - ", my_level)
  logger.debug("My existing logger level {} : level.name={} level.no={}  level.color={} level.icon={}", str_level_name, my_level.name, my_level.no, my_level.color, my_level.icon)
except ValueError:  # Level not found
  # set customized logging level
  MYNOTICE=21
  #logger.level("MYNOTICE", no=MYNOTICE, color="<LIGHT-YELLOW>", icon="@")
  logger.level("MYNOTICE", no=MYNOTICE, color="<black><LIGHT-YELLOW>", icon="@")
  this_level = logger.level("MYNOTICE")
  logger.log("MYNOTICE", "New logging level for MYNOTICE set with values {}", this_level)
  logger.debug("Setting for loguru logger level MYNOTICE : level.name={} level.no={}  level.color={} level.icon={}", this_level.name, this_level.no, this_level.color, this_level.icon)

# Verify registered levels
for level in logger._core.levels.values():
  print(level.name, level.no, level.color)

# ----------  this code works perfectly -------------------end-----


def custom_decorator()
   '''
In Python, a custom decorator is a function that takes another function as input, adds some functionality to it, and returns the modified function. Decorators are a powerful feature in Python that allows you to extend or modify the behavior of functions or methods.

Here's a basic example of a custom decorator:

python

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Calling the decorated function
say_hello()

In this example:

    my_decorator is a custom decorator function that takes another function func as input.
    wrapper is a nested function inside my_decorator that adds some functionality before and after calling the original function.
    The @my_decorator syntax is a shorthand for applying the decorator to the function that follows it (say_hello in this case).

When you call say_hello(), it is actually equivalent to calling the decorated version of say_hello:

python

my_decorator(say_hello)()

This results in the additional functionality defined in the wrapper being executed before and after the original say_hello function.

Custom decorators are commonly used for tasks such as logging, access control, and performance monitoring. They provide a clean and reusable way to extend the behavior of functions in a modular fashion.   
   
   
   '''


def fn_dates_related():
  # all dates related things

  # convert Timestamp object from DATAFRAME cell (1st row pd_time col) to string
  str_dt_time = df['pd_time'].head(1).item() .strftime('%Y-%m-%d %H:%M:%S')

def main():

import platform

if platform.system() == "Windows":
    print("Running on Windows")
elif platform.system() == "Linux":
    print("Running on Linux")
else:
    print("Operating system not recognized")

  #get_arguments_info()
  #todo_get_how_to_document()
  #explain_about_module_and_package():
  #connect_to_DB_using_SQLAlchemy_and_get_results()
  #how_to_use_logger_module()
  different_data_types()
  how_to_use_loguru_module_for_logging()
  fn_dates_related()
  #custom_decorator()

# --- main ---
if __name__ == '__main__':
  # main(sys.argv)
  main()



from datetime import datetime, timezone

# Assuming you have a datetime object like this
original_datetime = datetime(2024, 1, 19)

# Set the time (assuming midnight)
datetime_with_time = original_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

# Set the timezone (UTC in this example)
datetime_with_timezone = datetime_with_time.replace(tzinfo=timezone.utc)

print(datetime_with_timezone)


--------------------------------------------------------------------------------

import sys
import inspect
import traceback

# to check which caller function invoked the function, using inspect module
def fn_inspect_caller_functions():

  print("-----0000----")
  #print(inspect.stack()[0].function) # skip as it is this inspect function itself
  #print(inspect.stack()[1].function)  # actual caller to inspect but we do not want that either
  print('This function called by -', inspect.stack()[2].function)  # caller of the function of interest to us

  # below is expensive to do, so only do for specific situations
  #print("Traceback stack :")
  #stack = traceback.extract_stack()[:-1]  # exclude the current frame because we are interested in the caller of the caller and higher up
  #for frame in stack:
  #  print(f"File: {frame.filename}, Line: {frame.lineno} Function: {frame.name} calls =>")
  #print(inspect.stack())


    """Prints function names and line numbers from the call stack."""
    for frame in inspect.stack()[2:]:
        print(f"  - Function: {frame.function} ({frame.filename}:{frame.lineno})")

  #filename - full path of the code being executed by frame this traceback corresponds to
  #lineno - of current line associated with the code being executed by this traceback frame 
  #function - function name that is being executed by frame this traceback corresponds to.
  # if not in a function, it will just say <module>
  #previous_frame = inspect.currentframe().f_back
  #print("previous_frame = ", previous_frame)
  #print("caller function name = ", previous_frame.f_code.co_name)
  # Use sys._getframe().f_back.f_code.co_name to access caller information directly, faster
  # but will need to do in each and every function
  #print('--WORKS---2---', sys._getframe().f_back.f_code.co_name)
  #f = inspect.currentframe()  
  #tb = inspect.getframeinfo(f)  # Traceback object
  #print(f"----WORKS----3---- In function {tb.function}, file={tb.filename} lineno={tb.lineno}")

def fn_grandfather():
  print("")
  print("--- in fn_grandfather()----")
  fn_inspect_caller_functions()
  fn_father()


# this is the one i am documenting all about
def fn_father():
  print("")
  print("-- in fn_father()----")
  fn_inspect_caller_functions()
  fn_son()

def fn_son():
  print("")
  print("-- in fn_son()----")
  fn_inspect_caller_functions()

# --- main ----
print("--starting main---")
fn_grandfather()

def fn_inspect_code
  import inspect
  import yfinance as yf

  # inspect.getsource gives us the code snippet of the code being called, output like below - 
  #   @utils.log_indent_decorator
  #    def history(self, *args, **kwargs) -> pd.DataFrame:
  #       return self._lazy_load_price_history().history(*args, **kwargs)
  print(inspect.getsource(yf.Ticker("AAPL").history))

  # help() is a python function that provides help on (my local or pkg module) function that we are calling, output will be like below - 
  #   Help on method history in module yfinance.base:
  #   history(*args, **kwargs) -> pandas.core.frame.DataFrame method of yfinance.ticker.Ticker instance
  help(yf.Ticker("AAPL").history)

---


def fn_dataframes_related():

  # note - this one has multiindex columns
  data = {
      ('Open', 'XOM'): [35.12, 35.45, 37.63, 38.13, 38.30],
      ('High', 'XOM'): [34.74, 35.44, 37.03, 37.73, 38.09],
      ('Low', 'XOM'): [35.16, 36.86, 37.80, 38.09, 38.52],
      ('Close', 'XOM'): [35.80, 37.96, 38.21, 38.61, 38.82],
      ('Volume', 'XOM'): [27764700, 44035100, 36484800, 29528100, 28628200],
  }
  index = pd.date_range(start='2021-01-04', periods=5, freq='D')
  df = pd.DataFrame(data, index=index)
  print("----Source---", df)
  print(f"--DataFrame Shape: {df.shape} rows and columns--")
#(5, 5) rows and columns
  print("--DataFrame Info : ")
  df.info()
"""
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 5 entries, 2021-01-04 to 2021-01-08
Freq: D
Data columns (total 5 columns):
 #   Column         Non-Null Count  Dtype
---  ------         --------------  -----
 0   (Open, XOM)    5 non-null      float64
 1   (High, XOM)    5 non-null      float64
 2   (Low, XOM)     5 non-null      float64
 3   (Close, XOM)   5 non-null      float64
 4   (Volume, XOM)  5 non-null      int64
dtypes: float64(4), int64(1)
memory usage: 240.0 bytes 
"""
  print(f"--df.columns and their levels = {df.columns}--")
"""
MultiIndex([(  'Open', 'XOM'),
            (  'High', 'XOM'),
            (   'Low', 'XOM'),
            ( 'Close', 'XOM'),
            ('Volume', 'XOM')],
           )
"""

  print(f"--type(df.columns) = {type(df.columns)}--")
# <class 'pandas.core.indexes.multi.MultiIndex'>

  print(df.columns.levels)  # Display levels of the MultiIndex
#[['Close', 'High', 'Low', 'Open', 'Volume'], ['XOM']]

  print(df.columns.names)   # View names of the levels (if set)
#[None, None]


# extract just 1 column from the dataframe
df_symbols = df_symbols[["symbol"]]

# convert to list
lst_symbols = df_symbols["symbol"].tolist()



def print_caller_info(index=2):
    """Prints details about a specific frame in the call stack."""
    frame = inspect.stack()[index]
    print(f"Frame #{index}:")
    print(f"  - Function: {frame.function}")
    print(f"  - Filename: {frame.filename}")
    print(f"  - Line number: {frame.lineno}")

# Example usage
print_caller_info(1)  # Print information about the caller (index 1)
--------------------------------------------------------------------------------




