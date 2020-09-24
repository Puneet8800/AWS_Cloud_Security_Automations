import boto3
import json
import requests
import sys
import argparse

parser = argparse.ArgumentParser(description="Identify all the public objects in your Bucket")
parser.add_argument('-b', '--bucket', metavar='', required=True, help="Please specify the Bucket Name")
args = parser.parse_args()

def get_objects(args):
    
    object = boto3.client('s3')
    object_paginator = object.get_paginator('list_objects_v2')
    object_paginator_iterator = object_paginator.paginate(Bucket=args)
    keys = []
    for page in object_paginator_iterator:
        for obj in page['Contents']:
            keys.append(obj.get('Key'))
    
    return keys

def public_object(keys):
    object = boto3.client('s3')
    object_key = keys[1:]
    for i in object_key:
        response = object.get_object_acl(Bucket=args, Key=i)
        for j in response['Grants']:
            #print(j['Permission'])
            if j['Grantee']['Type'] == 'Group':
                print("{} is public and has {} permission".format(i,j['Permission']))
                
        

if __name__ == '__main__':
    l = get_objects(args.bucket)
    public_object(l)
