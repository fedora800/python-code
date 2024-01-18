import sys


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

def main():

  get_arguments_info()
  #todo_get_how_to_document()



# --- main ---
if __name__ == '__main__':
  # main(sys.argv)
  main()
