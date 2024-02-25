import time
import yaml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score
import joblib
import numpy as np
from utils.decorators import exec_timer
from config import BASE_DIR
from config.constants import PHRASES, PHRASE_VAR, COMMAND_THRESHOLD, COMMAND_RATIO_THRESHOLD
from utils.yaml_utils import YamlData
import re
from fuzzywuzzy import fuzz
import os
from pprint import pprint
import logging
from errors.errors import CommandSyntaxInYamlError

def execute_commands_for_learning(commands : dict):
    learning_commands = {}
    for category, details in commands.items():
        if type(details) == dict:
            try:
                phrase_var = details[PHRASE_VAR]
            except:
                details[PHRASE_VAR] = []

            try:
                phrases = details[PHRASES]
            except:
                try:
                    raise CommandSyntaxInYamlError(
                        command_class=category,
                        key=PHRASES,
                    )
                except CommandSyntaxInYamlError as e:
                    e.log_critical_error()
                details[PHRASES] = []

            if details[PHRASE_VAR]:
                vars = list(details[PHRASE_VAR].keys())
                

            for phrase in details[PHRASES]:
                if any(var in phrase for var in vars):
                    for var in vars:
                        if var in phrase:
                            for var_word in details[PHRASE_VAR][var]:
                                phrase_replaced = re.sub(r"\[[^()]*\]", var_word, phrase)
                                learning_commands[phrase_replaced] = category
                else:
                    learning_commands[phrase] = category
        else:
            logging.log(logging.WARNING, f"Неправильная структура команды: {YamlData.path_to_command(category)}, она не будет использоваться в качестве доступной команды")

    return learning_commands

class CommandRecongitionModel:
    def __init__(self):
        self.model_path = os.path.join(BASE_DIR, 'models', 'command_detection', 'commands_detection.joblib')
        self.vectorizer_path = os.path.join(BASE_DIR, 'models', 'command_detection', 'commands_vectorizer.joblib')
        self.test_data_path = os.path.join(BASE_DIR, 'models', 'command_detection', 'commands_detection_test_data.yaml')
    
    @exec_timer
    def train_model(self):
        commands = YamlData.load_all_commands_dict()

        learning_commands = execute_commands_for_learning(commands)

        vectorizer = CountVectorizer()
        vectors = vectorizer.fit_transform(list(learning_commands.keys()))

        model = RandomForestClassifier()
        model.fit(vectors, list(learning_commands.values()))

        joblib.dump(model, self.model_path)
        joblib.dump(vectorizer, self.vectorizer_path)

        del learning_commands
        del commands

    @exec_timer
    def test_model(self, text):
        '''
        TESTING MODEL
        '''
        model = joblib.load(self.model_path)
        vectorizer = joblib.load(self.vectorizer_path)


        testing = dict(yaml.safe_load(open(self.test_data_path, 'r', encoding='utf-8')))

        learning_commands = execute_commands_for_learning(testing)

        vectors = vectorizer.transform(list(learning_commands.keys()))

        y_pred = model.predict(vectors)
        y_true = list(learning_commands.values())

        print(accuracy_score(y_true, y_pred))


        text_vector = vectorizer.transform([text]).toarray()[0]
        answer = model.predict_proba([text_vector])[0]

        classes = model.classes_
        probabilities = answer

        sorted_indices = np.argsort(-np.array(probabilities))

        top_classes = classes[sorted_indices[:]]
        top_probabilities = probabilities[sorted_indices[:]]
        print(text)
        for class_, prob in zip(top_classes, top_probabilities):
            print(f"{class_} - {prob}")

    @exec_timer
    def recognize_command(self, text : str) -> str:
        if not text:
            return None
        
        model = joblib.load(self.model_path)
        vectorizer = joblib.load(self.vectorizer_path)

        commands = YamlData.load_all_commands_dict()

        text_vector = vectorizer.transform([text]).toarray()[0]
        answer = model.predict_proba([text_vector])[0]

        classes = model.classes_
        probabilities = answer

        sorted_indices = np.argsort(-np.array(probabilities))

        top_classes = classes[sorted_indices[:]]
        top_probabilities = probabilities[sorted_indices[:]]

        for command_class, command_probality in zip(top_classes, top_probabilities):
            try:
                if len(commands[command_class]['necessary_phrases']) > 0 and not any(phrase in text for phrase in commands[command_class]['necessary_phrases']):
                    top_classes = np.delete(top_classes, np.where(top_classes == command_class))
                    top_probabilities = np.delete(top_probabilities, np.where(top_probabilities == command_probality))
                elif len(commands[command_class]['exclude_phrases']) > 0 and any(phrase in text for phrase in commands[command_class]['exclude_phrases']):
                    top_classes = np.delete(top_classes, np.where(top_classes == command_class))
                    top_probabilities = np.delete(top_probabilities, np.where(top_probabilities == command_probality))
            except KeyError:
                pass
        
        
        for command_class, command_probality in zip(top_classes, top_probabilities):
            print(f"{command_class} - {command_probality}")
        
        if len(top_probabilities) == 1:
            max_command = top_classes[0]
        elif len(top_probabilities) == 0:
            max_command = None
        else:
            if top_probabilities[0] - top_probabilities[1] > COMMAND_THRESHOLD:
                max_command = top_classes[np.argmax(top_probabilities)]
            else:
                max_command = None 
        return max_command


class CommandRecongition(CommandRecongitionModel):
    def __init__(self):
        super().__init__()

    @exec_timer
    def recognize_command_by_fuzz(self, text : str) -> str:
        max_command = None
        max_ratio = 0
        commands = YamlData.load_all_commands_dict()
        commands_classes = execute_commands_for_learning(commands)
        for phrase, commands_class in commands_classes.items():
            ratio = fuzz.token_set_ratio(text, phrase) / 100
            print(phrase, commands_class, ratio)
            if ratio > max_ratio and ratio > COMMAND_RATIO_THRESHOLD:
                max_command = commands_class
                max_ratio = ratio
                print(max_command, max_ratio)
        return max_command

    @exec_timer
    def recognize_command(self, text : str) -> str:
        max_command = super().recognize_command(text)
        if not max_command:
            max_command = self.recognize_command_by_fuzz(text)
        return max_command

# m = CommandRecongitionModel()
# m.train_model()
# m.test_model("ты такая тупая это кошмар")



