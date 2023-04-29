from ipywidgets import FloatProgress, Layout
from IPython.display import display
import micasense.imageset as imageset
import os

## This progress widget is used for display of the long-running process
f = FloatProgress(min=0, max=1, layout=Layout(width='100%'), description="Loading")
display(f)
def update_f(val):
    if (val - f.value) > 0.005 or val == 1: #reduces cpu usage from updating the progressbar by 10x
        f.value=val

# images_dir = os.path.expanduser(os.path.join('~','Downloads','RedEdgeImageSet','0000SET'))

#Linux filepath
#imagePath = os.path.expanduser(os.path.join('~','Downloads','RedEdge3'))
#Windows filepath
imagePath = os.path.join('r:\\','RedEdgeImageSet','0000SET')