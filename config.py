import ConfigParser, os

config = ConfigParser.RawConfigParser()
config.read('test.cfg')

for section in config.sections():
    print section
    for option in config.options(section):
        print " ", option

