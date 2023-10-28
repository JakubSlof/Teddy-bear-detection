import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Define the data points
x = np.array([-118,8,71])
y = np.array([0,20,30])

# Fit a curve to the data points
model = LinearRegression()
model.fit(x.reshape(-1, 1), y)

# Plot the data points and the fitted curve
plt.scatter(x, y)
plt.plot(x, model.predict(x.reshape(-1, 1)), color='red')
plt.show()

# Display the equation of the fitted curve
print("The equation of the fitted curve is y = {0}x + {1}".format(model.coef_[0], model.intercept_))