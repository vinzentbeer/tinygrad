import os
from tinygrad import Tensor
from tinygrad.device import Device

# before running this file:
# docker build -t api . --platform=linux/amd64
# docker run -p 80:80 api

# clone remu and run cargo build --release, change RHIP_PATH
os.environ["RHIP_PATH"] = "/Users/qazal/code/remu"
os.environ["RHIP"] = "1"

# DEBUG=1 prints instructions, green is an active thread, gray is inactive thread.
os.environ["DEBUG"] = "1"

# PROFILE=1 counts resources used
os.environ["PROFILE"] = "1"

assert Device.DEFAULT == "RHIP"
out = Tensor([2]) * Tensor([2])
out.realize()
