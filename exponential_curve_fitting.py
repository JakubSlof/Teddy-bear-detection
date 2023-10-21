import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def exponenial_func(x, a, b, c):
    return a*np.exp(b*x)+c


x = np.array([15, 87, 138, 178, 206, 228, 246, 260, 274, 283, 291, 300, 307])#np.array([20, 30, 40, 50, 60])
y = np.array([40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160])#np.array([0.015162344, 0.027679854, 0.055639098, 0.114814815, 0.240740741])


popt, pcov = curve_fit(exponenial_func, x, y, p0=(1, 1e-6, 1))

xx = np.linspace(15, 307, 1000000)
yy = exponenial_func(xx, *popt)

# please check whether that is correct
r2 = 1. - sum((exponenial_func(x, *popt) - y) ** 2) / sum((y - np.mean(y)) ** 2)

plt.plot(x, y, 'o', xx, yy)
plt.title('Exponential Fit')
plt.xlabel(r'Temperature, C')
plt.ylabel(r'1/Time, $s^-$$^1$')
plt.text(30, 0.15, "equation:\n{:.4f} exp({:.4f} x) + {:.4f}".format(*popt))
plt.text(30, 0.1, "R^2:\n {}".format(r2))
print(popt)
plt.show()