#TwircBot  

The TWitch IRC Bot is a basic bot that connects to [Twitch.tv](https://www.twitch.tv/)'s IRC network for the purposes of keeping chat logs.

##Running TwircBot
###Default configuration
TwircBot can be run by simply using the ``start()`` method.

```python
from TwircBot import TwircBot
TwircBot().start()
```

TwircBot's default configuration is not very interesting. It will anonymously connect to the ``#twircbot`` channel and log whatever chat it sees there. You can get more useful behavior by specifying your own configuration file and referencing it when you instantiate TwircBot:  ``TwircBot("myFile.config").start()``.

The source includes a simple script, ``runTwircBot.py``, that will automatically open a connection. It will optionally take a command line argument to use a particular configuration: 

```bash
$ python3 runTwircBot.py                    # Default config
$ python3 runTwircBot.py myFile.config      # User-specifed config
```
###User-specified configuration
You can find an example configuration file at ``config/sample.config``. That should be enough to get most people up and running quickly. Check out [the documentation](https://github.com/johnmarcampbell/twircBot/blob/master/doc/Documentation.md) for more details on configuring TwircBot.

##What about Python versions?
TwircBot is currently being developed under Python 3.5.1. It is explicitly *incompatible* with Python 2.x, and probably always will be.