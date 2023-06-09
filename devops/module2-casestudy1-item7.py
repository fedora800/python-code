'''
7. Please write a program which count and print the numbers of each character in a
string input by console.
 Example: If the following string is given as input to the program:
 abcdefgabc
 Then, the output of the program should be:
a,2
c,2
b,2
e,1
d,1
g,1
f,1
'''

input_str = 'abcdefgabc'
set_input_str = set(input_str)      # will get set of only the unique occurences/characters of the string

print('input string = ', input_str)
#print('set of input string = ', set_input_str)
for char in set_input_str:
    print(char, ',', input_str.count(char))
