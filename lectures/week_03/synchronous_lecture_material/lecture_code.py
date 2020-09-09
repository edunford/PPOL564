# %% Logical Operators -----------------------------------------


# "==" for value equivalency
x = ["a","b","c"]
y = ["a","b","c"]
x == y


# Comparisons
x = 7
y = 6

x >= y
x > y
x < y
x <= y

# Object class determines behavior
dir(x)



# "in" for contains
"x" in ["x","a","v"]


# "is" for object equivalency
x = ["a","b","c"]
y = ["a","b","c"]
x is y
id(x)
id(y)

z = x
x is z
id(x) == id(z)






# %% Control Statements -----------------------------------------

if True:
    print("Hello")

if False:
    print("Goodbye")


x = 4
if x >= 5:
    print("Hello")
else:
    print("Goodbye")




# layered control statement
x = 1
if x > 5:
    print("Code Chunk A")
elif x >= 3 and x <= 5:
    print("Code Chunk B")
else:
    print("Code Chunk C")






# %% For Loops -----------------------------------------
items = ["apple","orange","grape"]

i = items[0]
print(i)
i = items[1]
print(i)
i = items[2]
print(i)


# Same idea
for i in items:
    print(i)



# How it works?
iterator = items.__iter__()
iterator.__next__()







# %% Loops + Control Statements-----------------------------------------
for i in range(10):
    if i < 4:
        print("hello")
    elif i >= 4 and i <= 7:
        print("Cool")
    else:
        print("Later")



# NOTE: `range()` generates a sequence of integer up to N.



# Another useful wrapper function, enumerate
for i in enumerate(items):
    print(i)



# We can use tuple unpacking to great advantage here.
for index, value in enumerate(items):
    print("The index is", index,"The value is", value)








# %% While Loops -----------------------------------------

# Repeat behavior while a condition holds

x = 0
while x < 5:
    print("This")
    x += 1











# %% Flow Conditions -----------------------------------------


# Problem When we don't have a code in a code chunk....
x = 0
while x < 10:
    if x <= 5:

    else:
        print(f"{x} is greater than five")
    x += 1




# Pass == "filler"
x = 0
while x < 10:
    if x <= 5:
        pass
    else:
        print(f"{x} is greater than five")
    x += 1




# Continue == "go back to the top"
items = ["33",5.4,None,8]
for item in items:
    if item is None:
        continue
    print(item)

# Compare to pass
items = ["33",5.4,None,8]
for item in items:
    if item is None:
        continue
    print(item)





# Break == "stop the loop!"
for i in range(10):
    if i > 5:
        break
    print(i)










# %% Functions -----------------------------------------


def fun1():
    for i in range(10):
        print(i)

fun1()


def fun2(n):
    for i in range(n):
        print(i)

fun2(10)





def fun3(n=10):
    for i in range(n):
        print(i)

fun3()
fun3(5)







# Arguments: positional first, then keyword
def my_func(a,b=''):
    return a + b
my_func("cat","dog")




# Other way around and python yells.
def my_func(a="",b):
    return a + b
my_func("cat","dog")






# DOCSTRINGS

def paste_strings(string_one,string_two):
    """This is a function that pastes two strings together.

    Args:
        string_one (str): object of class string.
        string_two (str): object of class string.

    Returns:
        str: object of class string with the two input strings pasted together

    """
    return string_one + " "  + string_two



paste_strings("public","policy")




# Can access the doc string
help(paste_strings)


# Also, remember functions are objects to.
print(paste_strings.__doc__)
