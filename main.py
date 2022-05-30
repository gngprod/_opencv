import cv2


cap = cv2.VideoCapture('video3.mp4')  #(0, cv2.CAP_DSHOW)
cap.set(3, 1280)  # установка размера окна
cap.set(4, 700)

ret_f, photo = cap.read()
ret, frame1 = cap.read()
ret, frame2 = cap.read()


def obr(im1, im2):
    im1_res = cv2.resize(im2, (im2.shape[1], im2.shape[0]))
    im2_res = cv2.resize(im1, (im2.shape[1], im2.shape[0]))
    diff_photo = cv2.absdiff(im1_res, im2_res)  # нахождение разницы двух кадров
    gray_photo = cv2.cvtColor(diff_photo, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию
    blur_photo = cv2.GaussianBlur(gray_photo, (5, 5), 0)  # фильтрация лишних контуров
    _photo, thresh_photo = cv2.threshold(blur_photo, 100, 255, cv2.THRESH_BINARY)
    dilated_photo = cv2.dilate(thresh_photo, None,
                              iterations=3)  # данный метод противоположен методу erosion(), т.е. эрозии объекта, и расширяет выделенную на предыдущем этапе область
    сontours_photo, _photo = cv2.findContours(dilated_photo, cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)  # нахождение массива контурных точек\
    for contour in сontours_photo:
        (x, y, w, h) = cv2.boundingRect(contour)  # преобразование массива из предыдущего этапа в кортеж из четырех координат
        # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить
        print(cv2.contourArea(contour))
        if cv2.contourArea(contour) > 10000:
            print('NULL')
            continue
        else:
            cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 0, 255), 2)  # получение прямоугольника из точек кортежа
            print('ВЫЗОВ')
    # cv2.imshow("frame1", im2)
    return True

n = 0
while cap.isOpened():  # метод isOpened() выводит статус видеопотока
    diff = cv2.absdiff(frame1, frame2)  # нахождение разницы двух кадров,
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # метод для выделения кромки объекта белым цветом
    dilated = cv2.dilate(thresh, None, iterations=3)  # данный метод противоположен эрозии объекта, и расширяет выделенную на предыдущем этапе область
    сontours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # нахождение массива контурных точек

    for contour in сontours:
        (x, y, w, h) = cv2.boundingRect(contour)  # преобразование массива из предыдущего этапа в кортеж из четырех координат
        if cv2.contourArea(contour) < 700:  # условие при котором площадь выделенного объекта меньше 700 px
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # получение прямоугольника из точек кортежа

    # print(сontours)
    if сontours == ():
        n += 1
        if n == 30:
            obr(photo, frame2)
    else:
        n = 0
    cv2.imshow("frame1", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
