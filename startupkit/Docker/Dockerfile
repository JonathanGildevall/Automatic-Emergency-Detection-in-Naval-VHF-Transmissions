
#Change this base image acccording to your convenience
FROM nvcr.io/nvidia/pytorch:21.02-py3

ARG u_id
ARG g_id
ARG username


ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN set -x && \
    apt update && \
    apt install -y --no-install-recommends \
        git\
        wget\
        build-essential \
        apt-utils \
        ca-certificates \
        curl \
        software-properties-common \
        libopencv-dev \
        python3-dev \
        python3-pip \
        python3-setuptools \
        cmake \
        swig \
        wget \
        unzip \
        apt-transport-https \
        gnupg \
        libboost-program-options-dev \
        libboost-stacktrace-dev \
        libboost-system-dev \
        libboost-test-dev \
        libboost-thread-dev \
        libbz2-dev \
        libfftw3-dev \
        liblzma-dev \
        libsndfile1 \
        nano \
        pkg-config \
        python3-dev \
        zlib1g-dev

RUN pip3 uninstall numpy -y

COPY misc/requirements.txt /tmp/
RUN pip3 install pip --upgrade
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${g_id} ${username}
RUN useradd --uid ${u_id} --gid ${g_id} --shell /bin/bash --create-home ${username}
USER ${username}
RUN chown -R ${u_id}:${g_id} /home/${username}
RUN chmod -R  755 /home/${username}

USER root

# CMake version 3.18.3
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://cmake.org/files/v3.18/cmake-3.18.3-Linux-x86_64.sh && \
    mkdir -p /usr/local && \
    /bin/sh /var/tmp/cmake-3.18.3-Linux-x86_64.sh --prefix=/usr/local --skip-license && \
    rm -rf /var/tmp/cmake-3.18.3-Linux-x86_64.sh
ENV PATH=/usr/local/bin:$PATH

# MKL version 2020.0-088
RUN wget -qO - https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2019.PUB | apt-key add - && \
    echo "deb https://apt.repos.intel.com/mkl all main" >> /etc/apt/sources.list.d/hpccm.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        intel-mkl-64bit-2020.0-088 && \
    rm -rf /var/lib/apt/lists/*
RUN echo "source /opt/intel/mkl/bin/mklvars.sh intel64" >> /etc/bash.bashrc

RUN cd /opt && \
    git clone --depth=1 https://github.com/kpu/kenlm.git && \
    cd kenlm && \
    mkdir -p build && \
    cd build && \
    cmake .. && \
    make -j 4

ENV KENLM_ROOT=/opt/kenlm

# https://github.com/facebookresearch/flashlight.git
RUN cd /home/${username} && git clone --depth=1 https://github.com/facebookresearch/flashlight.git && \
    cd flashlight/bindings/python && \
    python3 setup.py install

RUN cd /home/${username} && \
    git clone --depth=1 https://github.com/pytorch/fairseq.git && \
    cd fairseq && \
    pip3 install --editable ./

RUN rm -rf /workspace

WORKDIR /home/${username}

RUN chown -R ${u_id}:${g_id} /home/${username}/fairseq
RUN chmod -R  755 /home/${username}/fairseq
RUN chown -R ${u_id}:${g_id} /home/${username}/flashlight
RUN chmod -R  755 /home/${username}/flashlight

USER ${username}


# publish port
#EXPOSE 5656

# Example Entry point
#ENTRYPOINT ["/bin/bash","-c", "/usr/bin/python3 -m server.py"]
