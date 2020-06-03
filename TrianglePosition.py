import numpy as np
import math
from Transformation import Transformation
#hello
'''
INPUTS:
Spacecraft 1 (S/C1)
Attitude: yaw1, roll1, pitch1 [rad] #z,x,y
Position: x1. y1. z1 [km]
Bright pixel: n [pixel position]

Spacecraft 2 (S/C2)
Attitude: yaw2, roll2, pitch2 
Position: x2, y2, z2
Bright pixel: m

OUTPUTS:
Position: xp, yp, zp
'''

#Inputs for FOCUS payload
h = 500 #[km]
Re = 6378 #[km]
radius = Re+h #Sum between earth radius and altitude
factorsize = 15*10**(-3) #[km]

###S/C1###

#Longitude and latitude 
lat1 = np.pi/4 #[rad]
lon1 = np.pi/6 #[rad]

#S/C1 position in km
spacecraftlocation1 = radius*np.array([np.cos(lon1)*np.cos(lat1),np.sin(lon1)*np.cos(lat1),np.sin(lat1)])

#Attutide angles
yaw1 = 0 #[rad]
roll1 = np.pi/180*5 #[rad]
pitch1 = np.pi/180*10 #[rad]

#Angles of the bright pixel in radians
alpha1,beta1 = [np.pi/3,np.pi/4]

#Representation of vector in 3D using the two angles given (alpha and beta)
v1 = np.array([np.sin(alpha1),np.cos(alpha1)*np.sin(beta1),np.cos(alpha1)*np.cos(beta1)])

#Transformation of vector into Earth fixed coordinate system
vector1 = np.diagonal(Transformation(lon1,lat1,yaw1,pitch1,roll1)*v1)

###S/C2###

#Longitude and latitude
lat2 = np.pi/4.2 #[rad]
lon2 = np.pi/6 #[rad]


#S/C2 position in km
spacecraftlocation2 = radius*np.array([np.cos(lon2)*np.cos(lat2),np.sin(lon2)*np.cos(lat2),np.sin(lat2)])

#Attitude angles
yaw2 = 0 #[rad]
roll2 = np.pi/180*7 #[rad]
pitch2 = np.pi/180*12 #[rad]

#Angles of the bright pixel in radians
alpha2,beta2 = [np.pi/3,-np.pi/4]

#Representation of vector in #D using the two angles given (alpha and beta)
v2 = np.array([np.sin(alpha2),np.cos(alpha2)*np.sin(beta2),np.cos(alpha2)*np.cos(beta2)])

#Transformation of vector into Earth fixed coordinate system
vector2 = np.diagonal(Transformation(lon2,lat2,yaw2,pitch2,roll2)*v2)

#Nearest points
n = np.cross(vector1,vector2)
n1 = np.cross(vector1,n)
n2 = np.cross(vector2,n)

point1 = spacecraftlocation1+(np.dot((spacecraftlocation2-spacecraftlocation1),n2)/np.dot(vector1,n2))*vector1
point2 = spacecraftlocation2+(np.dot((spacecraftlocation1-spacecraftlocation2),n1)/np.dot(vector2,n1))*vector2

print(point1,point2)
print(np.dot((spacecraftlocation1-spacecraftlocation2),n1)/np.dot(vector2,n1))

#Distance for Error
n_normalized = n/np.linalg.norm(n)
distance1 = np.abs(np.dot(n_normalized,(spacecraftlocation2-spacecraftlocation1)))
distance2 = np.linalg.norm(point2-point1)
print(distance1,distance2)