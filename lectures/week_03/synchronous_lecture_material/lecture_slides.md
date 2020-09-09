# Logical Operators

<br><br>

| Operation |  Operator |
|:---------:|:---------:|
| Equal |  `==` |
| Not Equal |  `!=` |
| Greater Than or Equal To |  `>=` |
| Less Than or Equal To |  `<=` |
| Less Than |  `<` |
| Greater Than |  `>` |
| Contains |  `in` |
| Does'nt Contain |  `not in` |
| Same Object |  `is` |
| Not the Same Object |  `is not` |

<br><br>


### Compound Logical Operators

<br>

| Operation |  Operator |  Usage |
|:---------:|:---------:|:---------:|
| Combined |  `and` | `x > 8 and y < 4`
| Either/or |  `or` | `x > 8 or y < 4`

<br>

### Boolean operations

<br>

|Operation|Result|Notes|
|----------|--------| : --- :|
|x **`or`** y|if x is false, then y, else x|This is a short-circuit operator, so it only evaluates the second argument if the first one is false.|
|x **`and`** y|if x is false, then x, else y|This is a short-circuit operator, so it only evaluates the second argument if the first one is true.|
|**`not`** x|if x is false, then True, else False|`not` has a lower priority than non-Boolean operators, so `not a == b `is interpreted as `not (a == b)`, and `a == not b` is a _syntax error_.
| y **`in`** x | if the value contained within y (scalar) is contained within x (container)| Check if an item is member to an existing collection|
| y **`is`** x | if the object id of y is the same as the object id of x | Two objects refer to the same data structure |

<br><br>

### Logical operator behavior determined by the object class.


<br>

```
 '__and__',
 '__or__',
 '__bool__',
 '__eq__',
 '__ge__',
 '__gt__',
 '__le__',
 '__lt__',
 '__ne__',
 '__pos__'
```

<br><br>


# Control Statements

```python
if <logical statement>:
  ~~~~ CODE ~~~~
elif <logical statement>:
  ~~~~ CODE ~~~~
else:
  ~~~~ CODE ~~~~
```

<br><br><hr><br><br>

# Loops

**Iteration** in a basic sense is simply taking one item at a time from a collection. We start at the beginning of the collection and mover through it until we reach the end. Any time we use a loop we are going over each and every item in collection

**Empty container**

```
                ___________
                |         |
                |         |
                |         |
                |_________|
```


**Assign items to the container**

```
                ___________
                | "apple" |
                | "orange"|
                | "grapes"|
                |_________|
```


**For each iteration, we take one item out and do something with it.**
```

                    \
                     \
       eat("apple")   \
                       \
                        \__
                |         |
                | "orange"|
                | "grapes"|
                |_________|
```

```

                    \
                     \
       eat("orange")  \
                       \
                        \__
                |         |
                |         |
                | "grapes"|
                |_________|
```


**We _stop_ once the container is empty**
```

                    \
                     \
       eat()          \
                       \
                        \__
                |         |
                |         |
                |         |
                |_________|
```                


<br><br>

### **So what does a `for` loop do?**

#### 1. The `for` statement calls `iter()` on the container object (e.g. a list).
#### 2. The function returns an iterator object that defines the method `__next__()` which accesses elements in the container _one at a time_.
#### 3. When there are no more elements, `__next__()` raises a `StopIteration` exception which tells the for loop to terminate.


<br><br>

> ### Keep in mind that not all objects are iterable (i.e. have an __iter__ method). This is one of the main distinctions between scalar types and container types.


<br><br><hr><br><br>


# Functions

<br>

- **`def`**: keyword for generating a function
    + `def` + some_name + `()` + `:` to set up a function header


- **Arguments**: things we want to feed into the function and do something to.


- **`return`**: keyword for returning a specific value from a function

<br>

```python
def my_func(arg1,arg2):
  ~~~code~~~
  ~~~code~~~
  ~~~code~~~
  return obj
```


<br><br><br>

# Arguments

Arguments are all the input values that lie inside the parentheses.

```python
def fun(argument_1,argument_2):
```

We can supply **default values** to one or all arguments; in doing so, we've specified a default argument.

```python
def fun(argument_1 = "default 1",argument_2 = "default 2"):
```


```python
def fun(a,b=""):
```

- argument `a` is called a **positional argument** (`*arg`). We provide value to it by matching the position in the sequence.
- argument `b` is called a **keyword argument** (`**kwargs`). Because we give it a default value. So it has a "keyword" referring to it.

### Keyword arguments must **_come after_** positional arguments, or python will throw a SyntaxError.



<br><br>

# Docstrings

Docstrings are strings that occur as the first statement within a named function block.

```python
def function_name(input):
    """Short summary.

        Args:
            input (type): Description of parameter `input`.

        Returns:
            type: Description of returned object.

    """
    |
    |
    | Function block
    |
    |
    return something

```

**The goal of the docstring is to tell us what the function _does_.** We can request a functions docstring using the `help()` function.
