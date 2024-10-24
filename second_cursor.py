"""
https://chatgpt.com/share/671a4e6c-4304-8010-b008-d5cb478800c0
"""


import sys
import pyautogui
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPainter, QPolygon, QColor, QBrush, QPen
from PIL import ImageGrab


class SecondCursor(QLabel):
    def __init__(self):
        super().__init__()
        self.resize(30, 30)  # Set cursor size

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.Tool)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.arrow_color = QColor(0, 255, 0)  # Initial color (green)
        self.current_position = pyautogui.position()

        # Timer to update the position and color of the second cursor
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position_and_color)
        self.timer.start(50)  # Adjust refresh rate (50ms = 20 FPS)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(self.arrow_color))
        painter.setBrush(QBrush(self.arrow_color))

        # Draw an arrow-shaped polygon
        arrow = QPolygon([
            QPoint(15, 0), QPoint(30, 30),
            QPoint(15, 20), QPoint(0, 30)
        ])
        painter.drawPolygon(arrow)

    def update_position_and_color(self):
        # Get the actual mouse position and update the secondary cursor position
        actual_cursor_pos = pyautogui.position()

        # Example: Offset by 100px on both X and Y
        new_x = actual_cursor_pos.x + 100
        new_y = actual_cursor_pos.y + 100

        self.move(new_x, new_y)

        # Update the color based on the background at the new position
        self.update_color_based_on_background(new_x, new_y)

        # Redraw the widget with the updated color
        self.update()

    def update_color_based_on_background(self, x, y):
        # Capture a small region around the cursor's position (e.g., 5x5 pixel square)
        capture_box = (x, y, x + 5, y + 5)
        screenshot = ImageGrab.grab(bbox=capture_box)
        screenshot_np = np.array(screenshot)

        # Calculate the average color of the captured region
        avg_color = np.mean(screenshot_np, axis=(0, 1))

        # If the average color is close to white, change the arrow color to black
        if np.all(avg_color > 200):  # Close to white (RGB values all > 200)
            self.arrow_color = QColor(0, 0, 0)  # Change to black
        else:
            self.arrow_color = QColor(0, 255, 0)  # Revert to green (or other default color)


def main():
    app = QApplication(sys.argv)

    # Create and display the secondary cursor
    second_cursor = SecondCursor()
    second_cursor.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
