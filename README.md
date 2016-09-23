#twircBot  

The TWitch IRC Bot is a basic bot that connects to [Twitch.tv](https://www.twitch.tv/)'s IRC network for the purposes of keeping chat logs.  

##Running twircBot  
###Default configuration  
twircBot can be run by simply using the ``start()`` method.  

```python  
from twircbot.twircbot import TwircBot  
TwircBot().start()  
```  

twircBot's default configuration is not very interesting. It will anonymously connect to the ``#twircbot`` channel and log whatever chat it sees there. You can get more useful behavior by specifying your own configuration file and referencing it when you instantiate twircBot:  ``TwircBot("myFile.config").start()``.  

The source includes a simple script, ``runTwircBot.py``, that will automatically open a connection. It will optionally take a command line argument to use a particular configuration: 

```bash  
$ runTwircBot.py                    # Default config  
$ runTwircBot.py myFile.config      # User-specifed config  
```  
###User-specified configuration  
The source includes a sample configuration file: ``config/sample.config``. That should be enough to get most people up and running quickly. Check out [the documentation](https://github.com/johnmarcampbell/twircBot/blob/master/doc/Documentation.md) for more details on configuring twircBot.  

##What about Python versions?  
twircBot is currently being developed under Python 3.5.1. It is explicitly *incompatible* with Python 2.x, and probably always will be.  

