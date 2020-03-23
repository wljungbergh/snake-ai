import numpy as np

s = [21, 1]
print(all(i > 20 or i<0 for i in s))