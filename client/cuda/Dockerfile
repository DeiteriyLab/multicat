FROM ubuntu:22.04

LABEL com.nvidia.volumes.needed="nvidia_driver"

RUN apt-get update && apt-get install -y --no-install-recommends \
        ocl-icd-libopencl1 wget clinfo pkg-config make clinfo build-essential git libcurl4-openssl-dev libssl-dev zlib1g-dev libcurl4-openssl-dev libssl-dev pkg-config pciutils python3.11 python3.11-dev && \
        wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py && \
        rm -rf /var/lib/apt/lists/* && \
        python3.11 get-pip.py

RUN mkdir -p /etc/OpenCL/vendors && \
    echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}


RUN wget --no-check-certificate https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
RUN mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN wget --no-check-certificate https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2204-11-8-local_11.8.0-520.61.05-1_amd64.deb
RUN dpkg -i cuda-repo-ubuntu2204-11-8-local_11.8.0-520.61.05-1_amd64.deb
RUN rm cuda*.deb
RUN cp /var/cuda-repo-ubuntu2204-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
RUN apt-get update
RUN apt-get -y install cuda-toolkit-11-8

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

############################### end nvidia cuda driver ################################

ENV HASHCAT_VERSION        v6.2.6
ENV HASHCAT_UTILS_VERSION  v1.9
ENV HCXTOOLS_VERSION       6.2.7
ENV HCXDUMPTOOL_VERSION    6.2.7
ENV HCXKEYS_VERSION        master

# Fetch PCI IDs list to display proper GPU names
RUN update-pciids

WORKDIR /app

RUN git clone https://github.com/hashcat/hashcat.git && cd hashcat && git checkout ${HASHCAT_VERSION} && make install_library && make install -j4

RUN git clone https://github.com/hashcat/hashcat-utils.git && cd hashcat-utils/src && git checkout ${HASHCAT_UTILS_VERSION} && make
RUN ln -s /root/hashcat-utils/src/cap2hccapx.bin /usr/bin/cap2hccapx

RUN git clone https://github.com/ZerBea/hcxtools.git && cd hcxtools && git checkout ${HCXTOOLS_VERSION} && make install

RUN git clone https://github.com/ZerBea/hcxdumptool.git && cd hcxdumptool && git checkout ${HCXDUMPTOOL_VERSION} && make install

RUN git clone https://github.com/hashcat/kwprocessor.git && cd kwprocessor && git checkout ${HCXKEYS_VERSION} && make
RUN ln -s /root/kwprocessor/kwp /usr/bin/kwp

ENV HC_LIB_DIR=/usr/local/lib
ENV HC_SOURCES_DIR=/app/hashcat
ENV HC_PATH=/app/hashcat
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

COPY . /app/

RUN pip3.11 install setuptools && \
    git clone https://github.com/michael2to3/pyhashcat.git && \
    cd pyhashcat/ && \
    python3.11 setup.py build_ext -I /usr/include/lzma/ && \
    python3.11 setup.py install

RUN pip3.11 install --no-cache-dir -r /app/requirements.txt
