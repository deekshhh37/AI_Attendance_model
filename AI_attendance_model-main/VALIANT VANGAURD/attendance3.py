import cv2
import ctypes

# Function to get screen resolution
def get_screen_resolution():
    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return width, height

# Load the pre-trained face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the image
image = cv2.imread("C:\\Users\\likhi\\Downloads\\ANALYSIS OF IMG.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Get screen resolution
screen_width, screen_height = get_screen_resolution()

# Calculate the resize ratio to fit within the screen size
resize_ratio = min(1.0, screen_width / image.shape[1], screen_height / image.shape[0])

# Resize the image
resized_image = cv2.resize(image, None, fx=resize_ratio, fy=resize_ratio)

# Display the resized image with rectangles around detected faces
cv2.imshow("Detected Faces", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
