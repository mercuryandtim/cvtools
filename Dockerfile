FROM python:3.10

# Install libgl1-mesa-glx
RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app




CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]