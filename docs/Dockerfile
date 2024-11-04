FROM python:3.12

# install mkdocs
COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# build the documentation
COPY . /docs
WORKDIR /docs

RUN mkdocs build --clean

# serve the documentation if DEV_MODE is set, otherwise, serve built documentation
# for prod serving, we copy everything to root/docs/, as this is where the docs are actually served from in the container
CMD if [ "$DEV_MODE" = "true" ]; then mkdocs serve -a 0.0.0.0:8000; else mkdocs build; mkdir -p root; mv site root/docs; cd root; python -m http.server 8000 --bind 0.0.0.0; fi