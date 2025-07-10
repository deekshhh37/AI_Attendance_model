import cv2
from tkinter import *
from PIL import Image, ImageTk
import os
import shutil

# Directory to store user images and data
user_data_directory = "user_data"

# Function to capture and save multiple photos for a new user
def capture_and_save_user(username, num_photos, root):
    # Create the user data directory if it doesn't exist
    if not os.path.exists(user_data_directory):
        os.makedirs(user_data_directory)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Create a folder for the user's photos
    user_photos_directory = os.path.join(user_data_directory, username)
    os.makedirs(user_photos_directory, exist_ok=True)

    # Create a new window for video capture
    video_capture_window = Toplevel(root)
    video_capture_window.title("Capture User Photos")

    # Create a label for displaying the video stream
    video_label = Label(video_capture_window)
    video_label.pack()

    # Create a list to store references to imgtk
    imgtk_list = []

    def on_photos_captured():
        # Close the video capture window
        cap.release()
        video_capture_window.destroy()

        # Call recognize_user with the path of the last captured photo
        last_captured_photo_path = os.path.join(user_photos_directory, f"{username}_{num_photos}.jpg")
        recognize_user(last_captured_photo_path)

    def update_video_label():
        # Read a frame from the video stream
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error capturing frame. Please try again.")
            video_capture_window.after(100, update_video_label)  # Schedule the next update
            return

        # Save the captured photo
        photo_num = len(imgtk_list) + 1
        photo_path = os.path.join(user_photos_directory, f"{username}_{photo_num}.jpg")
        cv2.imwrite(photo_path, frame)
        print(f"Photo {photo_num}/{num_photos} captured for user: {username}")

        # Display the frame
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        imgtk_list.append(imgtk)  # Keep a reference to imgtk
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_capture_window.update()

        # Check if the required number of photos is reached
        if len(imgtk_list) == num_photos:
            # Call on_photos_captured function
            on_photos_captured()
        else:
            # Schedule the next update
            video_capture_window.after(10, update_video_label)

    # Schedule the first update
    video_capture_window.after(10, update_video_label)

    # Release the video capture when the window is closed
    video_capture_window.protocol("WM_DELETE_WINDOW", lambda: cap.release())

# Function to recognize and log in a user
def recognize_user(captured_photo_path):
    # Implementation for user recognition...
    print(f"Recognizing user from photo: {captured_photo_path}")

# Function to clear all data stored in the face data directory
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

# Main loop
while True:
    print("Select an option:")
    print("1. New User")
    print("2. Login")
    print("3. Clear All Data")
    print("4. Quit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        new_username = input("Enter the name of the new user: ")
        num_photos = 1  # Set the number of photos to capture

        # Create the main window for capturing and saving a new user's photo
        root = Tk()
        root.title("Capture User Photo")
        root.withdraw()  # Hide the main window

        # Call the capture_and_save_user function with the new username and number of photos
        capture_and_save_user(new_username, num_photos, root)
    elif choice == '2':
        # For now, let's pass a placeholder value as captured_photo_path
        recognize_user("path/to/captured/photo.jpg")
    elif choice == '3':
        clear_all_data()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
