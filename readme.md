# ♻️ REDAM: AI 기반 재활용 쓰레기 분류 시스템

> **Redam**(Recycling dam)은 YOLOv11 기반 객체 탐지와 오염도 분석, 좌표 기반 로봇팔 제어를 결합한 지능형 재활용 쓰레기 분류 시스템입니다.  
> 본 시스템은 분류 정확도 향상뿐 아니라 실제 물리적 동작까지 연동되어, 스마트 환경 구축에 기여할 수 있는 실질적인 솔루션입니다.

---

## 🧠 시스템 아키텍처

Redam 시스템은 다음과 같은 모듈로 구성됩니다:

- 📸 Camera: 쓰레기 이미지를 실시간 촬영
- 🤖 YOLOv11 Model: 객체 탐지 및 분류
- 🏷️ Object Classification: 탐지된 쓰레기의 클래스 및 바운딩 박스 추출
- 🎯 Coordinates Extraction: 중심 좌표 계산
- ⚙️ Arduino Servo Controller: 로봇팔 제어
- 🗑️ Sorting Mechanism: 재활용/폐기 쓰레기 자동 분리

### 🔽 시스템 다이어그램

![Redam 시스템 전체 프로세스](docs/5.png)

---

## 🔄 전체 시스템 프로세스

Redam은 단순한 객체 분류를 넘어, 오염도 분석 → 세척 여부 판단 → 로봇팔 제어 → 최종 자동 분리까지 자동화된 스마트 프로세스를 제공합니다.

| 단계 | 설명 |
|------|------|
| 재활용 스캔(A) | 쓰레기 이미지를 촬영하여 분석 시작 |
| 이미지 분류(B) | YOLO 기반 객체 탐지, 위험물 여부 파악 |
| 위험물 탐지 시(CC) | 우선 처리 명령 전달 |
| 오염도 분석(B2) | 세척 가능 여부 판단 |
| 세척 불가능 시 | 이미지 다시 전송 후 분류 재시도 |
| 세척 가능 시 | 로봇팔에 이미지 좌표 전송(D) |
| YOLOv11 기반 분류(A1) | 재질 및 특성 기반 정밀 분류 |
| 재활용 가능(D1) | 컨테이너로 자동 분류 이동 |
| 재활용 불가(D2) | 폐기/소각/특수 처리 대상 분류 |

---

## 🧪 실험 코드 구성

| 폴더 경로 | 설명 |
|-----------|------|
| `progressive_training/` | 클래스별 점진 학습 (클래스를 하나씩 순차적으로 학습하여 성능 추이 분석) |
| `random_training/` | 무작위로 선택된 클래스 조합으로 모델 학습하여 클래스 다양성에 대한 모델 반응 확인 |
| `sampling_training/` | 클래스별 데이터 수를 균등하게 샘플링하여 데이터 불균형 문제를 보완 |
| `evaluation/` | mAP, precision, recall, F1 등 성능 비교 지표 산출 예정 |
| `dataset_preparation/` | JSON → YOLO 변환기, 클래스 매핑, 샘플링 도구 포함 예정 |
| `utils/` | F1 그래프 시각화, 결과 요약 도구 포함 예정 |

---

## 🚀 실행 방법

```bash
# 패키지 설치
pip install -r requirements.txt

# 점진 학습 실행
python progressive_training/progressive_training.py

# 무작위 클래스 학습 실행
python random_training/random_train.py

# 균형 샘플 기반 학습 실행
python sampling_training/sampling_train.py
