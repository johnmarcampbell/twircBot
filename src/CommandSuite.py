class CommandSuite(object):
    """Abstract class for command suites"""

    def __init__(self, name):
        """Declare some variables, etc"""
        self.name = name
        print("CommandSuite is starting")

    def parse(self, data):
        """Test method for this suite"""

        print("Test suite is echoing data...")
        print(data)

    def finish(self):
        """Function that gets called as TwircBot is shutting down"""
        print("CommandSuite is finishing")
        
    def set_host(self, host):
        """Set the host bot object"""

        self.host = host
