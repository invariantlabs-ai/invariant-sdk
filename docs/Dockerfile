FROM python:3.12

# install mkdocs
COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# build the documentation
COPY . /docs
WORKDIR /docs

RUN mkdocs build --clean

# serve the documentation if DEV_MODE is set, otherwise, serve built documentation
CMD if [ "$DEV_MODE" = "true" ]; then mkdocs serve -a 0.0.0.0:8000; else mkdocs build; python -m http.server 8000 --directory site; fi