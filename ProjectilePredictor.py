#!/usr/bin/env python3
#
# Compute the min/max distances velocities for a given shooter angle.
#
# All distances are measured in inches.
# All times are measured in seconds.

import argparse
import math
import matplotlib.pyplot as plt
import numpy as np

# Speaker opening constants.
speaker_back_y = 78
speaker_front_distance_from_wall = 18
speaker_front_y = 82.875

# For the purposes of (x,y) coordinates, x=0 is at the wall, and y=0 is the floor. The robot
# can be a maximum of 26" high if clearance under the stage is desired, and it's unlikely we can
# have the effective exit less than ~3" from the top of the robot.
exit_height = 25.5 # inches

# The subwoofer prevents driving directly under the speaker opening, so the closest possible
# shooting distance is ~31". The overhung opening in practice prevents shots which have a negative
# (downward) velocity component upon entry; the exceptions are for steeper shooting angles, and
# we're better off shooting hard enough to hit the concave interior of the speaker. Shots get much
# more difficult as distance increases, and there are hard limits on legal shots (auto: must be in
# team wing, teleop: must be outside opponent wing). Limit search to worst-case mid-line shot, which
# is unlikely to be even remotely practical.
d_lower_bound = 30
d_upper_bound = 396

g = 386.089 #acceleration of gravity in in/s**2

parser = argparse.ArgumentParser(description='Compute note trajectories')
parser.add_argument('--angle', type=float, required=True, help='Shooter angle')
parser.add_argument('--vlimit', type=float, required=True, help='Maximum shot velocity')
args = parser.parse_args()
theta_0 = args.angle
v_ludicrous = args.vlimit

def plot_init():
    plt.xlabel('Horizontal inches from shooter exit')
    plt.ylabel('Vertical inches from floor')
    plt.suptitle('Team 9044 Ballistics Design (2024)')
    plt.title(f'exit_height={exit_height}", angle={theta_0}°')

    speaker_back_x = 0
    speaker_front_x = -speaker_front_distance_from_wall
    x_speaker = [speaker_back_x, speaker_front_x]
    y_speaker = [speaker_back_y, speaker_front_y]
    plt.plot(x_speaker, y_speaker, label = "Speaker Opening")

    x_wall = [0, 0]
    y_wall = [0, 98.302]
    plt.plot(x_wall, y_wall)

def plot_floor(d_max):
    x_floor = [-d_max, 0]
    y_floor = [0, 0]
    plt.plot(x_floor, y_floor)

def plot_trajectory(label, distance_to_wall, u_0):
    # Compute t_max to coincide with far side of speaker opening.
    v_x = u_0 * math.cos( math.radians( theta_0 ) )
    t_max = distance_to_wall / v_x

    t = np.linspace(0.0, t_max, 20)
    x = -distance_to_wall + u_0 * t * math.cos( math.radians( theta_0 ) )
    y = exit_height + u_0 * t * math.sin( math.radians( theta_0 ) ) - (0.5 * g * t**2)

#    print("Values of t:", t)
#    print("Values of x:", t)
#    print("Values of y:", t)

    plt.plot(x, y, label=label)

def show():
    plt.legend()
    plt.show()

def compute_v_flat(delta_x):
    # Slope 0 at delta_x occurs when the wall is half the full range, ignoring exit height.
    return math.sqrt((2*g*delta_x) / math.sin(2*math.radians(theta_0)))

def is_shot_possible(delta_x, delta_y):
    # The shot is not possible if v exceeds ludicrous speed.
    v = v_ludicrous
    v_x = v * math.cos( math.radians( theta_0 ) )
    t = delta_x / v_x
    y = v * t * math.sin( math.radians( theta_0 ) ) - (0.5 * g * t**2)
    return y >= delta_y

