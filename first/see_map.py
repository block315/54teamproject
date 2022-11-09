import matplotlib.pyplot as plt
import pandas as pd

ev3_map = pd.read_csv('./arena.csv',header=None)

plt.imshow(ev3_map,cmap="gray")
plt.show()