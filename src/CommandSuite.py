class CommandSuite(object):
    """Abstract class for command modules"""

    def __init__(self, name):
        """Declare some variables, etc"""
        self.name = name
        print("CommandSuite is starting")

    def parse(self, data):
        """Test method for this module"""

        print("Test module is echoing data...")
        print(data)

    def finish(self):
        """Function that gets called as TwircBot is shutting down"""
        print("CommandSuite is finishing")
        
    
