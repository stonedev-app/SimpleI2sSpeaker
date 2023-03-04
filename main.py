import wave
from machine import I2S, Pin

# wav file path
WAV_FILE_PATH = 'sound/test.wav'

# I2S ID
I2S_ID = 0
# read frame number
READ_FRAME_NUM = 1024
# I2S buffer size(bytes)
I2S_BUFFER_SIZE = 20000

# I2S pin number
SCK_PIN = 13
WS_PIN  = SCK_PIN + 1 # SCK_PIN number + 1
SD_PIN  = 15

# read wave file
with wave.open(WAV_FILE_PATH, 'rb') as wave_file:
    
    # get wave file info
    # get channels
    channels = wave_file.getnchannels()
    print('channels:', channels)
    # get framerate
    framerate = wave_file.getframerate()
    print('framerate:', framerate)
    # get sample size(bits). getsampwidth() return bytes, and 1bytes is 8bits. 
    sample_size = wave_file.getsampwidth() * 8
    print('sample_size(bits):', sample_size)
    # get frame number
    frame_num = wave_file.getnframes()
    print('frame_num:', frame_num)
    
    # set mono or stereo
    if channels == 1:
        # channels == 1 is mono
        mode = I2S.MONO
    else:
        # channels == 2 is stereo
        mode = I2S.STEREO
    
    # create I2S instance
    i2s = I2S(I2S_ID, sck=Pin(SCK_PIN), ws=Pin(WS_PIN), sd=Pin(SD_PIN),
              mode=I2S.TX, bits=sample_size, format=mode, rate=framerate, ibuf=I2S_BUFFER_SIZE)
    
    # read audio data
    audio_data = wave_file.readframes(READ_FRAME_NUM)
    # repeat till audio data exist
    while audio_data:
        # write audio data to I2S
        i2s.write(audio_data)
        # read audio data
        audio_data = wave_file.readframes(READ_FRAME_NUM)

    # stop I2S
    i2s.deinit()
    
