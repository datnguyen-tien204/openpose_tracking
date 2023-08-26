# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np
import time
import csv
from utils import choose_run_mode, load_pretrain_model, set_video_writer
from Pose.pose_visualizer import TfPoseVisualizer
from Action.recognizer import load_action_premodel, framewise_recognize
from warnings import filterwarnings
filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool` is a deprecated alias')
import pandas as pd
import os
import requests
current_struct_time = time.localtime()
formatted_time = time.strftime("%d/%m/%Y %H:%M:%S", current_struct_time)
baseUrl='https://api.telegram.org/bot6217962481:AAElrXjC0iR3wg1csX7ex-jaURJk1EbNOdk/sendPhoto'


# Load models
estimator = load_pretrain_model('VGG_origin')
action_classifier = load_action_premodel('Action/framewise_recognition.h5')

# Initialize parameters
fps_interval = 1
start_time = time.time()
fps_count = 0
frame_count = 0
frame_count2=0
capture_images = False
output_folder = 'ViPham'

dongtac = input("Hay nhap dong tac: ")

# Choose video source
cap = choose_run_mode('data.mp4')
video_writer = set_video_writer(cap, write_fps=int(7.0))

# Initialize joint data file
f = open('origin_data.txt', 'a+')
f.write('nose_x,nose_y,neck_x,neck_y,Rshoulder_x,Rshoulder_y,Relbow_x,Relbow_y,Rwrist_x,RWrist_y,LShoulder_x,LShoulder_y,LElbow_x,LElbow_y,LWrist_x,LWrist_y,RHip_x,RHip_y,RKnee_x,RKnee_y,RAnkle_x,RAnkle_y,LHip_x,LHip_y,LKnee_x,LKnee_y,LAnkle_x,LAnkle_y,REye_x,REye_y,LEye_x,LEye_y,REar_x,REar_y,LEar_x,LEar_y,class')
f.write('\n')

csv_file = open(f'{dongtac}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)




while cv.waitKey(1) < 0:
    has_frame, show = cap.read()
    if has_frame:
        fps_count += 1
        frame_count += 1

        humans = estimator.inference(show)
        pose = TfPoseVisualizer.draw_pose_rgb(show, humans)
        show,init_label = framewise_recognize(pose, action_classifier)

        height, width = show.shape[:2]
        # Calculate and show FPS
        if (time.time() - start_time) > fps_interval:
            realtime_fps = fps_count / (time.time() - start_time)
            fps_count = 0
            start_time = time.time()
        fps_label = 'FPS:{0:.2f}'.format(realtime_fps)
        cv.putText(show, fps_label, (width-160, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        # Show number of detected humans
        num_label = "Human: {0}".format(len(humans))
        cv.putText(show, num_label, (5, height-45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        # Show running time and frame count
        if frame_count == 1:
            run_timer = time.time()
        run_time = time.time() - run_timer
        time_frame_label = '[Time:{0:.2f} | Frame:{1}]'.format(run_time, frame_count)
        cv.putText(show, time_frame_label, (5, height-15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        #Show Frame
        cv.imshow('Phat hien gian lan', show)

        if init_label == "operate":
            if not capture_images:  # Nếu đang không trong trạng thái chụp ảnh
                capture_images = True  # Bắt đầu chế độ chụp ảnh
                frame_count2 = 0  # Đặt lại đếm số lượng ảnh chụp được

            if capture_images:
                frame_filename = os.path.join(output_folder, f"{init_label}_{frame_count2}.png")
                cv.imwrite(frame_filename, show)
                frame_count2 += 1

                try:
                    my_file = open(frame_filename, "rb")
                    phong = '413'
                    parameters = {
                        "chat_id": "-984762057",
                        "caption": f"Thoi gian: {formatted_time}" + "," + f"Noi dung vi pham: {init_label}','Phong:{phong}"
                    }

                    files = {
                        "photo": my_file
                    }
                    resp = requests.get(baseUrl, data=parameters, files=files)
                except:
                    pass

        else:
            capture_images = False




        #Luu file
        video_writer.write(show)

        joints_norm_per_frame = np.array(pose[-1]).astype(np.str_)
        f.write(','.join(joints_norm_per_frame))
        f.write(',' + str(dongtac))
        f.write('\n')


        strluu = (joints_norm_per_frame)
        writer.writerow(strluu)



video_writer.release()
cap.release()
f.close()
csv_file.close()

df = pd.read_csv(f'{dongtac}.csv', sep=',')
df.columns = ['nose_x','nose_y','neck_x','neck_y','Rshoulder_x','Rshoulder_y','Relbow_x','Relbow_y','Rwrist_x','RWrist_y','LShoulder_x','LShoulder_y','LElbow_x','LElbow_y','LWrist_x','LWrist_y','RHip_x','RHip_y','RKnee_x','RKnee_y','RAnkle_x','RAnkle_y','LHip_x','LHip_y','LKnee_x','LKnee_y','LAnkle_x','LAnkle_y','REye_x','REye_y','LEye_x','LEye_y','REar_x','REar_y','LEar_x','LEar_y']
df['class'] = dongtac
df.to_csv(f'{dongtac}.csv', index=False)
