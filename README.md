# Getting Started

1. Create virtual env
`python3 -m venv .venv`

2. Activate virtual env
`. .venv/bin/activate`

3. Install requirements
`pip install -r requirements.txt`


# TODO

- improve style and function of clothing item upload
- add image upload to s3
- set up hosting
- Make a better confirm delete modal
- Turn location updater into toggle
- move javascript to alpine?
- add image zoomer
- 

Current issue is with AWS permissions. 
Need to check that the same credentials are being used to create the signed url and are available for writing to the bucket
Maybe create IAM role for this application which can own the bucket and create signed urls for uploading to it
Then create credentials from that role and provide them to the flask app