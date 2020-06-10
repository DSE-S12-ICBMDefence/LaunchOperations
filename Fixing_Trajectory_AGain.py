import numpy as np
from math import *
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
# from AverageThrust import AvgThurst
# from CdEstimator import Cd
# from ISA_2 import density_at_height
# from TempAlt import  Temp
# from Mass_extract_2 import Mass_t
# from Velocity_Check import pixel_det
# from Velocity_Check import pixel_data
from Main_Trajectory import TrajectoryData
from scipy import spatial

def slicer(t,x,y):
    a = list(t.astype(int))
    starting_point = a.index(0)
    sliced_t = t[(starting_point+1):]
    sliced_x = x[(starting_point+1):]
    sliced_y = y[(starting_point+1):]

    return  sliced_t, sliced_x, sliced_y

def generate_trajectories(rot_alt_step,rot_angle_step,x_trans_step, y_trans_step):

    Re = 6370 * 1000  # m   #radius of the Earth
    x_trans = np.linspace(0,2*pi-0.01,y_trans_step)
    #theta is defined anti-clockwise from the positive x-axis

    delta_t = np.linspace(0,10,10)

    rot_alts = np.linspace(10000,100000,rot_alt_step)
    rot_angles = np.linspace(15,40,rot_angle_step)*(pi/180)

    temp_x = []
    temp_y = []
    temp_t = []
    for alt in rot_alts:
        for angle in rot_angles:
            x, y, h, vx, vy, v, t = TrajectoryData(alt, angle, 0, Re)
            xvector = np.zeros((len(x),3))
            xvector[:,0] = x
            xvector[:,1] = y
            for theta_x in x_trans:
                for dt in delta_t:
                    transformationmatrix = sp.spatial.transform.Rotation.from_euler('z',theta_x).as_matrix()
                    xvectorrot = np.einsum('ij,kj->ki',transformationmatrix,xvector)

                    xrot = np.copy(xvectorrot[:,0])
                    yrot = np.copy(xvectorrot[:,1])

                    temp_x.append(xrot)
                    temp_y.append(yrot)
                    temp_t.append(t-dt)

    for i  in range(len(temp_t)):
        if temp_t[i][0]<0 :
            sliced_t, sliced_x, sliced_y = slicer(temp_t[i],temp_x[i],temp_y[i])
            temp_t[i] = sliced_t
            temp_x[i] = sliced_x
            temp_y[i] = sliced_y

    return temp_x,temp_y,temp_t

# x,y,t = generate_trajectories(5,2,5, 10)
# for i in range(len(x)):
#      plt.plot(x[i],y[i])
# plt.show()



