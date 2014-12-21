import time
import os
import argparse
import webbrowser
import unidecode
import discogs_client

DISCOGS_CONSUMER_KEY = os.environ['DISCOGS_CONSUMER_KEY']
DISCOGS_CONSUMER_SECRET = os.environ['DISCOGS_CONSUMER_SECRET']

def save_image(im_url, d, outfile):
    headers = {
        'Accept-Encoding': 'gzip',
        'User-Agent': d.user_agent,
    }
    content, status_code = d._fetcher.fetch(d, 'GET', im_url, data=None, headers=headers)
    if 200 <= status_code < 300:
        with open(outfile, 'w') as f:
            f.write(content)

def clean_query(query):
    """
    example
        input: Philip Glass's "Solo Piano" (1989)
        output: Philip Glass - Solo Piano
    """
    query = query.strip()
    query = query.translate(None, '*~#?!') # remove legend symbols
    query = query.replace("[]", "") # leftover from removing legend symbols
    query = query.replace("'s ", " - ")
    query = query.replace('"', "") # remove quotes
    artist = query.split("[self-titled]")[0].replace(' - ', '').strip()
    query = query.replace("[self-titled]", artist)
    year_str = query[-6:]
    if year_str.startswith('(') and year_str.endswith(')'):
        query = query[:-6]
    query = query.strip()
    return query, query.replace('.', '_').replace('/', '_')

def get_im_url(d, query):
    res = d.search(query, type='title')
    for i in xrange(res.count):
        r = res[i]
        if r.__class__.__name__ in ['Release', 'Master']:
            if hasattr(r, 'images') and r.images:
                return r.images[0]['uri']
            if hasattr(r, 'master'):
                if hasattr(r.master, 'images') and r.master.images:
                    return r.master.images[0]['uri']
            if hasattr(r, 'thumb'):
                return r.thumb
    return None

def already_exists(query, outdir):
    return any([os.path.splitext(x)[0] == query for x in os.listdir(outdir)])

def download_album_cover(d, query, outname, outdir):
    im_url = get_im_url(d, query)
    if im_url is None:
        print query
        print '    NOT FOUND'
        return
    ext = os.path.splitext(im_url)[1]
    # ext = '.png'
    outfile = os.path.join(outdir, outname + ext)
    save_image(im_url, d, outfile)
    print query
    print '    Saved {0}'.format(outfile)

def auth(verifier=None):
    d = discogs_client.Client('ExampleApplication/0.1')
    d.set_consumer_key(DISCOGS_CONSUMER_KEY, DISCOGS_CONSUMER_SECRET)
    request_token, request_secret, url = d.get_authorize_url()
    if not verifier:
        print url
        if raw_input('Go to this url? ').strip().lower() != 'n':
            webbrowser.open_new_tab(url)
        else:
            return None
        verifier = raw_input('Gimme that verifier: ').strip()
    access_token, access_secret = d.get_access_token(verifier)
    me = d.identity()
    return d

def parse(content):
    lines = []
    for line in content.split('\n'):
        if line.startswith('    '): # skip comments on albums
            continue
        line = line.strip()
        if not line.startswith('#') and len(line) > 6: # skip headers
            lines.append(line)
    return lines

def load(infile):
    with open(infile) as f:
        out = unidecode.unidecode(f.read())
        return out.split('-----')[0] # keep everything before -----

def main(infile, outdir, d):
    lines = parse(load(infile))
    for line in lines:
        query, outname = clean_query(line)
        if already_exists(outname, outdir):
            pass
        elif d is None:
            print outname
        else:
            try:
                download_album_cover(d, query, outname, outdir)
            except Exception, e:
                print query
                print e.__str__()
                print '    BUG'
                time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='infile')
    parser.add_argument('-o', type=str, required=True, help='out dir')
    parser.add_argument('-c', action='store_true', default=False, help='check exist')
    parser.add_argument('--all', action='store_true', default=False, help='download all')
    args = parser.parse_args()
    d = auth() if not args.c else None
    if args.all:
        ys = range(2007, 2015)
        xs = ['albums_{0}.txt'.format(y) for y in ys]
        for i, o in zip(xs, ys):
            infile = os.path.abspath(i)
            outdir = os.path.abspath(str(o))
            print infile, outdir
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            main(infile, outdir, d)
    else:
        main(os.path.abspath(args.i), os.path.abspath(args.o), d)
