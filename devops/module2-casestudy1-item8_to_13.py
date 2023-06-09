'''
8.
With two given lists [1,3,6,78,35,55] and [12,24,35,24,88,120,155], write a
program to make a list whose elements are intersection of the above given lists.
'''

def do_item_8():
    print('\n----item 8----')
    list_A = [1,3,6,78,35,55]
    list_B = [12,24,35,24,88,120,155]

    print('list_A=', list_A)
    print('list_B=', list_B)
    list_intersection = [x for x in list_A if x in list_B]
    print('list_intersection=', list_intersection)


# --------------------------------------------------------------------------------

'''
9. 
With a given list [12,24,35,24,88,120,155,88,120,155], write a program to print this
list after removing all duplicate values with original order reserved.
'''

def do_item_9():
    print('\n----item 9----')
    list_1 = [12,24,35,24,88,120,155,88,120,155]
    print('list_1=', list_1)
    print('List with unique elements only in original order = ', list(dict.fromkeys(list_1)))
 
# --------------------------------------------------------------------------------

'''
10.
By using list comprehension, please write a program to print the list after removing
the value 24 in [12,24,35,24,88,120,155].
'''
def do_item_10():
    print('\n----item 10----')
    list_1=[12,24,35,24,88,120,155]
    print('list_1=', list_1)
    list_1 = [x for x in list_1 if x != 24]
    print('list_1 (after removal of all 24) =', list_1)
# --------------------------------------------------------------------------------

'''
11.
By using list comprehension, please write a program to print the list after removing
the 0th,4th,5th numbers in [12,24,35,70,88,120,155].
'''
def do_item_11():
    print('\n----item 11----')
    list_1=[12,24,35,70,88,120,155]
    #list_1=[-12,24,35,70,-88,-120,155]
    print('list_1=', list_1)
    list_1 = [x for (counter, x) in enumerate(list_1) if counter not in (0,4,5)]
    print('list_1 (after removal of required elements) =', list_1)

# --------------------------------------------------------------------------------
'''
12.
By using list comprehension, please write a program to print the list after removing
delete numbers which are divisible by 5 and 7 in [12,24,35,70,88,120,155].
'''
def do_item_12():
    print('\n----item 12----')
    list_1=[12,24,35,70,88,120,155]
    print('list_1=', list_1)
    list_1 = [x for x in list_1 if (x % 35) != 0]
    print('list_1 (after removal of elements divisible by 5 AND 7 ie 35 )=', list_1)
    
# --------------------------------------------------------------------------------
'''
13.
Please write a program to randomly generate a list with 5 numbers, which are
divisible by 5 and 7 , between 1 and 1000 inclusive.
'''
import random

def do_item_13():
    print('\n----item 13----')
    list_1 = [ x for x in range(1,1001) if x%35==0]
    print('list_1=', random.sample(list_1, 5))


# --------------------------------------------------------------------------------

def main():
    do_item_8()
    do_item_9()
    do_item_10()
    do_item_11()
    do_item_12()
    do_item_13()

if __name__ == "__main__":
    main()






