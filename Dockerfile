FROM python:3.10

WORKDIR /code
# Install libgl1-mesa-glx
RUN apt-get update && apt-get install -y libgl1-mesa-glx



COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]