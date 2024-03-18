from utils.audio import Audio
import os
from config import DATA_MODELS_PATH, MODELS_PATH
# from config.config import Config
import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
from pprint import pprint
import pvporcupine


class PicoVoiceHotWord:
    __slots__ = ("porcupine", "access_key")
    def __init__(
            self, 
            access_key_path : str = os.path.join(DATA_MODELS_PATH, "hotword", "porcupine", "access_key.txt"),
            key_word_paths : list = [os.path.join(MODELS_PATH, "hotword_detection", "pico_voice", "porcupine_keyword.ppn")],
            model_path : str = os.path.join(MODELS_PATH, "hotword_detection", "pico_voice", "porcupine_model_ru.pv"),
            ) -> None:
        self.access_key = PicoVoiceHotWord.read_access_key(access_key_path)
        
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=key_word_paths,
            model_path=model_path,
            sensitivities=[0.5]
        )

    def hotword_in_audio_frame(self, audio_frame):
        return self.porcupine.process(audio_frame)

    @staticmethod
    def read_access_key(path):
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('-')
        with open(path) as f:
            return f.read().strip()
    
    @staticmethod    
    def write_access_key(path, access_key):
        with open(path, 'w') as f:
            f.write(access_key)

class HotwordModel:
    def __init__(
            self, 
            hotword="эй луна", 
            path=os.path.join(DATA_MODELS_PATH, "hotword", "luna_hotword", "train_data"),
            threshold=0.95,
            sample_rate=44100,
            csv_name="hotword_audio_data.csv",
            n_mfcc=40
            ) -> None:
        self.all_data = []
        self.n_mfcc = n_mfcc
        self.csv_name = csv_name
        self.sample_rate = sample_rate
        self.hotword = hotword
        self.path = path
        self.threshold = threshold
        self.wake_path = os.path.join(self.path, "wake")
        self.not_wake_path = os.path.join(self.path, "not_wake")

        self.model = None

        self.load_model()

    def load_audio_file(self, path):
        audio, sr = librosa.load(path)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=self.n_mfcc)
        mfcc_processed = np.mean(mfccs.T, axis=0)
        return mfcc_processed
    
    def audio_to_mfcc(self, audio, sr):
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=self.n_mfcc)
        mfcc_processed = np.mean(mfccs.T, axis=0)
        return mfcc_processed
    
    def find_last_numbered_file(self, folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

        if not files:
            return 0

        last_number = len(files)

        return last_number

    def record_wake_audio_data(self, n_times=50, input_device_index=None):
        start = self.find_last_numbered_file(self.wake_path)
        Audio.record_audio_and_save(self.wake_path, n_times, input_device_index, self.sample_rate, start)
    
    def record_background_audio_data(self, n_times=50, input_device_index=None):
        start = self.find_last_numbered_file(self.not_wake_path)
        Audio.record_audio_and_save(self.not_wake_path, n_times, input_device_index, self.sample_rate, start)

    def prepare_data(self):
        data_path_dict = {
            0 : [f"not_wake/{wav_path}" for wav_path in os.listdir(self.not_wake_path)],
            1 : [f"wake/{wav_path}" for wav_path in os.listdir(self.wake_path)]
        }

        for class_label, wave_files in data_path_dict.items():
            for wave_file in wave_files:
                mfcc_processed = self.load_audio_file(os.path.join(self.path, wave_file))
                self.all_data.append([mfcc_processed, class_label])

            print(f"processed: {class_label}")

        df = pd.DataFrame(self.all_data, columns=["feature", "class_label"])
        df.to_pickle(os.path.join(self.path, self.csv_name))

    def train_model(self):
        df = pd.read_pickle(os.path.join(self.path, self.csv_name))
        X = df['feature'].values
        X = np.concatenate(X, axis=0).reshape(len(X), self.n_mfcc)
        
        y = np.array(df['class_label'].values)
        y = tf.keras.utils.to_categorical(y, num_classes=2)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(256, input_shape=X_train[0].shape),
            tf.keras.layers.Activation('relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(256),
            tf.keras.layers.Activation('relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(2, activation='softmax'),
        ])

        model.compile(
            loss='categorical_crossentropy',
            optimizer=tf.keras.optimizers.Adam(),
            metrics=['accuracy']
        )

        print(model.summary())

        print("Model score:")
        fit_model = model.fit(
            X_train,
            y_train,
            epochs=1000,
        )
        
        model.save(os.path.join(MODELS_PATH, "hotword_detection", "luna_hotword", "WWD.keras"))

        score = model.evaluate(X_test, y_test)
        print(score)

        print("Model classification report:")
        y_pred = model.predict(X_test)
        y_pred = np.argmax(y_pred, axis=1)
        y_test = np.argmax(y_test, axis=1)
        print(classification_report(y_test, y_pred))

    def load_model(self):
        if os.path.exists(os.path.join(MODELS_PATH, "hotword_detection", "luna_hotword", "WWD.keras")):
            self.model = tf.keras.models.load_model(os.path.join(MODELS_PATH, "hotword_detection", "luna_hotword", "WWD.keras"))
        else:
            self.model = None

    def predict_hotword_in_file(self, filename):
        if self.model is not None:
            mfcc_processed = self.load_audio_file(filename)
            pred = self.model.predict(np.expand_dims(mfcc_processed, axis=0), verbose=0)
            if pred[:, 1] > self.threshold:
                print(pred[:, 1])
                return True
            return False
        else:
            raise Exception("Model is not loaded")
        

