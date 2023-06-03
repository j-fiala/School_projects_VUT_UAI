import sys
import numpy as np
import os

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QHBoxLayout
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import model_from_json
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

# Thread for progress bar and build without freezing the window
class Worker(QObject):
    def __init__(self):
        super().__init__()
        self._paused = True

    progression = pyqtSignal(int)
    finished = pyqtSignal()

    @pyqtSlot(tuple)
    def train_data(self, file):
        # Intial parameters setup
        progress = 0
        progress_max = 100
        epochs_size = 25
        progress_max = epochs_size
        batch_size = 10
        file_path = file

        # Load data and preprocess
        df = pd.read_csv(r'{0}'.format(file_path), encoding='utf8', sep=";") 
        df.head()
        
        X_train = df.iloc[:,:-1].values
        y_train = df.iloc[:,-1:].values

        # Building model
        model = Sequential()
        model.add(Dense(450, activation='relu', input_shape=(len(X_train[1,:]),)))
        model.add(Dropout(0.1))
        model.add(Dense(150, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(1, activation='sigmoid'))

        # Compile the model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        for epochs in range(epochs_size):
            model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=0)
            progress += 1
            self.progression.emit(int(progress / progress_max * 100))

        # Save the trained model
        model_json = model.to_json()
        with open("trained_model.json", "w") as json_file:
            json_file.write(model_json)
        model.save_weights("trained_model_weights.h5")
    
    
    @pyqtSlot(tuple)
    def test_data(self, file):
        # Intial parameters setup
        file_path = file

        # Load the pre-trained model
        json_file = open('trained_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        pretrained_model = model_from_json(loaded_model_json)
        pretrained_model.load_weights("trained_model_weights.h5")

        # Load data and preprocess
        df = pd.read_csv(r'{0}'.format(file_path), encoding='utf8', sep=";") 
        df.head()
        
        X_test = df.iloc[:,:-1].values
        y_test = df.iloc[:,-1:].values

        print(X_test)

        # Prepare data for confusion matrix
        pred_test = []
        p_pred = pretrained_model.predict(X_test)
        
        pretrained_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        scores = pretrained_model.evaluate(X_test, y_test, verbose=0)
        self.progression.emit(int(100))

        pred_other = 1 - p_pred
        np.reshape(p_pred,[len(y_test),1])
        pred_test = np.append(p_pred,pred_other,axis=1)

        y_other = 1 - y_test
        np.reshape(y_test,[len(y_test),1])
        y_pred_test = np.append(y_test,y_other,axis=1)

        y_pred=np.argmax(pred_test, axis=1)
        y_test=np.argmax(y_pred_test, axis=1)
       
        result = [scores, y_pred, y_test]
        self.finished.emit()

        return result

    def stop(self):
        self.threadactive = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Data Classification')

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create title label and center it
        self.title = QLabel('VSC - DATA CLASSIFICATION APP - made by Jan Fiala')
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 20))

        # Add title label to the main layout
        main_layout.addWidget(self.title)

        # Create layout for building and testing widgets
        build_test_layout = QHBoxLayout()

        # Building layout
        build_layout = QVBoxLayout()

        # Building neural network
        self.titlebuild = QLabel('Building model')
        self.titlebuild.setAlignment(QtCore.Qt.AlignCenter)

        # Loading model
        load_button = QPushButton('Load train file')
        load_button.clicked.connect(self.load_file)
        self.load_label = QLabel('No file to train loaded')
        self.file_name = None

        # Create build button
        build_button = QPushButton('Build')
        build_button.clicked.connect(self.build_model)

        # Add building widgets to the build layout
        build_layout.addWidget(self.titlebuild)
        build_layout.addWidget(load_button)
        build_layout.addWidget(self.load_label)
        build_layout.addWidget(build_button)

        # Testing layout
        test_layout = QVBoxLayout()

        # Testing neural network
        self.titletest = QLabel('Testing model')
        self.titletest.setAlignment(QtCore.Qt.AlignCenter)

        # Loading model
        load_test_button = QPushButton('Load test file')
        load_test_button.clicked.connect(self.load_test_file)
        self.load_test_label = QLabel('No file to test loaded')
        self.file_load_name = None

        # Create test button
        test_button = QPushButton('Test')
        test_button.clicked.connect(self.test_model)

        # Add testing widgets to the test layout
        test_layout.addWidget(self.titletest)
        test_layout.addWidget(load_test_button)
        test_layout.addWidget(self.load_test_label)
        test_layout.addWidget(test_button)

        # Add building layout and testing layout to the build_test_layout
        build_test_layout.addLayout(build_layout)
        build_test_layout.addLayout(test_layout)

        # Add build_test_layout to the main layout
        main_layout.addLayout(build_test_layout)

        # Create layout for progress bar, accuracy, and canvas
        progress_layout = QVBoxLayout()

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Check if model is already pretrained in folder
        if os.path.exists('trained_model.json'):
            self.status_label = QLabel('Model already pre-trained - READY TO TEST')
        else:
            self.status_label = QLabel('')
        self.status_label.setFont(QFont('Arial', 20))

        self.accurancy = QLabel('')

        # Create figure and canvas for confusion matrix
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.axes.clear()

        # Add progress bar, accuracy label, and canvas to the progress_layout
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.accurancy)
        progress_layout.addWidget(self.canvas)
        progress_layout.addStretch()  # Add stretch to center align the widgets

        # Add progress_layout to the main_layout
        main_layout.addLayout(progress_layout)

        # Set main layout as the main widget's layout
        main_widget.setLayout(main_layout)

        # Set main widget as the central widget of the main window
        self.setCentralWidget(main_widget)


    @pyqtSlot()
    def load_file(self):
        # Load data file .csv
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Load Data File', '',
                                                   'Data Files (*.csv);;All Files (*)', options=options)
        if self.file_name:
            self.load_label.setText('Data loaded')

    @pyqtSlot()
    def load_test_file(self):
        # Load data file .csv
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_test, _ = QFileDialog.getOpenFileName(self, 'Load Data File', '',
                                                    'Data Files (*.csv);;All Files (*)', options=options)
        if self.file_test:
            self.load_test_label.setText('Data loaded')

    @pyqtSlot()
    def build_model(self):
        if self.file_name is None:
            self.load_label.setText('Please select file')
            return
        # Setup for worker widget
        self.status_label.setText('Building model...')
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.worker = Worker()
        self.worker_thread = QThread(parent=self)
        self.worker.moveToThread(self.worker_thread)
        self.worker.progression.connect(self.update_progress)
        self.worker_thread.started.connect(self.start_training)
        self.worker.progression.connect(self.update_progress)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()

    @pyqtSlot()
    def test_model(self):
        if self.file_test is None:
            self.load_test_label.setText('Select file to test')
            return
        # Setup for worker widget
        self.status_label.setText('Testing model...')
        self.worker = Worker()
        self.worker_thread = QThread(parent=self)
        self.worker.moveToThread(self.worker_thread)
        self.worker.progression.connect(self.update_progress)
        self.worker_thread.started.connect(self.start_testing)
        self.worker.progression.connect(self.update_progress)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.start()

    @pyqtSlot()
    def start_training(self):
        # Setup for training
        self.result = self.worker.train_data(self.file_name)
        self.training_result()

    @pyqtSlot()
    def start_testing(self):
        # Setup for testing
        self.result = self.worker.test_data(self.file_test)
        self.test_result(self.result)

    @pyqtSlot(int)
    def update_progress(self, progress):
        # Progress bar value increase
        self.progress_bar.setValue(progress)

    @pyqtSlot(int)
    def training_result(self):
        # Model trained
        self.status_label.setText('Model Trained')
        self.worker.stop()

    @pyqtSlot(int)
    def test_result(self,result):
        # Model tested
        scores, y_pred, y_test = result
        self.status_label.setText('Classification finished')
        self.accurancy.setText(' Accuracy on tested data: {}% \n Error on test data: {}%'.format(scores[1], 1 - scores[1]))
        self.draw_matrix(y_pred, y_test)
        self.worker.stop()

    @pyqtSlot()
    def draw_matrix(self, y_test, y_pred):
        # Display of confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        self.disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        self.axes.clear()
        self.disp.plot()
        self.cax = self.axes.matshow(cm, cmap=plt.cm.Reds)
        # self.figure.colorbar(self.cax)

        # Set the labels for the confusion matrix
        self.axes.set_xticklabels([''] + ['Class 0', 'Class 1'])
        self.axes.set_yticklabels([''] + ['Class 0', 'Class 1'])
        self.axes.xaxis.set_ticks_position('bottom')

        # Set the title and axis labels for the plot
        self.axes.set_title('Confusion Matrix of validated data')
        self.axes.set_xlabel('Predicted data')
        self.axes.set_ylabel('True data')

          # Add the predicted and true values to the matrix
        for i in range(2):
            for j in range(2):
                text = self.axes.text(j, i, cm[i, j],
                               ha="center", va="center", color="black")
                text = self.axes.text(j, i+0.3, f"True value: {i}\nPredicted: {j}",
                               ha="center", va="center", color="black")
        self.canvas.draw()

if __name__ == '__main__':
    # Initial setup
    app = QApplication(sys.argv)
    sshFile="style.qss"
    with open(sshFile,"r") as fh:
        app.setStyleSheet(fh.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())