FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3-pip python3.6-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

# # Add NVIDIA package repositories
# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
# RUN dpkg -i cuda-repo-ubuntu1804_10.1.243-1_amd64.deb
# RUN apt-get update
# RUN wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
# RUN apt-get install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
# RUN apt-get update

# # Install NVIDIA driver
# RUN apt-get install --no-install-recommends nvidia-driver-430
# # Reboot. Check that GPUs are visible using the command: nvidia-smi

# # Install development and runtime libraries (~4GB)
# RUN apt-get install --no-install-recommends \
#     cuda-10-1 \
#     libcudnn7=7.6.4.38-1+cuda10.1  \
#     libcudnn7-dev=7.6.4.38-1+cuda10.1

# # Install TensorRT. Requires that libcudnn7 is installed above.
# RUN apt-get install -y --no-install-recommends libnvinfer6=6.0.1-1+cuda10.1 \
#     libnvinfer-dev=6.0.1-1+cuda10.1 \
#     libnvinfer-plugin6=6.0.1-1+cuda10.1
#
# RUN pip3 install tensorflow-gpu==1.15.2


ENV FLASK_APP wsgi.py
ENV FLASK_RUN_HOST 0.0.0.0

WORKDIR /app

COPY . /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["wsgi.py"]