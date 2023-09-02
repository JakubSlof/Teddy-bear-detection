import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Define the data points
x = np.array([15,87,138,178,206,228,246,260,274,283,291,300,307])
y = np.array([40,50,60,70,80,90,100,110,120,130,140,150,160])

# Fit a curve to the data points
model = LinearRegression()
model.fit(x.reshape(-1, 1), y)

# Plot the data points and the fitted curve
plt.scatter(x, y)
plt.plot(x, model.predict(x.reshape(-1, 1)), color='red')
plt.show()

# Display the equation of the fitted curve
print("The equation of the fitted curve is y = {0}x + {1}".format(model.coef_[0], model.intercept_))