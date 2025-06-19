# sampling_training/sampling_train.py

import os, gc
from ultralytics import YOLO
import torch
import csv

# ------------------ [1] 클래스 목록 정의 ------------------
CLASSES = [
    "금속캔-철캔", "금속캔-알류미늄캔", "종이-종이팩", "종이-일반종이",
    "페트-투명페트", "플라스틱-PP", "플라스틱-PS", "플라스틱-PE",
    "플라스틱-기타", "스티로폼", "비닐", "유리병-갈색",
    "유리병-녹색", "유리병-무색", "고철", "알류미늄",
    "폐건전지", "형광등"
]

# ------------------ [2] 경로 설정 ------------------
project_root = "/home/RXO/Redam"
save_dir = os.path.join(project_root, "sampling_training/balanced_train")
os.makedirs(save_dir, exist_ok=True)

# ------------------ [3] 전처리 (클래스별 균등 샘플 추출 필요시 구현)
# (예시에서는 생략되어 있음 → dataset_preparation 단계에서 처리해둔 상태로 가정)

# ------------------ [4] 학습 설정 ------------------
model = YOLO("yolov11m.pt")
train_data = {
    "train": f"{project_root}/yolo_dataset_balanced/train",
    "val": f"{project_root}/yolo_dataset_balanced/val",
    "names": CLASSES,
    "nc": len(CLASSES)
}

results = model.train(
    data=train_data,
    epochs=10,
    imgsz=640,
    batch=32,
    device=0,
    name="balanced_sampling",
    project=save_dir,
    save=True
)

# ------------------ [5] 평가 및 저장 ------------------
metrics = model.val()
with open(os.path.join(save_dir, "metrics_balanced.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["mAP50", "mAP50-95", "Precision", "Recall"])
    writer.writerow([metrics.box.map50, metrics.box.map, metrics.box.p, metrics.box.r])

gc.collect()
torch.cuda.empty_cache()
