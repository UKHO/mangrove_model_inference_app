Project code is derived from https://github.com/awslabs/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own/container/decision_trees

Model is a TensorFlow model in our S3 buckets

Endpoint is set up without Elastic Inference on a ml.m4.xlarge instance

Invoking the endpoint in a manner that somewhat simulates multiple hits from Lambda (Now with new sessions per worker when invoking,
 and with 4 instances):

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

Instance 1
```
10.32.0.2 - - [17/Sep/2019:10:15:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 21s10.32.0.2 - - [17/Sep/2019:10:15:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 7s 10.32.0.2 - - [17/Sep/2019:10:16:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 36s 2s/step
10.32.0.2 - - [17/Sep/2019:10:16:15 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 22s10.32.0.2 - - [17/Sep/2019:10:18:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 7s 10.32.0.2 - - [17/Sep/2019:10:18:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 36s 2s/step
10.32.0.2 - - [17/Sep/2019:10:18:38 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:21:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:21:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:21:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:21:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:21:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"

```

Instance 2
```
10.32.0.2 - - [17/Sep/2019:10:15:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 42s10.32.0.2 - - [17/Sep/2019:10:15:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 43s10.32.0.2 - - [17/Sep/2019:10:15:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/17 10:15:59 [error] 15#15: *110 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [17/Sep/2019:10:15:59 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/17 10:15:59 [error] 15#15: *210 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [17/Sep/2019:10:15:59 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
[2019-09-17 10:16:01 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:18)
[2019-09-17 10:16:01 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:20)
[2019-09-17 10:16:02 +0000] [185] [INFO] Booting worker with pid: 185
[2019-09-17 10:16:03 +0000] [186] [INFO] Booting worker with pid: 186
10.32.0.2 - - [17/Sep/2019:10:16:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
Using TensorFlow backend.
Using TensorFlow backend.
10.32.0.2 - - [17/Sep/2019:10:16:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019-09-17 10:16:16.343128: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
8/20 [===========>..................] - ETA: 46s10.32.0.2 - - [17/Sep/2019:10:16:18 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019-09-17 10:16:26.758620: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
16/20 [=======================>......] - ETA: 11s10.32.0.2 - - [17/Sep/2019:10:16:28 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 57s 3s/step
10.32.0.2 - - [17/Sep/2019:10:16:36 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 21s10.32.0.2 - - [17/Sep/2019:10:16:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 8s 10.32.0.2 - - [17/Sep/2019:10:17:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 51s 3s/step
10.32.0.2 - - [17/Sep/2019:10:17:29 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 47s10.32.0.2 - - [17/Sep/2019:10:17:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 46s10.32.0.2 - - [17/Sep/2019:10:17:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/17 10:18:00 [error] 15#15: *234 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [17/Sep/2019:10:18:00 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
[2019-09-17 10:18:02 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:186)
[2019-09-17 10:18:03 +0000] [271] [INFO] Booting worker with pid: 271
16/20 [=======================>......] - ETA: 14s10.32.0.2 - - [17/Sep/2019:10:18:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
Using TensorFlow backend.
10.32.0.2 - - [17/Sep/2019:10:18:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/17 10:18:16 [error] 15#15: *244 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
16/20 [=======================>......] - ETA: 13s10.32.0.2 - - [17/Sep/2019:10:18:16 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019-09-17 10:18:16.305426: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[2019-09-17 10:18:17 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:23)
10.32.0.2 - - [17/Sep/2019:10:18:18 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
[2019-09-17 10:18:18 +0000] [297] [INFO] Booting worker with pid: 297
10.32.0.2 - - [17/Sep/2019:10:18:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
Using TensorFlow backend.
2019-09-17 10:18:26.532349: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [17/Sep/2019:10:18:28 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 29s10.32.0.2 - - [17/Sep/2019:10:18:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 10s10.32.0.2 - - [17/Sep/2019:10:19:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 41s10.32.0.2 - - [17/Sep/2019:10:19:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 58s 3s/step
10.32.0.2 - - [17/Sep/2019:10:19:15 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 11s10.32.0.2 - - [17/Sep/2019:10:19:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 55s 3s/step
10.32.0.2 - - [17/Sep/2019:10:19:37 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:40 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 26s10.32.0.2 - - [17/Sep/2019:10:19:50 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:55 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:00 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 8s 10.32.0.2 - - [17/Sep/2019:10:20:05 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:10 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 40s 2s/step
10.32.0.2 - - [17/Sep/2019:10:20:10 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:15 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:20 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:25 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:20:30 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
```

Instance 3
```
10.32.0.2 - - [17/Sep/2019:10:14:54 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:14:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:09 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 22s10.32.0.2 - - [17/Sep/2019:10:15:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:24 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:29 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 7s 10.32.0.2 - - [17/Sep/2019:10:15:34 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 36s 2s/step
10.32.0.2 - - [17/Sep/2019:10:15:37 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:44 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:49 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:54 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:09 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:24 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:29 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:34 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:44 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:49 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:54 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:09 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:24 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:29 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:34 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:44 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:49 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:54 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:59 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:04 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:09 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:14 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:19 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 21s10.32.0.2 - - [17/Sep/2019:10:18:24 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:29 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 7s 10.32.0.2 - - [17/Sep/2019:10:18:34 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:39 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 35s 2s/step
10.32.0.2 - - [17/Sep/2019:10:18:40 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:44 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:49 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:54 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
```

