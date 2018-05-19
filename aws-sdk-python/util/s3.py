from os import path

def upload_dir(root, bucket, s3path=None):
    for (cur_dirpath, dirnames, filenames) in os.walk(dirpath):
        for fn in filenames:
            filepath = path.join(dirpath, fn)
            key = path.relpath(filepath, dirpath)
            bucket.upload_file(filepath, 



