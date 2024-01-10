import math
import matplotlib.pyplot as plt
import numpy as np

distance_to_wall = 36.125 # inches
exit_height = 24 # inches
u_0 = 250  # inches/second
theta_0 = 70 # degrees  

speaker_back_x = distance_to_wall
speaker_back_y = 78 - exit_height
speaker_front_x = speaker_back_x - 18
speaker_front_y = 82.875 - exit_height
g = 386.089 #acceleration of gravity in in/s**2

x_speaker = [speaker_back_x, speaker_front_x]
y_speaker = [speaker_back_y, speaker_front_y]

t = np.linspace(0.0, 1.0, 20)
x = u_0 * t * math.cos( math.radians( theta_0 ) )
y = u_0 * t * math.sin( math.radians( theta_0 ) ) - (0.5 * g * t**2)

print("Values of t:", t)
print("Values of x:", t)
print("Values of y:", t)

plt.xlabel('Horizontal inches from shooter exit') 
plt.ylabel('Vertical inches from shooter exit') 
plt.title('Team 9044 Ballistics Design (2024)') 

plt.plot(x_speaker, y_speaker, label = "Speaker Opening")
plt.plot(x, y, label = "Note Path")

plt.legend()

plt.show()