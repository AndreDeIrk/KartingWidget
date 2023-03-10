import sys
import time
import datetime
import numpy as np
import NDIlib as ndi
import cv2
import json
from pynput import keyboard
import threading
import oval as o
import from_angle as fa


angle = 0
# dx, dy = o.track_fun(angle)
dx, dy = fa.from_angle(angle)
meta_data_karting = f"1;250;450;ivanov;20 km/h;1;10;{angle};{dx};{dy}\\0;350;450;ivanov;20 km/h;3;10;{angle};{dx};{dy}\\0;150;450;ivanov;20 km/h;5;10;{angle};{dx};{dy}\\0;250;350;ivanov;20 km/h;6;10;{angle};{dx};{dy}\\0;100;200;ivanov;20 km/h;7;10;{angle};{dx};{dy}\\0;300;200;ivanov;20 km/h;10;10;{angle};{dx};{dy}\\0;500;200;ivanov;20 km/h;11;10;{angle};{dx};{dy}\\0;700;200;ivanov;20 km/h;9;10;{angle};{dx};{dy}"

class vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x 
        self.y = y
        self.z = z



RES = vector(1920, 1080)
MAP_RES = vector(400, 400)
# MAP_DIRECTION = vector(1., 1.)
MAP_SPEED = vector(1., 1.)

def inc(a: str, d: float):
    return str(float(a) + d)

def next_map_position(x: str, y: str, dx=1., dy=1.):
    global MAP_SPEED
    if (0 < float(x) + dx < RES.x - MAP_RES.x):
        pass
    else:
        MAP_SPEED.x = -MAP_SPEED.x
        dx = MAP_SPEED.x

    if (0 < float(y) + dy < RES.y - MAP_RES.y):
        pass
    else:
        MAP_SPEED.y = -MAP_SPEED.y
        dy = MAP_SPEED.y
    
    return inc(x, dx), inc(y, dy)

telemetry = dict(
    Team='USSR',
    Speed='100mph',
    Widget=dict(
        Map=dict(
            Visible='On',
            X='0.0',
            Y='0.0',
        ),
        DetailLong=dict(
            Visible='On',
        ),
    ),    
    Length="1.0",
    Data='0'*(2**10),
)
# WORKING = True    
# stop_event = threading.Event()
controller = keyboard.Controller()

class StopException(Exception): pass

def on_press(key):
    global telemetry
    try: 
        if key == keyboard.Key.home:
            raise StopException(key)
        elif key.char == 'm':
            telemetry["Widget"]["Map"]["Visible"] = 'On' if telemetry["Widget"]["Map"]["Visible"] == 'Off' else 'Off'
            print(f'Map switched to {telemetry["Widget"]["Map"]["Visible"].upper()}')
            # Collect events until released
        elif key.char == 'l':
            telemetry["Widget"]["DetailLong"]["Visible"] = 'On' if telemetry["Widget"]["DetailLong"]["Visible"] == 'Off' else 'Off'
            print(f'DetailLong switched to {telemetry["Widget"]["DetailLong"]["Visible"].upper()}')
            # Collect events until released
        elif key.char == "p":
            telemetry["Data"] = "0"*(2**16)
            print('Decrease data')
    except AttributeError:
        pass


def kb_catch():
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except StopException as e:
            print(f'{e.args[0]} was pressed')
        except Exception as e:
            print(f'Keyboard exception: {e}')

listener = threading.Thread(target=kb_catch)

