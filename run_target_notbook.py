import logging
import os
from argparse import ArgumentParser

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def main():
    parser = ArgumentParser(description="Run a Jupyter Notebook")
    parser.add_argument('-f', '--file', required=True, help="Name of the notebook file.")
    args = parser.parse_args()
    notebook_name = args.file
    final_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), notebook_name)
    run_notebook(final_path)


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
