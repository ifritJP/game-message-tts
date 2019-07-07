# -*- coding: utf-8; -*-
import sys
import numpy as np
import cv2
from PIL import Image
import data
import math

# 画像を表示する。
# キーを押すか、ウィンドウを閉じるまで待つ。


def show(image, debugFlag):
    if not debugFlag:
        return

    title = 'image'
    cv2.imshow(title, image)
    while True:
        if cv2.waitKey(100) != -1:
            break
        if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
            break


# image から line を検出し、
# メッセージボックスを見つける。
# 見つけたメッセージボックスの領域を返す。
def detectLine(image, disp_img, parameter, debugFlag):
    image_height = image.shape[0]
    candidateList = []

    def detect(im, workList):
        minLineLength = 50
        maxLineGap = 150
        # minLineLength = 10
        # maxLineGap = 50

        lines = cv2.HoughLinesP(im, 1, np.pi/180, 100, minLineLength, maxLineGap)
        show(im, debugFlag)

        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    xlen = abs(x1 - x2)
                    ylen = abs(y1 - y2)
                    if (ylen == 0) and (xlen > parameter.MIN_WIDTH):
                        if (min(y1, y2) > parameter.top_margin) and (max(y1, y2) < image_height - parameter.bottom_margin):
                            workList.append((x1, y1, x2, y2))
                    # candidateList.append((x1, y1, x2, y2))

    detect(image, candidateList)
    detect(cv2.bitwise_not(image), candidateList)

    candidateList.sort(key=lambda X: X[1]+X[3])

    def findPair(line, pool):
        max_width = 0
        max_area = 0
        pair = None
        for work in pool:
            if work == line:
                continue

            line_y = line[1]
            work_y = work[1]
            if abs(line_y - work_y) < parameter.MIN_HEIGHT:
                continue

            line_x1 = line[0]
            line_x2 = line[2]
            work_x1 = work[0]
            work_x2 = work[2]

            min_y = min(line[1], line[3], work[1], work[3])
            max_y = max(line[1], line[3], work[1], work[3])

            width = 0
            if line_x1 <= work_x1 and line_x2 >= work_x1:
                # line_x1 --------+------- line_x2
                #                 +
                #              work_x1
                if work_x2 >= line_x2:
                    width = line_x2 - work_x1
                elif work_x2 >= line_x1:
                    width = work_x2 - work_x1
                else:
                    width = line_x1 - work_x1
            elif line_x1 <= work_x2 and line_x2 >= work_x2:
                # line_x1 --------+------- line_x2
                #                 +
                #              work_x2
                if work_x1 <= line_x1:
                    width = work_x2 - line_x1
                elif work_x1 <= line_x2:
                    width = work_x2 - work_x1
                else:
                    width = line_x2 - work_x2
            width = abs(width)
            height = abs(max_y - min_y)
            if width > height:
                # 横長の領域のときのみ検出する。
                # 縦長の領域は対応しない。
                area = width * height

                if width > max_width:
                    max_width = width
                    max_area = area
                    pair = work
                elif area > max_area and max_width - width < 50:
                    max_width = width
                    max_area = area
                    pair = work

        return (pair, max_width, max_area)

    def drawLine(line, color, tick):
        x1 = line[0]
        y1 = line[1]
        x2 = line[2]
        y2 = line[3]
        cv2.line(disp_img, (x1, y1), (x2, y2), color, tick)

    for line in candidateList:
        drawLine(line, (0, 255, 0), 1)

    max_width = 0
    max_area = 0
    pairLine = None
    for line in candidateList:
        pair = findPair(line, candidateList)
        # if pair[1] > max_width:
        #     max_width = pair[1]
        #     pairLine = [line, pair[0]]

        if pair[2] > max_area:
            max_area = pair[2]
            pairLine = [line, pair[0]]

    if not pairLine:
        return None

    for line in pairLine:
        drawLine(line, (0, 0, 255), 2)

    show(disp_img, debugFlag)

    if len(pairLine) != 2:
        return None

    return (min(pairLine[0][0], pairLine[1][0]) + parameter.OFFSET[0],
            min(pairLine[0][1], pairLine[1][1]) + parameter.OFFSET[1],
            max(pairLine[0][2], pairLine[1][2]) + parameter.OFFSET[2],
            max(pairLine[0][3], pairLine[1][3]) + parameter.OFFSET[3])


# 切り出したメッセージボークスから、背景を消して文字を残す。
def pickChar(image, parameter):
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image, parameter.message_thresh, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY )
    #show(thresh, True )

    # OCR は 白背景 で黒文字で判定する
    return cv2.bitwise_not(thresh)


def ColorDodge(bg_img, fg_img):
    bg_img = bg_img / 255
    fg_img = fg_img / 255

    result = np.zeros(bg_img.shape)

    fg_reverse = 1 - fg_img
    non_zero = fg_reverse != 0

    result[non_zero] = bg_img[non_zero]/fg_reverse[non_zero]
    result[~non_zero] = 0

    result = (result.clip(0, 1) * 255).astype(np.uint8)

    return result


def createPreparedOCRImage(image, parameter, debugFlag):
    # openCV 形式の画像フォーマットに変換
    im = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

    if parameter.valid_message_fix_region:
        ocrImage = pickChar(im, parameter)
        show(ocrImage, debugFlag)

        # opencv の画像フォーマットを PIL に変換
        image_pil = Image.fromarray(ocrImage).convert('RGB')
    else:
        imgray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        # im = cv2.imread( targetImagePath )
        # imgray = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
        # show(imgray)

        # img_hsl = cv2.cvtColor( im, cv2.COLOR_BGR2HSV )
        # show( img_hsl, debugFlag )
        # imgray = cv2.cvtColor(img_hsl, cv2.COLOR_RGB2GRAY)
        # show( imgray, debugFlag )
        # imgray = ColorDodge( imgray, imgray )
        # imgray = ColorDodge( imgray, imgray )
        # show( imgray, debugFlag )

        # エッジ抽出
        # edge_img = cv2.Canny(imgray, 50, 200,apertureSize=3)

        edge_img = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, 11, 2)
        # edge_img = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                  cv2.THRESH_BINARY, 11, 2)

        # edge_img = cv2.Canny(edge_img, 50, 100)

        # show(edge_img)
        region = detectLine(edge_img, im.copy(), parameter, debugFlag)

        if region != None:
            # 領域を検出できた場合
            box_img = im[region[1]:region[3], region[0]:region[2]]
            show(box_img, debugFlag)
            ocrImage = pickChar(box_img, parameter)
            show(ocrImage, debugFlag)

            # opencv の画像フォーマットを PIL に変換
            image_pil = Image.fromarray(ocrImage).convert('RGB')
        else:
            ocrImage = pickChar(im, parameter)
            show(ocrImage, debugFlag)

            # opencv の画像フォーマットを PIL に変換
            image_pil = Image.fromarray(ocrImage).convert('RGB')


    cv2.destroyAllWindows()

    return image_pil


if __name__ == '__main__':
    ocrImage = createPreparedOCRImage(Image.open('test.png'),
                                      data.Parameter.create_default(), True)
    # ocrImage = createPreparedOCRImage( Image.open('test2.png'),
    #                                    data.Parameter.create_default(), True )
