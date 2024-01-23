import sys
import inspect
#import logging
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



def your_function_name(parameter1, parameter2, optional_parameter3=None):
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
    """
    # Your function code here

#    Brief description: A concise one-line summary of what the function does.
#    Parameters: List each parameter with its type and a brief description. Specify whether a parameter is optional and provide its default value if applicable.
#    Returns: Describe the type of value the function returns.
#    Raises: List any exceptions that the function might raise, along with a description of the circumstances under which they occur. Omit if there are no exceptions.



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
  https://betterstack.com/community/guides/logging/loguru/
  https://medium.com/analytics-vidhya/a-quick-guide-to-using-loguru-4042dc5437a5
  https://loguru.readthedocs.io/en/stable/api/logger.html

  '''
  from loguru import logger

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

  logger.level("CUSTOM", no=45, color="<red>", icon="🚨")  # add/set a new custom level for logger
  logger.level("CUSTOM")   # => (name='CUSTOM', no=33, color="<red>", icon="🚨")      # gets the settings for this level
  logger.log("CUSTOM", "logging hello world in my CUSTOM logger style")

  logger.add(sys.stderr, format = "<red>[{level}]</red> Message : <green>{message}</green> @ {time}", colorize=True)    # to change the format
  logger.success("Successfully changed format")

  logger.remove(0) # remove the default handler configuration
  #logger.add(sys.stdout, level="INFO")
  logger.add(sys.stdout, level="INFO", serialize=True)  # adds a new handler and only records logs with INFO severity or greater and prints in JSON format

  logger.trace("Executing program")
  # default level is debug, so above won't print
  logger.debug("Processing data...")
  logger.info("Server started successfully.")
  logger.success("Data processing completed successfully.")
  logger.warning("Invalid configuration detected.")
  logger.error("Failed to connect to the database.")
  logger.critical("Unexpected system error occurred. Shutting down.")
  logger.info("Printing a variable value using logger : {}", var1)


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

def main():

  #get_arguments_info()
  #todo_get_how_to_document()
  #connect_to_DB_using_SQLAlchemy_and_get_results()
  #how_to_use_logger_module()
  how_to_use_loguru_module_for_logging()

# --- main ---
if __name__ == '__main__':
  # main(sys.argv)
  main()



