# Console Timetable
## Introduction
The Console Timetable is a timetable manager, designed for those who prefer to work within the console. It was designed by a university student, who had an irregular timetable. He figured that it would be worth designing a program into which he could code all of the intricacies of his schedule, so that he wouldn't go insane keeping track of it himself. He hopes that others will find the software as useful as he did. Note that this script is written for academic timetables, however it could be tweaked for other purposes quite easily. 
## Dependencies
Console Timetable is a Python script, and so requires the user to have a Python installation. **Python 3** is recommended. 
Console Timetable also relies on the following Python packages:

- **numpy** (https://numpy.org/)
- **tabulate** (https://github.com/astanin/python-tabulate)

Both may be installed with pip. 
```
pip install numpy
pip install tabulate
```
## Usage
Console Timetable works mainly on a command-argument based system. The general format is,
```
[command] [arg1] [arg2] . . . [argn]
```
Note that arguments are separated by spaces, and so each argument should be void of spaces.

Below is a list of basic commands. 

- **create** [abrv] ; Creates a new type of session, e.g. a particular class one may have. *abrv* is the abbreviated name you would like to use for the session in commands. The user will be prompted to give information about this session type. 
- **trash** [abrv] ; Destroys the session known as *abrv*.
- **edit** [abrv]; Allows the user to change details about the session type. 
- **set** [abrv] [week] [day] [hour]; Schedules *abrv* to occur at *hour*:00 (24 hour clock) on *day* (Mon, Tue, Wed, Thu, Fri, Sat, Sun), on the *week*th week of the year (1 to 52). 
- **multiset [abrv] [weekmin] [weekmax] [weekinc] [day] [hour]; Schedules *abrv* to occur at *hour*:00 (24 hour clock) on *day* (Mon, Tue, Wed, Thu, Fri, Sat, Sun), on every *weekinc*th week between *weekmin* and *weekmax*. 
- **erase** [week] [day] [hour]; Removes whatever is scheduled at *hour*:00 (24 hour clock) on *day* (Mon Tue, Wed, Thu, Fri, Sat, Sun) on the *week*th week of the year (1 to 52). 
- **save** [filename]; Saves all of the commands entered in this session to *filename*.stt. 
- **reset**; Clears the command history.
- **show** [week] [daymin] [daymax] [timemin] [timemax]; Displays the current timetable in console for the *week*th week (1-52), from *daymin* (Mon to Sun) to *daymax* (Mon to Sun) and from *timemin*:00 to *timemax*:00.
- **export** [week] [daymin] [daymax] [timemin] [timemax] [filename]; Exports the current timetable to *filename*.txt for the *week*th week (1-52), from *daymin* (Mon to Sun) to *daymax* (Mon to Sun) and from *timemin*:00 to *timemax*:00.
- **html** [week] [daymin] [daymax] [timemin] [timemax] [filename]; Exports the current timetable to *filename*.html for the *week*th week (1-52), from *daymin* (Mon to Sun) to *daymax* (Mon to Sun) and from *timemin*:00 to *timemax*:00.
- **superHTML** [weekmin] [weekmax] [daymin] [daymax] [timemin] [timemax] [fileroot]; Exports the current timetable to *filename*_*j*.html in *directory* for every week number j (ranging *weekmin* to *weekmax*, from *daymin* (Mon to Sun) to *daymax* (Mon to Sun) and from *timemin*:00 to *timemax*:00.

Users may also make files to help build their timetables. They may create .stt files with commands separated by line and load them as,
```
read [filename (without extension)]
```
They may also create .scls files with information about their classes, and load these with,
```
load [filename (without extension)]
```

## License

Console Timetable is provided under an MIT License. See the LICENSE file for more information. 
