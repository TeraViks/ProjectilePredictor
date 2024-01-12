import math
import matplotlib.pyplot as plt
import numpy as np

distance_to_subwoofer = 6 # inches
exit_height = 24 # inches
v_shooter = 250  # inches/second
v_robot_x = 0  # inches/second
theta_shooter = 67 # degrees  
time_to_show = .75

speaker_back_x = 0 
speaker_back_y = 78
speaker_front_x = speaker_back_x - 18
speaker_front_y = 82.875
g = 386.089 #acceleration of gravity in in/s**2
subwoofer_distance_from_wall = 36.125
subwoofer_height = 10

x_speaker = [speaker_back_x, speaker_front_x]
y_speaker = [speaker_back_y, speaker_front_y]

x_subwoofer = [-subwoofer_distance_from_wall, -subwoofer_distance_from_wall]
y_subwoofer = [0, subwoofer_height]

t = np.linspace(0.0, time_to_show, 20)

v_x = v_shooter * math.cos( math.radians( theta_shooter ) ) + v_robot_x
v_y = v_shooter * math.sin( math.radians( theta_shooter ) ) 

x = v_x * t - (distance_to_subwoofer + subwoofer_distance_from_wall) 
y = v_y * t - (0.5 * g * t**2) + exit_height

# print("Values of t:", t)
# print("Values of x:", t)
# print("Values of y:", t)

plt.xlabel('Horizontal inches to wall') 
plt.ylabel('Vertical inches from floor') 
plt.title('Team 9044 Ballistics Design (2024)') 
plt.figtext(.65, .3, f"v_robot: {v_robot_x} in/s\nv_shooter: {v_shooter} in/s\ntheta_shooter: {theta_shooter} deg\nh_shooter: {exit_height} in\nd_subwoofer: {distance_to_subwoofer} in")

plt.plot(x_subwoofer, y_subwoofer, label = "Subwoofer")
plt.plot(x_speaker, y_speaker, label = "Speaker Opening")
plt.plot(x, y, label = "Note Path")

plt.legend()

plt.show()