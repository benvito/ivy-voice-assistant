import pyaudio
import wave
import os
import numpy as np
from pvrecorder import PvRecorder
from config.config import Config


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
        super().__init__(frame_length=512, device_index=self.input_device_index, *args, **kwargs)
        
class Audio:
    @staticmethod
    def play_mono_audio(file_path, output_device_index):
        try:
            wf = wave.open(file_path, 'rb')

            p = pyaudio.PyAudio()

            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True,
                            output_device_index=output_device_index)

            data = wf.readframes(1024)

            while data:
                stream.write(data)
                data = wf.readframes(1024)

            stream.stop_stream()
            stream.close()

            p.terminate()
        except PermissionError:
            pass

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

                