def main():

    angle = 0
    plate_x = 10
    plate_y = 450
    dx, dy = o.track_fun(angle)
    meta_data_karting = f"1;250;450;ivanov;20 km/h;1;10;{angle};{dx};{dy}\\0;350;450;ivanov;20 km/h;3;10;{angle};{dx};{dy}\\0;150;450;ivanov;20 km/h;5;10;{angle};{dx};{dy}\\0;250;350;ivanov;20 km/h;6;10;{angle};{dx};{dy}\\0;100;200;ivanov;20 km/h;7;10;{angle};{dx};{dy}\\0;300;200;ivanov;20 km/h;10;10;{angle};{dx};{dy}\\0;500;200;ivanov;20 km/h;11;10;{angle};{dx};{dy}\\0;700;200;ivanov;20 km/h;9;10;{angle};{dx};{dy}"


    if not ndi.initialize():
        return 0

    ndi_send = ndi.send_create()

    if ndi_send is None:
        return 0

    # img = np.zeros((1080, 1920, 4), dtype=np.uint8)

    video_frame = ndi.VideoFrameV2()

    video_frame.frame_rate_N = 50
    video_frame.frame_rate_D = 1

    video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX

    # print(f'Frame format: {video_frame.data.shape}')

    listener.start()

    while True:
        try:
            vidcap = cv2.VideoCapture('planes.mp4')
            success, image = vidcap.read()
            count = 0
            print(f'{count=}')
            telemetry["Widget"]["Map"]["X"] = '0.0'
            telemetry["Widget"]["Map"]["Y"] = '0.0'
            telemetry["Data"] = "0"*(2**16)
            
            while success:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
                video_frame.data = image
                # telemetry["Widget"]["Map"]["X"] = inc(telemetry["Widget"]["Map"]["X"], 1.0)
                # telemetry["Widget"]["Map"]["Y"] = inc(telemetry["Widget"]["Map"]["Y"], 1.0)
                telemetry["Widget"]["Map"]["X"], telemetry["Widget"]["Map"]["Y"] = next_map_position(x=telemetry["Widget"]["Map"]["X"], 
                                                                                                     y=telemetry["Widget"]["Map"]["Y"],
                                                                                                     dx=MAP_SPEED.x,
                                                                                                     dy=MAP_SPEED.y)

                angle = (angle+1) % 360
                plate_x = (plate_x + 1) % 1920
                plate_y = 450 + 100 * np.cos(plate_x / 10)
                dx, dy = fa.from_angle(angle)
                dx1, dy1 = fa.from_angle((angle+120) % 360)
                dx2, dy2 = fa.from_angle((angle+240) % 360)
                meta_data_karting = f"1;{plate_x};{plate_y};ivanov;20 km/h;1;10;{angle};{dx};{-dy}\\1;350;450;ivanov;20 km/h;3;10;{angle};{dx1};{-dy1}\\1;150;450;ivanov;20 km/h;5;10;{angle};{dx2};{-dy2}\\0;250;350;ivanov;20 km/h;6;10;{angle};{dx};{dy}\\0;100;200;ivanov;20 km/h;7;10;{angle};{dx};{dy}\\0;300;200;ivanov;20 km/h;10;10;{angle};{dx};{dy}\\0;500;200;ivanov;20 km/h;11;10;{angle};{dx};{dy}\\0;700;200;ivanov;20 km/h;9;10;{angle};{dx};{dy}"


                # if count % 30 == 0:
                #     telemetry["Data"] += "0"*(2**16)
                telemetry["Length"] = len(json.dumps(telemetry))
                # video_frame.metadata = f'<json>{json.dumps(telemetry)}</json>'#json.dumps(telemetry[count])
                video_frame.metadata = f'<json>{meta_data_karting}</json>'#json.dumps(telemetry[count])

                ndi.send_send_video_v2(ndi_send, video_frame)
                print(datetime.datetime.now())

                success, image = vidcap.read()
                count += 1

            print(f'{count=}')    
            print('Starting video again...')
        except KeyboardInterrupt:
            print('Keyboard interruption...')
            # stop_event.set()
            controller.press(keyboard.Key.home)
            break

    listener.join()
    ndi.send_destroy(ndi_send)

    ndi.destroy()
    print('FINISHED')
    return 0

if __name__ == "__main__":
    sys.exit(main())
