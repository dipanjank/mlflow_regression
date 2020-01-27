FROM continuumio/miniconda3

SHELL ["/bin/bash", "-c"]

RUN mkdir -p /srv/src/mlflow_regression && mkdir -p /srv/model

COPY . /srv/src/mlflow_regression

WORKDIR /srv/src/mlflow_regression

RUN conda env create --name mlflow --file env.yaml

RUN echo "conda activate mlflow" >> ~/.bashrc

ENV PATH /opt/conda/envs/mlflow/bin:$PATH

CMD ['/bin/bash']
