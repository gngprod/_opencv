import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # обращение к камере
cap.set(3, 5000)
cap.set(4, 2000)

while True:
    success, img = cap.read()
    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
