import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = np.array([15,87,138])#np.array([15, 87, 138, 178, 206, 228, 246, 260, 274, 283, 291, 300, 307])
y = np.array([40,50,60])#np.array([40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160])

def exponential_function(x, a, b, c):
    return a * np.exp(b * x) + c

popt, pcov = curve_fit(exponential_function, x, y)

plt.scatter(x, y, label='Data')
plt.plot(x, exponential_function(x, *popt), color='red', label='Fitted Curve')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Exponential Curve Fitting')
plt.legend()
plt.show()

print("The equation of the fitted curve is y = {0:.4f} * exp({1:.4f} * x) + {2:.4f}".format(popt[0], popt[1], popt[2]))
