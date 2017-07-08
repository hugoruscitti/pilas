# piTweener
#
# Tweening functions for python
#
# Heavily based on caurina Tweener: http://code.google.com/p/tweener/
# Forked from pyTweener:
# http://wiki.python-ogre.org/index.php/CodeSnippits_pyTweener
#
# Released under the MIT License - see above url
# Original Python version by Ben Harling 2009
# Bugfixes and fork by Benjamin Woodruff 2010
#
#
# Copyright (c) Ben Harling (2009), Benjamin Woodruff (2010)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import math

class TweenerEquations(object):
    """A set of predefined interpolation (tweening) equations. They are ported
       from the work of Robert Penner. Each equation takes 4 arguments, the
       current time from start, the start value, the desired final change from
       the start value, and the total duration of the tween. As is the nature of
       interpolation, no equation has units.

       **Note:** When using the Tweener class, you should use the Tweener class'
       instance copies of the equations (Tweener extends TweenerEquations)
       """

    def OUT_EXPO(self, t, b, c, d):
        if t == d:
            return b + c
        return c * (-2 ** (-10 * t / d) + 1) + b;

    def LINEAR(self, t, b, c, d):
        return c * t / d + b

    def IN_QUAD(self, t, b, c, d):
        t /= d
        return c * t * t + b

    def OUT_QUAD(self, t, b, c, d):
        t /= d
        return -c * t * (t - 2) + b

    def IN_OUT_QUAD(self, t, b, c, d):
        t /= d * .5
        if t < 1.:
            return c * .5 * t * t + b
        t -= 1.
        return -c * .5 * (t * (t - 2.) - 1.) + b

    def OUT_IN_QUAD(self, t, b, c, d):
        if t < d * .5:
            return self.OUT_QUAD(t * 2, b, c * .5, d)
        return self.IN_QUAD(t * 2 - d, b + c * .5, c * .5, d)

    def IN_CUBIC(self, t, b, c, d):
        t /= d
        return c * t * t * t + b

    def OUT_CUBIC(self, t, b, c, d):
        t = t / d - 1
        return c * (t * t * t + 1) + b

    def IN_OUT_CUBIC(self, t, b, c, d):
        t /= d * .5
        if t < 1:
            return c * .5 * t * t * t + b
        t -= 2
        return c * .5 * (t * t * t + 2) + b

    def OUT_IN_CUBIC(self, t, b, c, d ):
        if t < d * .5:
            return self.OUT_CUBIC (t * 2., b, c * .5, d)
        return self.IN_CUBIC(t * 2. - d, b + c * .5, c * .5, d)

    def IN_QUART(self, t, b, c, d):
        t /= d
        return c * t * t * t * t + b

    def OUT_QUART(self, t, b, c, d):
        t = t / d - 1
        return -c * (t * t * t * t - 1) + b

    def IN_OUT_QUART(self, t, b, c, d):
        t /= d * .5
        if t < 1:
            return c * .5 * t * t * t * t + b
        t -= 2
        return -c / 2 * (t * t * t * t - 2) + b

    def OUT_ELASTIC(self, t, b, c, d):
        if t == 0:
            return b
        t /= d
        if t == 1:
            return b + c
        p = d * .3 # period
        a = 1. # amplitude
        if a < abs(c):
            a = c
            s = p / 4
        else:
            s = p / (2. * math.pi) * math.asin(c / a)

        return (a * 2. ** (-10. * t) * math.sin((t * d - s) * (2. * math.pi)
                                                / p) + c + b)

