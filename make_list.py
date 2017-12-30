import sys

def parse_line(line):
	ps = line.split("'s")
	artist = ps[0].strip()
	album = ps[1].strip()
	album, year = album.split(' (')
	year = year.replace(')', '').strip()
	album = album.strip()
	return artist, album, year

def print_line(pos, artist, album, year):
	out = ['-']
	out.append('    pos: {}'.format(pos))
	out.append('    artist: {}'.format(artist))
	out.append('    album: {}'.format(album))
	out.append('    year: {}'.format(year))
	return '\n'.join(out)

def main(infile):
	with open(infile) as f:
		lines = f.readlines()
	for i, line in enumerate(lines):
		artist, album, year = parse_line(line)
		print print_line(i+1, artist, album, year)

if __name__ == '__main__':
	main(sys.argv[1])
