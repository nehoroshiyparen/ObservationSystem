import cv2
import numpy as np
from inference_sdk import InferenceHTTPClient
from datetime import datetime
import base64
from bot import send_image
import time
import os

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",  # Это URL для API Roboflow
    api_key="GNNR9dTrjnIDQlRNpYb1"  # Ваш API ключ
)

def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_video(): 
    cap = cv2.VideoCapture(0)
    if not cap.isOpened:
        print('Не удалось получить доступ к камере')
        return

    print('Запуск модели на устройстве OAK')
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = datetime.now()
        image_filename = f'Photo-{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
        cv2.imwrite('images/' + image_filename, frame)

        image_base64 = image_to_base64('images/' + image_filename)
        
        result = CLIENT.infer(image_base64, model_id="people-4evn7/1")
        predictions = result.get('predictions', [])

        for pred in predictions: 
            x = int(pred['x'] - pred['width']/2)
            y = int(pred['y'] - pred['height']/2)
            w = int(pred['width'])
            h = int(pred['height'])
            confidence = pred['confidence']

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'Conf: {confidence:.2f}', (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imwrite(f'images/Photo-{current_time.strftime("%Y-%m-%d_%H-%M-%S")}-processed.jpg', frame)
            send_image(f'images/Photo-{current_time.strftime("%Y-%m-%d_%H-%M-%S")}-processed.jpg')
        
        os.remove('images/' + image_filename)
        time.sleep(5)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def run_video():
    process_video()