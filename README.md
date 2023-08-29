# Discogs Vinyl Record Display

This project queries the Discogs API to retrieve a user's record collection and then stores the information in a folder with Markdown files.
A separate Markdown file will be created for each record.
The record's data is stored in a YAML header.

I wanted to do this so that I can create a digital record display on my website, which uses Markdown for its content.

As a demo you can see [my vinyl record display](https://www.edwinwenink.xyz/records/).


## Set environment variables

Create an `.env` file in the project root and create the following variables (replace with your own values):

```
USER_AGENT="yourappname/1.0"  # required
PAT_TOKEN='1324098b09q8123'  # optional
```

Note: if you want to include URLs to images, such as the album thumbnail and album cover, you need to create and set a personal access token (PAT) for Discogs.

The PAT is optional and can be omitted.
The `USER_AGENT` is a required parameter though.

## Install requirements

`pip install -r requirements.txt`

I've used the `|` operator in type hints, so use Python > 3.10.

## Interactive usage

You need to specify a valid Discogs user name, as such:

```
python main.py --user_name=EJWenink
```

By default the results are written to a folder called `collection`.
You can override this default.

See `python main.py --help` for the options.

## Tips for deployment

Discogs will throttle if you make many requests in a short time, which will prevent some records from displaying if you load them all from a single page like I do.
To avoid this, allow caching of request results via a content delivery system (CDS).
In my case, I modified all calls to `https://i.discogs.com` (which you will find in the output markdown files) to `/discogs` on my own domain, and set up a proxy so that `/discogs/*` redirects to `https://i.discogs.com`.
This allows my hosting provider to cache the responses.
