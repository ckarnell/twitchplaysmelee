# twitchplaysmelee
This repo was created for the 2019 TrialSpark winter hackathon.

# How to run

Requirements:
The Dolphin emulator.
Python

Steps:
1. Find your Dolphin emulator user folder (for me it was `~/Library/Application Support/Dolphin`)
2. From there, `cd` into `Config`, and either add or change the contents of `GCPadNew.ini` to the following:
```
[GCPad1]
Device = Pipe/0/pipe1
Buttons/A = `Button A`
Buttons/B = `Button B`
Buttons/X = `Button X`
Buttons/Y = `Button Y`
Buttons/Z = `Button Z`
Buttons/Start = `Button START`
D-Pad/Up = `Button D_UP`
D-Pad/Down = `Button D_DOWN`
D-Pad/Left = `Button D_LEFT`
D-Pad/Right = `Button D_RIGHT`
Triggers/L = `Button L`
Triggers/R = `Button R`
Main Stick/Up = `Axis MAIN Y -`
Main Stick/Down =  `Axis MAIN Y +`
Main Stick/Left = `Axis MAIN X -`
Main Stick/Right = `Axis MAIN X +`
C-Stick/Up = `Axis C Y -`
C-Stick/Down =  `Axis C Y +`
C-Stick/Left = `Axis C X -`
C-Stick/Right = `Axis C X +`
```
3. `cd` into it and `mkdir Pipes`.
4. `cd` into `Pipes` and `mkfifo pipe1`.
5. Clone the project.
6. `pip install -r requirements.txt`
7. From the cloned directory, run `python pytry2.py`.

Now the chatbot is hooked up to the twitch.tv/trialsparkplays channel!
