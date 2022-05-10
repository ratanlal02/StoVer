from z3 import *
x0=Real('x0')
x1=Real('x1')
solve(x0 >= 0, -x0+1>=0, x0-2>=0, -x0+5>=0, x1>=0, -x1+2>=0)