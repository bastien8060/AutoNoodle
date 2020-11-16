# AutoNoodle
It registers attendance automatically everyday during each classes for some compatible Moodle (© 2020) Platforms

  - Your Timetable is synced with the **Google Calendar API**.
  - Can be left running for days even months. **Works 24/7**.
  - Can tell the attendance whether you are at **home** or at **school**
  - Made 100% in Python and works in **Linux / MacOS / Windows**.
 
### Installation

AutoNoodle requires some [Modules](#modules-and-pip) to run.

To run AutoNoodle, go ahead and clone the repo, and execute `main.py`

```sh
$ git clone https://github.com/bastien8060/AutoNoodle autonoodle
$ cd autonoodle
$ python3 ./main.py
```
This commands slightly varies on Windows.

Otherwise, you may download the code as a zip archive, here [(download)](https://github.com/bastien8060/AutoNoodle/archive/main.zip)

#### Screen

For Linux/MacOs, it is recommended to run it inside a Screen/Tmux Session, in order to leave the script running even when your terminal or ssh connection gets closed, for durability & stability. To start a screen in the background, here is an example. 
```sh
$ screen -U python3 ./main.py #Launches it in the background
$ screen -r #Brings it back to the forground to monitor it, (aka. It re-attaches the screen).
```
Press `ctrl+a+d`, in order to bring a screen session back to the background, from the foreground, (aka. To detach the screen).


### First Run

AutoNoodle is based on Google Calendar Api, therefor, you will need to connect to the API. The terminal should attempt to open an url, in order to let you login with your prefered account.

If no url, is opened, a url should display at least. If still not, you may open a ticket/issue on the repository.

Your Google Account Password is never accessed by the script or stored anywhere. The Python script only gets a token, from Google, that only enables the script into viewing Calendars Events. That special token is stored in the file `.token`. You may "Log-Out" by deleting that file.

### Arguments
If you wish, and if you are running it with the Terminal or your IDE supports it, you can supply an argument, overriding, the default location. (home/school)
  - **"-l": school/home.** It specifies the script where you are, so it can notify the attendance.
  - **E.g:** `python3 ./main.py -l school`


Else, if you wish to add the argument manually, go ahead and edit the onsite variable, at the beginning of the file.

In order for the script to know your timetable, it must find it in your Calendar. Enter your timetable there. Like this: [Screenshot](https://ibb.co/B3FMTzb). Lunchtime should be named `Lunch`, without any extra space and without forgetting the capital letter.

### Modules and Pip

AutoNoodle Uses Many Modules to run. Here is a list.

| Plugin | README |
| ------ | ------ |
| Pickle | [PyPi: Pickle5](https://pypi.org/project/pickle5/) |
| Google API | [Read More](https://developers.google.com/calendar/quickstart/python) |
| TQDM | [PyPi: Tqdm](https://pypi.org/project/tqdm/) |
| Beautiful Soup 4 | [PyPi: Bs4](https://pypi.org/project/bs4/) |
| LXML | [PyPi: Lxml](https://pypi.org/project/lxml/) |
| Requests | [PyPi: Requests](https://pypi.org/project/requests/) |


To install them:
```sh
$ pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib tqdm lxml bs4 requests
```

### Todos
 - Write Support for .CSV timetable
 - Write Support for Other Apis such as (© 2020) Microsoft's Outlook Calendar

### More about (© 2020) Google Calendar API
See [Read More](https://developers.google.com/calendar/)

License
----

MIT License

Copyright (c) 2020 Bastien Saidi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
