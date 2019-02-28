# twitchplaysmelee
This repo was created for the 2019 TrialSpark winter hackathon.

# How to run

Requirements:
The Dolphin emulator.
Python

Steps:
1. Find your Dolphin emulator user folder (for me it was `~/Library/Application Support/Dolphin`)
2. `cd` into it and `mkdir Pipes`.
3. `cd` into `Pipes` and `mkfifo pipe1`.
4. Clone the project.
5. `pip install -r requirements.txt`
6. From the cloned directory, run `python pytry2.py`.

Now the chatbot is hooked up to the twitch.tv/trialsparkplays channel!
