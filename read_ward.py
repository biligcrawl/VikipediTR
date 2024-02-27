from warcio.archiveiterator import ArchiveIterator


def read_warc_file(path):
    with open(path, 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                print(record.rec_headers.get_header('WARC-Target-URI'))
                print(record.rec_headers.get_header('WARC-Date'))
                content = record.content_stream().read()
                print(content[:5000])


warc_path = 'wikipedia_pages.warc'
read_warc_file(warc_path)
