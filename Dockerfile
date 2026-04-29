FROM public.ecr.aws/lambda/python:3.11

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all source code
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set the handler to the Mangum object we created earlier
CMD ["src.api.main.handler"]
