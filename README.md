# Year Progress Calculator
A simple package providing two classes to calculate the percentage
of time passed from the beginning of a year.

## Basic Usage
The ProgressYear class forms the basis for all calculations. Call
the public methods directly from the class (no instantiation needed) 
to return a float representing a percentage of time passed for the current year, 
in days, hours, or minutes resolution. You may also pass a datetime 
object to these methods to return a progress percentage for that 
specific date within its respective year.

```python
from progyear import ProgressYear

# Get percentage of time passed until today
ProgressYear.get_day_resolution()

ProgressYear.get_hour_resolution()

ProgressYear.get_minute_resolution()


# Get percentage of time passed till 9:41pm Oct 17th, 2021
import datetime
custom_date = datetime.datetime(2021, 10, 17, 21, 41)

ProgressYear.get_day_resolution(custom_date)
# returns 0.7917808219178082  -> 79.178 %

ProgressYear.get_hour_resolution(custom_date)
# returns 0.7941780821917808  -> 79.417 %

ProgressYear.get_minute_resolution(custom_date)
# returns 0.7942560882800608  -> 79.425 %
```

The percentage returned is only calculated on time *passed*. In the example above, the 
`get_day_resolution` method does not count the 17th itself, since *it's not 
yet over.* 

## Experimental usage
The ProgressYearServer class is an experimental class meant for long-running,
request-heavy applications. It saves the values in memory instead of 
calculating on each call anew. It must be instantiated, and will run its 
update method in the background on a separate thread. The user can 
then call its public methods at any time to retrieve the values. This 
class does not accept any custom datetime objects and will always 
return today's values.

```python
from progyear import ProgressYearServer

# Instantiate class - by default updates every 60 seconds / 1 min
progress = ProgressYearServer() 

# Or, pass a custom update time on creation, in seconds
progress = ProgressYearServer(3600)     # Updates once every hour

# Get percentage of time passed
progress.get_day_resolution()
progress.get_hour_resolution()
progress.get_minute_resolution()
```

This class does not handle complex scenarios, catch errors, or have been tested in 
strenuous environments. As such it must be considered incomplete and be used with caution.


## Limitations
These classes depend on the datetime module, which in turn depends on the host 
computer's internal clock. If the host computer's time is inaccurate the default method 
return values will also be inaccurate. The exception to this is when using a custom datetime object 
with the ProgressYear class methods. Using a custom datetime object will always return
an accurate calculation.
