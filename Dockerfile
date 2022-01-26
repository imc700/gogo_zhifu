FROM python:3.7
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "app.py"]
# CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]