class Tweener(TweenerEquations):
    """This class manages all active tweens, and provides a factory for
        creating and spawning tween motions.
        """

    def __init__(self):
        self.current_tweens = []
        self.default_tween_type = self.IN_OUT_QUAD
        self.default_duration = 1.0
        self.prev_time = time.time()

    def count_tweens(self):
        return len(self.current_tweens)

    def has_tweens(self):
        """Returns ``True`` if there are any tweens (paused or unpaused),
           ``False`` otherwise. This function can be useful to determine if a
           redraw should be done or not.
           """
        return len(self.current_tweens) > 0


    def add_tween(self, obj, inicial=None, **kwargs):
        """Returns Tween object or False

           Example::

               tweener.add_tween(my_rocket, throttle=50, set_thrust=400,
                                 tween_time=5.0, tween_type=tweener.OUT_QUAD)

           You must first specify an object, and at least one property or
           function with a corresponding change value. The tween will throw an
           error if you specify an attribute the object does not possess. Also
           the data types of the change and the initial value of the tweened
           item must match. If you specify a 'set' -type function, the tweener
           will attempt to get the starting value by call the corresponding
           'get' function on the object. If you specify a property, the tweener
           will read the current state as the starting value. You add both
           functions and property changes to the same tween.

           in addition to any properties you specify on the object, these
           keywords do additional setup of the tween.

           * ``tween_time``: the duration of the motion
           * ``tween_type``: a predefined tweening equation or your own function
           * ``on_complete_function``: called on completion of the tween
           * ``on_update_function``: called every time the tween updates
           * ``tween_delay``: a delay before starting.
           """
        if "tween_time" in kwargs:
            t_time = kwargs.pop("tween_time")
        else:
            t_time = self.default_duration

        if "tween_type" in kwargs:
            t_type = kwargs.pop("tween_type")
        else:
            t_type = self.default_tween_type

        if "on_complete_function" in kwargs:
            t_complete_func = kwargs.pop("on_complete_function")
        else:
            t_complete_func = None

        if "on_update_function" in kwargs:
            t_update_func = kwargs.pop("on_update_function")
        else:
            t_update_func = None

        if "tween_delay" in kwargs:
            t_delay = kwargs.pop("tween_delay")
        else:
            t_delay = 0

        tw = Tween(obj, t_time, t_type, t_complete_func, t_update_func, t_delay,
                   inicial=inicial,
                   **kwargs)
        if tw:
            self.current_tweens.append(tw)
        return tw

    def remove_all_tweens(self):
        "Stops and removes every tween associated with this Tweener object."
        for i in self.current_tweens:
            i.complete = True
        self.current_tweens = []

    def remove_tween(self, tween_obj):
        "Stops and removes the Tween instance passed."
        if tween_obj in self.current_tweens:
            tween_obj.complete = True
            self.current_tweens.remove(tween_obj)

    def get_tweens_affecting_object(self, obj):
        """Get a list of all tweens acting on the specified object. Useful for
           manipulating tweens on the fly.
           """
        tweens = []
        for t in self.current_tweens:
            if t.target is obj:
                tweens.append(t)
        return tweens

    def remove_tweening_from(self, obj):
        """Stop tweening an object, without completing the motion or firing the
           complete_function.
           """
        # TODO: This loop could be optimized a bit
        for t in self.current_tweens[:]:
            if t.target is obj:
                t.complete = True
                self.current_tweens.remove(t)

    def update(self, time_since_last_frame=None):
        """Update every tween with the time since the last frame. If there is an
           update function, it is always called whether the tween is running or
           paused.

           ``time_since_last_frame`` is the change in time in seconds. If no
           value is passed, the change in time is measured with time.time() from
           the previous call of this function. If it is the first time calling
           this function, timing is measured from the construction of the
           Tweener engine.
           """
        current_time = time.time()
        if time_since_last_frame is None:
            time_since_last_frame = current_time - self.prev_time
        self.prev_time = current_time
        for t in self.current_tweens:
            t.update(time_since_last_frame)
            if t.complete:
                self.current_tweens.remove(t)

    def update_time_without_motion(self):
        current_time = time.time()
        self.prev_time = current_time

    def force_update_one_frame(self):
        self.update(1/60.0)


