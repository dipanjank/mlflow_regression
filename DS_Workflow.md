General Overview
----------------

- Every model is created by a jupyter notebook.
- Every notebook looks up input data (in csv or msgpack format) locally.
- The parent repository for the notebook is an MLFlow project.
- The repository also contains utilities to load the raw data from remote storage (S3), run the notebook 
    and publish the artifacts to remote storage (S3) using the MLFlow tracking server.
- The norebooks use MLFlow tracking to store additional info about the data and models 
    (number of rows, number of CV folds, best hyperparameter values and so on).
- Administration of which models are live at which stage is done using the MLFlow tracking server UI. 

Model Development
-----------------
- Create a notebook.
- Load data.
- Experiment until happy.
- Check in the notebook.
- Update said MLProject file with an entry specific to your model.
- Push to Github.
- CircleCI creates a docker image containing the latest snapshot of the repository and pushes to ECR.

Artifact Publishing
-------------------

Launch an on-demand Fargate task to execute "mlflow run <model_wrapper.py> -e <my_new_model>".


Re-build Existing Model with Updated Data
-----------------------------------------

Launch previous task on a time based or event based trigger.

Serving
-------

- Build a Fargate based Service that takes input from HTTP service and then uses the MLFlow API to load and use the currently active model.

Model Activation and Quality Control
------------------------------------

- Run the mlflow ui (possibly also as a Fargate Service).
- Use the Front-end to activate models and inspect model metadata.

Support for Customer Managed models
-----------------------------------
- First option is: "Give us an API".
- Otherwise, Customer needs to package the model in MLFlow format.
- And then create a docker image (MLFlow has shortcuts for this).
- We will need to create one Fargate service per customer image.
- Re-building the model will work the same way.
