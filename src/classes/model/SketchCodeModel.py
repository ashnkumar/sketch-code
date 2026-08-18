from __future__ import absolute_import

from tensorflow.keras.models import Model, Sequential, model_from_json
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger, Callback
from tensorflow.keras.layers.core import Dense, Dropout, Flatten
from tensorflow.keras.layers import Embedding, GRU, TimeDistributed, RepeatVector, LSTM, concatenate , Input, Reshape, Dense
from tensorflow.keras.layers.convolutional import Conv2D
from tensorflow.keras.optimizers import RMSprop

from .ModelUtils import *
from classes.dataset.Dataset import *

MAX_LENGTH = 48
MAX_SEQ    = 150

class SketchCodeModel():

    def __init__(self, model_output_path, model_json_file=None, model_weights_file=None):

        # Create model output path
        self.model_output_path = model_output_path

        # If we have an existing model json / weights, load in that model
        if model_json_file is not None and model_weights_file is not None:
            self.model = self.load_model(model_json_file, model_weights_file)
            optimizer = RMSprop(lr=0.0001, clipvalue=1.0)
            self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)
            print("Loaded pretrained model from disk")

        # Create a new model if we don't have one
        else:
            self.create_model()
            print("Created new model, vocab size: {}".format(self.vocab_size))

        print(self.model.summary())

    def load_model(self, model_json_file, model_weights_file):
        json_file = open(model_json_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(model_weights_file)
        return loaded_model

    def save_model(self):
        model_json = self.model.to_json()
        with open("{}/model_json.json".format(self.model_output_path), "w") as json_file:
            json_file.write(model_json)
        self.model.save_weights("{}/weights.h5".format(self.model_output_path))

    def create_model(self):
        tokenizer, vocab_size = Dataset.load_vocab()
        self.vocab_size = vocab_size

        # Image encoder
        image_model = Sequential()
        image_model.add(Conv2D(16, (3, 3), padding='valid', activation='relu', input_shape=(256, 256, 3,)))
        image_model.add(Conv2D(16, (3,3), activation='relu', padding='same', strides=2))
        image_model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
        image_model.add(Conv2D(32, (3,3), activation='relu', padding='same', strides=2))
        image_model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
        image_model.add(Conv2D(64, (3,3), activation='relu', padding='same', strides=2))
        image_model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
        image_model.add(Flatten())
        image_model.add(Dense(1024, activation='relu'))
        image_model.add(Dropout(0.3))
        image_model.add(Dense(1024, activation='relu'))
        image_model.add(Dropout(0.3))
        image_model.add(RepeatVector(MAX_LENGTH))
        visual_input = Input(shape=(256, 256, 3,))
        encoded_image = image_model(visual_input)

        # Language encoder
        language_input = Input(shape=(MAX_LENGTH,))
        language_model = Embedding(vocab_size, 50, input_length=MAX_LENGTH, mask_zero=True)(language_input)
        language_model = GRU(128, return_sequences=True)(language_model)
        language_model = GRU(128, return_sequences=True)(language_model)

        # Decoder
        decoder = concatenate([encoded_image, language_model])
        decoder = GRU(512, return_sequences=True)(decoder)
        decoder = GRU(512, return_sequences=False)(decoder)
        decoder = Dense(vocab_size, activation='softmax')(decoder)

        # Compile the model
        self.model = Model(inputs=[visual_input, language_input], outputs=decoder)
        optimizer = RMSprop(lr=0.0001, clipvalue=1.0)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    def train(self, training_path, validation_path, epochs):

        # Setup data generators
        training_generator, train_steps_per_epoch = Dataset.create_generator(training_path, max_sequences=MAX_SEQ)
        validation_generator, val_steps_per_epoch = Dataset.create_generator(validation_path, max_sequences=MAX_SEQ)

        # Setup model callbacks
        callbacks_list = self.construct_callbacks(validation_path)

        # Begin training
        print("\n### Starting model training ###\n")
        self.model.fit_generator(generator=training_generator, validation_data=validation_generator, epochs=epochs, shuffle=False, validation_steps=val_steps_per_epoch, steps_per_epoch=train_steps_per_epoch, callbacks=callbacks_list, verbose=1)
        print("\n### Finished model training ###\n")
        self.save_model()

    def construct_callbacks(self, validation_path):
        checkpoint_filepath="{}/".format(self.model_output_path) + "weights-epoch-{epoch:04d}--val_loss-{val_loss:.4f}--loss-{loss:.4f}.h5"
        csv_logger = CSVLogger("{}/training_val_losses.csv".format(self.model_output_path))
        checkpoint = ModelCheckpoint(checkpoint_filepath,
                                    verbose=0,
                                    save_weights_only=True,
                                    save_best_only=True,
                                    mode= 'min',
                                    period=2)
        callbacks_list = [checkpoint, csv_logger]
        return callbacks_list






