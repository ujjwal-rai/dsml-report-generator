import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
import pickle

def train_models(data_path):
    data = pd.read_csv(data_path)
    X, y = data.drop(columns=['target']), data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    models = {
        'Logistic Regression': LogisticRegression(),
        'KNN': KNeighborsClassifier(),
        'GaussianNB': GaussianNB(),
        'MultinomialNB': MultinomialNB(),
        'BernoulliNB': BernoulliNB(),
        'Random Forest': RandomForestClassifier()
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average='weighted')
        cm = confusion_matrix(y_test, predictions)
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'confusion_matrix': cm
        }

        if name == "Random Forest":  # Example of saving the best model
            with open("best_model.pkl", "wb") as f:
                pickle.dump(model, f)

    return results
