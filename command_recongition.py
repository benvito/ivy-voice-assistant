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

def execute_commands_for_learning(commands : dict):
    learning_commands = {}
    for category, details in commands.items():
        for phrase in details['phrases']:
            learning_commands[phrase] = category

    return learning_commands

@exec_timer
def train_model():
    commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

    learning_commands = execute_commands_for_learning(commands)
    
    # print(yaml.dump(learning_commands, allow_unicode=True))

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(learning_commands.keys()))

    model = RandomForestClassifier()
    model.fit(vectors, list(learning_commands.values()))
    # model = svm.SVC(probability=True)
    # model.fit(vectors, list(learning_commands.values()))


    joblib.dump(model, "models/command_detection/commands_detection.joblib")
    joblib.dump(vectorizer, "models/command_detection/commands_vectorizer.joblib")

    del learning_commands
    del commands

@exec_timer
def test_model(text):
    '''
    TESTING MODEL
    '''
    model = joblib.load("models/command_detection/commands_detection.joblib")
    vectorizer = joblib.load("models/command_detection/commands_vectorizer.joblib")


    testing = dict(yaml.safe_load(open('models/command_detection/commands_detection_test_data.yaml', 'r', encoding='utf-8')))

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

train_model()
test_model("сколько сейчас время")


@exec_timer
def recognize_command(text : str) -> str or None:
    if not text:
        return None
    
    model = joblib.load("models/command_detection/commands_detection.joblib")
    vectorizer = joblib.load("models/command_detection/commands_vectorizer.joblib")

    commands = dict(yaml.safe_load(open('data/commands/commands.yaml', 'r', encoding='utf-8')))

    text_vector = vectorizer.transform([text]).toarray()[0]
    answer = model.predict_proba([text_vector])[0]

    classes = model.classes_
    probabilities = answer

    # TODO: добавить условие, чтобы вероятность сильно расходилась между последним и предпоследним по вероятности классом
    # Получение индексов элементов в отсортированном порядке
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

    # Это сравнение по количеству совпадающих фраз
    # count_matches_phrase = [0, 0]

    # for command_class, command_probality in zip(top_classes, top_probabilities):
    #     print(command_class, command_probality)
    #     count_matches_phrase[0], count_matches_phrase[-1] = count_matches_phrase[1], 0
    #     try:         
    #         for phrase in commands[command_class]['necessary_phrases']:
    #             if phrase in text and max(top_probabilities) - command_probality < 0.25:
    #                 count_matches_phrase[-1] += 1
    #         if count_matches_phrase[-1] > count_matches_phrase[0] and count_matches_phrase[-1] > 0:
    #             max_command = command_class
    #     except KeyError as e:
    #         pass

    return max_command
