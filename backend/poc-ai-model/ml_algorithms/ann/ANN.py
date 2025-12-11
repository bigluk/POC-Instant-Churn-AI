import os

import matplotlib.pyplot as plt
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

from utils import prepare_dataset, fetch_dataset_from_csv


def create_model():

    model = Sequential()
    model.add(Dense(10, input_shape=(24,), activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    return model



def loadDataframeFromCSV (folderName: str, fileName: str) -> pd.DataFrame:
    try:
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        projectRoot = os.path.dirname(scriptDir)
        filePath = os.path.join(projectRoot, '..', folderName, fileName)

        print(f"\nLooking schema at this path: {filePath}")

        df = pd.read_csv(filePath, sep=";")

        print("File Correctly read")
        return df

    except FileNotFoundError:
        print(f"\nERROR schema not found at this path: {filePath}!")
    except Exception as e:
        print(f"Unexpected exception during csv reading: {e}")


def trainAnn(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    classifier = create_model()

    classifier.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    history = classifier.fit(x_train, y_train, epochs=50000, batch_size=64, validation_split=0.2)

    plotAccuracyAndLoss(history)

    evaluate_model(classifier, x_test, y_test)


def plotAccuracyAndLoss(history):

    plt.ion()

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train','validation'], loc='upper left')

    accuracy_path = os.path.join('model_accuracy.png')
    plt.savefig(accuracy_path)
    plt.close() # Chiude la figura per liberare memoria
    print(f"Grafico Accuratezza salvato in: {accuracy_path}")

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train','validation'], loc='upper right')
    plt.draw()
    plt.pause(0.001) # Pausa breve per aggiornare l'interfaccia


def evaluate_model(model, x_test, y_test):

    print("\n" + "=" * 50)
    print("VALUTAZIONE SUL SET DI TEST")
    print("=" * 50)

    # Previsione delle probabilità sul set di test
    # .predict restituisce probabilità (es. 0.98, 0.05)
    y_pred_proba = model.predict(x_test, verbose=0)

    # Conversione delle probabilità in classi binarie (0 o 1)
    # 0.5 è la soglia standard: probabilità >= 0.5 viene classificata come 1
    y_pred_classes = (y_pred_proba > 0.5).astype(int)

    cm = confusion_matrix(y_test, y_pred_classes)

    print("Confusion Matrix:")
    print(cm)
    print("-" * 50)

    print("Classification Report:")
    print(classification_report(y_test, y_pred_classes, target_names=['No', 'Yes']))

    TN = cm[0][0]  # True Negative
    FP = cm[0][1]  # False Positive
    FN = cm[1][0]  # False Negative
    TP = cm[1][1]  # True Positive

    print(f"\nRisultati dettagliati sul set di test:")
    print(f"  True Positives (TP - Previsto Sì, Reale Sì): {TP}")
    print(f"  True Negatives (TN - Previsto No, Reale No): {TN}")
    print(f"  False Positives (FP - Previsto Sì, Reale No): {FP}")
    print(f"  False Negatives (FN - Previsto No, Reale Sì): {FN}")



if __name__ == '__main__':
    bank_marketing = fetch_dataset_from_csv('../data/csv/bank-full-balanced.csv')
    X, y = prepare_dataset(bank_marketing)
    trainAnn(X, y)