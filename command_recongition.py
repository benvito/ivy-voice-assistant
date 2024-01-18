import time
import yaml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import joblib
import numpy as np

def execute_commands_for_learning(commands : dict):
    learning_commands = {}
    for category, details in commands.items():
        for phrase in details['phrases']:
            learning_commands[phrase] = category

    return learning_commands

def train_model():
    commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

    learning_commands = execute_commands_for_learning(commands)
    
    # print(yaml.dump(learning_commands, allow_unicode=True))

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(learning_commands.keys()))

    # model = LogisticRegression()
    # model.fit(vectors, list(learning_commands.values()))
    model = svm.SVC(probability=True)
    model.fit(vectors, list(learning_commands.values()))

    joblib.dump(model, "models/command_detection/commands_detection.joblib")
    joblib.dump(vectorizer, "models/command_detection/commands_vectorizer.joblib")

    del learning_commands
    del commands


def test_model(text):
    '''
    TESTING MODEL
    '''
    model = joblib.load("models/command_detection/commands_detection.joblib")
    vectorizer = joblib.load("models/command_detection/commands_vectorizer.joblib")

    text_vector = vectorizer.transform([text]).toarray()[0]
    answer = model.predict_proba([text_vector])[0]

    classes = model.classes_
    probabilities = answer
    print(text)
    for class_, prob in zip(classes, probabilities):
        print(f"{class_} - {prob}")

# train_model()
# test_model("не выключай компьютер через два часа")

def recognize_command(text : str) -> str or None:
    if not text:
        return None
    
    model = joblib.load("models/command_detection/commands_detection.joblib")
    vectorizer = joblib.load("models/command_detection/commands_vectorizer.joblib")

    text_vector = vectorizer.transform([text]).toarray()[0]
    answer = model.predict_proba([text_vector])[0]

    classes = model.classes_
    probabilities = answer

    # TODO: добавить условие, чтобы вероятность сильно расходилась между последним и предпоследним по вероятности классом
    # Получение индексов элементов в отсортированном порядке
    # sorted_indices = np.argsort(-np.array(probabilities))

    # Получение двух наиболее вероятных классов и их вероятностей
    # top_two_classes = classes[sorted_indices[:2]]
    # top_two_probabilities = probabilities[sorted_indices[:2]]

    # print(top_two_classes)
    # print(top_two_probabilities)
    
    max_command = classes[np.argmax(probabilities)]

    commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))
    

    return max_command
