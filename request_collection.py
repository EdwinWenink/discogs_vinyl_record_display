"""
Query the Discogs API for a user's collection
N.B. without authentication cover_image is empty.
"""

import sys
import requests
import json
import logging
from dataclasses import dataclass
# from pydantic.dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


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


def get_collection_records(user_name: str, user_agent: str, pat_token: str | None) -> List[Record]:
    '''
    Get collection of records. The term 'collection' in the discogs API refers to metadata only.
    With 'collection' I refer to the *releases* in a collection i.e. the actual records.

    Args:
        username: Discogs user name whose collection you are requesting

    Returns:
        a list of records.
    '''
    logger.info("Retrieving collection of Discogs user %s", user_name)

    base_url = "https://api.discogs.com"
    url = f"{base_url}/users/{user_name}/collection/folders/0/releases"
    logger.info("Endpoint: %s", url)

    headers: dict = {
        'User-Agent': user_agent,
    }

    # A collection can be requested without authentication, but the response
    # will not include image URIs.
    if pat_token:
        headers["Authorization"] = f"Discogs token={pat_token}"

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
        logger.info("Request succeeded.")
    else:
        logger.error("Request failed with status code %s", response.status_code)
        sys.exit()

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
