import time,random
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_volume(left_volume, right_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    current_volume_left, current_volume_right, _ = volume.GetVolumeRange()

    # Set volume levels
    volume.SetChannelVolumeLevelScalar(0, left_volume, None)  # Left channel
    volume.SetChannelVolumeLevelScalar(1, right_volume, None)  # Right channel

def increase_volume(min_volume,max_volume):
    for i in range(min_volume, max_volume):
        volume = i / 100
        try:
            set_volume(volume, volume)
            time.sleep(0.1)  # Adjust sleep time as needed
        except Exception as e:
            print(f"Error setting volume: {e}")
    return volume        

def oscillate_volume():
    global volume
    count = 1 / 100
    volume_left = volume
    volume_right = volume

    for i in range (2000):
        if volume_left <= 0.3 or volume_right <= 0.35:
            count = -count
        
        volume_right += count
        volume_left -= count
        if volume_left >=1: 
            volume_left=1
        if volume_right >=1:
            volume_right=1
        try:
            set_volume(volume_left, volume_right)
            time.sleep(0.1)  # Adjust sleep time as needed
        except Exception as e:
            None
def random_volume_change():
    global left_volume,right_volume
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume_left, current_volume_right, _ = volume.GetVolumeRange()

        for _ in range(15):  # Change volume randomly 10 times
            left_volume = (random.randint(30, 90))/100
            right_volume = (random.randint(30, 90))/100
            while True:
                try:
                    set_volume(left_volume, right_volume)# Random volume level between 10% and 100%
                    break
                except:
                    None
            time.sleep(0.3)       
    except Exception as e:
        None
def compair_argument():
    global left_volume,right_volume,volume
    if left_volume >= right_volume:
        for i in range (int((right_volume)*100), int((left_volume)*100+1)):
            while True:
                try:
                    set_volume(left_volume, i/100)
                    time.sleep(0.1)
                    break
                except:
                    None
    else:
        for i in range ( int((left_volume)*100),int((right_volume)*100 +1)):
            while True:
                try:
                    set_volume(i/100, left_volume)
                    time.sleep(0.1)
                    break
                except:
                    None
    volume=i/100
while True:
    for count in range (2):
        try:
            if count ==0:
                volume=increase_volume(10,51)
                random_volume_change()
                compair_argument()
                oscillate_volume()
                compair_argument()
                volume=(increase_volume(int(volume*100),101))
                time.sleep(50)
                oscillate_volume()
            if count ==1:
                compair_argument()
                volume=(increase_volume(int(volume*100),101))
                time.sleep(100)
                oscillate_volume()
        except KeyboardInterrupt:
            print("\nExiting program.")
        except Exception as e:
            print(f"Unexpected error: {e}")
