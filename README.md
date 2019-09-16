Project code is derived from https://github.com/awslabs/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own/container/decision_trees

Model is a TensorFlow model in our S3 buckets

Endpoint is set up without Elastic Inference on a ml.m4.xlarge instance

Invoking the endpoint in a manner that somewhat simulates multiple hits from Lambda (Now with new sessions per worker when invoking):

```
import boto3
import json
import requests
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

sm = boto3.client('sagemaker-runtime', aws_access_key_id='', aws_secret_access_key='', region_name='eu-west-2')

paths = []

s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='', region_name='eu-west-2')

response = s3.list_objects_v2(
    Bucket='our-chips-bucket',
    MaxKeys=2000,
    Prefix='S2A_MSIL2A_20190112T161631_N0211_R140_T99ZZZ_20190112T201503/chip_'
)['Contents']

[paths.append(path['Key']) for path in response]

def invoke_endpoint(thing):
    session = boto3.session.Session()
    sm = session.client('sagemaker-runtime', aws_access_key_id='', aws_secret_access_key='', region_name='eu-west-2')
    sm.invoke_endpoint(
        EndpointName='aws-debug',
        ContentType='application/json',
        Body=json.dumps({"chip_paths":paths}))


# Does actual invocations
with PoolExecutor(max_workers=4) as executor:
    for _ in executor.map(invoke_endpoint, range(1, 100)):
        pass
```

This results in logs such as:

```
10.32.0.2 - - [16/Sep/2019:13:16:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:17:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:17:09 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:17:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:17:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 1:22
8/20 [===========>..................] - ETA: 1:22
8/20 [===========>..................] - ETA: 1:25
8/20 [===========>..................] - ETA: 1:2510.32.0.2 - - [16/Sep/2019:13:18:20 +0000] "POST /invocations HTTP/1.1" 499 0 "-" "AHC/2.0"
2019/09/16 13:18:20 [error] 18#18: *53 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
2019/09/16 13:18:20 [error] 18#18: *55 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:18:20 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:20 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/16 13:18:20 [error] 18#18: *57 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:18:20 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
[2019-09-16 13:18:22 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:24)
[2019-09-16 13:18:22 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:21)
[2019-09-16 13:18:23 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:22)
[2019-09-16 13:18:23 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:23)
[2019-09-16 13:18:24 +0000] [193] [INFO] Booting worker with pid: 193
[2019-09-16 13:18:24 +0000] [194] [INFO] Booting worker with pid: 194
2019/09/16 13:18:24 [error] 18#18: *59 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "GET /ping HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/ping", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:18:24 +0000] "GET /ping HTTP/1.1" 504 192 "-" "AHC/2.0"
[2019-09-16 13:18:24 +0000] [196] [INFO] Booting worker with pid: 196
[2019-09-16 13:18:24 +0000] [197] [INFO] Booting worker with pid: 197
Using TensorFlow backend.
Using TensorFlow backend.
Using TensorFlow backend.
Using TensorFlow backend.
2019-09-16 13:18:28.439024: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019/09/16 13:18:29 [error] 18#18: *61 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "GET /ping HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/ping", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:18:29 +0000] "GET /ping HTTP/1.1" 504 192 "-" "AHC/2.0"
2019-09-16 13:18:30.033489: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019/09/16 13:18:34 [error] 18#18: *63 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "GET /ping HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/ping", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:18:34 +0000] "GET /ping HTTP/1.1" 504 192 "-" "AHC/2.0"
2019-09-16 13:18:35.440129: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:44 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:49 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:18:54 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 23s10.32.0.2 - - [16/Sep/2019:13:18:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019-09-16 13:19:10.690635: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
16/20 [=======================>......] - ETA: 7s 10.32.0.2 - - [16/Sep/2019:13:19:12 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 39s 2s/step
10.32.0.2 - - [16/Sep/2019:13:19:19 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/16 13:19:21 [error] 18#18: *85 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:19:21 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/16 13:19:21 [error] 18#18: *87 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:19:21 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/16 13:19:21 [error] 18#18: *89 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:19:21 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:24 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:29 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:34 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
[2019-09-16 13:19:40 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:194)
[2019-09-16 13:19:41 +0000] [365] [INFO] Booting worker with pid: 365
10.32.0.2 - - [16/Sep/2019:13:19:44 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
Using TensorFlow backend.
10.32.0.2 - - [16/Sep/2019:13:19:49 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019-09-16 13:19:57.152926: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
8/20 [===========>..................] - ETA: 51s10.32.0.2 - - [16/Sep/2019:13:19:57 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:19:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 51s10.32.0.2 - - [16/Sep/2019:13:20:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:20:09 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:20:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:20:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/16 13:20:19 [error] 18#18: *83 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:20:19 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
[2019-09-16 13:20:20 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:197)
[2019-09-16 13:20:22 +0000] [404] [INFO] Booting worker with pid: 404
2019/09/16 13:20:22 [error] 18#18: *89 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:20:22 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/16 13:20:23 [error] 18#18: *87 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:20:23 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/16 13:20:23 [error] 18#18: *85 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [16/Sep/2019:13:20:23 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
10.32.0.2 - - [16/Sep/2019:13:20:24 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
[2019-09-16 13:20:27 +0000] [17] [CRITICAL] WORKER TIMEOUT (pid:193)
Using TensorFlow backend.
[2019-09-16 13:20:28 +0000] [417] [INFO] Booting worker with pid: 417
2019-09-16 13:20:32.229222: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
Using TensorFlow backend.

```

This time out behaviour was not observed when predictions aren't actually performed (e.g) Line `59` in `predictor.py` is commented out
