
The idea is that you've got a bunch of files each with a list of albums/films/books in it. And you want to download all the album/poster/cover art.

## Set-up

* For albums, add files called `albums_X.txt` to the `lists/` directory that contain a list of albums like this:

    ```
    Parts & Labor's "Receivers"
    Ty Segall's "Twins" (2012)
    The Blues Collection Vol. 5: Bo Diddley's "Jungle Music" (1993)
    Kanye West's "Yeezus" (2013)
    Julian Lynch's "Lines" (2013)
    ```

* Add books in the same format, but to a file called `books_X.txt`.

* Add films as a list of titles only.

## Usage

(Note: use with python3)

By default, we download music albums. Use the `--type` option to toggle between `film`, `album`, or `book`.

__Download albums from all files in `lists/` directory__:

`python cover_art.py -i lists/ -o . --all --type album`

__Download albums from a single file__:

`python cover_art.py -i lists/albums_2007.txt -o 2007/ --type album`

__List albums with missing cover art__:

`python cover_art.py -i lists/ -o . --all -c --type album`

__Print info only (no images)__:

`python cover_art.py -i lists/albums_2007.txt --type album --get_info`

This won't work perfectly, but it's a start!

## Requirements

Python3.

For films, we need IMDBpy. For books, we need the Goodreads API with the associated developer keys. For albums, we need the [Discogs API](https://www.discogs.com/settings/developers) and developer keys.

Save all developer keys as environment variables for your consumer key and consumer secret keys. For example, you can create a local file called `.env` with the following:

    ```
    export DISCOGS_CONSUMER_KEY=asdfasdfasdf
    export DISCOGS_CONSUMER_SECRET=asdfasdfasdfsadfasdfasdf
    export GOODREADS_KEY=asdfasdfasdf
    export GOODREADS_SECRET=asdfasdfasdfsadfasdfasdf
    ```

(Remember to run `source .env` to load these variables prior to running `cover_art.py`.)
