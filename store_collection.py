"""
This module takes a record collection and writes them
to a local `collection` folder. Each record will have its
own Markdown file with the data as a YAML header
"""

import os
import re
import logging
from typing import List
from request_collection import Record
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


def extract_info(record: Record) -> dict:
    '''
    Takes a record and returns a dictionary
    with the info we wish to write out to file.
    '''
    info = {
        'title': record.title,
        'artists': get_record_artists(record),
        'year': 'Unknown' if record.year == 0 else record.year,
        'format': get_record_formats(record),
        'genres': record.genres,
        'styles': record.styles,
        'labels': get_record_labels(record),
        'thumbnail': record.thumb,
        'cover': record.cover_image,
    }
    return info


def get_record_artists(record: Record) -> List[str]:
    return [artist['name'] for artist in record.artists]


def get_record_labels(record: Record) -> List[str]:
    return [label['name'] for label in record.labels]


def get_record_formats(record: Record) -> List[str]:
    return [format['name'] for format in record.formats]


def get_all_artists_in_collection(records: List[Record]):
    return set([artist['name'] for record in records
                for artist in record.artists])


def slugify(input: str):
    '''
    Sanitize a string for usage as a filename.
    Add the file extension afterwards, else the `.` is stripped.
    '''
    val = re.sub(r'[^\w\s-]', '', input.lower())
    val = re.sub(r'[-\s]+', '-', val)
    return val


def collection_to_markdown(collection: List[Record], out_folder='collection'):
    '''
    Write the record collection to a folder where each record gets its
    own Markdown file. Record information is written out as a YAML header.
    '''
    collection_folder = Path(out_folder)
    os.makedirs(collection_folder, exist_ok=True)
    logger.info("Storing collection records under '%s'", out_folder)

    for record in collection:
        info = extract_info(record)
        extension = '.md'
        filename = slugify(f"{record.year}-{record.title}") + extension
        yaml_metadata = yaml.dump(info)
        yaml_header = '---\n' + yaml_metadata + '---\n'
        with open(collection_folder / filename, mode='w', encoding='utf-8') as fhandle:
            fhandle.write(yaml_header)
    logger.info("Done writing records.")
