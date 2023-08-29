'''
Request the record collection of a Discogs user and write the results
to a folder with a markdown file for each record.

N.B. you need to provide a PAT token to retrieve image URLs.
'''

import os
import argparse
import logging
import logging.config
from dotenv import load_dotenv

import yaml

from src.request_collection import get_collection_records
from src.store_collection import collection_to_markdown


logger = logging.getLogger(__name__)

# Get logging config
with open('logging.yaml') as yf:
    logging_config = yaml.load(yf, Loader=yaml.SafeLoader)

logging.config.dictConfig(logging_config)

# Specify unique identifier for your application in .env file
# N.B. we authorize as our own user with a Personal Access Token (PAT)
# So we do not need the whole OAuth flow.
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT")
PAT_TOKEN = os.getenv("PAT_TOKEN")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--user_name', type=str,
                        help="Discogs user name.")
    parser.add_argument(
        '--output_folder', type=str, nargs='?',
        const='collection', default='collection',
        help="Name of output folder for the collection records. Default is 'collection'.")
    args = parser.parse_args()

    records = get_collection_records(args.user_name, USER_AGENT, PAT_TOKEN)

    collection_to_markdown(records, args.output_folder)
