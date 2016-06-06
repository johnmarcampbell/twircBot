#TwircBot  

The TWitch IRC Bot is a basic bot that connects to [Twitch.tv](https://www.twitch.tv/)'s IRC network for the purposes of keeping chat logs.

##Running TwircBot
TwircBot can be run by simply using the ``connect()`` method.

```python
from TwircBot import TwircBot
TwircBot().connect()
```

TwircBot's default configuration is not very interesting. It will anonymously connect to the ``#twircbot`` channel and log whatever chat it sees there. You can get more useful behavior by specifying your own configuration file and referencing it when you instantiate TwircBot:  ``bot = TwircBot("myFile.config")``.

The source includes a simple script, ``runTwircBot.py``, that will automatically open a connection. It will optionally take a command line argument to use a particular configuration: 

```
$ python3 runTwircBot.py                    # Default config
$ python3 runTwircBot.py myFile.config      # User-specifed config
```

##Writing your own config file
The syntax for specifying your own configuration options is very simple:
- Write options in a ``key: value`` format. Example: ``nick: coolGuy42``. The semi-colon may be omitted: ``nick coolGuy42`` is fine too.
- Multiple ``value``'s are seperated with spaces: ``key: value1 value2``. This is only necessary when you wish to connect to multiple ``channels``.
- If you want to specify a ``value`` that has a space, you can surround it with *single* quotes. Example: ``time_format: '[%Y-%m-%d %H:%M:%S]'``

A sample user-specified configuration file is provided in ``config/sampleConfig.sample``. TwircBot will automatically load the default configuration *first*, so you only need to specify the options you want to change.
####User options
There are five options a user might want to configure:
- **nick**: A user name to use to connect. TwircBot will connect anonymously if this is not specified.
- **oauth**: A 30-character alphanumeric token that is associated with your username. Generate one [here](http://twitchapps.com/tmi/).
- **channels**: A list of channels to connect to.
- **log**: The name of the log file you want TwircBot to write to.
- **time_format**: TwircBot time stamps every line of chat it records. The format for the time stamp is specified as in the ``strftime()`` method in Python's ``datetime`` module. You can read about the formatting [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior). Note that if your formatting string has space in it you'll have to enclose the whole thing in *single* quotes.

####Dev options
There are three options users will not need to touch:
- **host**: The host URL that TwircBot will connect to
- **port**: The port that TwircBot will connect to
- **block_size**: A buffer size for receiving data from the IRC socket

##What about Python versions?
TwircBot is currently being developed under Python 3.5.1. It is explicitly *incompatible* with Python 2.x, and probably always will be.