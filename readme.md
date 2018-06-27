# Description
Live video streaming over WebSockets (Currently only Raspberry Pi Camera is supported)

## Getting Started
```bash
$ git clone https://github.com/ShellAddicted/wsCamera.git
$ cd wsCamera
$ pip3 install -r requirements.txt
$ python3 src/main.py
```
then
open in your Web Broweser:
http://<RASPBERRY_PI_IP>:8000/ws

### Default Settings
- Default HTTP port -> 8000
- Frame resolution -> 640x480px @ 30 FPS


to edit this settings you can edit [src/main.py](https://github.com/ShellAddicted/wsCamera/blob/master/src/main.py)