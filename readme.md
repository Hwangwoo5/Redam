# ♻️ REDAM: AI 기반 재활용 쓰레기 분류 시스템

> **Redam**(Recycling Detection and Automated Management)은 인공지능 기반의 스마트 분리수거 시스템입니다.  
> YOLO 객체 탐지 모델을 이용하여 다양한 재활용 쓰레기를 분류하고, 로봇팔 제어를 통해 자동 선별을 수행합니다.

---

## 📌 프로젝트 개요

- **프로젝트명:** REDAM (Recycling Detection and Automated Management)
- **주요 목표:** 재활용 쓰레기 자동 인식 및 분류를 통한 자원 효율성 향상
- **사용 기술:** YOLOv8/YOLOv11, Python, PyTorch, Raspberry Pi, Jetson, Arduino, 센서 통신

---

## 🧠 주요 기능

- YOLO 기반 실시간 이미지 분류 (금속캔, 종이, 플라스틱, 유리병 등)
- 오염도 분석 및 위험물 탐지 (배터리, 가스통 등)
- 객체 좌표 전송 → 로봇 팔 제어로 실시간 분류 수행
- 센서 기반 보조 감지 (광센서, CO2, 적외선 등)
- 데이터셋 전처리 및 YOLO 학습 파이프라인 구축

---

## 🖥️ 시스템 아키텍처

```plaintext
[Camera] → [YOLOv11 Model] → [Object Classification]
                    ↓
              [Coordinates Extraction]
                    ↓
        [Arduino Servo Controller]
                    ↓
              [Sorting Mechanism]
