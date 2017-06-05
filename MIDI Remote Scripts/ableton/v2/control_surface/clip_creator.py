
from __future__ import absolute_import, print_function
import Live
_Q = Live.Song.Quantization

class ClipCreator(object):
    """
    Manages clip creation over all components.
    """
    grid_quantization = None
    is_grid_triplet = False
    fixed_length = 8
    legato_launch = True

<<<<<<< HEAD
    def create(self, slot, length = None, launch_quantization = None):
=======
    def create(self, slot, length = None, launch_quantization = None, legato_launch = None):
>>>>>>> master
        if not slot.clip == None:
            raise AssertionError
            if length is None:
                length = self.fixed_length
            slot.create_clip(length)
<<<<<<< HEAD
            if self.grid_quantization != None:
                slot.clip.view.grid_quantization = self.grid_quantization
                slot.clip.view.grid_is_triplet = self.is_grid_triplet
            launch_quantization = (launch_quantization == None or self.legato_launch == True) and _Q.q_no_q
        slot.fire(force_legato=self.legato_launch, launch_quantization=launch_quantization)
=======
            should_legato_launch = self.legato_launch if legato_launch is None else legato_launch
            if self.grid_quantization is not None:
                slot.clip.view.grid_quantization = self.grid_quantization
                slot.clip.view.grid_is_triplet = self.is_grid_triplet
            launch_quantization = (launch_quantization is None or should_legato_launch) and _Q.q_no_q
        slot.fire(force_legato=should_legato_launch, launch_quantization=launch_quantization)
>>>>>>> master
