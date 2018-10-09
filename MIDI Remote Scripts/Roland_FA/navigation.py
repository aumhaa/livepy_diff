from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from .scroll import ScrollComponent

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        self._horizontal_paginator = self.register_component(ScrollComponent())
        self._horizontal_paginator.can_scroll_up = self._can_scroll_page_left
        self._horizontal_paginator.can_scroll_down = self._can_scroll_page_right
        self._horizontal_paginator.scroll_up = self._scroll_page_left
        self._horizontal_paginator.scroll_down = self._scroll_page_right
