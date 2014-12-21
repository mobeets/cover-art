## Requirements

* Create a Discogs API application [here](https://www.discogs.com/settings/developers).
* Create environment variables for your consumer key and consumer secret keys. For example:

    ```
    $ export DISCOGS_CONSUMER_KEY=asdfasdfasdf
    $ export DISCOGS_CONSUMER_SECRET=asdfasdfasdfsadfasdfasdf
    ```

* Add files called `albums_X.txt` to the `lists/` directory that contain a list of albums like this:

    ```
    Parts & Labor's "Receivers"
    Ty Segall's "Twins" (2012)
    The Blues Collection Vol. 5: Bo Diddley's "Jungle Music" (1993)
    Kanye West's "Yeezus" (2013)
    Julian Lynch's "Lines" (2013
    ```

(The `X` in `albums_X.txt` will send downloaded cover art to a directory called `X`.)

## Usage

The idea is that you've got a bunch of files each with a list of albums in it. And now you want all the album art.

__Download albums from all files in `lists/` directory__:

`python download_album_covers.py -i lists/ -o . --all`

__Download albums from a single file__:

`python download_album_covers.py -i lists/albums_2007.txt -o 2007/`

__List albums with missing cover art__:

`python download_album_covers.py -i lists/ -o . --all -c`

This won't work perfectly, but it's a start!
