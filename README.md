# Reduce Size of Pictures for Publishing Them to Web 

## Description
The tool can be used to reduce image size for publishing images to Web. It's useful to create galleries of pictures when there are square pictures of smaller sizes.

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
Success = 0
Source folder not exist = 1
No picture files found = 2
Desired size out of bound = 3
Source folder empty = 4
Ready folder empty = 5
Unexpected = 255
```

2. Graphical interface

Run it without any parameters

## Installation
It requests to set up PIL library. If the library is installed in Windows, make sure to run command line prompt as administrator.
```bash
pip install pillow
```

## Contributing
Please read [CONTRIBUTING.md](https://github.com/larandvit/picture-trimmer/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
 
## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/larandvit/picture-trimmer/blob/master/LICENSE) file for details

## Acknowledgments
* Core transformation logic is taken from https://jdhao.github.io/2017/11/06/resize-image-to-square-with-padding/.
