# The main file to implement a dimmable HomeKit
# lightbulb.

# Based heavily on the standard example in
# https://github.com/ikalchev/HAP-python/blob/master/main.py

import sys
sys.path.append('lib')

import logging
import signal
import evdev

from pyhap.accessory_driver import AccessoryDriver

from LightBulb import LightBulb

logging.basicConfig(level=logging.INFO)

driver = AccessoryDriver(port=51826, persist_file='lamp.state')

lamp = LightBulb(driver, 'ToyLamp'
                 , evdevs = [ evdev.InputDevice(f) for f in evdev.list_devices() ]
                 )

driver.add_accessory(accessory=lamp)

# We want SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()
