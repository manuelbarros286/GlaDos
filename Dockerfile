FROM public.ecr.aws/lambda/python:3.11

RUN yum -y install gcc gcc-c++

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    --prefer-binary \
    -r requirements.txt

COPY src/ ${LAMBDA_TASK_ROOT}/

CMD ["api.v1.main.handler"]
