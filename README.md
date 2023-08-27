# Ultralytics Requirements

## install
- Cuda Toolkit 11.8
- download visual studio community 2017
- download visual studio community 2019
- download visual studio community 2022

## requirements
- loguru
- scikit-image
- tqdm
- torchvision>=0.10.0
- Pillow
- thop
- ninja
- tabulate
- tensorboard
- lap
- motmetrics
- filterpy
- h5py
- onnx==1.8.1
- onnxruntime==1.12.0
- onnx-simplifier==0.3.5
- python -m pip install --upgrade pip==21.1.1
- pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
- torch==2.0.1+cu118
- torchaudio==2.0.2+cu118
- torchvision==0.15.2+cu118
- pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 --index-url https://download.pytorch.org/whl/cu118
- pip install torch==2.0.1+cu118 torchvision==0.15.2+cu118 torchaudio==2.0.2+cu118 --index-url https://download.pytorch.org/whl/cu118

## Base
- matplotlib>=3.2.2
- opencv-python>=4.6.0
- Pillow>=7.1.2
- PyYAML>=5.3.1
- requests>=2.23.0
- scipy>=1.4.1
- torch>=1.7.0
- torchvision>=0.8.1
- tqdm>=4.64.0
- flask
- flask-mysqldb
- cv2
- datetime
- json

## Plotting
- pandas>=1.1.4
- seaborn>=0.11.0

## Extras
- psutil  # system utilization

# Uncomment the following lines as needed

## Logging
- tensorboard>=2.13.0
- clearml
- comet

## Export
- coremltools>=6.0  # CoreML export
- onnx  # ONNX export
- onnxsim  # ONNX simplifier
- nvidia-pyindex  # TensorRT export
- nvidia-tensorrt  # TensorRT export
- scikit-learn==0.19.2  # CoreML quantization
- tensorflow>=2.4.1  # TF exports (-cpu, -aarch64, -macos)
- tflite-support
- tensorflowjs>=3.9.0  # TF.js export
- openvino-dev>=2022.3  # OpenVINO export

## Other
- thop>=0.1.1  # FLOPs computation
- ipython  # interactive notebook
- albumentations>=1.0.3
- pycocotools>=2.0.6  # COCO mAP
- roboflow

## Training

Langkah-langkah untuk melakukan pelatihan:

1. Klon repositori Ultralytics dari: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)

2. Contoh penggunaan:

```sh
yolo task=detect mode=train model=yolov8s.pt imgsz=640 data=../dataset_baru/data.yaml epochs=50 batch=8 name=yolov8s_custom device=0 tracker=bytetrack.yaml lr0=0.001

