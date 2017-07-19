import cv2
import os.path
import sys


def InvertColor(img):
    return 255 - img

def main():
    fullPath = sys.argv[1]
    _, tail = os.path.split(fullPath)
    videoName = os.path.splitext(tail)[0]
    
    # Remove old output file if it exists.
    outputPath = 'Output/' + videoName + '.mp4'
    if os.path.isfile(outputPath):
        os.remove(outputPath)

    print("Processing: " + outputPath)

    cap = cv2.VideoCapture(fullPath)

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    ret, frame = cap.read()
    height, width, channel = frame.shape

    out = cv2.VideoWriter(outputPath, fourcc, fps, (width, height))

    while(cap.isOpened()):
        ret, frame = cap.read()       
        if ret == False:
            break

        frame = InvertColor(frame)
        b,g,r = cv2.split(frame)

        ret, bThresh = cv2.threshold(b, 50, 255, cv2.THRESH_TOZERO)
        ret, gThresh = cv2.threshold(g, 50, 255, cv2.THRESH_TOZERO)
        ret, rThresh = cv2.threshold(r, 50, 255, cv2.THRESH_TOZERO)
        
        frame = cv2.merge((bThresh, gThresh, rThresh))
        frame = InvertColor(frame)
        
        out.write(frame)

    cap.release()
    print("Completed!")

if __name__ == '__main__':
    main()
