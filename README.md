# Autoreach
Autoreach is designed to simplify student life at Choate by notifying and auto-marking
students as "In House". This removes the mental burden of having to remember
to REACH at 8:00 PM. For students who are not at Choate but are under the yoke
of REACH, they may also try to use this to ease their life.

# Disclaimer
```
Mr. Rogers has noted that it should not be against school rules so long as the
student is auto-marked in the location that they are actually occupying.

I hold no responsibility for the execution of this code or for the potential
disciplinary responses the school may choose to carry out (although if you are
*actually* in house, it should be fine). My interpretation of the school rules
and the JC's interpretation of the school rules may differ.
```

# Setup
Install the following deps:
```
selenium
chrome/chromium (you may need to update chromedriver_77
```
For each user using autoreach, create a file matching `cred_[NAME].json` using
the fields provided in `cred_template.json`.

Use cron or a tool of your choosing to run the script at your desired time.

# Contribution Policy
This software is released into the public domain and all contributions are
welcome. Just make a pull request or issue to get my attention.
