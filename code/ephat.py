# The main file to publish data from an EnviropHat to HomeKit

# Based heavily on the standard example in
# https://github.com/ikalchev/HAP-python/blob/master/main.py

import sys
sys.path.append('lib')

import logging
import signal

from pyhap.accessory_driver import AccessoryDriver

from Ephat import Ephat

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

driver = AccessoryDriver(persist_file='ephat.state')
logger.info("pincode %s", driver.state.pincode)

ephat = Ephat(driver, 'ToyEnvphat')
driver.add_accessory(accessory=ephat)

# We want SIGTERM (kill) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()
