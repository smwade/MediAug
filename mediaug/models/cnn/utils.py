from tensorflow.keras.callbacks import TerminateOnNaN, TensorBoard, EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os


def get_callbacks(log_dir):
    callbacks = [
        TensorBoard(log_dir=log_dir, write_images=True, write_grads=True),
        EarlyStopping(monitor='val_loss', patience=15),
        TerminateOnNaN(),
        ModelCheckpoint(os.path.join(log_dir, 'weights.{epoch:02d}-{val_loss:.2f}.hdf5'), save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=.1, patience=10,
            verbose=0, mode='auto', min_delta=0.0001, cooldown=0, min_lr=0)
    ]
    return callbacks

