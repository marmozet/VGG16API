# example of using a pre-trained model as a classifier

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from fastapi import FastAPI, File, UploadFile, Form
from PIL import Image
import numpy as np
import shutil

# cargamos el modelo y la API
model = VGG16()
app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Bienvenido"}

@app.post('/file')
async def _file_upload(
        image: UploadFile = File(...),
):
    file_location = f"images/destination.png"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(image.file, file_object)
    # Cargamos la imagen de un Archivo
    image = load_img('images/destination.png', target_size=(224, 224))

    # Procesamos la imagen para que pueda ser utilizada en el modelo
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    # Este modelo se encarga de predecir el animal de se encuentra en la imagen
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]
    
    # Agregamos la predicción a un diccionario
    dictionary = {}
    dictionary['pred'] = str(label[1])
    dictionary['accuracy'] = float(label[2])

    # retornamos el diccionario 
    return dictionary

