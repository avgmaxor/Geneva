# Builds Geneva for the OS you run this on and zips it into dist/
# Setup:  pip install -r requirements.txt pyinstaller pillow
# Build:  python build.py
import os, sys, shutil, subprocess, platform
import PyInstaller.__main__

root = os.path.dirname(os.path.abspath(__file__))
dist = os.path.join(root, 'dist')
osname = {'win32': 'windows', 'darwin': 'mac'}.get(sys.platform, 'linux')
zipname = 'Geneva-' + osname + '-' + platform.machine().lower()

PyInstaller.__main__.run([
    os.path.join(root, 'Geneva.py'),
    '--name', 'Geneva',
    '--onedir',
    '--windowed',
    '--noconfirm',
    '--clean',
    '--add-data', os.path.join(root, 'assets') + os.pathsep + 'assets',
    '--icon', os.path.join(root, 'assets', 'logo.png'),
    '--distpath', dist,
    '--workpath', os.path.join(root, 'build'),
    '--specpath', os.path.join(root, 'build'),
])

zippath = os.path.join(dist, zipname + '.zip')
if os.path.exists(zippath):
    os.remove(zippath)

if osname == 'mac':
    # Ship just Geneva.app, ditto keeps the symlinks inside the app intact
    shutil.rmtree(os.path.join(dist, 'Geneva'), ignore_errors=True)
    subprocess.run(['ditto', '-c', '-k', '--keepParent', os.path.join(dist, 'Geneva.app'), zippath], check=True)
else:
    shutil.make_archive(os.path.join(dist, zipname), 'zip', dist, 'Geneva')

print('\nBuilt ' + zippath)
