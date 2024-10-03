import tkinter as tk
from camera.camera_feed import CameraFeed
from game_logic.player_manager import PlayerManager
from game_logic.game_logic import GameLogic
from PIL import Image, ImageTk
import threading
import time
import os

class GameFrame(tk.Frame):
    def __init__(self, parent, timer_running=True):

        super().__init__(parent)
        self.time_left = 60  # Time limit for the game

        # Load and resize background image using Pillow
        image = Image.open(r"assets/decor/game frame.png")
        resized_image = image.resize((1600, 900), Image.LANCZOS)  # Resize image using LANCZOS

        self.bg_image = ImageTk.PhotoImage(resized_image)

        # Create a label to hold the background image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Make it full screen

        pm = PlayerManager.get_instance()

        # Initialize pygame mixer for music
        music_folder = r"assets/Music_Game"

        # Middle frame for reference image, score, timer, and combo
        self.middle_frame = tk.Frame(self, bg='gold2')
        self.middle_frame.pack(pady=0, padx=0)
        self.middle_frame.place(relx=0.5, rely=0.58, relwidth=0.91, anchor=tk.CENTER)

        # Load match status images
        self.match_img_match = Image.open(r"assets/decor/spot.png")
        self.match_img_match = self.match_img_match.resize((230, 70), Image.LANCZOS)
        self.match_imgtk_match = ImageTk.PhotoImage(self.match_img_match)

        self.match_img_no_match = Image.open(r"assets/decor/keep.png")
        self.match_img_no_match = self.match_img_no_match.resize((230, 70), Image.LANCZOS)
        self.match_imgtk_no_match = ImageTk.PhotoImage(self.match_img_no_match)

        # Pose match status label to display images
        self.match_status_label = tk.Label(self, image=self.match_imgtk_no_match, bg='gold2')  # Default to no match image
        self.match_status_label.pack(side=tk.TOP, pady=0.3)

        # Define the possible extensions
        extensions = ['.png', '.jpg', '.jpeg', '.webp']

        # Create the list of reference images
        reference_poses_dir = 'assets/reference_poses/'
        self.reference_images = [os.path.join(reference_poses_dir, file) for file in os.listdir(reference_poses_dir) if os.path.splitext(file)[1].lower() in extensions]

        self.pose_id = 0

        # Step 1: Load a new image
        self.reference_img = Image.open(self.reference_images[self.pose_id])
        self.reference_img = self.reference_img.resize((700, 525), resample=3)

        # Step 2: Create a new ImageTk.PhotoImage object
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)

        # Reference label without background color
        self.reference_label = tk.Label(self.middle_frame, image=self.reference_imgtk, bg='gold2')
        self.reference_label.pack(side=tk.LEFT, padx=0)

        # Top block (frame) with 'gold2' color
        self.top_block = tk.Label(self, bg='gold2')
        self.top_block.place(relx=0.5, rely=0.29, relwidth=0.91, relheight=0.03, anchor=tk.CENTER)

        # Bottom block (frame) with 'gold2' color
        self.bottom_block = tk.Label(self, bg='gold2')
        self.bottom_block.place(relx=0.5, rely=0.88, relwidth=0.91, relheight=0.03, anchor=tk.CENTER)

        # Frame for score, timer, and combo
        self.overlay_frame = tk.Frame(self, bg='#E6CF00')  # Set background color to #E6CF00
        self.overlay_frame.place(relx=0.5, rely=0.18, anchor=tk.CENTER)  # Center the frame

        # Score label (Top-left)
        self.score_label = tk.Label(self.overlay_frame, text=f"{pm.get_player_score()}", font=('Arial 30 bold'), bg='#E6CF00')
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Combo label (Top-right)
        self.combo_label = tk.Label(self.overlay_frame, text="", font=('Arial 30 bold'), bg='#E6CF00')
        self.combo_label.pack(side=tk.LEFT, padx=50)

        # Timer label (Centered)
        self.timer_label = tk.Label(self.overlay_frame, text=f"{self.time_left}", font=('Arial 30 bold'), bg='#E6CF00')
        self.timer_label.pack(side=tk.RIGHT, padx=70)

        # Video feed label without background color
        self.video_label = tk.Label(self.middle_frame, width=0, height=0, bg='gold2')
        self.video_label.pack(side=tk.RIGHT, padx=0)

        self.camera_feed = CameraFeed(self.video_label)
        self.timer_running = timer_running
        threading.Thread(target=self.update_timer, daemon=True).start()

        # Load images for the buttons
        skip_image = Image.open(r"assets/decor/skip.png")
        skip_image = skip_image.resize((150, 45), Image.LANCZOS)  # Adjust the size as necessary
        self.skip_imgtk = ImageTk.PhotoImage(skip_image)

        give_up_image = Image.open(r"assets/decor/give.png")
        give_up_image = give_up_image.resize((150, 45), Image.LANCZOS)  # Adjust the size as necessary
        self.give_up_imgtk = ImageTk.PhotoImage(give_up_image)

        # Skip Pose button with image
        self.skip_pose_button = tk.Button(self, image=self.skip_imgtk, command=self.skip_pose, bg="gold2")
        self.skip_pose_button.place(relx=0.40, rely=0.95, anchor=tk.CENTER, width=150, height=45)

        # Give up button with image
        self.give_up_button = tk.Button(self, image=self.give_up_imgtk, command=self.end_game, bg="#C7253E")
        self.give_up_button.place(relx=0.60, rely=0.95, anchor=tk.CENTER, width=150, height=45)

        # Game Logic initialization
        self.game_logic = GameLogic(self.reference_images, self.camera_feed, self.update_score, self.update_combo_text, self.update_match_status)
        self.game_logic.start_game()

    def update_timer(self):
        while self.time_left > 0 and self.timer_running:
            time.sleep(1)
            self.time_left -= 1
            self.timer_label.config(text=f"{self.time_left}")
        if self.timer_running:
            self.end_game()

    def update_match_status(self, match):
        # Update the match_status_label with the correct image based on the match status
        if match:
            self.match_status_label.config(image=self.match_imgtk_match)
        else:
            self.match_status_label.config(image=self.match_imgtk_no_match)

    def update_score(self):
        pm = PlayerManager.get_instance()
        self.score_label.config(text=f"{pm.get_player_score()}")
        self.change_ref_photo()

    def update_combo_text(self, combo):
        if combo > 1:
            self.combo_label.config(text=f'{combo}x')
        else:
            self.combo_label.config(text="")

    def end_game(self):
        pm = PlayerManager.get_instance()
        pm.decrement_player_attempts(*pm.get_current_player())
        pm.update_leaderboard()

        self.game_logic.end_game()
        self.timer_running = False
        self.camera_feed.stop()
        self.pack_forget()

        # Transition to session review
        from gui.game_review import GameReview
        game_review = GameReview(self.master)
        game_review.pack(fill=tk.BOTH, expand=True)

    def skip_pose(self):
        self.change_ref_photo()
        self.game_logic.next_photo()

    def change_ref_photo(self):
        self.pose_id += 1
        self.pose_id %= len(self.reference_images)

        # Step 1: Load a new image
        self.reference_img = Image.open(self.reference_images[self.pose_id])
        self.reference_img = self.reference_img.resize((700, 525), resample=3)

        # Step 2: Create a new ImageTk.PhotoImage object
        self.reference_imgtk = ImageTk.PhotoImage(self.reference_img)

        # Step 3: Update the label to display the new image
        self.reference_label.config(image=self.reference_imgtk)

        # Step 4: Keep a reference to the new image to avoid garbage collection
        self.reference_label.image = self.reference_imgtk
