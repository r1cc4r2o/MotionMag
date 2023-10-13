import cv2

def amplify_motion(in_video_path, out_video_path, amplification_factor=2):
    cap = cv2.VideoCapture(in_video_path)
    f_w = int(cap.get(3))
    f_h = int(cap.get(4))
    fps = int(cap.get(5))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_video_path, fourcc, fps, (f_w, f_h))
    prev_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = cv2.absdiff(gray_frame, prev_frame)
            amplified_diff = diff * amplification_factor
            amplified_frame = cv2.add(gray_frame, amplified_diff)
            amplified_frame = cv2.cvtColor(amplified_frame, cv2.COLOR_GRAY2BGR)
            out.write(amplified_frame)

        prev_frame = gray_frame

    cap.release()
    out.release()

if __name__ == "__main__":
    input_video_path = "data/baby.mp4"
    output_video_path = "data/baby_test.mp4"
    amplification_factor = 4

    amplify_motion(input_video_path, output_video_path, amplification_factor)