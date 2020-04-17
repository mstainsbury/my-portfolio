import boto3
import StringIO
import zipfile
import mimetypes

# from botocore.client import Config

s3 = boto3.resource('s3')
# s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
portfolio_bucket = s3.Bucket('portfolio.longjing3.co.uk')

portfolio_bucket.download_file('index.html','D:\Dev5\index.html')
build_bucket = s3.Bucket('portfoliobuild.longjing3.co.uk')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
