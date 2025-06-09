import cv2
import time
import argparse

from facial_tracking.facialTracking import FacialTracker
import facial_tracking.conf as conf


def main():
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='面部追踪功能')
    parser.add_argument('--webcam', type=int, default=conf.CAM_ID, 
                        help='摄像头ID (默认: conf.py中设置的CAM_ID)')
    args = parser.parse_args()
    
    # 使用指定的摄像头ID
    cam_id = args.webcam
    print(f"使用摄像头ID: {cam_id}")
    
    cap = cv2.VideoCapture(cam_id)
    cap.set(3, conf.FRAME_W)
    cap.set(4, conf.FRAME_H)
    facial_tracker = FacialTracker()
    ptime = 0
    ctime = 0

    if not cap.isOpened():
        print(f"错误: 无法打开摄像头 {cam_id}")
        print("请运行 'python3 camera_list.py' 查看可用摄像头")
        return

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("忽略空摄像头帧。")
            continue
        
        facial_tracker.process_frame(frame)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f'FPS: {int(fps)}', (30,30), 0, 0.6,
                    conf.TEXT_COLOR, 1, lineType=cv2.LINE_AA)
        
        if facial_tracker.detected:
            cv2.putText(frame, f'{facial_tracker.eyes_status}', (30,70), 0, 0.8,
                        conf.WARN_COLOR, 2, lineType=cv2.LINE_AA)
            cv2.putText(frame, f'{facial_tracker.yawn_status}', (30,110), 0, 0.8,
                        conf.WARN_COLOR, 2, lineType=cv2.LINE_AA)

        cv2.imshow('Facial tracking', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
