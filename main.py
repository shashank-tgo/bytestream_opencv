# from opencv_test import byte_stream_to_opencv
# from mp4_to_byte import mp4_to_byte_stream
# from play_video import play_frames

import cv2
import subprocess
global file_path
file_path = '/home/tg0014/Desktop/highway.mp4'


def mp4_to_byte_stream(file):
    cap = cv2.VideoCapture(file)
    byte_stream = bytearray()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

        byte_stream.extend(frame_bytes)

    cap.release()
    return byte_stream


def byte_stream_to_opencv(byte_stream):
    temp_file = 'temp_video.mp4'
    with open(temp_file, 'wb') as f:
        f.write(byte_stream)

    ffmpeg_command = ['ffmpeg', '-i', temp_file, '-vcodec', 'mpeg4', '-acodec', 'aac', 'output_video.mp4']
    subprocess.run(ffmpeg_command)

    video_capture = cv2.VideoCapture('output_video.mp4')

    frames = []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frames.append(frame)

    video_capture.release()
    cv2.destroyAllWindows()
    subprocess.run(['rm', temp_file])
    subprocess.run(['rm', 'output_video.mp4'])

    return frames


def play_frames(frames):
    for frame in frames:
        cv2.imshow('highway', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  # Press 'q' to quit
    cv2.destroyAllWindows()


play_frames(byte_stream_to_opencv(mp4_to_byte_stream(file_path)))
