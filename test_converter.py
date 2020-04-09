from converter import Converter
conv = Converter()

info = conv.probe('out_srf_4_VC.avi')

convert = conv.convert('out_srf_4_VC.avi', 'out_srf_4_VC.mp4', {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 720,
        'height': 400,
        'fps': 25
    }})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')
