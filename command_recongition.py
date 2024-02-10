import time
import yaml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score
import joblib
import numpy as np
from decorators import exec_timer
from config import PHRASES, PHRASE_VAR
from func import YamlData
import re

def execute_commands_for_learning(commands : dict):
    learning_commands = {}
    for category, details in commands.items():
        try:
            phrase_var = details[PHRASE_VAR]
        except:
            details[PHRASE_VAR] = []

        if details[PHRASE_VAR]:
            vars = details[PHRASE_VAR].keys()
        else:
            vars = []
        for phrase in details[PHRASES]:
            if any(var in phrase for var in vars):
                for var in vars:
                    if var in phrase:
                        for var_word in details[PHRASE_VAR][var]:
                            phrase_replaced = re.sub(r"\[[^()]*\]", var_word, phrase)
                            learning_commands[phrase_replaced] = category
            else:
                learning_commands[phrase] = category

    return learning_commands

class CommandRecongitionModel:
    def __init__(self):
        self.model_path = 'models/command_detection/commands_detection.joblib'
        self.vectorizer_path = 'models/command_detection/commands_vectorizer.joblib'
        self.test_data_path = 'models/command_detection/commands_detection_test_data.yaml'
    
    @exec_timer
    def train_model(self):
        commands = YamlData.load_all_commands_dict()

        learning_commands = execute_commands_for_learning(commands)
        
        # print(yaml.dump(learning_commands, allow_unicode=True))

        vectorizer = CountVectorizer()
        vectors = vectorizer.fit_transform(list(learning_commands.keys()))

        model = RandomForestClassifier()
        model.fit(vectors, list(learning_commands.values()))
        # model = svm.SVC(probability=True)
        # model.fit(vectors, list(learning_commands.values()))


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
        
        max_command = top_classes[np.argmax(top_probabilities)]
        
        for command_class, command_probality in zip(top_classes, top_probabilities):
            print(f"{command_class} - {command_probality}")

        return max_command

m = CommandRecongitionModel()
m.train_model()
# m.test_model("ты такая тупая это кошмар")



