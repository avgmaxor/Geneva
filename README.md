# Geneva
## DOWNLOAD [Here](https://maxorr.itch.io/geneva)

### DISCLAIMERS
- Code is wonky, a lot of it was rushed so I could play with friends quicker
- Ignore the amount of commits a lot of them were little changes made in a minute for quick fixx
- Multiplayer is obviously not the most optimized method but It was quick and easy to set up 
- Code is free to use but credit is appreciated * NOT REQUIRED *

### RUN FROM SOURCE
- Install Python 3
- `pip install -r requirements.txt`
- `python Geneva.py`

### BUILDING FOR FRIENDS
- `pip install -r requirements.txt pyinstaller pillow`
- `python build.py`
- Send them the zip in `dist/` (e.g. `Geneva-windows-amd64.zip`). They unzip it and run Geneva
- A build only works on the OS it was made on, so Windows friends need a Windows build
- Easiest way to get all of them: push to GitHub. The Build action makes Windows, Mac and Linux zips (Actions tab, Artifacts). Push a tag like `v0.17` to also put them on a Release page
- The game isn't code signed, so on first launch: Windows - "More info" then "Run anyway". Mac - right click Geneva, Open, then Open again

### MULTIPLAYER
- One player picks Client 1 (host). The lobby shows their IP
- The other player picks Client 2 and types in that IP
- Uses TCP port 5555. Over the internet the host needs to port forward 5555 (or use something like Tailscale/Hamachi)
- First to round 50 wins

### Credits
- [avgjew](https://maxor.xyz) - lead dev

- william - dev2

- jusuf - playtester/bugfinder

- groses - art

# Contact
- avg#3851
- avgjewmail@gmail.com