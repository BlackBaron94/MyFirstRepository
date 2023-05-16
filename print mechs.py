#A lot of prints
x = "World!"
print("1. Hello,", x ) #leaves gap
print("2. Hello, "+x) #eliminates gap
print("3. Hello, {0}".format(x)) #good for positionals
print("4. Hello, %s" % x) #good for floats
