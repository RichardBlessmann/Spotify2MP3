# Spotify2MP3Python
several scripts and a guide on how to turn your spotify playlists into MP3 Files 

For convenience's sake i have seperated the scripts into several scripts and steps.

## Needed
Python 
Pip


### Step 1: Turn your Spotify Playlists into CSV Files.
To do the first step and get all your spotify Playlists we can use an external tool. Since it's really hard to get Spotify to spit out anything. Someone did that already on [Exportify.
](https://exportify.net/). There you can link your current Spotify Account to Exportify and Export all your Playlists into your preferred folder.

Keep in mind that the following scripts will work on ALL the Playlists in the folder.

### Step 2: CSV Files into a understandable format.
Actually it's not that important to do this step. I just added it beacause i think the data Exportify gives you is overflowing and not that clear to comprehend. So i jst reduced the CSV File into 3 different Categories per Song. `Song Title`, `Interpret` and `Album Title`.

To do that you can run the first script provided in the repo. To be able to execute the repo you need several libraries installed. If you are using [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows) as IDE these can be installed in the IDE after executing the script. If not you need to manually install the needed packages using:
```
py -m pip install pandas
py -m pip install youtube-search-python
```

Afterwards you should be good to go. 
Select the folder in which all your csv files are.
The script will make seperate Files which you then can put into a different folder for the next script to properly function. If you don't put the files into a different folder, the following script will operate on all csv files, not just the augmented ones.


### Step 3: Add the coresponding Youtube link

To execute the `second script` you need to have first the following packages installed. 
`py -m pip install youtube-search-python`
If you use the VM of PyCharm you can find the package in the bottom left of your IDE in the Package Manager Tab.

This will automatically search for the most likely youtube video, that fits your songtitle and appends the youtube link into the csv file.

### Step 4: Download the MP3 Files

To execute this file you will need the following package installed:
`py -m pip install yt-dlp`
This will download all songs. Try letting it run overnight if you have long Playlists ;)
