import pyaudio
import wave
import os
import numpy as np
from pvrecorder import PvRecorder
from config.config import Config
import struct
from equalizer import Equalizer
import asyncio


class PvRecorderAudio(PvRecorder):
    def __init__(self, *args, **kwargs):
        self.input_device_dict = Config.read_config().io_devices.input_device
        if self.input_device_dict.index == 0:
            self.input_device_index = -1
        else:
            available_input_devices = self.get_available_devices()
            for i, name in enumerate(available_input_devices):
                if name.startswith(self.input_device_dict.name):
                    self.input_device_index = i
                    break
            else:
                self.input_device_index = -1
        if self.input_device_index == -1:
            super().__init__(frame_length=512, device_index=-1, *args, **kwargs)
        else:
            super().__init__(frame_length=512, device_index=self.input_device_index, *args, **kwargs)

class Audio:
    @staticmethod
    def play_mono_audio(file_path, output_device_index, chunk_size=2048, equalizer : Equalizer=None):
        try:
            dataint = None
            wf = wave.open(file_path, 'rb')

            p = pyaudio.PyAudio()

            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True,
                            output_device_index=output_device_index
                            )                            

            frame_size = wf.getsampwidth() * wf.getnchannels()
            if frame_size > 3:
                chunk_size = 4096
            else:
                chunk_size = 1024
            chunk_size_frame = int(chunk_size*2 // frame_size)
            
            data = wf.readframes(chunk_size_frame)

            while data:
                stream.write(data)
                data = wf.readframes(chunk_size_frame)
                if equalizer:
                    equalizer.equalizer_data_to_vizualize = data
                    equalizer.now_audio_play = True
                    # equalizer.chunk_size = chunk_size_frame
                    # equalizer.audio_file = file_path

            if equalizer:
                equalizer.now_audio_play = False
                equalizer.equalizer_data_to_vizualize = None
                
            stream.stop_stream()
            stream.close()

            

            p.terminate()
        # except PermissionError:
        #     pass
        except Exception as e:
            print(e)

    @staticmethod
    def record_audio_and_save(save_path, n_times=50, input_device_index=0, sample_rate=44100, start=0):
        fs = sample_rate
        second = 2
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=fs,
                        input=True,
                        input_device_index=input_device_index,)
        
        for i in range(n_times):
            print(f'Recording {start + i + 1}.wav...')
            data = stream.read(second * fs)
            with wave.open(os.path.join(save_path, f'{start + i + 1}.wav'), 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(fs)
                wf.writeframes(data)
            input('Press Enter to record again...')

        stream.close()
        p.terminate()

    @staticmethod
    def listen_for_frame(sample_rate=44100, input_device_index=None, chunk_size=512):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        input_device_index=input_device_index,
                        frames_per_buffer=chunk_size)
        
        frame = stream.read(chunk_size)

        audio_frame = np.frombuffer(frame, dtype=np.int16)

        stream.stop_stream()
        stream.close()
        p.terminate()

        return audio_frame

    @staticmethod
    def listen_for(sample_rate=44100, input_device_index=0, seconds=2, chunk_size=1024, filename="input.wav"):
        try:    
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=sample_rate,
                            input=True,
                            input_device_index=input_device_index,)

            frames = []

            for _ in range(int(sample_rate / chunk_size * seconds)):
                data = stream.read(chunk_size)
                frames.append(np.frombuffer(data, dtype=np.int16))

            stream.stop_stream()
            stream.close()
            p.terminate()
            audio = np.concatenate(frames, axis=0)
            # import librosa
            with wave.open(os.path.join(".", filename), 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio)
            return filename
        except KeyboardInterrupt:
            exit(0)
        except:
            return None

                