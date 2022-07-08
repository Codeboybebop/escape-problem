# Import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Arc
from modeling import *

# Create a subplot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.45)
ax.set_aspect(1)
ax.set_ylim(-3, 3)
ax.set_xlim(-3, 3)
r = 0.6
g = 0.2
b = 0.5

# Create and plot a bar chart


# Create 3 axes for 3 sliders red,green and blue
axinit = plt.axes([0.25, 0.3, 0.65, 0.03])
axvinit = plt.axes([0.25, 0.26, 0.65, 0.03])
axperiod = plt.axes([0.25, 0.22, 0.65, 0.03])
axboundary = plt.axes([0.25, 0.18, 0.65, 0.03])
axstiffness = plt.axes([0.25, 0.14, 0.65, 0.03])

axssteps = plt.axes([0.25, 0.10, 0.65, 0.03])


xinit_slider = Slider(axinit, 'X init ', -3.0, 3.0, 0.6)

vinit_slider = Slider(axvinit, 'V init  ', -3.0, 3.0, 0.2)

# xinit_slider = Slider(axinit, 'X init / a', -2.0, 2.0, 0.6)


# vinit_slider = Slider(axvinit, 'V init / a w ', -2.0, 2.0, 0.2)

period_slider = Slider(axperiod, 'period', 0.0, 20.00, 1)

boundary_slider = Slider(axboundary, 'a', 0.0, 5, 1)

stiffness_slider = Slider(axstiffness, 'k', 0.0, 10, 1)

steps_slider = Slider(axssteps, 'step', 1, 50, 1,  valstep=1)


# Create fuction to be called when slider value is changed


def update(val):
    ax.clear()
    ax.set_aspect(1)
    ax.set_ylim(-5, 5)
    ax.set_xlim(-5, 5)
    x1 = xinit_slider.val
    v1 = vinit_slider.val
    T = period_slider.val
    time_left = T/2
    a = boundary_slider.val
    k = stiffness_slider.val
    w = np.power(k, 0.5)
    steps = int(steps_slider.val)
    '''
    xx = [x1]
    vv = [v1]
    n = 1000
    dt = T / (2 * n)

    for i in range(n):
        xx.append(xx[-1] + dt * vv[-1])
        vv.append(vv[-1] - k * dt * xx[-2])


    xxx = [xx[n * i // 1000] for i in range(1000)]
    vvv = [vv[n * i // 1000] for i in range(1000)]
    ax.plot(xxx, vvv)
    '''
    for i in range(steps):
        x1, v1 = half_period_evolution(x1, v1, T, time_left, a, k, True)
        x1, v1 = teleportation(x1, v1, -1, True)
        x1, v1 = half_period_evolution(x1, v1, T, time_left, a, k, True)
        x1, v1 = teleportation(x1, v1, 1, True)


def teleportation(x, v, val, to_plot=False):
    x2, v2 = teleport(x, v, val)
    if to_plot:
        ax.plot([x, x2], [v, v2], '--')
    return x2, v2


