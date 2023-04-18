import jetson.inference
import jetson.utils

net=jetson.inference.detectNet(argv=["--model=../jetson-inference/python/training/detection/ssd/models/hanoi_04_20/ssd-mobilenet.onnx", "--labels=../jetson-inference/python/training/detection/ssd/models/hanoi_04_20/labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes", "--threshold=0.2"])
camera = jetson.utils.videoSource("/dev/video0")      # "/dev/video0" for V4L2
display = jetson.utils.videoOutput("display://0") # "my_video.mp4" for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	print(display.GetHeight)
	print(display.GetWidth)
	for detection in detections :
		print(detection.ClassID)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
