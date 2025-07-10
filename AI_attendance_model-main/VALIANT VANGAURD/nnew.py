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

# Function to analyze captured photos for recognition
def analyze_captured_photos(username, num_photos, captured_photos):
    # Load known user data
    known_user_encodings = []
    known_user_names = []

    for file in os.listdir(user_data_directory):
        if file.endswith(".jpg") and username in file:
            user_image_path = os.path.join(user_data_directory, file)
            image = face_recognition.load_image_file(user_image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_user_encodings.append(encoding)
            known_user_names.append(username)

    # Initialize results dictionary
    results = {}

    for photo_num in range(1, num_photos + 1):
        # Load the captured photo
        photo_path = os.path.join(user_data_directory, f"{username}_{photo_num}.jpg")
        image = face_recognition.load_image_file(photo_path)

        # Get facial landmarks
        landmarks = face_landmark_predictor(image, dlib.rectangle(0, 0, image.shape[0], image.shape[1]))

        # Process the landmarks for recognition (customize this part based on your needs)
        # For example, you can calculate distances between specific points or use a machine learning model

        # Placeholder: Assign a name based on a simple condition (customize this part)
        name = "Known" if some_recognition_condition(landmarks) else "Unknown"

        results[os.path.basename(photo_path)] = name

    # Display results
    print("\nRecognition Results:")
    for photo, name in results.items():
        print(f"{photo}: {name}")

# Placeholder function for facial landmark recognition condition (customize this)
def some_recognition_condition(landmarks):
    # Customize this function based on your recognition requirements
    # For example, you can calculate distances between specific points or use a machine learning model
    return True

# Placeholder function for clearing all data (customize this)
def clear_all_data():
    # Confirm with the user before proceeding
    confirmation = input("Are you sure you want to clear all data? (yes/no): ")
    if confirmation.lower() == "yes":
        # Remove the user_data_directory and recreate it
        shutil.rmtree(user_data_directory, ignore_errors=True)
        os.makedirs(user_data_directory)
        print("All data cleared.")
    else:
        print("Data clearing aborted.")

# Placeholder function for recognizing and logging in a user (customize this)
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

        # Find all face locations in the current frame
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")

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
    print("1. Capture and Display Facial Landmarks")
    print("2. Capture and Save User")
    print("3. Analyze Captured Photos")
    print("4. Clear All Data")
    print("5. Quit")

    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == '1':
        new_username = input("Enter the name of the user: ")

        # Create the main window for capturing and displaying facial landmarks
        root = Tk()
        root.title("Capture and Display Facial Landmarks")
        root.withdraw()  # Hide the main window

        # Call the capture_and_save_user function with the username
        capture_and_save_user(new_username, root)
    elif choice == '2':
        new_username = input("Enter the name of the new user: ")

        # Create the main window for capturing and saving a new user's photo
        root = Tk()
        root.title("Capture and Save User")
        root.withdraw()  # Hide the main window

        # Call the capture_and_save_user function with the new username
        capture_and_save_user(new_username, root)
    elif choice == '3':
        username = input("Enter the name of the user: ")
        num_photos = int(input("Enter the number of photos to analyze: "))

        # Analyze captured photos for recognition
        analyze_captured_photos(username, num_photos, captured_photos)
    elif choice == '4':
        clear_all_data()
    elif choice == '5':
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
