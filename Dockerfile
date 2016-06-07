#INSTALL A MOTION DETECTOR NODE

FROM ubuntu:15.04
MAINTAINER Ricard Vilalta <ricard.vilalta@cttc.es>

RUN apt-get update && apt-get install -y install net-tools inetutils-ping git libopencv-dev python-pip python-dev python-opencv && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install imutils numpy
RUN git clone https://github.com/rvilalta/motion_detector.git

CMD ["python motion_detector/motion_detector.py -v motion_detector/example.mp4 -d True -r True", "-D", "FOREGROUND"]
