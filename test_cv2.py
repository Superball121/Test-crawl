import cv2, time

def collect_image(folder_path, category_name, camera_id):
    window_name = "Collector"
    camera = cv2.VideoCapture(camera_id)
    is_collection_start = False # 預設不會一開始就蒐集

    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            # 我想要在這邊可以透過camera蒐集圖片
            show_frame = frame.copy() # Copy frame for display
            cv2.putText(
                img=show_frame,
                text=f"Collecting: {is_collection_start}",
                org=(50, 50),  # 圖片的像素坐標系，Y軸是反過來的(向下變大)
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=1,
                color=(0, 255, 255), 
                thickness=5, 
                lineType=cv2.LINE_AA
            )
            cv2.imshow(window_name, show_frame)
            if is_collection_start: # 要蒐集
                image_name = f"{time.time()}.jpg" # 用 timestamp
                filename = f"{folder_path}/{category_name}/{image_name}" # 組合檔名
                cv2.imwrite(filename, frame)
                key = cv2.waitKey(333)
            else: # 不蒐集
                key = cv2.waitKey(1)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if   key == ord('q') or key == ord("Q"): # 中止
            break
        elif key == ord('a') or key == ord('A'): # 開始
            is_collection_start = True
        elif key == ord('z') or key == ord('Z'): # 暫停
            is_collection_start = False

    cv2.destroyWindow(window_name)
    
if __name__ == '__main__':
    camera_id = 0
    folder_path = 'Pics_for_cv2/Gesture'
    category_name = ['Open_palm','Victory','Thumb_up']
    for name in category_name:
        collect_image(folder_path, name, camera_id)