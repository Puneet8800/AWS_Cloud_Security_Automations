### Purpose
 The purpose of this automation is to detects all the public objects which is present in your bucket. This script is helpful because it will prevent from data leakage.

### Prerequisites
IAM role with a s3 read only access enable.

### Configuration Steps
Configure iam role with a persmission of s3 read only.

### How to run
python3 public_object_in_a_bucket.py -b bucket_name

python3 public_object_in_a_bucket.py --bucket bucket_name
 
python3 public_object_in_a_bucket.py -help

### References
1. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html
