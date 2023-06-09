'''
14.
Write a program to compute 1/2+2/3+3/4+...+n/n+1 with a given n input by
console (n>0).
Example:
If the following n is given as input to the program:
5
Then, the output of the program should be:
3.55
'''

print('Input a positve number between 1 and 10000 : ')
input_num = int(input())
print('Your number = ', input_num)
sum=0.0
for x in range(1,input_num+1):
    sum+=x/(x+1)
print('Equation value = ', round(sum, 2))


