import cv2
from pyzbar.pyzbar import decode
import requests
import numpy as np
from firebase_admin import credentials, initialize_app, firestore
from gtts import gTTS
import os
import pygame

cred = credentials.Certificate('Place the path to your private key')
initialize_app(cred)
db = firestore.client()

firebase_url = 'https://vision-vanguards-trial-default-rtdb.firebaseio.com'

pygame.mixer.init()

def fetch_product_data(barcode):
    product_url = f'{firebase_url}/{barcode}.json'
    print("Constructed Firebase URL:", product_url)  

    try:
        response = requests.get(product_url)
        data = response.json()

        if data:
            return data
        else:
            print(f"No data found for barcode: {barcode}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return None

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")

    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():  
        pygame.time.Clock().tick(10)  

    os.remove("output.mp3")

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture image")
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')

            product_data = fetch_product_data(barcode_data)
            if product_data:
                print("Barcode:", barcode_data)
                product_name = product_data.get("Name", "N/A")
                product_price = product_data.get("Price", "N/A")
                print("Product Name:", product_name)
                print("Product Price:", product_price)
                # Declare the product in hand with its value
                speak(f"The product is {product_name} and the price is {product_price}")

            else:
                print("Product data not found for barcode:", barcode_data)

            points = obj.polygon
            if len(points) == 4:
                pts = [(points[j].x, points[j].y) for j in range(4)]
                pts = np.array(pts, dtype=int)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        cv2.imshow("Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == 27:  
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    main()