def half_period_evolution(x1, v1, T, time_left, a, k, to_plot=False):
    if is_inside(x1, v1, a, k, T):
        if is_bounded(x1, v1, a, k, T):
            x2, v2 = turn(x1, v1, time_left, a, k, T)
            x0, v0 = hieght_widht(x1, v1, a, k, T)
            if to_plot:
                if full_rotation(x1, v1, time_left, a, k, T):
                    ax.add_patch(Arc((0, 0), 2*x0, 2*v0))
                else:
                    ax.add_patch(Arc((0, 0), 2*x0, 2*v0, angle=0.0,  theta1=polar(x2, v2) *
                                     (180.0 / np.pi), theta2=polar(x1, v1) * (180.0 / np.pi)))
            time_left = 0.0
        else:
            if has_enough_time_to_exit(x1, v1, time_left, a, k, T):
                x2, v2 = exit_point(x1, v1, a, k, T)
                x0, v0 = hieght_widht(x1, v1, a, k, T)
                if to_plot:
                    ax.add_patch(Arc((0, 0), 2*x0, 2*v0, angle=0.0,  theta1=polar(x2, v2) *
                                     (180.0 / np.pi), theta2=polar(x1, v1) * (180.0 / np.pi)))
                time_left = time_left - turning_time_to_exit(x1, v1, a, k, T)
                x1, v1 = x2, v2
                x2, v2 = forward(x1, v1, time_left, a, k, T)
                if to_plot:
                    ax.plot([x1, x2], [v1, v2])
                time_left = 0.0
            else:
                x2, v2 = turn(x1, v1, time_left, a, k, T)
                x0, v0 = hieght_widht(x1, v1, a, k, T)
                if to_plot:
                    ax.add_patch(Arc((0, 0), 2*x0, 2*v0, angle=0.0,  theta1=polar(x2, v2) *
                                 (180.0 / np.pi), theta2=polar(x1, v1) * (180.0 / np.pi)))
                time_left = 0.0
    else:
        if has_enough_time_to_enter(x1, v1, time_left, a, k, T):
            x2, v2 = enter_point(x1, v1, time_left, a, k, T)
            if to_plot:
                ax.plot([x1, x2], [v1, v2])
            time_left -= time_to_enter(x1, v1, time_left, a, k, T)
            x1, v1 = x2, v2
            if is_bounded(x1, v1, a, k, T):
                x2, v2 = turn(x1, v1, time_left, a, k, T)
                x0, v0 = hieght_widht(x1, v1, a, k, T)
                if to_plot:
                    if full_rotation(x1, v1, time_left, a, k, T):
                        ax.add_patch(Arc((0, 0), 2*x0, 2*v0))
                    else:
                        ax.add_patch(Arc((0, 0), 2*x0, 2*v0, angle=0.0,  theta1=polar(x2, v2) *
                                         (180.0 / np.pi), theta2=polar(x1, v1) * (180.0 / np.pi)))
                time_left = 0.0
            else:
                if has_enough_time_to_exit(x1, v1, time_left, a, k, T):
                    x2, v2 = exit_point(x1, v1, a, k, T)
                    x0, v0 = hieght_widht(x1, v1, a, k, T)
                    if to_plot:
                        ax.add_patch(Arc((0, 0), 2*x0, 2*v0, angle=0.0,  theta1=polar(x2, v2) *
                                     (180.0 / np.pi), theta2=polar(x1, v1) * (180.0 / np.pi)))
                    time_left = time_left - \
                        turning_time_to_exit(x1, v1, a, k, T)
                    x1, v1 = x2, v2
                    x2, v2 = forward(x1, v1, time_left, a, k, T)
                    if to_plot:
                        ax.plot([x1, x2], [v1, v2])
                    time_left = 0.0
                else:
                    x2, v2 = turn(x1, v1, time_left, a, k, T)
                    x0, v0 = hieght_widht(x1, v1, a, k, T)
                    if to_plot:
                        ax.add_patch(Arc((0, 0), 2*x0, 2*v0, angle=0.0,  theta1=polar(x2, v2) *
                                     (180.0 / np.pi), theta2=polar(x1, v1) * (180.0 / np.pi)))
                    time_left = 0.0

        else:
            x2, v2 = forward(x1, v1, time_left, a, k, T)
            if to_plot:
                ax.plot([x1, x2], [v1, v2])
            time_left = 0.0
    return x2, v2


# Call update function when slider value is changed
xinit_slider.on_changed(update)
vinit_slider.on_changed(update)
period_slider.on_changed(update)
boundary_slider.on_changed(update)
stiffness_slider.on_changed(update)
steps_slider.on_changed(update)

# Create axes for reset button and create button
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color='gold',
                hovercolor='skyblue')

# Create a function resetSlider to set slider to
# initial values when Reset button is clicked


def resetSlider(event):
    xinit_slider.reset()
    vinit_slider.reset()
    period_slider.reset()
    boundary_slider.reset()
    stiffness_slider.reset()
    steps_slider.reset()


# Call resetSlider function when clicked on reset button
button.on_clicked(resetSlider)

# Display graph
update(12)
plt.show()
