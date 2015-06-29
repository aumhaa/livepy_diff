
from _Framework.TransportComponent import TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._metronome_toggle.view_transform = lambda v: 'DefaultButton.Alert' if v else 'DefaultButton.On'