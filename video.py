import imageio
import torch

frames = torch.load("frames.pt")

imagio.mimsave("video.mp4",frames, fps=25)