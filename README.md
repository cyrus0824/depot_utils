# Utility functions for accessing some DEPOT objects

This repository contains functions to retrieve objects (CXR, CT scans) from DEPOT by querying the DEPOT postgres database,
and downloading objects from the DEPOT s3 bucket using the DEPOT Presigned URL API.

Currently, the database access is managed by SQLAlchemy, and thus relies on database models for the tables/views that are
accessed.  These database models are housed in [utils/models](https://github.com/cyrus0824/depot_utils/tree/main/utils/models).

## Installing requirements

The utilities depend on the [SQLAlchemy](https://docs.sqlalchemy.org/en/14/), and 
[requests](https://docs.python-requests.org/en/master/) libraries.  To install them run:

```
pip install -r requirements.txt
```

in the root of the repository.

## Setting environment variables

Several environment variables need to be set in the environment where the script will be executed:

- The DEPOT database username (```DEPOT_USERNAME```)
- The DEPOT database password (```DEPOT_PASSWORD```)
- The DEPOT database URL (```DEPOT_DATABASE```)
- The DEPOT API URL (```DEPOT_API```) - This will default to the production API URL if not specified.

## Using the utility

When the requirements are installed and the appropriate environment variables are set, you can use the utilities.
They are located in [utils](https://github.com/cyrus0824/depot_utils/blob/main/utils/__init__.py).

The code below shows some examples usage.

### Getting all CTs from a DEPOT patient identifier

```Jupyter Notebook:
In [1]: from utils import download_all_ct_for_patient_with_identifier

In [2]: download_all_ct_for_patient_with_identifier(identifier='304', destination='/Users/afrasiabic2')
```

### Getting all CTs from a DEPOT patient_id

```Jupyter Notebook:
In [1]: from utils import download_all_ct_for_patient_with_patient_id

In [2]: download_all_ct_for_patient_with_patient_id(patient_id='16fcee10-6296-413d-939c-d3b612ca4ed6', destination='/Users/afrasiabic2')
```

### Getting all CTs from a study UID

```Jupyter Notebook:
In [1]: from utils import download_all_ct_for_study_uid

In [2]: download_all_ct_for_study_uid(study_uid='1.2.156.14702.1.1001.17.0.20201013130611209', destination='/Users/afrasiabic2')
```
