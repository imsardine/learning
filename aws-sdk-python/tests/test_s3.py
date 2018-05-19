from StringIO import StringIO
import boto3

def test_upload_file(s3_bucket, testdata, tmpdir):
    data = testdata.read('data/hello.txt')
    s3_bucket.put_object(Key='hello.txt', Body=data)

    assert [o.key for o in s3_bucket.objects.all()] == ['hello.txt']

    fobj = StringIO()
    s3_bucket.download_fileobj('hello.txt', fobj)

    assert fobj.getvalue() == 'Hello, World!'

def test_upload_directory(s3_bucket, testdata):
    pass

