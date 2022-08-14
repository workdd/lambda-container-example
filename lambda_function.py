import json
import boto3
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
import time

bucket_name = 'imagenet-sample'
bucket_ensemble = 'lambda-ensemble'
model_name = 'mobilenet_v2'
model_path = '/var/task/lambda-container-example/model/' + model_name
model = load_model(model_path, compile=True)


def filenames_to_input(file_list):
    imgs = []
    for file in file_list:
        img = Image.open(file)
        img.convert('RGB')
        img = img.resize((224, 224), Image.ANTIALIAS)
        img = np.array(img)
        # if image is grayscale, convert to 3 channels
        if len(img.shape) != 3:
            img = np.repeat(img[..., np.newaxis], 3, -1)
        # batchsize, 224, 224, 3
        img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
        img = preprocess_input(img)
        imgs.append(img)

    batch_imgs = np.vstack(imgs)
    return batch_imgs


def inference_model(batch_imgs):
    pred_start = time.time()
    result = model.predict(batch_imgs)
    pred_time = time.time() - pred_start

    result = np.round(result.astype(np.float64), 8)
    result = result.tolist()

    return result, pred_time


def lambda_handler(event, context):
    file_list = ['/var/task/lambda-container-example/test.jpeg']
    batch_size = 1
    batch_imgs = filenames_to_input(file_list)

    total_start = time.time()
    result, pred_time = inference_model(batch_imgs)
    total_time = time.time() - total_start

    return {
        'model_name': model_name,
        'total_time': total_time,
        'pred_time': pred_time,
    }
