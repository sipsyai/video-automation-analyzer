#!/usr/bin/env python3
"""Create real test fixtures for video automation analyzer tests."""
import cv2
import numpy as np
from pathlib import Path

def create_test_video():
    """Create a real test video with changing content."""
    output_path = Path(__file__).parent / "sample_login.mp4"

    # Video parameters
    width, height = 1280, 720
    fps = 30
    duration_seconds = 5
    total_frames = fps * duration_seconds

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    if not writer.isOpened():
        print(f"Error: Could not create video writer")
        return False

    print(f"Creating test video: {output_path}")

    # Create frames with progressive changes
    for frame_num in range(total_frames):
        # Create blank frame (white background)
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255

        # Add some UI elements that change over time
        # Simulate a login page with different states

        # Header bar
        cv2.rectangle(frame, (0, 0), (width, 80), (70, 130, 180), -1)
        cv2.putText(frame, "Example Login Page", (50, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

        # Login form box
        form_x, form_y = 400, 200
        form_width, form_height = 480, 400
        cv2.rectangle(frame, (form_x, form_y),
                     (form_x + form_width, form_y + form_height),
                     (200, 200, 200), 2)

        # Title
        cv2.putText(frame, "Sign In", (form_x + 180, form_y + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (50, 50, 50), 2)

        # Different states based on time
        if frame_num < fps * 1:  # First second: empty form
            # Email field
            cv2.rectangle(frame, (form_x + 40, form_y + 120),
                         (form_x + 440, form_y + 160), (220, 220, 220), -1)
            cv2.putText(frame, "Email", (form_x + 50, form_y + 145),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

            # Password field
            cv2.rectangle(frame, (form_x + 40, form_y + 200),
                         (form_x + 440, form_y + 240), (220, 220, 220), -1)
            cv2.putText(frame, "Password", (form_x + 50, form_y + 225),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

        elif frame_num < fps * 2.5:  # Second 1-2.5: typing email
            # Email field with text
            cv2.rectangle(frame, (form_x + 40, form_y + 120),
                         (form_x + 440, form_y + 160), (255, 255, 220), -1)
            email_text = "user@example.com"[:int((frame_num - fps) / 3)]
            cv2.putText(frame, email_text, (form_x + 50, form_y + 145),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

            # Password field (empty)
            cv2.rectangle(frame, (form_x + 40, form_y + 200),
                         (form_x + 440, form_y + 240), (220, 220, 220), -1)
            cv2.putText(frame, "Password", (form_x + 50, form_y + 225),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

        elif frame_num < fps * 4:  # Second 2.5-4: typing password
            # Email field (filled)
            cv2.rectangle(frame, (form_x + 40, form_y + 120),
                         (form_x + 440, form_y + 160), (255, 255, 255), -1)
            cv2.putText(frame, "user@example.com", (form_x + 50, form_y + 145),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

            # Password field with dots
            cv2.rectangle(frame, (form_x + 40, form_y + 200),
                         (form_x + 440, form_y + 240), (255, 255, 220), -1)
            dots = "•" * min(8, int((frame_num - fps * 2.5) / 4))
            cv2.putText(frame, dots, (form_x + 50, form_y + 225),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)

        else:  # Second 4-5: clicking login button
            # Email field (filled)
            cv2.rectangle(frame, (form_x + 40, form_y + 120),
                         (form_x + 440, form_y + 160), (255, 255, 255), -1)
            cv2.putText(frame, "user@example.com", (form_x + 50, form_y + 145),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

            # Password field (filled)
            cv2.rectangle(frame, (form_x + 40, form_y + 200),
                         (form_x + 440, form_y + 240), (255, 255, 255), -1)
            cv2.putText(frame, "••••••••", (form_x + 50, form_y + 225),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)

            # Login button (highlighted when clicking)
            button_color = (100, 150, 250) if frame_num > fps * 4.5 else (70, 130, 180)
            cv2.rectangle(frame, (form_x + 140, form_y + 300),
                         (form_x + 340, form_y + 350), button_color, -1)
            cv2.putText(frame, "Login", (form_x + 195, form_y + 335),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Always show login button outline
        if frame_num >= fps * 1:
            cv2.rectangle(frame, (form_x + 140, form_y + 300),
                         (form_x + 340, form_y + 350), (70, 130, 180), 2)
            cv2.putText(frame, "Login", (form_x + 195, form_y + 335),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        writer.write(frame)

    writer.release()
    print(f"✅ Created test video: {output_path}")
    return True


def create_test_screenshot():
    """Create a real test screenshot."""
    output_path = Path(__file__).parent / "screenshot_click.png"

    width, height = 1280, 720

    # Create image (white background)
    image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Header bar
    cv2.rectangle(image, (0, 0), (width, 80), (70, 130, 180), -1)
    cv2.putText(image, "Example Application", (50, 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    # Some buttons
    buttons = [
        {"x": 200, "y": 200, "text": "Submit", "color": (70, 180, 100)},
        {"x": 400, "y": 200, "text": "Cancel", "color": (180, 70, 70)},
        {"x": 600, "y": 200, "text": "Save", "color": (70, 130, 180)},
    ]

    for btn in buttons:
        cv2.rectangle(image, (btn["x"], btn["y"]),
                     (btn["x"] + 150, btn["y"] + 50), btn["color"], -1)
        cv2.putText(image, btn["text"], (btn["x"] + 35, btn["y"] + 33),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Input field
    cv2.rectangle(image, (200, 300), (600, 350), (220, 220, 220), -1)
    cv2.rectangle(image, (200, 300), (600, 350), (150, 150, 150), 2)
    cv2.putText(image, "Enter text here...", (210, 330),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

    # Checkbox
    cv2.rectangle(image, (200, 400), (230, 430), (200, 200, 200), 2)
    cv2.putText(image, "I agree to terms", (250, 422),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 1)

    cv2.imwrite(str(output_path), image)
    print(f"✅ Created test screenshot: {output_path}")
    return True


if __name__ == "__main__":
    print("Creating real test fixtures...")

    # Create test video
    if create_test_video():
        print("Test video created successfully")
    else:
        print("Failed to create test video")

    # Create test screenshot
    if create_test_screenshot():
        print("Test screenshot created successfully")
    else:
        print("Failed to create test screenshot")

    print("\n✅ All test fixtures created!")
