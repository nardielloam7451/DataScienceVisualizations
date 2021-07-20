import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


buildings_data_frame = pd.read_csv('buildings.csv')


print(buildings_data_frame[:5])

buildings_data_frame['Backup Power'].value_counts().plot(kind='pie', autopct='%.2f')
plt.axis('equal')
plt.title("Number of Buildings with Backup Power")
plt.show()
