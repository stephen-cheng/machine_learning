import numpy
import matplotlib.pyplot as plt

timeStep =  10         # years
waterDepth = 4000         # meters
L = 1               # Watts/m2
albedo = 0.3
epsilon = 1
sigma = 5.67E-8          # W/m2 K4

heatCapacity = waterDepth * 4.2E6 #J/K m2
time_list = [0]
temperature_list = [400.]
# dHeatContent/dt = L*(1-alpha)/4 - epsilon * sigma * T^4
heatContent = heatCapacity * temperature_list[0]
heatIn = L * (1-albedo) / 4
heatOut = 0

nSteps = 200

for itime in range(0, nSteps):
	time_list.append(timeStep+time_list[-1])
	# HeatContent(t+1) = HeatContent(t) + dHeatContent/dT * TimeStep
	heatContent = heatContent + (heatIn - heatOut) * timeStep * 3.14e7
	# T[K] = HeatContent [J/m2] / HeatCapacity [J/m2 K]
	temperature_list.append(heatContent/heatCapacity)
	heatOut = epsilon * sigma * pow(temperature_list[-1],4)
	# print(itime, time_list[-1])
print(temperature_list[-1], heatOut)
# print(temperature_list[-1])
plt.plot(time_list, temperature_list)
plt.show()









