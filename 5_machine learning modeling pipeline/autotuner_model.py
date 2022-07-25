from gc import callbacks
from pickletools import optimize
from tracemalloc import stop

from yaml import DirectiveToken
import tensorflow  as tf
from tensorflow import keras 
import kerastuner as kt

mnist = tf.keras.datasets.mnist
(x_train,y_train),(x_test,y_test) = mnist.load_data()
x_train, x_test = x_train /255.0, x_test /255.0

def model_builder(hp):
    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(28, 28)))

    hp_units=hp.Int('units', min_value=16, max_value=512, step=16)
    model.add(keras.layers.Dense(units=hp_units, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(10))

    model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
    return model

tuner = kt.Hyperband(model_builder,
                    objective = 'val_accuracy',
                    max_epochs=10,
                    factor=3,
                    directory='my_dir',
                    project_name = 'intro_to_kt')

stop_early = tf.keras.callbacks.EarlyStopping(monitor="val_loss",
                                                patience=5)
# 5 steps not significantly changed 
                                            
tuner.search(x_train,
            y_train,
            epochs=50,
            validation_split=0.2,
            callbacks=[stop_early])