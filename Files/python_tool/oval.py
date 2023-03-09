import cv2
import json

path_img = 'map_in_01_00100.png'

points_json = json.load(open('points.json', "r"))

# img = cv2.imread(path_img)
# show = img.copy()

def track_fun(ygol, points=points_json):
    if ygol >=0 and ygol < 360:
        ind = -1
        for i in range(len(points)):
            if ygol >= points[i][0]:
                ind = i
        if ind == -1:
            return (-1, -1)
        else:
            ygol0 = points[ind][0]
            x0 = points[ind][1]
            y0 = points[ind][2]
            if ind+1 < len(points):
                ygol1 = points[ind+1][0]
                x1 = points[ind+1][1]
                y1 = points[ind+1][2]
            else:
                ygol1 = 360.
                x1 = points[0][1]
                y1 = points[0][2]
            koef = (ygol - ygol0) / (ygol1 - ygol0)
            x_res = koef * (x1 - x0) + x0
            y_res = koef * (y1 - y0) + y0
            return((x_res-540)*500/1080 , (y_res-540)*500/1080)
    else:
        return (-1, -1)

# for i in range(0, 720):
#     step = i * 0.5
#     point = track_fun(step, points_json)
#     pt_int = (int(point[0]), int(point[1]))
#     cv2.circle(show, pt_int, 2, (255, 255, 255), 2)

# while True:
#     cv2.imshow("Track", show)

#     key = cv2.waitKey(40)
#     if key == 27:
#         break
