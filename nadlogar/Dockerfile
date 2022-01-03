FROM python:3
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y texlive texlive-fonts-extra
WORKDIR /src
RUN groupadd -g 1000 nadlogar && useradd -m -u 1000 -g nadlogar nadlogar -s /bin/bash
COPY requirements /src/requirements
RUN pip install --no-cache-dir -r requirements/docker.txt
COPY . /src/
RUN chown -R nadlogar /src
USER nadlogar
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]