import pandas as pd
import matplotlib.pyplot as plt

starwars_data_frame = pd.read_csv('StarWars.csv', encoding="unicode_escape")

#Simple Visualization that demonstrates that of this data set, about 20% have not seen a Star Wars movie!! Surprising, isn't it? 
seenSW = starwars_data_frame["Have you seen any of the 6 films in the Star Wars franchise?"].value_counts().plot(kind="bar")
plt.title("Number of respondents who have watched Star Wars")
plt.xlabel("Has the respondent seen Star Wars?")
plt.show()

#Simple Visualization that demonstrates that how many respondents view themselves as SW fans
fanSW = starwars_data_frame["Do you consider yourself to be a fan of the Star Wars film franchise?"].value_counts().plot(kind="bar")
plt.title("Number of respondents who consider themselves SW Fans")
plt.show()

#Simple Visualization that demonstrates the education level of all respondants. 
starwars_data_frame["Education"].value_counts().plot(kind="bar")
plt.title("Education levels")
plt.show()


