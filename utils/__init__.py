""" Some utility functions to interact with and download things from depot """

import os
import requests
import urllib.parse
from .environment import get_env
from .models.xray_instance import XRayInstance
from .models.ct_instance import CTInstance
from .models.patient import Patient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# The depot database username/password/access url are all set as environment variables
DEPOT_USERNAME = get_env('DEPOT_USERNAME')
DEPOT_PASSWORD = urllib.parse.quote_plus(get_env('DEPOT_PASSWORD'))
DEPOT_DATABASE = get_env('DEPOT_DATABASE')
DEPOT_API = get_env('DEPOT_API', default='https://depotapi.tbportals.niaidprod.net')
DEPOT_BULK_PRESIGNED_ENDPOINT = urllib.parse.urljoin(DEPOT_API, '/api/Amazon/GetBulkPresignedUrls')

depot_engine = create_engine(f"postgresql://{DEPOT_USERNAME}:{DEPOT_PASSWORD}@{DEPOT_DATABASE}")
depot_session_maker = sessionmaker(bind=depot_engine)
depot_session = depot_session_maker()


def download_depot_objects(object_list: list, destination_list: list, verbose: bool=False):
    """
    Download the DEPOT objects indicated in `object_list`.

    :param object_list: A list of dictionaries, each with the following format:

    {
        "directory": <The directory of the object in the DEPOT s3 bucket>,
        "objectKey": <The filename of the object in the DEPOT s3 bucket>
    }

    :param destination_list: A list of paths, the same length as object_list indicating
    where to save each object in object_list locally
    :param verbose: Verbose mode
    """
    for (index, (destination, obj, presigned_url)) in enumerate(zip(destination_list, object_list, 
            requests.post(DEPOT_BULK_PRESIGNED_ENDPOINT, json=object_list).json())):
        out_path = os.path.abspath(destination)
        with open(out_path, 'wb') as outf:
            if verbose:
                print(f"Writing instance number {index} to file at {out_path}")
            outf.write(requests.get(presigned_url).content)


def download_ct_series(study_uid: str, series_uid: str, destination: str, verbose: bool=False):
    """
    Download the ct series referenced by study_uid and series_uid, put it in destination.

    :param study_uid: The CT series study_uid (uid in DEPOT)
    :param series_uid: The CT series series_uid (series_uid in DEPOT)
    :param destination: The path where the series should be saved
    :param verbose: Verbose mode
    """
    object_list = []
    destination_list = []
    
    destination_path = os.path.join(os.path.abspath(destination), study_uid, series_uid)
    os.makedirs(destination_path, exist_ok=True)

    for ct_instance in depot_session.query(CTInstance).filter(CTInstance.uid==study_uid, CTInstance.series_uid==series_uid):
        directory, objectKey = os.path.split(ct_instance.series_instance_content_url)
        object_list.append({"directory": directory, "objectKey": objectKey})
        destination_list.append(os.path.join(destination_path, objectKey))

    download_depot_objects(object_list=object_list, destination_list=destination_list, verbose=verbose)


def download_all_ct_for_patient_with_patient_id(patient_id: str, destination: str, verbose: bool=False):
    """
    Download all CT series for patient with `patient_id`, put them in directories in `destination` path.

    :param patient_id: The Patient's patient_id
    :param destination: The path where the patient's CT scans should be saved
    :param verbose: Verbose mode
    """
    destination_path = os.path.join(os.path.abspath(destination), patient_id)
    os.makedirs(destination_path, exist_ok=True)

    for ct_instance in depot_session.query(CTInstance).filter(CTInstance.patient_id==patient_id).distinct(CTInstance.series_uid):
        if verbose:
            print("*"*60)
            print(f"Downloading study {ct_instance.uid}, series {ct_instance.series_uid} . . .")
            print("*"*60)
        download_ct_series(study_uid=ct_instance.uid, series_uid=ct_instance.series_uid, 
                            destination=destination_path, verbose=verbose)


def download_all_ct_for_patient_with_identifier(identifier: str, destination: str, verbose: bool=False):
    """
    Download all CT series for patient with `identifier`, put them in directories in `destination` path.

    :param identifier: The Patient's identifier
    :param destination: The path where the patient's CT scans should be saved
    :param verbose: Verbose mode
    """
    destination_path = os.path.join(os.path.abspath(destination), identifier)
    os.makedirs(destination_path, exist_ok=True)

    patient_id = list(depot_session.query(Patient).filter(Patient.identifier==identifier))[0].patient_id

    for ct_instance in depot_session.query(CTInstance).filter(CTInstance.patient_id==patient_id).distinct(CTInstance.series_uid):
        if verbose:
            print("*"*60)
            print(f"Downloading study {ct_instance.uid}, series {ct_instance.series_uid} . . .")
            print("*"*60)
        download_ct_series(study_uid=ct_instance.uid, series_uid=ct_instance.series_uid, 
                            destination=destination_path, verbose=verbose)


def download_all_ct_for_study_uid(study_uid: str, destination: str, verbose: bool=False):
    """
    Download all CT series for study with `study_uid`, put them in directories in `destination` path.

    :param study_uid: The CT study_uid (DEPOT uid)
    :param destination: The path where the patient's CT scans should be saved
    :param verbose: Verbose mode
    """
    study_series_uids = [(study_uid, ct_instance.series_uid) for ct_instance in
        depot_session.query(CTInstance).filter(CTInstance.uid==study_uid).distinct(CTInstance.series_uid)]

    for study_id, series_id in study_series_uids:
        if verbose:
            print("*"*60)
            print(f"Downloading study {study_id}, series {series_id} . . .")
            print("*"*60)
        download_ct_series(study_uid=study_id, series_uid=series_id, 
                            destination=destination, verbose=verbose)
