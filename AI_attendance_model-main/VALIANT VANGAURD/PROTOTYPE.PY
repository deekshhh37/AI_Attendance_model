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

# Function to capture and save a single photo with landmarks for a user
def capture_and_save_user(username, root):
    # Create the user data directory if it doesn't exist
    if not os.path.exists(user_data_directory):
        os.makedirs(user_data_directory)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Create a new window for video capture
    video_capture_window = Toplevel(root)
    video_capture_window.title("Capture User Photo")

    # Create a label for displaying the video stream
    video_label = Label(video_capture_window)
    video_label.pack()

    def on_photo_captured():
        # Close the video capture window
        cap.release()
        video_capture_window.destroy()

    def update_video_label():
        # Read a frame from the video stream
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error capturing frame. Please try again.")
            video_capture_window.after(100, on_photo_captured)  # Schedule the next update
            return

        # Convert the frame to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")

        # Draw rectangles around the detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Use dlib to get facial landmarks
            landmarks = face_landmark_predictor(rgb_frame, dlib.rectangle(left, top, right, bottom))
            for point in landmarks.parts():
                cv2.circle(frame, (point.x, point.y), 2, (255, 0, 0), -1)  # Draw blue landmarks

        # Display the frame
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Check if any faces are detected
        if face_locations:
            # Save the captured photo
            user_image_path = os.path.join(user_data_directory, f"{username}.jpg")
            cv2.imwrite(user_image_path, frame)
            print(f"Photo captured for user: {username}")

            # Call on_photo_captured function
            on_photo_captured()
            return

        # Schedule the next update
        video_capture_window.after(10, update_video_label)

    # Schedule the first update
    video_capture_window.after(10, update_video_label)

    # Release the video capture when the window is closed
    video_capture_window.protocol("WM_DELETE_WINDOW", on_photo_captured)

# Placeholder function for recognizing and logging in a user based on facial landmarks
def recognize_user():
    # Load known user data
    known_user_encodings = []
    known_user_names = []

    for file in os.listdir(user_data_directory):
        if file.endswith(".jpg"):
            username = os.path.splitext(file)[0]
            user_image_path = os.path.join(user_data_directory, file)
            image = face_recognition.load_image_file(user_image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_user_encodings.append(encoding)
            known_user_names.append(username)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error capturing frame. Please try again.")
            break

        # Convert the frame to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")

        # Draw rectangles around the detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Use dlib to get facial landmarks
            landmarks = face_landmark_predictor(rgb_frame, dlib.rectangle(left, top, right, bottom))
            for point in landmarks.parts():
                cv2.circle(frame, (point.x, point.y), 2, (255, 0, 0), -1)  # Draw blue landmarks

        # Find face encodings
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Check if any faces are detected
        if face_locations:
            # Compare each face encoding with the known user encodings
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_user_encodings, face_encoding)

                # Display the name of the recognized user if a match is found
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_user_names[first_match_index]

                # Draw a rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Display the name on the frame
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            # Display the frame with face recognition
            cv2.imshow('Face Recognition', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the video capture and close the window
    cap.release()
    cv2.destroyAllWindows()

# Main loop
while True:
    print("Select an option:")
    print("1. Capture User Photo")
    print("2. Login")
    print("3. Quit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        new_username = input("Enter the name of the user: ")

        # Create the main window for capturing and saving a new user's photo
        root = Tk()
        root.title("Capture User Photo")
        root.withdraw()  # Hide the main window

        # Call the capture_and_save_user function with the new username
        capture_and_save_user(new_username, root)
    elif choice == '2':
        recognize_user()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
