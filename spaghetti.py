import jetson.inference
import jetson.utils

net=jetson.inference.detectNet(argv=["--model=../jetson-inference/python/training/detection/ssd/models/hanoi_04_20/ssd-mobilenet.onnx", "--labels=../jetson-inference/python/training/detection/ssd/models/hanoi_04_20/labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes", "--threshold=0.2"])
camera = jetson.utils.videoSource("/dev/video0")      # "/dev/video0" for V4L2
display = jetson.utils.videoOutput("display://0") # "my_video.mp4" for file

while display.IsStreaming():
	a={}
	b={}
	c={}
	img = camera.Capture()
	detections = net.Detect(img)
	height=display.GetHeight()
	width=display.GetWidth()
	jetson.utils.cudaDrawLine(img,(width/3,0),(width/3,height),(255,255,255,255),5)
	jetson.utils.cudaDrawLine(img,(width/3*2,0),(width/3*2,height),(255,255,255,255),5)	
	
	for detection in detections :
		if (detection.Center[0]>0 and detection.Center[0]<width/3):
			# a.append(detection.ClassID)
			a[detection.ClassID] = detection.Center[1]
		elif (detection.Center[0]>width/3 and detection.Center[0]<width/3*2):
			# b.append(detection.ClassID)
			b[detection.ClassID] = detection.Center[1]
		elif (detection.Center[0]>width/3*2 and detection.Center[0]<width):
			# c.append(detection.ClassID)
			c[detection.ClassID] = detection.Center[1]
	
	
	sort_a = sorted(a.items(), key = lambda item: item[1])
	sorted_a_labels = [label[0] for label in sort_a]
	
	sort_b = sorted(b.items(), key = lambda item: item[1])
	sorted_b_labels = [label[0] for label in sort_b]
	
	sort_c = sorted(c.items(), key = lambda item: item[1])
	sorted_c_labels = [label[0] for label in sort_c]
 
 
	print(f"a:{sorted_a_labels}\nb:{sorted_b_labels}\nc:{sorted_c_labels}")
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
