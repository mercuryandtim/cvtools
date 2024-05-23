FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app
COPY ./output_frames /code/output_frames
COPY ./uploaded_videos /code/uploaded_videos



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]