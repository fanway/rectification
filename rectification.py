import numpy as np
import cv2
import sys


class Rectification(object):
    def __init__(self, path):
        # Load an color image in grayscale
        self.img = cv2.imread(path, 0)
        self.lines = []
        self.coords = []
        self.i = 0
    # mouse callback function
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.img, (x,y), 5, (0,255,0), -1)
            if len(self.lines) < 4:
                if self.i % 2 == 0:
                    print("Select second point to complete the line")
                    self.coords = [x,y,1]
                if self.i % 2 == 1:
                    print(f'Line added {self.i // 2 + 1}')
                    l_coords = self.cross_product([[x,y,1], self.coords])
                    l_coords = np.reshape(l_coords, (1, 3))
                    self.lines.append(l_coords)
                self.i += 1

    def cross_product(self, lines):
        return np.cross(lines[0], lines[1])

    def rectify(self):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL) # Can be resized
        cv2.setMouseCallback('image', self.mouse_callback) # Mouse callback
        while True:
            cv2.imshow('image', self.img)
            k = cv2.waitKey(0) & 0xFF
            # if q is pressed -> close window
            if k == 113:
                break

            # if where is 4 lines in list, compute 2 vanishing points and hence vinishing line
            if len(self.lines) == 4:
                vp1 = self.cross_product([self.lines[0], self.lines[1]])
                vp2 = self.cross_product([self.lines[2], self.lines[3]])
                v_line = self.cross_product([vp1, vp2])
            else:
                v_line = None

            if v_line is not None:
                H = np.identity(3)
                H[2,0], H[2,1] = v_line[0, 0] / v_line[0, 2], v_line[0, 1] / v_line[0, 2]
                self.img = cv2.warpPerspective(self.img, H, (self.img.shape[1], self.img.shape[0]))
                self.i = 0
            else:
                print("Not enough data to compute vanishing line")

        cv2.destroyAllWindows()


if __name__ == "__main__":
    rect = Rectification(sys.argv[1])
    rect.rectify()