FROM python:3.10

WORKDIR /code


COPY ./__init__.py /code/__init__.py
COPY ./.venv /code/.venv
COPY ./app /code/app
COPY ./output_frames /code/output_frames
COPY ./uploaded_videos /code/uploaded_videos



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]