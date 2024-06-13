FROM python:3.10

RUN useradd -m -u 1000 user

WORKDIR /code
# Install libgl1-mesa-glx
RUN apt-get update && apt-get install -y libgl1-mesa-glx

COPY ./requirements.txt /code/requirements.txt

RUN python -m venv /code/venv

RUN /code/venv/bin/pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --chown=user . /code

# Create necessary directories and set permissions before switching to non-root user
RUN mkdir -p /code/app/uploaded_videos code/app/output_frames 


ENV PATH="/code/venv/bin:$PATH"

CMD ["uvicorn", "code.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
