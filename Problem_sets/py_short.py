### VARIABLES ###
x = 54
phrase = "This is CS50"
# we dont declare variable type in python + we can declare variables only by initialization!

### LISTS ###
nums = list()
nums2 = [] # empty list

nums3 = [1, 2, 3, 4]
nums3.append(5) # Attaches an element (5) on to the end of the list.
nums3.insert(4,5) # Same as above. Put number 5 into 4th position (counting from 0) into the list.
nums3[len(nums3):] = [5] # Same as above. // len = lenght of nums3 list // From position 4 (len of nums) this list gets this other list assigned with number 5
                         # Good for "joining" two lists together rather than elements.

nums4 = [x for x in range(500)] # for loop inside of a list -> creates a list with 500 elements (0 - 499)

### LOOPS ###

# While loop
counter = 0
while counter < 100:
    print(counter)
    counter += 1

# For loop (Initialised at, how many elements, how much to increment x)
for x in range(0, 100, 2):
    print(x)

### CONDITIONALS ###

if y < 43 or z == 15:
    print("python in great")



if y < 43 and z == 15:
    print("this is fun")
else:
    print("indentation is important in python")



if coursenum == 50:
    print("this is going to be a pain to get used to")
elif not coursenum == 51:               # in C same as -> else if (coursenum != 51)
    print("I have no idea what I am doing")



### TUPLES ###

presidents = [
    ("George Washington", 1789),
    ("John Adams", 1797),
    ("Thomas Jefferson", 1801),
    ("James Madison", 1809)
]

for prez, year in presidents:
    print("In {1}, {0} took office".format(prez, year))



### DICTIONARIES ### (Sort of like hash tables)

pizzas = {
    "cheese": 9,    ## associating key (cheese) with value "9"
    "pepperoni": 10,    ## separated by ":"
    "vegetables": 11,
    "buffalo chicken": 12
}
## change value
pizzas["cheese"] = 8


if pizzas["vegetables"] < 12:
    print("something")

# Can add into the dictionary
pizzas["bacon"] = 14

# We can use loops to itirate over elements in dictionary (for loop in python is Extremely flexible)

for pie in pizzas:      #use pie in here as a stand-in for "i" // pie becomes every single key
    print(pie)          ## prints out all the keys in dictionary

    # OR #

for pie, price in pizzas.items():       # If we want to iterate over the values we need to transform the dictionary into a list -- > .items()
    print(price)                        ## would print out !!(12, 10, 9, 11)!! -- If we transform into a list, it may (very likely) not retain its order !!!
                                        ### If printing the pairs together it would still appear correctly

for pie, price in pizzas.items():
    print("A whole {} pizza cost ${}".format(pie, price))   ## Would print out "A whole buffalo chicken pizza costs $12, ...

#Printing and variable interpolation
print("A whole {} pizza cost ${}".format(pie,price))
print("A whole " + pie + "pizza costs $" + str(price))

print("A whole %s pizza costs $%2d" % (pie, price)) # <-------- Avoid using  <--------------- !!! (deprecated)


### FUNCTIONS ###

# Functions introduced with the "def" keyword
# no need for main() - usually

#If wishing to define main nonetheless, you must have at the very end of code
if __name__ == "__main__":
    main()

def square(x):
    return x ** 2 ## exponentiation operator

    #OR

def square(x):
    result = 0
    for i in range(0, x):
        result += x
    return result
print(square(5))  ## should print "25"

#### OBJECTS ####

# Python is object oriented language / Closest to an object is a structure in C

# Methods = basicaly functions that are inherent to the object and mean nothing outside of it. Methods are defined inside the object also.
            # type of object defined using the "class" keyword in python
            # Classes require initialization function (constructor) that sets the starting values of the properties of the object
            # In defining each method of an object, "self" should be its first parameter, which stipulates on what object the method is called.

class Student():

    def __init__(self, name, id):                                   ## Constructor (initialization function) - always called "__init__"
        self.name = name                                            ## 2 properties = "name" and "id" // Because defining a method inside a class we need to include "self" parameter
        self.id = id                                                    ## assigning name and id properties of the Student() object to be whatever we pass in here.

    def changeID(self, id):                                         ## Here we can change ID of a Student when already initialized.
        self.id = id                                                ## takes 2 parameters(self - to know which Student(object) are we talking about and id)

    def print(self):                                                ## We always have to indicate the "self" parameter // needs to be part of any method we define for a class we create.
        print("{} - {}".format(self.name, self.id))

# Creating new object - Jane

jane = Student("Jane", 10)                              ## We would create new object - Jane // namefield = Jane / ID = 10
jane.print()                                            ## We would print out "Jane - 10"
jane.changeID(11)                                           # id change
jane.print()                                            ## We would now print out "Jane - 11"


### STYLE ###

# good style is CRUCIAL in python
# Tabs and indentation matter a lot and things may not work if we disregard styling

### INCLUDING FILES ###
# modules instead of headers
import cs50                     # allows us to use functions like cs50.get_int(), cs50.get_float(), cs50.get_string(), cs50.get)char(),...

## We can make programs look a lot more like C programs when executed by adding a "shebang" to the top of our python files
           #!/usr/bin/env python3     (including the hash #)

# If we do this, we need to change permissions on our file as well using the Linux command chmod as follows :       chmod a+x <file>