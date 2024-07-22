FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY ./app /app/

ENV ENVIRONMENT=product

RUN pip install --no-cache-dir --upgrade -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /app/requirement.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