# Iteratively solve for v that causes intersection with the point (delta_x, delta_y).
def solve_v(delta_x, delta_y):
    if not is_shot_possible(delta_x, delta_y): return None
    solve_epsilon = 1 # in/s
    v_lower_bound = 0
    v_upper_bound = v_ludicrous
    while True:
        v = (v_lower_bound + v_upper_bound) / 2
        if (v_lower_bound + solve_epsilon >= v_upper_bound):
            break
        v_x = v * math.cos( math.radians( theta_0 ) )
        t = delta_x / v_x
        y = v * t * math.sin( math.radians( theta_0 ) ) - (0.5 * g * t**2)
        if y < delta_y:
            v_lower_bound = v
        else:
            v_upper_bound = v
    return v

def compute_v_min(distance_to_wall):
    # Assuming the shot is possible, we define the minimum velocity is the greater of {velocity that
    # results in intersection with the back of the opening, velocity that results in slope 0 at the
    # wall}.
    delta_x = distance_to_wall
    delta_y = speaker_back_y - exit_height
    v_intersect = solve_v(delta_x, delta_y)
    if v_intersect is None: return None

    v_flat = compute_v_flat(distance_to_wall)
#    print(f'v_intersect={v_intersect}, v_flat={v_flat}')

    return max(v_intersect, v_flat)
    v_min = (v_intersect, v_flat)
    if v_min == v_ludicrous: return None
    return v_min

def compute_v_max(distance_to_wall):
    # Assuming the shot is possible, if a ludicrous-speed shot intersects the speaker opening beyond
    # the front of the speaker opening, we clamp at ludicrous speed. Otherwise, the maximum velocity
    # causes the trajectory to intersect the front of the speaker opening.

    delta_x = distance_to_wall - speaker_front_distance_from_wall
    delta_y = speaker_front_y - exit_height
    v_intersect = solve_v(delta_x, delta_y)
    if v_intersect is None:
        if compute_v_min(distance_to_wall) is None:
            return None
        else:
            return v_ludicrous
    v_flat = compute_v_flat(distance_to_wall)
    if v_intersect < v_flat: return None
    return v_intersect

plot_init()

found_min = False
found_inflection = False
maybe_found_max = False
for distance_to_wall in range(d_lower_bound, d_upper_bound):
    v_min = compute_v_min(distance_to_wall)
    v_max = compute_v_max(distance_to_wall)
    if v_min is None or v_max is None:
        if found_min:
            break
        continue
    print(f'distance_to_wall={distance_to_wall}, v_min={v_min:.0f}, v_max={v_max:.0f}')
    if not found_min:
        found_min = True
        d_max = distance_to_wall
        plot_trajectory(f'Near d={distance_to_wall}", v_min={v_min:.0f}"/s', distance_to_wall, v_min)
        plot_trajectory(f'Near d={distance_to_wall}", v_max={v_max:.0f}"/s', distance_to_wall, v_max)
    else:
        if not found_inflection and maybe_found_max and v_min_prev < v_min:
            found_inflection = True
            plot_trajectory(f'Inflection d={distance_to_wall_prev}", v_min={v_min_prev:.0f}"/s',
              distance_to_wall_prev, v_min_prev)
            plot_trajectory(f'Inflection d={distance_to_wall_prev}", v_max={v_max_prev:.0f}"/s',
              distance_to_wall_prev, v_max_prev)
        maybe_found_max = True
        distance_to_wall_prev = distance_to_wall
        v_min_prev = v_min
        v_max_prev = v_max
if maybe_found_max:
    d_max = distance_to_wall_prev
    plot_trajectory(f'Far d={distance_to_wall_prev}", v_min={v_min_prev:.0f}"/s',
      distance_to_wall_prev, v_min_prev)
    plot_trajectory(f'Far d={distance_to_wall_prev}", v_max={v_max_prev:.0f}"/s',
      distance_to_wall_prev, v_max_prev)

if not found_min:
    print('No solution')
    exit(1)

plot_floor(d_max)
show()
