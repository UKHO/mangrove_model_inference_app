Project code is derived from https://github.com/awslabs/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own/container/decision_trees

Model is a TensorFlow model in our S3 buckets

Endpoint is set up without Elastic Inference on a ml.m4.xlarge instance

Invoking the endpoint in a manner that somewhat simulates multiple hits from Lambda:

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
10.32.0.2 - - [03/Sep/2019:12:41:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:41:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:41:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/21 [==========>...................] - ETA: 1:27
2019/09/03 12:42:13 [error] 16#16: *160 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
8/21 [==========>...................] - ETA: 1:3310.32.0.2 - - [03/Sep/2019:12:42:13 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/03 12:42:13 [error] 16#16: *239 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:42:13 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/03 12:42:13 [error] 16#16: *241 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:42:13 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/03 12:42:13 [error] 16#16: *243 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:42:13 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
8/21 [==========>...................] - ETA: 1:35
[2019-09-03 12:42:14 +0000] [15] [CRITICAL] WORKER TIMEOUT (pid:24)
[2019-09-03 12:42:14 +0000] [15] [CRITICAL] WORKER TIMEOUT (pid:19)
[2019-09-03 12:42:14 +0000] [15] [CRITICAL] WORKER TIMEOUT (pid:20)
[2019-09-03 12:42:14 +0000] [15] [CRITICAL] WORKER TIMEOUT (pid:23)
2019/09/03 12:42:15 [error] 16#16: *245 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "GET /ping HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/ping", host: "model.aws.local:8080"
8/21 [==========>...................] - ETA: 1:3610.32.0.2 - - [03/Sep/2019:12:42:15 +0000] "GET /ping HTTP/1.1" 504 192 "-" "AHC/2.0"
[2019-09-03 12:42:16 +0000] [191] [INFO] Booting worker with pid: 191
[2019-09-03 12:42:16 +0000] [193] [INFO] Booting worker with pid: 193
[2019-09-03 12:42:16 +0000] [195] [INFO] Booting worker with pid: 195
[2019-09-03 12:42:16 +0000] [197] [INFO] Booting worker with pid: 197
Using TensorFlow backend.
Using TensorFlow backend.
Using TensorFlow backend.
Using TensorFlow backend.
2019-09-03 12:42:20.156207: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019/09/03 12:42:20 [error] 16#16: *247 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "GET /ping HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/ping", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:42:20 +0000] "GET /ping HTTP/1.1" 504 192 "-" "AHC/2.0"
2019-09-03 12:42:21.491548: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019/09/03 12:42:25 [error] 16#16: *249 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "GET /ping HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/ping", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:42:25 +0000] "GET /ping HTTP/1.1" 504 192 "-" "AHC/2.0"
2019-09-03 12:42:26.856832: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:27 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:28 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:29 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019-09-03 12:42:32.223731: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [03/Sep/2019:12:42:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/21 [==========>...................] - ETA: 30s10.32.0.2 - - [03/Sep/2019:12:42:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:42:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:43:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/21 [=====================>........] - ETA: 10s10.32.0.2 - - [03/Sep/2019:12:43:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:43:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
21/21 [==============================] - 42s 2s/step
10.32.0.2 - - [03/Sep/2019:12:43:11 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
2019/09/03 12:43:14 [error] 16#16: *241 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:43:14 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/03 12:43:14 [error] 16#16: *239 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [03/Sep/2019:12:43:14 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:43:14 +0000] "POST /invocations HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [03/Sep/2019:12:43:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/21 [==========>...................] - ETA: 1:15
```

This time out behaviour was not observed when predictions aren't actually performed (e.g) Line `59` in `predictor.py` is commented out
