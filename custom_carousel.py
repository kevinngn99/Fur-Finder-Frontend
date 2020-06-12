'''
Modified by Kevin Nguyen
A modified carousel widget using the Carousel source code from Kivy at https://kivy.org/doc/stable/_modules/kivy/uix/carousel.html
Original comments removed for readability
'''

from functools import partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.stencilview import StencilView
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import BooleanProperty, OptionProperty, AliasProperty, NumericProperty, ListProperty, ObjectProperty, StringProperty


class CustomCarousel(StencilView):
    slides = ListProperty([])
    direction = OptionProperty('right', options=('right', 'left', 'top', 'bottom'))
    min_move = NumericProperty(0.2)
    anim_move_duration = NumericProperty(0.5)
    anim_cancel_duration = NumericProperty(0.3)
    loop = BooleanProperty(False)
    scroll_timeout = NumericProperty(200)
    scroll_distance = NumericProperty('20dp')
    anim_type = StringProperty('out_quad')
    ignore_perpendicular_swipes = BooleanProperty(False)

    _index = NumericProperty(0, allownone=True)
    _prev = ObjectProperty(None, allownone=True)
    _current = ObjectProperty(None, allownone=True)
    _next = ObjectProperty(None, allownone=True)
    _offset = NumericProperty(0)
    _touch = ObjectProperty(None, allownone=True)
    _change_touch_mode_ev = None

    def _get_slides_container(self):
        return [x.parent for x in self.slides]

    def _get_index(self):
        if self.slides:
            return self._index % len(self.slides)
        return None

    def _set_index(self, value):
        if self.slides:
            self._index = value % len(self.slides)
        else:
            self._index = None

    def _prev_slide(self):
        slides = self.slides
        len_slides = len(slides)
        index = self.index
        if len_slides < 2:  # None, or 1 slide
            return None
        if len_slides == 2:
            if index == 0:
                return None
            if index == 1:
                return slides[0]
        if self.loop and index == 0:
            return slides[-1]
        if index > 0:
            return slides[index - 1]

    def _prev_prev_slide(self):
        if self.index > 1:
            return self.slides[self.index - 2]

    def _curr_slide(self):
        if len(self.slides):
            return self.slides[self.index or 0]

    def _next_slide(self):
        if len(self.slides) < 2:  # None, or 1 slide
            return None
        if len(self.slides) == 2:
            if self.index == 0:
                return self.slides[1]
            if self.index == 1:
                return None
        if self.loop and self.index == len(self.slides) - 1:
            return self.slides[0]
        if self.index < len(self.slides) - 1:
            return self.slides[self.index + 1]

    def _next_next_slide(self):
        if self.index < len(self.slides) - 2:
            return self.slides[self.index + 2]

    slides_container = AliasProperty(_get_slides_container, bind=('slides',))
    index = AliasProperty(_get_index, _set_index, bind=('_index', 'slides'), cache=True)
    previous_slide = AliasProperty(_prev_slide, bind=('slides', 'index', 'loop'), cache=True)
    previous_previous_slide = AliasProperty(_prev_prev_slide, bind=('slides', 'index', 'loop'), cache=True)
    current_slide = AliasProperty(_curr_slide, bind=('slides', 'index'), cache=True)
    next_slide = AliasProperty(_next_slide, bind=('slides', 'index', 'loop'), cache=True)
    next_next_slide = AliasProperty(_next_next_slide, bind=('slides', 'index', 'loop'), cache=True)

    def __init__(self, **kwargs):
        self._trigger_position_visible_slides = Clock.create_trigger(
            self._position_visible_slides, -1)
        super(CustomCarousel, self).__init__(**kwargs)
        self._skip_slide = None
        self.touch_mode_change = False

    def load_slide(self, slide):
        slides = self.slides
        start, stop = slides.index(self.current_slide), slides.index(slide)
        if start == stop:
            return

        self._skip_slide = stop
        if stop > start:
            self._insert_visible_slides(_next_slide=slide)
            self.load_next()
        else:
            self._insert_visible_slides(_prev_slide=slide)
            self.load_previous()

    def load_previous(self):
        self.load_next(mode='prev')

    def load_next(self, mode='next'):
        if self.index is not None:
            w, h = (275, 200)
            _direction = {
                'top': -h / 2,
                'bottom': h / 2,
                'left': w / 2,
                'right': -w / 2}
            _offset = _direction[self.direction]
            if mode == 'prev':
                _offset = -_offset

            self._start_animation(min_move=0, offset=_offset)

    def get_slide_container(self, slide):
        return slide.parent

    def _insert_visible_slides(self, _next_slide=None, _prev_slide=None, _next_next_slide=None, _prev_prev_slide=None):
        get_slide_container = self.get_slide_container

        previous_slide = _prev_slide if _prev_slide else self.previous_slide
        if previous_slide:
            self._prev = get_slide_container(previous_slide)
        else:
            self._prev = None

        current_slide = self.current_slide
        if current_slide:
            self._current = get_slide_container(current_slide)
        else:
            self._current = None

        next_slide = _next_slide if _next_slide else self.next_slide
        if next_slide:
            self._next = get_slide_container(next_slide)
        else:
            self._next = None

        next_next_slide = _next_next_slide if _next_next_slide else self.next_next_slide
        if next_next_slide:
            self._next_next = get_slide_container(next_next_slide)
        else:
            self._next_next = None

        previous_previous_slide = _prev_prev_slide if _prev_prev_slide else self.previous_previous_slide
        if previous_previous_slide:
            self._prev_prev = get_slide_container(previous_previous_slide)
        else:
            self._prev_prev = None

        super_remove = super(CustomCarousel, self).remove_widget
        for container in self.slides_container:
            super_remove(container)

        if self._prev and self._prev.parent is not self:
            super(CustomCarousel, self).add_widget(self._prev)
        if self._prev_prev and self._prev_prev.parent is not self:
            super(CustomCarousel, self).add_widget(self._prev_prev)
        if self._next and self._next.parent is not self:
            super(CustomCarousel, self).add_widget(self._next)
        if self._next_next and self._next_next.parent is not self:
            super(CustomCarousel, self).add_widget(self._next_next)
        if self._current:
            super(CustomCarousel, self).add_widget(self._current)

    def _position_visible_slides(self, *args):
        slides, index = self.slides, self.index
        no_of_slides = len(slides) - 1
        if not slides:
            return
        x, y, width, height = self.x, self.y, 275, self.height
        _offset, direction = self._offset, self.direction
        _prev, _prev_prev, _next, _next_next, _current = self._prev, self._prev_prev, self._next, self._next_next, self._current
        get_slide_container = self.get_slide_container
        last_slide = get_slide_container(slides[-1])
        first_slide = get_slide_container(slides[0])
        skip_next = False
        _loop = self.loop

        if direction[0] in ['r', 'l']:
            xoff = x + _offset + 62.5
            x_prev = {'l': xoff + width, 'r': xoff - width}
            x_next = {'l': xoff - width, 'r': xoff + width}

            x_prev_prev = {'l': xoff + width + width, 'r': xoff - width - width}
            x_next_next = {'l': xoff - width - width, 'r': xoff + width + width}
            if _prev:
                _prev.pos = (x_prev[direction[0]], y)
            if _prev_prev:
                _prev_prev.pos = (x_prev_prev[direction[0]], y)
            elif _loop and _next and index == 0:
                # if first slide is moving to right with direction set to right
                # or toward left with direction set to left
                if ((_offset > 0 and direction[0] == 'r') or
                        (_offset < 0 and direction[0] == 'l')):
                    # put last_slide before first slide
                    last_slide.pos = (x_prev[direction[0]], y)
                    skip_next = True
            if _current:
                _current.pos = (xoff, y)
            if skip_next:
                return
            if _next:
                _next.pos = (x_next[direction[0]], y)
            if _next_next:
                _next_next.pos = (x_next_next[direction[0]], y)
            elif _loop and _prev and index == no_of_slides:
                if ((_offset < 0 and direction[0] == 'r') or
                        (_offset > 0 and direction[0] == 'l')):
                    first_slide.pos = (x_next[direction[0]], y)
        if direction[0] in ['t', 'b']:
            yoff = y + _offset
            y_prev = {'t': yoff - height, 'b': yoff + height}
            y_next = {'t': yoff + height, 'b': yoff - height}
            if _prev:
                _prev.pos = (x, y_prev[direction[0]])
            elif _loop and _next and index == 0:
                if ((_offset > 0 and direction[0] == 't') or
                        (_offset < 0 and direction[0] == 'b')):
                    last_slide.pos = (x, y_prev[direction[0]])
                    skip_next = True
            if _current:
                _current.pos = (x, yoff)
            if skip_next:
                return
            if _next:
                _next.pos = (x, y_next[direction[0]])
            elif _loop and _prev and index == no_of_slides:
                if ((_offset < 0 and direction[0] == 't') or
                        (_offset > 0 and direction[0] == 'b')):
                    first_slide.pos = (x, y_next[direction[0]])

    def on_size(self, *args):
        size = (275, 200)
        for slide in self.slides_container:
            slide.size = size
        self._trigger_position_visible_slides()

    def on_pos(self, *args):
        self._trigger_position_visible_slides()

    def on_index(self, *args):
        self._insert_visible_slides()
        self._trigger_position_visible_slides()
        self._offset = 0

    def on_slides(self, *args):
        if self.slides:
            self.index = self.index % len(self.slides)
        self._insert_visible_slides()
        self._trigger_position_visible_slides()

    def on__offset(self, *args):
        self._trigger_position_visible_slides()
        # if reached full offset, switch index to next or prev
        direction = self.direction
        _offset = self._offset
        width = 275
        height = self.height
        index = self.index
        if self._skip_slide is not None or index is None:
            return

        # Move to next slide?
        if (direction[0] == 'r' and _offset <= -width) or \
                (direction[0] == 'l' and _offset >= width) or \
                (direction[0] == 't' and _offset <= - height) or \
                (direction[0] == 'b' and _offset >= height):
            if self.next_slide:
                self.index += 1

        # Move to previous slide?
        if (direction[0] == 'r' and _offset >= width) or \
                (direction[0] == 'l' and _offset <= -width) or \
                (direction[0] == 't' and _offset >= height) or \
                (direction[0] == 'b' and _offset <= -height):
            if self.previous_slide:
                self.index -= 1

    def _start_animation(self, *args, **kwargs):
        # compute target offset for ease back, next or prev
        new_offset = 0
        direction = kwargs.get('direction', self.direction)
        is_horizontal = direction[0] in ['r', 'l']
        extent = 275 if is_horizontal else self.height
        min_move = kwargs.get('min_move', self.min_move)
        _offset = kwargs.get('offset', self._offset)

        if _offset < min_move * -extent:
            new_offset = -extent
        elif _offset > min_move * extent:
            new_offset = extent

        # if new_offset is 0, it wasnt enough to go next/prev
        dur = self.anim_move_duration
        if new_offset == 0:
            dur = self.anim_cancel_duration

        # detect edge cases if not looping
        len_slides = len(self.slides)
        index = self.index
        if not self.loop or len_slides == 1:
            is_first = (index == 0)
            is_last = (index == len_slides - 1)
            if direction[0] in ['r', 't']:
                towards_prev = (new_offset > 0)
                towards_next = (new_offset < 0)
            else:
                towards_prev = (new_offset < 0)
                towards_next = (new_offset > 0)
            if (is_first and towards_prev) or (is_last and towards_next):
                new_offset = 0

        anim = Animation(_offset=new_offset, d=dur, t=self.anim_type)
        anim.cancel_all(self)

        def _cmp(*l):
            if self._skip_slide is not None:
                self.index = self._skip_slide
                self._skip_slide = None

        anim.bind(on_complete=_cmp)
        anim.start(self)

    def _get_uid(self, prefix='sv'):
        return '{0}.{1}'.format(prefix, self.uid)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('cavoid')] = True
            return
        if self.disabled:
            return True
        if self._touch:
            return super(CustomCarousel, self).on_touch_down(touch)
        Animation.cancel_all(self)
        self._touch = touch
        uid = self._get_uid()
        touch.grab(self)
        touch.ud[uid] = {
            'mode': 'unknown',
            'time': touch.time_start}
        self._change_touch_mode_ev = Clock.schedule_once(
            self._change_touch_mode, self.scroll_timeout / 1000.)
        self.touch_mode_change = False
        return True

    def on_touch_move(self, touch):
        if not self.touch_mode_change:
            if self.ignore_perpendicular_swipes and \
                    self.direction in ('top', 'bottom'):
                if abs(touch.oy - touch.y) < self.scroll_distance:
                    if abs(touch.ox - touch.x) > self.scroll_distance:
                        self._change_touch_mode()
                        self.touch_mode_change = True
            elif self.ignore_perpendicular_swipes and \
                    self.direction in ('right', 'left'):
                if abs(touch.ox - touch.x) < self.scroll_distance:
                    if abs(touch.oy - touch.y) > self.scroll_distance:
                        self._change_touch_mode()
                        self.touch_mode_change = True

        if self._get_uid('cavoid') in touch.ud:
            return
        if self._touch is not touch:
            super(CustomCarousel, self).on_touch_move(touch)
            return self._get_uid() in touch.ud
        if touch.grab_current is not self:
            return True
        ud = touch.ud[self._get_uid()]
        direction = self.direction
        if ud['mode'] == 'unknown':
            if direction[0] in ('r', 'l'):
                distance = abs(touch.ox - touch.x)
            else:
                distance = abs(touch.oy - touch.y)
            if distance > self.scroll_distance:
                ev = self._change_touch_mode_ev
                if ev is not None:
                    ev.cancel()
                ud['mode'] = 'scroll'
        else:
            if direction[0] in ('r', 'l'):
                self._offset += touch.dx
            if direction[0] in ('t', 'b'):
                self._offset += touch.dy
        return True

    def on_touch_up(self, touch):
        if self._get_uid('cavoid') in touch.ud:
            return
        if self in [x() for x in touch.grab_list]:
            touch.ungrab(self)
            self._touch = None
            ud = touch.ud[self._get_uid()]
            if ud['mode'] == 'unknown':
                ev = self._change_touch_mode_ev
                if ev is not None:
                    ev.cancel()
                super(CustomCarousel, self).on_touch_down(touch)
                Clock.schedule_once(partial(self._do_touch_up, touch), .1)
            else:
                self._start_animation()

        else:
            if self._touch is not touch and self.uid not in touch.ud:
                super(CustomCarousel, self).on_touch_up(touch)
        return self._get_uid() in touch.ud

    def _do_touch_up(self, touch, *largs):
        super(CustomCarousel, self).on_touch_up(touch)
        # don't forget about grab event!
        for x in touch.grab_list[:]:
            touch.grab_list.remove(x)
            x = x()
            if not x:
                continue
            touch.grab_current = x
            super(CustomCarousel, self).on_touch_up(touch)
        touch.grab_current = None

    def _change_touch_mode(self, *largs):
        if not self._touch:
            return
        self._start_animation()
        uid = self._get_uid()
        touch = self._touch
        ud = touch.ud[uid]
        if ud['mode'] == 'unknown':
            touch.ungrab(self)
            self._touch = None
            super(CustomCarousel, self).on_touch_down(touch)
            return

    def add_widget(self, widget, index=0, canvas=None):
        slide = RelativeLayout(size=(275, 200), x=self.x - 275, y=self.y)
        slide.add_widget(widget)
        super(CustomCarousel, self).add_widget(slide, index, canvas)
        if index != 0:
            self.slides.insert(index - len(self.slides), widget)
        else:
            self.slides.append(widget)

    def remove_widget(self, widget, *args, **kwargs):
        # XXX be careful, the widget.parent refer to the RelativeLayout
        # added in add_widget(). But it will break if RelativeLayout
        # implementation change.
        # if we passed the real widget
        if widget in self.slides:
            slide = widget.parent
            self.slides.remove(widget)
            return slide.remove_widget(widget, *args, **kwargs)
        return super(CustomCarousel, self).remove_widget(widget, *args, **kwargs)

    def clear_widgets(self):
        for slide in self.slides[:]:
            self.remove_widget(slide)
        super(CustomCarousel, self).clear_widgets()
