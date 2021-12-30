import cv2
import numpy as np
import random

# 開啟網路攝影機
cap = cv2.VideoCapture(1) #我的電腦要設1才能開啟鏡頭
# cap = cv2.VideoCapture(0) 

COLORS = np.random.randint(0, 255, [1000, 3])

if not cap.isOpened():
	print("Cannot open camera")
	exit()

# 設定影像尺寸
width = 1280 #1024
height = 960 #768

# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 初始化平均影像
ret, frame = cap.read()

frame = cv2.flip(frame, 1)
print(type(frame))
ROI1 = frame[50:300, 50:400].copy()
ROI2 = frame[50:300,880:1230].copy()

avg1 = np.uint8(np.zeros((ROI1.shape[0], ROI1.shape[1], ROI1.shape[2]), dtype=float))
avg_float1 = np.float32(avg1)
avg2 = np.uint8(np.zeros((ROI2.shape[0], ROI2.shape[1], ROI2.shape[2]), dtype=float))
avg_float2 = np.float32(avg2)

i = 0 #all loop
meme_loop = 0
meme_sum = 0

while(cap.isOpened()):
	# 讀取一幅影格
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)

	# 若讀取至影片結尾，則跳出
	if ret == False:
		break

	ROI1 = frame[50:300, 50:400].copy()	
	ROI2 = frame[50:300,880:1230].copy()

  	# 模糊處理
	blur1 = cv2.blur(ROI1, (4, 4))
	blur2 = cv2.blur(ROI2, (4, 4))

	# 計算目前影格與平均影像的差異值
	diff1 = cv2.absdiff(avg1, blur1)
	diff2 = cv2.absdiff(avg2, blur2)

	# 將圖片轉為灰階
	gray1 = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
	gray2 = cv2.cvtColor(diff2, cv2.COLOR_BGR2GRAY)

	# 篩選出變動程度大於門檻值的區域
	ret1, thresh1 = cv2.threshold(gray1, 50, 255, cv2.THRESH_BINARY)
	ret2, thresh2 = cv2.threshold(gray2, 50, 255, cv2.THRESH_BINARY)

	if np.sum(np.uint8(thresh1))>4000000:
		if i>20:
			print(i,"photo taken!")
			cv2.imwrite('./photo_shoot/'+str(i)+'.jpg',frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
			for j in range(20):
				cv2.putText(frame,"*",(random.randint(50, 400), random.randint(50, 300)),
					cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

	if i>10:
		meme_sum += np.sum(np.uint8(thresh2))
	meme_loop += 1

	if meme_loop<15:
		if meme_sum>15000000:
			meme_sum, meme_loop = 0, 0
			print(meme_loop, i)

			print(i,"midterm meme send!")
			pic = cv2.imread('./meme/'+str(random.randint(1, 10))+'.jpg')
			cv2.imshow("meme", pic)
			for j in range(20):
				cv2.putText(frame,"*",(random.randint(880, 1230), random.randint(50, 300)),
					cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
			
	else:
		meme_sum, meme_loop = 0, 0


	ret, frame2 = cap.read()
	frame2 = cv2.flip(frame2, 1)

	# color = tuple(COLORS[i])
	# color = [int(c) for c in color]
	
	# 主畫面的差異
	frame_diff = cv2.absdiff(frame, frame2)
	frame_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)

	# 顯示偵測結果影像
	# print(type(frame_diff))
	cv2.rectangle(frame_diff, (50,50), (400,300), (255,255,255), thickness=5)
	cv2.rectangle(frame_diff, (880,50), (1230,300), (255,255,255), thickness = 5)
	cv2.putText(frame_diff,"Smile!", (150, 30)
	        ,cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) 
	cv2.putText(frame_diff,"Wave for midterm meme!", (800, 30)
	        ,cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) 
	cv2.putText(frame_diff,"Press q to exit.", (500, 105)
	        ,cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2) 

	print(frame_diff)
	cv2.imshow('diff', frame_diff) # 2 frame difference
	# cv2.imshow('frame', frame) # 原始畫面

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	# 更新平均影像
	cv2.accumulateWeighted(blur1, avg_float1, 0.3)
	avg1 = cv2.convertScaleAbs(avg_float1)

	cv2.accumulateWeighted(blur2, avg_float2, 0.3)
	avg2 = cv2.convertScaleAbs(avg_float2)

	i += 1 
	#cv2.destroyWindow("meme")	

cap.release()
cv2.destroyAllWindows()
