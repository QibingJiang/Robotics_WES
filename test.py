# a = {
#   "1000001": ["127.0.0.1", "2B10"],
#   "1000002": ["127.0.0.1", "2B09"],
#   "1000003": ["127.0.0.1", "2B08"],
#   "1000004": ["127.0.0.1", "2B07"],
#   "1000005": ["127.0.0.1", "2B06"],
#   "1000006": ["127.0.0.1", "2B05"],
#   "1000007": ["127.0.0.1", "2B04"],
#   "1000008": ["127.0.0.1", "2B03"],
#   "1000009": ["127.0.0.1", "2B02"],
#   "1000010": ["127.0.0.1", "2B01"],
#   "1000011": ["127.0.0.1", "2C20"],
#   "1000012": ["127.0.0.1", "2C19"],
#   "1000013": ["127.0.0.1", "2C18"],
#   "1000014": ["127.0.0.1", "2C17"],
#   "1000015": ["127.0.0.1", "2C16"],
#   "1000016": ["127.0.0.1", "2C15"]
# }
#
# a['1000020'] = "hi"
# print(a)
import numpy as np

# import pyautogui
# import time
#
# # Give yourself a few seconds to focus the input field
# time.sleep(5)
#
# # The string you want to type
# input_string = "Hello, this is a simulated input!\n"
#
# # Type the string
# pyautogui.write(input_string, interval=0)

# p1 = "C:\work\main_demo\items.csv"
# p2 = "C:\work\main_demo\dict.csv"
#
# import pandas as pd
# # Convert dictionaries to DataFrames
# df_item_order = pd.read_csv(p1)
# df_item_order = df_item_order.drop_duplicates(subset='item', keep='first')
#
# df_chute_order = pd.read_csv(p2)
# df_chute_order = df_chute_order.drop_duplicates(subset='order', keep='first')
#
#
# # Merge the dataframes on 'order' column
# df_result = pd.merge(df_item_order, df_chute_order, on='order', how='inner')
#
# # Select only 'item' and 'chute' columns
# df_result = df_result[['item', 'chute']]
#
# # Print the result
# print(df_result.to_csv(index=False, header=False))

# import keyboard
#
# def on_key_event(event):
#     if event.name == 'esc':  # Exit on ESC key
#         print("Exiting...")
#         return False  # Stop the listener
#     else:
#         print(f"Key pressed: {event.name}, ASCII code: {ord(event.name[0])}")
#
# print("Press any key to see its ASCII value. Press ESC to exit.")
#
# # Set up a listener that calls on_key_event for each key press
# keyboard.hook(on_key_event)
#
# # Keep the program running to listen for key events
# keyboard.wait('esc')

# import pyautogui
# import time
# import random
#
# # Function to simulate typing into the active window
# def type_string():
#     text = ["test001", "test002", "test003", "test004", "test005", ]
#     interval = 3
#
#
#
#     while True:
#         pyautogui.write(random.choice(text))  # Simulate typing
#         pyautogui.press('enter')  # Optional: press enter after typing
#         time.sleep(interval)  # Wait for the specified interval
#
# if __name__ == "__main__":
#     time.sleep(5)  # Give you 5 seconds to focus the text box
#     type_string()


import matplotlib.pyplot as plt

# Define the dimensions of the tri-fold display board
board_height = 1  # meters (arbitrary)
board_length = 12  # meters

# Define the fold positions (assuming symmetric tri-fold)
left_fold = board_length / 3
right_fold = 2 * board_length / 3

# Plot the board
fig, ax = plt.subplots(figsize=(12, 2))
ax.plot([0, board_length], [0, 0], color="black", linewidth=2)  # Bottom edge
ax.plot([0, 0], [0, board_height], color="black", linewidth=2)  # Left edge
ax.plot([board_length, board_length], [0, board_height], color="black", linewidth=2)  # Right edge
ax.plot([left_fold, left_fold], [0, board_height], color="black", linestyle="--", linewidth=2)  # Left fold
ax.plot([right_fold, right_fold], [0, board_height], color="black", linestyle="--", linewidth=2)  # Right fold

# Add labels
ax.text(left_fold / 2, board_height / 2, "Left Panel", ha="center", va="center", fontsize=10)
ax.text((left_fold + right_fold) / 2, board_height / 2, "Center Panel", ha="center", va="center", fontsize=10)
ax.text((right_fold + board_length) / 2, board_height / 2, "Right Panel", ha="center", va="center", fontsize=10)

# Set plot limits and labels
ax.set_xlim(-1, board_length + 1)
ax.set_ylim(-0.5, board_height + 0.5)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")
plt.title("Tri-Fold Display Board (12 meters long)")
plt.show()