Instance 4
```
10.32.0.2 - - [17/Sep/2019:10:15:03 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:08 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:13 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 22s10.32.0.2 - - [17/Sep/2019:10:15:18 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:23 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:28 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 7s 10.32.0.2 - - [17/Sep/2019:10:15:33 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 36s 2s/step
10.32.0.2 - - [17/Sep/2019:10:15:37 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:43 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:48 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:53 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:15:58 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:03 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:08 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:13 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:18 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:23 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:28 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 49s10.32.0.2 - - [17/Sep/2019:10:16:33 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 52s10.32.0.2 - - [17/Sep/2019:10:16:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:43 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:48 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:16:53 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 1:0210.32.0.2 - - [17/Sep/2019:10:16:58 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/17 10:16:59 [error] 15#15: *126 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [17/Sep/2019:10:16:59 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019/09/17 10:16:59 [error] 15#15: *228 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [17/Sep/2019:10:16:59 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
[2019-09-17 10:17:00 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:20)
[2019-09-17 10:17:00 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:21)
[2019-09-17 10:17:01 +0000] [185] [INFO] Booting worker with pid: 185
[2019-09-17 10:17:01 +0000] [186] [INFO] Booting worker with pid: 186
10.32.0.2 - - [17/Sep/2019:10:17:03 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
Using TensorFlow backend.
Using TensorFlow backend.
2019-09-17 10:17:11.140965: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [17/Sep/2019:10:17:11 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:15 +0000] "POST /invocations HTTP/1.1" 499 0 "-" "AHC/2.0"
2019-09-17 10:17:16.667130: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[2019-09-17 10:17:16 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:19)
[2019-09-17 10:17:18 +0000] [240] [INFO] Booting worker with pid: 240
Using TensorFlow backend.
2019-09-17 10:17:24.916628: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [17/Sep/2019:10:17:31 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:31 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 42s10.32.0.2 - - [17/Sep/2019:10:17:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:35 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:43 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:45 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:48 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:53 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:17:58 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/17 10:18:01 [error] 15#15: *126 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
16/20 [=======================>......] - ETA: 14s10.32.0.2 - - [17/Sep/2019:10:18:01 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 44s10.32.0.2 - - [17/Sep/2019:10:18:03 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
[2019-09-17 10:18:04 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:18)
[2019-09-17 10:18:05 +0000] [309] [INFO] Booting worker with pid: 309
Using TensorFlow backend.
10.32.0.2 - - [17/Sep/2019:10:18:08 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019-09-17 10:18:15.362254: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [17/Sep/2019:10:18:16 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:18 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 11s10.32.0.2 - - [17/Sep/2019:10:18:23 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
20/20 [==============================] - 55s 3s/step
10.32.0.2 - - [17/Sep/2019:10:18:28 +0000] "POST /invocations HTTP/1.1" 200 15 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:28 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:33 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:38 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:43 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 27s10.32.0.2 - - [17/Sep/2019:10:18:48 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:53 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:18:58 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:03 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
8/20 [===========>..................] - ETA: 42s10.32.0.2 - - [17/Sep/2019:10:19:08 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:13 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
16/20 [=======================>......] - ETA: 11s10.32.0.2 - - [17/Sep/2019:10:19:18 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:23 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:28 +0000] "POST /invocations HTTP/1.1" 499 0 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:28 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
[2019-09-17 10:19:30 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:309)
[2019-09-17 10:19:30 +0000] [309] [INFO] Worker exiting (pid: 309)
[2019-09-17 10:19:31 +0000] [357] [INFO] Booting worker with pid: 357
Using TensorFlow backend.
16/20 [=======================>......] - ETA: 13s10.32.0.2 - - [17/Sep/2019:10:19:33 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
2019/09/17 10:19:38 [error] 15#15: *267 upstream timed out (110: Connection timed out) while reading response header from upstream, client: 10.32.0.2, server: , request: "POST /invocations HTTP/1.1", upstream: "http://unix:/tmp/gunicorn.sock/invocations", host: "model.aws.local:8080"
10.32.0.2 - - [17/Sep/2019:10:19:38 +0000] "POST /invocations HTTP/1.1" 504 192 "-" "AHC/2.0"
2019-09-17 10:19:40.217665: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
[2019-09-17 10:19:40 +0000] [14] [CRITICAL] WORKER TIMEOUT (pid:240)
[2019-09-17 10:19:40 +0000] [240] [INFO] Worker exiting (pid: 240)
[2019-09-17 10:19:41 +0000] [383] [INFO] Booting worker with pid: 383
10.32.0.2 - - [17/Sep/2019:10:19:41 +0000] "GET /ping HTTP/1.1" 499 0 "-" "AHC/2.0"
Using TensorFlow backend.
2019-09-17 10:19:44.624077: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
10.32.0.2 - - [17/Sep/2019:10:19:48 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:51 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:53 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
10.32.0.2 - - [17/Sep/2019:10:19:58 +0000] "GET /ping HTTP/1.1" 200 1 "-" "AHC/2.0"
```

Invoking code error message
```
ModelError: An error occurred (ModelError) when calling the InvokeEndpoint operation: Received server error (504) from model with message "<html>
<head><title>504 Gateway Time-out</title></head>
<body bgcolor="white">
<center><h1>504 Gateway Time-out</h1></center>
<hr><center>nginx/1.10.3 (Ubuntu)</center>
</body>
</html>
". See https://eu-west-2.console.aws.amazon.com/cloudwatch/home?region=eu-west-2#logEventViewer:group=/aws/sagemaker/Endpoints/aws-debug 
```

This time out behaviour was not observed when predictions aren't actually performed (e.g) Line `59` in `predictor.py` is commented out
