FROM docker.io/frolvlad/alpine-python3
RUN pip install aliyun-python-sdk-ecs && \
    pip install aliyun-python-sdk-core && \
    pip install ksc-sdk-python && \
    apk add unzip && \
    wget https://codeload.github.com/huaweicloud/huaweicloud-sdk-python/zip/master -P /home/ && \
    cd /home && unzip master -d . && \
    cd huaweicloud-sdk-python-master && \
    pip install -r requirements.txt && \ 
    python setup.py install && \
    rm -rf /home huaweicloud-sdk-python-master; rm -rf master 
COPY . /home
WORKDIR /home
ENTRYPOINT python get.py
