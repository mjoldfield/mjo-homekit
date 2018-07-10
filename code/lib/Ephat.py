# An envirophat accessory
#
# Based on https://github.com/ikalchev/HAP-python/blob/dev/accessories/*.py
# but then butchered by M J Oldfield
#

from pyhap.accessory import Accessory
from pyhap.const     import CATEGORY_SENSOR

from envirophat import light, weather

class Ephat(Accessory):

    category = CATEGORY_SENSOR

    def __init__(self, driver, *args, **kwargs):
        super().__init__(driver, *args, **kwargs)

        chars = { 'LightSensor':
                  [ ( 'CurrentAmbientLightLevel',  lambda: light.light() )
                  ]
                  ,
                  'TemperatureSensor':
                  [ ( 'CurrentTemperature', lambda: weather.temperature() )
                  ]
                  ,
                  'Switch':
                  [ ('On', lambda: light.light() < 100)
                  ]
                }

        self.chars = []
        for sname, charlist in chars.items():
            cnames = [ name for (name,_) in charlist ]
            service = self.add_preload_service(sname, chars = cnames)

            for (name, getter) in charlist:
                c = service.configure_char(name)
                self.chars.append((c, getter))
            
    @Accessory.run_at_interval(3)
    def run(self):
        for (char, getter) in self.chars:
            v = getter()
            char.set_value(v)
            
        
