# Binge-Watch
Light-weight playlist manager. Requires VLC media player. To use this program VLC must be in PATH variable in windows.

## Usage
Install required libraries.
```
pip install -r requirements.txt
```
Then run the main file.
```
python Ui.py
```
After the main windows pops up. Add your movie/series directories one at a time. The episodes must be contained inside the selected directory.
Select any one of the series listed in the screen after some movie/series have been added. Then click "Resume Watching" to start watching. The program
remembers which episode you left off, and with correct playback resume settings in VLC the binge-watching experience is great. Click "Prev" or "Next" to watch
previous or next episodes. 