import argparse
import cv2
import numpy as np
import torch
import tensorflow as tf

from dms_utils.dms_utils import load_and_preprocess_image, ACTIONS
from net import MobileNet
# 注释掉FacialTracker导入
# from facial_tracking.facialTracking import FacialTracker
import facial_tracking.conf as conf


def infer_one_frame(image, model, yolo_model, facial_tracker=None):
    eyes_status = '未知'
    yawn_status = '未知'
    action = ''

    # 注释掉面部追踪相关代码
    # if facial_tracker:
    #     facial_tracker.process_frame(image)
    #     if facial_tracker.detected:
    #         eyes_status = facial_tracker.eyes_status
    #         yawn_status = facial_tracker.yawn_status

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    yolo_result = yolo_model(rgb_image)

    rgb_image = cv2.resize(rgb_image, (224,224))
    rgb_image = tf.expand_dims(rgb_image, 0)
    y = model.predict(rgb_image)
    result = np.argmax(y, axis=1)

    if result[0] == 0 and yolo_result.xyxy[0].shape[0] > 0:
        action = list(ACTIONS.keys())[result[0]]
    # 注释掉依赖于面部追踪的判断
    # if result[0] == 1 and eyes_status == 'eye closed':
    #     action = list(ACTIONS.keys())[result[0]]

    # 更换为中文提示
    eyes_status_cn = eyes_status
    yawn_status_cn = yawn_status
    action_cn = ""
    if action == "phonecall":
        action_cn = "打电话"
    elif action == "texting":
        action_cn = "发短信"

    cv2.putText(image, f'驾驶员眼睛状态: {eyes_status_cn}', (30,40), 0, 1,
                conf.LM_COLOR, 2, lineType=cv2.LINE_AA)
    cv2.putText(image, f'驾驶员嘴部状态: {yawn_status_cn}', (30,80), 0, 1,
                conf.CT_COLOR, 2, lineType=cv2.LINE_AA)
    cv2.putText(image, f'驾驶员行为: {action_cn}', (30,120), 0, 1,
                conf.WARN_COLOR, 2, lineType=cv2.LINE_AA)
    
    return image


def infer(args):
    image_path = args.image
    video_path = args.video
    cam_id = args.webcam
    checkpoint = args.checkpoint
    save = args.save

    print("正在加载模型...")
    model = MobileNet()
    model.load_weights(checkpoint)

    print("正在加载YOLOv5模型...")
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    yolo_model.classes = [67]

    # 注释掉面部追踪器初始化
    print("已禁用面部追踪器...")
    # facial_tracker = FacialTracker()
    facial_tracker = None

    if image_path:
        print(f"处理图像: {image_path}")
        image = cv2.imread(image_path)
        image = infer_one_frame(image, model, yolo_model, facial_tracker)
        cv2.imwrite('images/test_inferred.jpg', image)
        print(f"处理完成，结果已保存至 images/test_inferred.jpg")
    
    if video_path or cam_id is not None:
        if video_path:
            print(f"处理视频: {video_path}")
        else:
            print(f"使用摄像头 ID: {cam_id}")
            
        cap = cv2.VideoCapture(video_path) if video_path else cv2.VideoCapture(cam_id)
        
        if cam_id is not None:
            cap.set(3, conf.FRAME_W)
            cap.set(4, conf.FRAME_H)
        
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if save:
            print("视频将保存至 videos/output.avi")
            out = cv2.VideoWriter('videos/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'),
                fps, (frame_width,frame_height))
        else:
            print("按 'q' 退出")
        
        while True:
            success, image = cap.read()
            if not success:
                break

            image = infer_one_frame(image, model, yolo_model, facial_tracker)
            if save:
                out.write(image)
            else:
                cv2.imshow('驾驶员监控系统', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
        cap.release()
        if save:
            out.release()
        cv2.destroyAllWindows()
        print("处理完成")
    

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--image', type=str, default=None, help='图像路径')
    p.add_argument('--video', type=str, default=None, help='视频路径')
    p.add_argument('--webcam', type=int, default=None, help='摄像头ID')
    p.add_argument('--checkpoint', type=str, help='预训练模型文件路径')
    p.add_argument('--save', type=bool, default=False, help='是否保存视频')
    args = p.parse_args()

    infer(args)
