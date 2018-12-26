# Reduce Size of Pictures for Publishing Them to Web 

## Description
The tool can be used to reduce size of pictures for publishing them to Web. One of the usages can be to create galleries of pictures when there are square pictures of smaller size.

## Features
1. Set up a desired size of output images

2. Process images different types
* jpg
* bmp
* png
* gif

3. Support 2 user interfaces
* Command line user interface (CLI)
* Graphical user interface (GUI)

## Usage
1. Command line interface

Wnen run it, provide with the mandatory parameters

```
usage: image_transfrom.py [-h] --sourcefolder "source folder" --desiredsize "desired size"

Reduce size of pictures for publishing them to web

optional arguments:
  -h, --help            show this help message and exit
  --sourcefolder        "source folder" Input folder with pictures
  --desiredsize         "desired size" Output image size

Exit codes: 
0 - Success
1 - Source folder not exist
2 - No picture files found
3 - Desired size out of bound
4 - Source folder empty
5 - Ready folder empty
255 - Unexpected
```

2. Graphical interface

Run it without any parameters

## Installation
It requests to set up PIL library. 

### Windows
Run command line prompt as administrator.
```bash
pip install pillow
```
### Unix
```bash
sudo pip install pillow
```

## Optional Installation
If you have decided to bundle it in executable application. You need to install [PyInstall](http://www.pyinstaller.org/).

### Windows
Run command line prompt as administrator.
```bash
pip install pyinstaller
```
### Unix
```bash
sudo pip install pyinstaller
```

## Build Executable Bundle
Run a batch file below depending on your operation system. If it has been completed successfully, you can find an executable file in **dist** folder.

### Windows
```bat
build_app_windows.bat
```
A ready bundle can be found in [Releases](https://github.com/larandvit/picture-trimmer/releases) folder. It's tested in Windows 10/7 editions.

### Unix
```bash
./build_app_unix.sh
```

A ready bundle can be found in [Releases](https://github.com/larandvit/picture-trimmer/releases) folder. It's tested in CentOS 7.

## Contributing
Please read [CONTRIBUTING.md](https://github.com/larandvit/picture-trimmer/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
 
## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/larandvit/picture-trimmer/blob/master/LICENSE) file for details

## Acknowledgments
* Core transformation logic is taken from https://jdhao.github.io/2017/11/06/resize-image-to-square-with-padding/.
* Executable bundle software developed by [PyInstall](http://www.pyinstaller.org/).
