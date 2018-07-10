# A dimmable Light Bulb accessory
#
# Based on https://github.com/ikalchev/HAP-python/blob/dev/accessories/LightBulb.py
# but then butchered by M J Oldfield
#

from pwm import PWM
import evdev

from pyhap.accessory import Accessory
from pyhap.const     import CATEGORY_LIGHTBULB

def clamp(min, max, x):
    if x < min:
        return min
    if x > max:
        return max
    return x

class LightBulb(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, driver, *args,pwm_channel=0, evdevs=[], **kwargs):
        super().__init__(driver, *args, **kwargs)

        chars = [ ( 'On',         self.set_on )
                , ( 'Brightness', self.set_brightness )
                ] 

        server = self.add_preload_service(
            'Lightbulb', chars = [ name for (name,_) in chars ])

        self.char = {}
        for (name, setter) in chars:
            self.char[name] = server.configure_char(name, setter_callback = setter)

        self.pwm_channel = pwm_channel
        self.brightness  = 1.0  # fraction
        self.bri_delta   = 0.05
        self.is_on       = False

        # Initialize this now, so that it has time to initialize
        # properly before we call it
        self.pwm_device  = PWM(self.pwm_channel)
        self.pwm_device.export()

        self.local_update = False
        for d in evdevs:
            driver.async_add_job(self.event_handler(d))

    def set_on(self, value):
        self.is_on = bool(value)
        self.set_bulb()

    def set_brightness(self, value):
        # HAP spec says brightness is specified as a percentage
        self.brightness = float(value) / 100.0
        self.set_bulb()

    # push local state to PWM
    def set_bulb(self):
        if self.is_on and self.brightness > 0:
            theta  = self.brightness ** 2.5
            self.set_pwm_state(theta)
        else:
            self.set_pwm_state(0)

    # actually drive PWM device
    def set_pwm_state(self, f):
        pwm_period = 1000000 # 1ms = 1000000ns => 1kHz

        self.pwm_device.period     = pwm_period
        self.pwm_device.duty_cycle = int(f * pwm_period)
        self.pwm_device.enable     = True

    def stop(self):
        super().stop()

    # handler for linux events (which come from controls on the
    # lamp).
    async def event_handler(self, dev):
      async for e in dev.async_read_loop():

        # all events _might_ update local state variables...
        t = e.type
        v = e.value

        # key presses toggle state...
        if   t == evdev.ecodes.EV_KEY and v == 1:
            self.is_on = not(self.is_on)
            self.local_update = True

        # rotary encoder changes brightness (and turns light on)...
        elif t == evdev.ecodes.EV_REL and v != 0:
            if not self.is_on:
                self.is_on = True
                self.local_update = True

            b = clamp(0, 1.0, self.brightness + v * self.bri_delta)

            if self.brightness != b:
                self.brightness = b
                self.local_update = True

        # if the state has changed push those changes to the bulb
        if self.local_update:
            self.set_bulb()
            # don't reset the flag here: only do that when we push the
            # changes back to HomeKit

    @Accessory.run_at_interval(1)
    def run(self):
        if self.local_update:
            self.char['On'].set_value(self.is_on)
            self.char['Brightness'].set_value(int(100.0 * self.brightness))
            self.local_update = False
            
        
