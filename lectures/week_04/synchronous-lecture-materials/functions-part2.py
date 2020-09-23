'''
MORE ON FUNCTIONS...
'''


# %% -----------------------------------------

# Function basics (refresh)
def fun(x=1):
    return 4 + x

fun()



# %% markdown -----------------------------------------

## Using Mutable Values as Arguments


#%% Never Use a mutable value as default arg -------

# Issue
def my_func(a = []):
    a.append('x')
    return a

my_func()
my_func()
my_func()



# To get around this, we only use immutable value as placeholders.
def my_func(a = None):
    if a is None:
        a = []
    a.append('x')
    return a

my_func()
my_func()
my_func()




x = 3
def my_func():
    return x

my_func()



# %% markdown -----------------------------------------

## Scoping

# %% -----------------------------------------


'''
Scopes are contexts in which named references can be looked up.
Scopes are arranged in a hierarchy from which object references can be looked up

There are 4 scopes total (From narrowest to broadest):

- Local: name is defined inside the current function
- Enclosing: Any and all enclosing functions
- Global: Any and all names defined at the top level of a module.
- Built-in: names "built into" python through the builtins module

Note that for loops and code blocks do not introduce new nested scopes.
We can alter the rules slightly when need by using the global and local calls
'''

def tt():
    print(f'val = {count}')
count = 0
tt()
count = 5
tt()




# %% -----------------------------------------


val = 5
# This is a global variable
a = 0

if a == 0:
    # This is still a global variable
    b = 1

def my_function(c):
    # this is a local variable
    d = 3
    print(c)
    print(d)




# %% -----------------------------------------

# Now we call the function, passing the value 7 as the first and only parameter
my_function(7)



# We can be explicit with regard to which variables we
# reference using the global keyword.
def tt():
    global count # call to the global scope to get the object reference
    print(f'val = {count}')
tt()


'''
NOTE: it is usually very bad practice to access global variables from inside functions,
and even worse practice to modify them.

If a function needs to access some external value, we should pass the value into
the function as an argument.
'''






# %% markdown -----------------------------------------

## Lambda Functions

# %% -----------------------------------------


def fun(x):
    return x**2

fun(4)

lambda x: x**2
square(4)






'''
Sometimes we need to perform a simple computation, but would rather not generate a function to do so.

Example:

- Say we wanted to sort this list of US Presidents by the longest to shortest last name.
- The sorted() function is a built in function that can do this for us.
- If we were to just run this on the list, it would sort in alphabetical order.
- sorted() has two keyword arguments: key= and reverse=.
- The key argument offers us a way to define our own sorting function.
'''




presidents = ['Barak Obama','Donald Trump','George Bush','Jimmy Carter','Bill Clinton']
presidents.sort()

sorted(presidents)





# %% -----------------------------------------

def sort_by_longest_last_name(x):
    return len(x.split()[-1])

# Sort by longest to shortest last name.
sorted(presidents,key=sort_by_longest_last_name,reverse=True)

sorted(presidents,key=lambda x: len(x),reverse=True)






# %% -----------------------------------------

# Setting up the lambda function:
# lambda <function arguments>: <expression>


square = lambda x: x**2
square(5)




'''
Using a lambda function
Lambda functions are most useful when used in concert with higher-order functions,
which are functions that take other functions as input.

We'll see these in play when we use Pandas methods.
'''
