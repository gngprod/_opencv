import cv2
import random
from paho.mqtt import client as mqtt_client


def detect(photo, frame1, frame2):
    n= 0
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in сontours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 700:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if сontours == ():
            n += 1
            if n == 30:
                processing(photo, frame2)
        else:
            n = 0
        cv2.imshow("frame1", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def processing(im1, im2):
    im1_res = cv2.resize(im2, (im2.shape[1], im2.shape[0]))
    im2_res = cv2.resize(im1, (im2.shape[1], im2.shape[0]))
    dif = cv2.absdiff(im1_res, im2_res)
    gray_photo = cv2.cvtColor(dif, cv2.COLOR_BGR2GRAY)
    blur_photo = cv2.GaussianBlur(gray_photo, (5, 5), 0)
    _photo, thresh_photo = cv2.threshold(blur_photo, 100, 255, cv2.THRESH_BINARY)
    dilated_photo = cv2.dilate(thresh_photo, None,
                              iterations=3)
    сontours_photo, _photo = cv2.findContours(dilated_photo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in сontours_photo:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 10000:
            print('NULL')
            continue
        else:
            cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            publish(client, f'alarm: {x}, {y}')
    cv2.imshow("frame1", im2)
    return True


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, message):
    msg = f"messages: {message}"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
         print(f"Send `{msg}` to topic `{topic}`")
    else:
         print(f"Failed to send message to topic {topic}")


broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = connect_mqtt()
client.loop_start()

cap = cv2.VideoCapture('video3.mp4')
cap.set(3, 1280)
cap.set(4, 700)
ret_f, model = cap.read()
ret, before = cap.read()
ret, after = cap.read()

detect(model, before, after)

cap.release()
cv2.destroyAllWindows()

