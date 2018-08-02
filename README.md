# DIY HomeKit accessories

Simple accessories written in Python for Apple’s HomeKit API.

Presently there is:

* [a light](https://mjoldfield.com/atelier/atelier-dest/2018/06/homekit-light.html);

* [a temperature and light sensor](https://mjoldfield.com/atelier/2018/07/homekit-ephat.html) based around
   the [Enviro pHAT](https://shop.pimoroni.com/products/enviro-phat).

# Credits 

Most of the hard work has been done by other people:

## HAP-python

[Ivan Kalchev](https://github.com/ikalchev) wrote the key HomeKit
library, which you can see on [GitHub](https://github.com/ikalchev/HAP-python)

He provides example code under the Apache License, version 2.0, which
I have butchered to make my accessories. This applies to:

* code/*.py

* code/lib/*.py except code/lib/pwm.py

## PWM

[Scott Ellis](https://github.com/scottellis/) released a Python class
which wraps the sysfs PWM device. It’s just one file, so I’ve copied
it into this repo, making a small edit en route. Scott’s [original
repo](https://github.com/scottellis/pwmpy) has good documentation.

This file is covered by the New BSD license.

