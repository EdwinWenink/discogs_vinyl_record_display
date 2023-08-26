"""
Query the Discogs API for a user's collection

N.B. without authentication cover_image is empty.
"""
import os
import requests
import json
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
# from pydantic.dataclasses import dataclass

load_dotenv()

# Specify unique identifier for your application in .env file
# N.B. we authorize as our own user with a Personal Access Token (PAT)
# So we do not need the whole OAuth flow.
USER_AGENT = os.getenv("USER_AGENT")
PAT_TOKEN = os.getenv("PAT_TOKEN")


@dataclass
class Record():
    id: int
    master_id: int
    master_url: str
    resource_url: str
    thumb: str
    cover_image: str
    title: str
    year: int
    formats: list
    artists: list
    labels: list
    genres: list
    styles: list
    # notes: list


def get_collection_records(username: str = "EJWenink") -> List[Record]:
    '''
    Get collection of records. The term 'collection' in the discogs API refers to metadata only.
    With 'collection' I refer to the *releases* in a collection i.e. the actual records.

    Args:
        username: Discogs user name whose collection you are requesting

    Returns:
        a list of records.
    '''
    base_url = "https://api.discogs.com"
    url = f"{base_url}/users/{username}/collection/folders/0/releases"

    headers: dict = {
        'User-Agent': USER_AGENT,
        "Authorization": f"Discogs token={PAT_TOKEN}"
    }

    # TODO up page automatically
    params = {
        "page": 1,
        "per_page": 100,
        "sort": "artist",
        "sort_order": "asc"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Data:", data)
    else:
        print("Request failed with status code:", response.status_code)

    # TODO while page != n_pages, submit GET for following page
    releases = data['releases']
    records = [Record(**release['basic_information']) for release in releases]

    return records


def get_example_response_json():
    '''
    This convenience function loads an example response
    showing
    '''
    with open('example_response.json', mode='r') as fhandle:
        response = json.load(fhandle)
    return response