class Tween(object):
    def __init__(self, obj, tduration, tween_type, complete_function,
                 update_function, delay, inicial, **kwargs):
        """Tween object:
           Can be created directly, but much more easily using
           ``Tweener.add_tween(...)``
           """
        self.duration = tduration
        self.delay = delay
        self.target = obj
        self.tween = tween_type
        self.tweenables = kwargs
        self.delta = 0
        self.complete_function = complete_function
        self.update_function = update_function
        self.complete = False
        self.t_props = []
        self.t_funcs = []
        self.paused = self.delay > 0
        self.decode_arguments(inicial)

    def decode_arguments(self, inicial):
        """Internal setup procedure to create tweenables and work out how to
           deal with each
           """

        if len(self.tweenables) == 0:
            # nothing to do
            raise BaseException("No Tweenable properties or functions defined")
            self.complete = True
            return

        for k, v in self.tweenables.items():

            # check that it's compatible
            if not hasattr(self.target, k):
                raise AttributeError(str(self.target) + " has no function " + k)
                self.complete = True
                continue

            prop = func = False
            start_val = 0
            change = v

            var = getattr(self.target, k)

            if hasattr(var, "__call__"):
                func = var
                func_name = k
            else:
                if inicial:
                    start_val = inicial
                else:
                    start_val = var
                change = v - start_val
                prop = k
                prop_name = k


            if func:
                try:
                    get_func = getattr(self.target,
                                       func_name.replace("set", "get"))
                    start_val = get_func()
                    change = v - start_val
                except:
                    # no start value, assume its 0
                    # but make sure the start and change
                    # datatypes match :)
                    startVal = change * 0
                tweenable = Tweenable(start_val, change)
                new_func = [k, func, tweenable]


                self.t_funcs.append(new_func)


            if prop:
                tweenable = Tweenable(start_val, change)
                new_prop = [k, prop, tweenable]
                self.t_props.append(new_prop)


    def pause(self, seconds = -1):
        """Pause this tween

           Do ``tween.pause(2)`` to pause for a specific time, or
           ``tween.pause()`` which pauses indefinitely.
           """
        self.paused = True
        self.delay = seconds

    def resume(self):
        "Resume from pause"
        if self.paused:
            self.paused = False

    def update(self, ptime=None):
        """Update this tween with the time since the last frame. If there is an
           update function, it is always called whether the tween is running or
           paused. ptime is the change in time in seconds.
           """

        if self.paused:
            if self.delay > 0:
                self.delay = max(0, self.delay - ptime)
                if self.delay == 0:
                    self.paused = False
                    self.delay = -1
                    return  # ARREGLO PARA EVITAR QUE DOS INTERPOLACIONES SE SOLAPEN.
                if self.update_function:
                    self.update_function()
            return

        self.delta = min(self.delta + ptime, self.duration)

        if not self.complete:
            for prop_name, prop, tweenable in self.t_props:
                setattr(self.target, prop,
                        self.tween(self.delta, tweenable.start_value,
                                   tweenable.change, self.duration))
            for func_name, func, tweenable in self.t_funcs:
                func(
                    self.tween(self.delta, tweenable.start_value,
                               tweenable.change, self.duration)
                )


        if self.delta == self.duration:
            self.complete = True
            if self.complete_function:
                self.complete_function()

        if self.update_function:
            self.update_function()



    def get_tweenable(self, name):
        """Return the tweenable values corresponding to the name of the original
        tweening function or property.

        Allows the parameters of tweens to be changed at runtime. The parameters
        can even be tweened themselves!

        Eg::

            # the rocket needs to escape!! -- we're already moving, but must go
            # faster!
            twn = tweener.get_tweens_affecting_object(my_rocket)[0]
            tweenable = twn.get_tweenable("thruster_power")
            tweener.addTween(tweenable, change=1000.0, tween_time=0.4,
                             tween_type=tweener.IN_QUAD)
        """
        ret = None
        for n, f, t in self.t_funcs:
            if n == name:
                ret = t
                return ret
        for n, p, t in self.t_props:
            if n == name:
                ret = t
                return ret
        return ret




    def Remove(self):
        "Disables and removes this tween without calling the complete function"
        self.complete = True



class Tweenable(object):
    def __init__(self, start, change):
        """Tweenable:
            Holds values for anything that can be tweened
            these are normally only created by Tweens
            """
        self.start_value = start
        self.change = change



class TweenTestObject(object):
    def __init__(self):
        self.pos = 20
        self.rot = 50

    def update(self):
        print(str(self.pos) + ", " + str(self.rot))

    def set_rotation(self, rot):
        self.rot = rot

    def get_rotation(self):
        return self.rot

    def complete(self):
        print("I'm done tweening now mommy!")



if __name__=="__main__":
    import time
    T = Tweener()
    tst = TweenTestObject()
    mt = T.add_tween(tst, tween_time=2.5, tween_type=T.LINEAR, pos=-200,
                     on_complete_function=tst.complete,
                     on_update_function=tst.update)
    changed = False
    while T.has_tweens():
        T.update()
        time.sleep(.06)
    print("finished: " + str(tst.get_rotation()) + ", " + str(tst.pos))
