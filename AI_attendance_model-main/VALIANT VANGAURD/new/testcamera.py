import cv2

cap = cv2.VideoCapture(1)  # Change the index if needed

# Target width for the wider frame
target_width = 1200

while True:
    ret, frame = cap.read()

    # Get the original width and height of the frame
    original_width = frame.shape[1]
    original_height = frame.shape[0]

    # Calculate the corresponding height to maintain the aspect ratio
    target_height = int((target_width / original_width) * original_height)

    # Resize the frame
    frame = cv2.resize(frame, (target_width, target_height))

    cv2.imshow("iVCam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
