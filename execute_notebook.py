import logging
import os
from argparse import ArgumentParser

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


TRAIN_DATA_DIR = '/srv/model/input'
MODEL_OUTPUT_DIR = '/srv/model/output'


def download_files(input_path):
    os.makedirs(TRAIN_DATA_DIR, exist_ok=True)
    logging.info(f"Copying {input_path} to {TRAIN_DATA_DIR}")


def main():
    parser = ArgumentParser(description="Execute a Jupyter Notebook Programmatically.")

    parser.add_argument('-f', '--file', required=True, help="Name of the notebook file.")
    parser.add_argument('-i', '--input_path', required=True, help="S3 location of the output path.")

    args = parser.parse_args()
    notebook_name = args.file
    notebook_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), notebook_name)

    download_files(args.input_path)
    run_notebook(notebook_path)


def run_notebook(notebook_path):
    assert os.path.isfile(notebook_path)

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    logging.info("Running: {}".format(notebook_path))
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': 'notebooks/'}})

    exec_name = os.path.join(
        os.path.dirname(notebook_path),
        '_'.join(['executed', os.path.basename(notebook_path)])
    )

    logging.info("Saving results to: {}".format(exec_name))

    with open(exec_name, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
