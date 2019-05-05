import sys
import serial
import argparse
import numpy as np
import matplotlib.pyplot as pp
import matplotlib.animation as animation

from time import sleep
from collections import deque
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D


class LivePlot():
  def __init__(self, num_inputs, max_range=100):
    self.fig, self.ax = pp.subplots()
    self.inits = np.zeros(num_inputs)
    print(self.inits)
    self.max_range = max_range
    self.datas = [deque([0 for j in range(max_range)]) for i in range(num_inputs)]
    self.lines = [Line2D(range(len(data)), data) for data in self.datas]
    self.ax.set_ylim(0, 1)
    self.ax.set_xlim(0, max_range)
    for line in self.lines:
      self.ax.add_line(line)

  def update(self, t):
    self.inits = get_val(self.inits)
    for i, data in enumerate(self.datas):
      if len(data) < self.max_range:
        self.datas[i].append(self.inits[i])
      else:
        self.datas[i].popleft()
        self.datas[i].append(self.inits[i])

    for i, line in enumerate(self.lines):
      self.lines[i].set_data(range(len(self.datas[i])), self.datas[i])

    # self.ax.relim()
    # self.ax.autoscale_view(tight=True)
    
    return self.lines

def get_val(vals):
  try:
    line = sys.stdin.readline()
    data = [float(val) for val in line.split()]
    nvals = np.array(data)
  except:
    nvals = vals
  return nvals
line = sys.stdin.readline()
data = [float(val) for val in line.split()]
num_inputs = len(data)
print(len(data))
live_plotter = LivePlot(num_inputs, max_range=500)
ani = FuncAnimation(live_plotter.fig, live_plotter.update, blit=False, interval=0, frames=None)
pp.show()
