
import cv2

class OpenCV:
        
    def init(self, id):
        self.cap = cv2.VideoCapture()
        b = self.cap.open(id)
        self.contours = None
        self.prevFrame = None
        return b
    
    def free(self):
        self.cap.release()
        
    def getFrame(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    def getDeviceCount(self):
        tmp = cv2.VideoCapture()
        id = 0
        while True:
            b = tmp.open(id)
            if not b:
                break
            tmp.release()
            id += 1
        return id
    
    def grayFrame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        return gray
    
    def processFrame(self, frame):
        
        gray = self.grayFrame(frame)
        
        if self.prevFrame is None:
            self.prevFrame = gray
            return frame
        
        # compute the absolute difference between the current frame and 
        # first frame
        frameDelta = cv2.absdiff(self.prevFrame, gray)

        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]        
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        _, cnts, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 1000:
                continue
            
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.prevFrame = gray
        
        self.contours = cnts;
        
        return frame
    

if __name__ == '__main__':
    ocv = OpenCV()
    b = ocv.init(0)
    if b:
        frame = ocv.getFrame();
        ocv.free()
