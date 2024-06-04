import cv2
import subprocess
import tempfile
import os


def mp4_to_byte_stream(file_path):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {file_path}")
        return None

    byte_stream = bytearray()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        _, frame_bytes = cv2.imencode('.jpg', frame)
        byte_stream.extend(frame_bytes)

    cap.release()
    return byte_stream


def byte_stream_to_opencv(byte_stream):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(byte_stream)
        temp_file_path = temp_file.name

    output_file_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name

    ffmpeg_command = ['ffmpeg', '-i', temp_file_path, '-vcodec', 'mpeg4', '-acodec', 'aac', output_file_path]
    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg command failed with error {e}")
        return []

    video_capture = cv2.VideoCapture(output_file_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open temporary video file {output_file_path}")
        return []

    frames = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frames.append(frame)

    video_capture.release()
    cv2.destroyAllWindows()

    os.remove(temp_file_path)
    os.remove(output_file_path)

    return frames


def play_frames(frames, width=640, height=360):
    if not frames:
        print("Error: No frames to display")
        return

    for frame in frames:
        resized_frame = cv2.resize(frame, (200, 100))
        cv2.imshow('highway', resized_frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  # Press 'q' to quit
    cv2.destroyAllWindows()


if __name__ == "__main__":
    file_path = '/home/tg0014/Desktop/highway.mp4'
    byte_stream = mp4_to_byte_stream(file_path)
    if byte_stream:
        frames = byte_stream_to_opencv(byte_stream)
        play_frames(frames, width=640, height=360)
    else:
        print("Error: Byte stream conversion failed")
