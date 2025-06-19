#!/usr/bin/env python3
import os, shutil, time, random, json
from ultralytics import YOLO
from datetime import datetime
import torch
import gc
import matplotlib.pyplot as plt
import csv

# ------------------ [1] 한글 폰트 설정 ------------------
import matplotlib
from matplotlib import font_manager, rc
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    rc("font", family="NanumGothic")
    rc("axes", unicode_minus=False)
    log_font_status = "✅ 한글 폰트 설정 완료"
else:
    log_font_status = f"[WARN] 한글 폰트를 찾을 수 없습니다: {font_path}"
print(log_font_status)

# ------------------ [2] 클래스 정의 ------------------
CLASSES = {
    "금속캔-철캔":0, "금속캔-알류미늄캔":1, "종이-종이팩":2, "종이-일반종이":3,
    "페트-투명페트":4, "플라스틱-PP":5, "플라스틱-PS":6, "플라스틱-PE":7,
    "플라스틱-기타":8, "스티로폼":9, "비닐":10, "유리병-갈색":11,
    "유리병-녹색":12, "유리병-무색":13, "고철":14, "알류미늄":15,
    "폐건전지":16, "형광등":17
}
CLASS_LIST = list(CLASSES.keys())

# ------------------ [3] 경로 설정 ------------------
project_root = "/home/RXO/Redam"
save_dir = f"{project_root}/progressive_training/sample_10"
os.makedirs(save_dir, exist_ok=True)

# ------------------ [4] 학습 설정 ------------------
model = YOLO("yolov11m.pt")
epochs = 7
batch = 32
imgsz = 640

# ------------------ [5] 점진적 학습 루프 ------------------
metrics_list = []

for class_name in CLASS_LIST:
    print(f"\n📦 클래스 학습 시작: {class_name}")
    class_id = CLASSES[class_name]
    
    train_data = {
        "train": f"{project_root}/yolo_dataset/images/train",
        "val": f"{project_root}/yolo_dataset/images/val",
        "names": list(CLASSES.keys()),
        "nc": len(CLASSES),
    }

    results = model.train(
        data=train_data,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=0,
        name=f"train_{class_name}",
        project=save_dir,
        save=True,
        exist_ok=True,
        patience=5
    )

    # ------------------ [6] 성능 저장 ------------------
    metrics = model.val()
    ap50 = metrics.box.map50
    map95 = metrics.box.map
    precision = metrics.box.p
    recall = metrics.box.r
    f1 = 2 * (precision * recall) / (precision + recall + 1e-8)

    metrics_list.append({
        "class": class_name,
        "AP50": ap50,
        "mAP50-95": map95,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    })

    # 메모리 정리
    gc.collect()
    torch.cuda.empty_cache()

# ------------------ [7] 결과 CSV 저장 ------------------
csv_path = os.path.join(save_dir, "metrics_summary.csv")
with open(csv_path, "w", newline="") as csvfile:
    fieldnames = ["class", "AP50", "mAP50-95", "Precision", "Recall", "F1"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in metrics_list:
        writer.writerow(row)
print(f"\n📊 결과 요약 저장 완료: {csv_path}")

# ------------------ [8] 시각화 ------------------
classes = [m["class"] for m in metrics_list]
f1_scores = [m["F1"] for m in metrics_list]

plt.figure(figsize=(12, 6))
plt.barh(classes, f1_scores)
plt.xlabel("F1 Score")
plt.title("클래스별 F1 Score (점진학습 결과)")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "f1_score_plot.png"))
print(f"📈 F1 그래프 저장 완료: {save_dir}/f1_score_plot.png")
