from dataclasses import dataclass
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pickle
import os
from pathlib import Path
from tqdm import tqdm
from argparse import ArgumentParser


# get command-line arguments
parser = ArgumentParser()
parser.add_argument('data_dir', help='The data directory to plot')
parser.add_argument('--save', nargs='?', metavar='FILENAME',
                    help='Save the animation to a video file')
args = parser.parse_args()


# load all the frame data
@dataclass
class FrameData:
    value_grid: np.ndarray
    pellet_locs: np.ndarray
    super_pellet_locs: np.ndarray
    ghost_locs: np.ndarray
    pacbot_loc: Tuple[int, int]

def load_frame_data(data_file):
    with data_file.open('rb') as f:
        value_grid, pellet_locs, super_pellet_locs, ghost_locs, pacbot_loc = pickle.load(f)
    ghost_locs = np.array(ghost_locs).reshape((-1, 2))
    pellet_locs = np.array(pellet_locs).reshape((-1, 2))
    super_pellet_locs = np.array(super_pellet_locs).reshape((-1, 2))
    return FrameData(value_grid, pellet_locs, super_pellet_locs, ghost_locs, pacbot_loc)

frame_data = [
    load_frame_data(path)
    for path in sorted(Path(args.data_dir).glob('*.pkl'))
]
all_value_grids = np.stack([data.value_grid for data in frame_data])
value_min = np.nanmin(all_value_grids)
value_max = np.nanmax(all_value_grids)
print(value_min, value_max)


fig, ax = plt.subplots()

aximg = ax.matshow(np.zeros_like(all_value_grids[0]), vmin=value_min, vmax=value_max)
fig.colorbar(aximg)

ghost_sca = ax.scatter([], [], color='red', edgecolors='none', marker='s')
pacbot_sca = ax.scatter([], [], color='red', edgecolors='none', marker='x')
pellet_sca = ax.scatter([], [], color='white', edgecolors='none', marker='.')
super_pellet_sca = ax.scatter([], [], color='white', edgecolors='none', marker='o')

fig.tight_layout()


last_frame_index = -1
def update_anim(frame_index):
    global last_frame_index
    if frame_index > last_frame_index:
        progress.update(frame_index - last_frame_index)
        last_frame_index = frame_index

    data = frame_data[frame_index]

    aximg.set_data(data.value_grid)

    ghost_sca.set_offsets(data.ghost_locs)
    pacbot_sca.set_offsets(data.pacbot_loc)
    pellet_sca.set_offsets(data.pellet_locs)
    super_pellet_sca.set_offsets(data.super_pellet_locs)

    return aximg, ghost_sca, pacbot_sca, pellet_sca, super_pellet_sca

num_frames = len(frame_data)
fps = 20
print(f'{num_frames=}')
progress = tqdm(total=num_frames)
ani = FuncAnimation(fig, update_anim, frames=num_frames, interval=1000/fps, blit=True)

if args.save is not None:
    ani.save(args.save, writer='ffmpeg', fps=fps)
else:
    plt.show()
