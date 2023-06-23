import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import cvxpy
import sys
import os

x = []
y = []


with open ('ref_linear1_latlng.csv') as f:
    map_df = pd.read_table(f, sep=',', header=0, names=['x','y'], lineterminator='\n')

x = map_df.x
y = map_df.y

plt.plot(x)
plt.plot(y)
plt.show()


