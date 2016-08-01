#TwircBot Documentation  

##Writing your own config file
The syntax for specifying your own configuration options is very simple:
- Write options in a ``key: value`` format. Example: ``nick: coolGuy42``. The semi-colon may be omitted: ``nick coolGuy42`` is fine too.
- Multiple ``value``'s are seperated with spaces: ``key: value1 value2``. This is only necessary when you wish to connect to multiple ``channels``.
- If you want to specify a ``value`` that has a space, you can surround it with *single* quotes. Example: ``time_format: '[%Y-%m-%d %H:%M:%S]'``

##User options  
There are four options a user might want to configure:  
- **nick**: A Twitch user name to use to connect. If you specify this you *must* also specify an **oauth** token or you will fail to connect. TwircBot will connect anonymously if this is not specified.  
- **oauth**: A 30-character alphanumeric token that is associated with your username. Generate one [here](http://twitchapps.com/tmi/).  
- **channels**: A list of channels to connect to.  
- **log**: The name of the log file you want TwircBot to write to.  


##Dev/admin options  
There some options users will probably not need to touch:  
- **time_format**: TwircBot time stamps every line of chat it records. The format for the time stamp is specified as in the ``strftime()`` method in Python's ``datetime`` module. You can read about the formatting [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior). Note that if your formatting string has space in it you'll have to enclose the whole thing in *single* quotes.  
- **host**: The host URL that TwircBot will connect to 
- **port**: The port that TwircBot will connect to  
- **block_size**: A buffer size for receiving data from the IRC socket  
- **reconnect_timer**: This is the time, in seconds, that TwircBot will wait without getting any data before trying to reconnect. Twitch's servers issue a PING request roughly every five minutes. If you haven't gotten any data for more than five minutes, there is probably something wrong with the connection. This value must be an **int**.  
- **stayalive_timer**: This is the time, in seconds, that TwircBot will operate before disconnecting and terminating itself. Setting this value to ``0`` means it will continue indefinitely. This value must be an **int**.  
- **connect_timeout**: This is the time, in seconds, that TwircBot will spend trying to connect to Twitch's servers. If a connection is not established in this amount of time, TwircBot will raise an exception. This value must be an **int** or a **float**.  
- **receive_timeout**: This is the time, in seconds, that TwircBot will wait to receive chat data from Twitch's servers. When this times out, TwircBot performs some internal checks and then loops around to wait for data again. If this value is set too low (like ``0`` or ``0.00001``), TwircBot will spend all of its time checking and looping, and will consume large amounts of system resources. If this value is set too high (like ``3600``, an hour) TwircBot spends all of its time waiting for data, and ignoring--among other things--the **stayalive_timer** and **reconnect_timer**. This is not a problem as long as TwircBot actually *is* receiving data every few seconds or so, but setting **receive_timeout** too high could cause TwircBot to behave poorly in the case of a severed connection. This value must be an **int** or a **float**.  

