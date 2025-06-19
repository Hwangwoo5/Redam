# random_training/random_train.py

import os, random, gc
from ultralytics import YOLO
import torch
import csv

# ------------------ [1] 클래스 정의 ------------------
CLASSES = {
    "금속캔-철캔":0, "금속캔-알류미늄캔":1, "종이-종이팩":2, "종이-일반종이":3,
    "페트-투명페트":4, "플라스틱-PP":5, "플라스틱-PS":6, "플라스틱-PE":7,
    "플라스틱-기타":8, "스티로폼":9, "비닐":10, "유리병-갈색":11,
    "유리병-녹색":12, "유리병-무색":13, "고철":14, "알류미늄":15,
    "폐건전지":16, "형광등":17
}
CLASS_LIST = list(CLASSES.keys())

# ------------------ [2] 설정 ------------------
NUM_CLASSES = 5
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
selected_classes = random.sample(CLASS_LIST, NUM_CLASSES)

# ------------------ [3] 경로 설정 ------------------
project_root = "/home/RXO/Redam"
save_dir = os.path.join(project_root, "random_training", f"sample_{NUM_CLASSES}")
os.makedirs(save_dir, exist_ok=True)

# ------------------ [4] 모델 및 학습 ------------------
model = YOLO("yolov11m.pt")

train_data = {
    "train": f"{project_root}/yolo_dataset/images/train",
    "val": f"{project_root}/yolo_dataset/images/val",
    "names": selected_classes,
    "nc": len(selected_classes)
}

results = model.train(
    data=train_data,
    epochs=10,
    imgsz=640,
    batch=32,
    device=0,
    name=f"random_{NUM_CLASSES}_classes",
    project=save_dir,
    save=True
)

# ------------------ [5] 결과 저장 ------------------
metrics = model.val()
with open(os.path.join(save_dir, "metrics_random.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["mAP50", "mAP50-95", "Precision", "Recall"])
    writer.writerow([metrics.box.map50, metrics.box.map, metrics.box.p, metrics.box.r])

gc.collect()
torch.cuda.empty_cache()
