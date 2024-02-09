from ultralytics import YOLO

model = YOLO("yolov8s.pt")

# replace "image.jpg" with the filename of an image to predict
results = model(["image.jpg"])

for result in results:
    boxes = result.boxes # bounding boxes of instrument tip
    probs = result.probs # classification probabilities

#stream set true when use video