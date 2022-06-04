from keras.models import load_model
from keras.preprocessing import image
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import warnings

warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=DeprecationWarning)

model_new = tf.keras.models.load_model("./model/violence_model.h5")

def load_image(img_path, show=False):

    img = keras.utils.load_img(img_path, target_size=(224, 224))
    img_tensor = keras.utils.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor


def call_pred(img_path):
    new_img = load_image(img_path)
    pred = model_new.predict(new_img)
    print(pred)

    if(pred[0][0] > pred[0][1]):
        #print("Non Voilent")
        return "non voilent"
    else:
        #print("Voilent")
        return "voilent"

#img_path = './test/v.jpg'
#print(call_pred(img_path))