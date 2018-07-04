# DIY HomeKit accessories

Simple accessories written in Python for Apple’s HomeKit API.

Most of the hard work has been done by other people:

## HAP-python

[Ivan Kalchev](https://github.com/ikalchev) wrote the key HomeKit
library, which you can see on [GitHub](https://github.com/ikalchev/HAP-python)

He provides example code under the Apache License, version 2.0, which
I have butchered to make my accessories. This applies to:

* code/lamp.py

* code/lib/LightBulb.py

## PWM

[Scott Ellis](https://github.com/scottellis/) released a Python class
which wraps the sysfs PWM device. It’s just one file, so I’ve copied
it into this repo, making a small edit en route. Scott’s [original
repo](https://github.com/scottellis/pwmpy) has good documentation.

This file is covered by the New BSD license.

# Related resources

You might find this interesting:

* [A HomeKit light](http://mjoldfield.com/atelier/atelier-dest/2018/06/homekit-light.html)
