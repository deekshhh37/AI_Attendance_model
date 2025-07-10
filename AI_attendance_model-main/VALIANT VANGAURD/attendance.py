import cv2
import face_recognition
import dlib
import os
from tkinter import *
from PIL import Image, ImageTk
import shutil

# Directory to store user images and data
user_data_directory = "user_data"

# Load the shape predictor for facial landmarks
shape_predictor_path = "shape_predictor_68_face_landmarks.dat"
face_landmark_predictor = dlib.shape_predictor(shape_predictor_path)

# Function to capture and save one photo for a user with landmarks
def capture_and_save_user(username, root):
    # Create the user data directory if it doesn't exist
    if not os.path.exists(user_data_directory):
        os.makedirs(user_data_directory)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    def on_face_detected():
        # Read a frame from the video stream
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error capturing frame. Please try again.")
            return

        # Save the captured photo
        user_image_path = os.path.join(user_data_directory, f"{username}.jpg")
        cv2.imwrite(user_image_path, frame)
        print(f"Photo captured and saved for user: {username}")

        # Use dlib to get facial landmarks
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = face_landmark_predictor(rgb_frame, dlib.rectangle(0, 0, frame.shape[1], frame.shape[0]))
        for point in landmarks.parts():
            cv2.circle(frame, (point.x, point.y), 2, (0, 255, 255), -1)

        # Display the frame
        cv2.imshow('Facial Landmarks', frame)
        cv2.waitKey(0)  # Wait for a key press

        # Close the video capture window
        cap.release()
        video_capture_window.destroy()  # Destroy the video capture window

    # Create a new window for video capture
    video_capture_window = Toplevel(root)
    video_capture_window.title("Capture User Photo")

    # Create a label for displaying the video stream
    video_label = Label(video_capture_window)
    video_label.pack()

    def update_video_label():
        # Read a frame from the video stream
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error capturing frame. Please try again.")
            video_capture_window.after(100, update_video_label)  # Schedule the next update
            return

        # Convert the frame to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")

        # Draw rectangles around the detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the frame
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Check if any faces are detected
        if face_locations:
            # Call on_face_detected function
            on_face_detected()
            return

        # Schedule the next update
        video_capture_window.after(10, update_video_label)

    # Schedule the first update
    video_capture_window.after(10, update_video_label)

    # Release the video capture when the window is closed
    video_capture_window.protocol("WM_DELETE_WINDOW", lambda: cap.release())

# Main loop
while True:
    print("Select an option:")
    print("1. Capture and Display Facial Landmarks")
    print("2. Quit")

    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        new_username = input("Enter the name of the user: ")

        # Create the main window for capturing and displaying facial landmarks
        root = Tk()
        root.title("Capture and Display Facial Landmarks")
        root.withdraw()  # Hide the main window

        # Call the capture_and_save_user function with the username
        capture_and_save_user(new_username, root)
    elif choice == '2':
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")
