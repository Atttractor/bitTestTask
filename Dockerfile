FROM python:latest
WORKDIR /bitTestTask
COPY ./requirements.txt /bitTestTask/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /bitTestTask/requirements.txt
COPY ./app /bitTestTask/app
CMD ["sleep" "30"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]