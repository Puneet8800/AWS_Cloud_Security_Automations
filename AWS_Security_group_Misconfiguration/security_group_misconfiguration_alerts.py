import boto3
import botocore
import json
from botocore.vendored import requests

 
APPLICABLE_APIS = ["AuthorizeSecurityGroupIngress", "AuthorizeSecurityGroupEgress","RevokeSecurityGroupEngress","RevokeSecurityGroupIngress"]

# Specify the required ingress permissions using the same key layout as that provided in the
# describe_security_group API response and authorize_security_group_ingress/egress API calls.
# ec2() to fetch the all private so that we can see ips apart from them, that will be assign to security group
def ec2():
    e=[]
    ec2 = boto3.client('ec2',region_name='us-east-1')
    ec2_paginator = ec2.get_paginator('describe_network_interfaces')
    ec2_page_iterator = ec2_paginator.paginate()  
    for page in ec2_page_iterator:
        for i in page['NetworkInterfaces']:
            for j in i['PrivateIpAddresses']:
                z =j['PrivateIpAddress'] + "/32"
                e.append(z)
    return e

def security_group(event):
    l = ec2()
    event_name = event["detail"]["eventName"]
    template = {}
    template['attachments'] = [{}]
    template['attachments'][0]['fallback'] = 'unable to display this message !'
    template['attachments'][0]['color'] = '#36a64f'
    template['attachments'][0]['pretext'] = "Security group list "
    template['attachments'][0]['title'] = "security group misconfiguration "
    template['attachments'][0]['fields'] = [{"title": "security group name "}]
    
    group_id = event["detail"]["requestParameters"]["groupId"]
    ip_permissions = event["detail"]["requestParameters"]["ipPermissions"]["items"]
    user_name = event["detail"]["userIdentity"]["principalId"]
    template['attachments'][0]['fields'] = [{"title": "Details of Security Group "}]
    # loop over items
    if event_name == "AuthorizeSecurityGroupEgress":
        for i in ip_permissions:
            for j in i["ipRanges"]["items"]:
                if j["cidrIp"] not in l:
                    template['attachments'][0]['fields'].append({"title": "Security Group Name"})
                    template['attachments'][0]['fields'].append({"value": group_id})
                    template['attachments'][0]['fields'].append({"title": " From Port Number"})
                    template['attachments'][0]['fields'].append({"value": i["fromPort"]})
                    template['attachments'][0]['fields'].append({"title": "To Port Number"})
                    template['attachments'][0]['fields'].append({"value": i["toPort"]})

                    template['attachments'][0]['fields'].append({"title": "Open to"})
                    template['attachments'][0]['fields'].append({"value": j["cidrIp"]})
                    template['attachments'][0]['fields'].append({"title": "Username"})
                    template['attachments'][0]['fields'].append({"value": user_name})
                    template['attachments'][0]['fields'].append({"title": " Event Name"})
                    template['attachments'][0]['fields'].append({"value": event_name})
                    json_template = json.dumps(template)
                    print(json_template)
                    requests.post(url='Slack Incoming webhook url', data=json_template)

    elif event_name == "AuthorizeSecurityGroupIngress":
        for i in ip_permissions:
            for j in i["ipRanges"]["items"]:
                if j["cidrIp"] not in l:
                    template['attachments'][0]['fields'].append({"title": "Security Group Name"})
                    template['attachments'][0]['fields'].append({"value": group_id})
                    template['attachments'][0]['fields'].append({"title": " From Port Number"})
                    template['attachments'][0]['fields'].append({"value": i["fromPort"]})
                    template['attachments'][0]['fields'].append({"title": "To Port Number"})
                    template['attachments'][0]['fields'].append({"value": i["toPort"]})

                    template['attachments'][0]['fields'].append({"title": "Open to"})
                    template['attachments'][0]['fields'].append({"value": j["cidrIp"]})
                    template['attachments'][0]['fields'].append({"title": "Username"})
                    template['attachments'][0]['fields'].append({"value": user_name})
                    template['attachments'][0]['fields'].append({"title": " Event Name"})
                    template['attachments'][0]['fields'].append({"value": event_name})
                    json_template = json.dumps(template)
                    print(json_template)
                    requests.post(url='slack incoming webhook url', data=json_template)

    elif event_name == "RevokeSecurityGroupIngress":
        for i in ip_permissions:
            template['attachments'][0]['fields'].append({"title": "Security Group Name"})
            template['attachments'][0]['fields'].append({"value": group_id})
            template['attachments'][0]['fields'].append({"title": " Deleted Ports"})
            template['attachments'][0]['fields'].append({"title": " From Port Number"})
            template['attachments'][0]['fields'].append({"value": i["fromPort"]})
            template['attachments'][0]['fields'].append({"title": "To Port Number"})
            template['attachments'][0]['fields'].append({"value": i["toPort"]})
            for j in i["ipRanges"]["items"]:
                template['attachments'][0]['fields'].append({"title": "Open to"})
                template['attachments'][0]['fields'].append({"value": j["cidrIp"]})
            template['attachments'][0]['fields'].append({"title": "Username"})
            template['attachments'][0]['fields'].append({"value": user_name})
            template['attachments'][0]['fields'].append({"title": " Event Name"})
            template['attachments'][0]['fields'].append({"value": event_name})
            json_template = json.dumps(template)
            print(json_template)
            requests.post(url='slack incoming webhook url', data=json_template)


    elif event_name == "RevokeSecurityGroupEngress":
        for i in ip_permissions:
            template['attachments'][0]['fields'].append({"title": "Security Group Name"})
            template['attachments'][0]['fields'].append({"value": group_id})
            template['attachments'][0]['fields'].append({"title": " Deleted Ports"})
            template['attachments'][0]['fields'].append({"title": " From Port Number"})
            template['attachments'][0]['fields'].append({"value": i["fromPort"]})
            template['attachments'][0]['fields'].append({"title": "To Port Number"})
            template['attachments'][0]['fields'].append({"value": i["toPort"]})
            for j in i["ipRanges"]["items"]:
                template['attachments'][0]['fields'].append({"title": "Open to"})
                template['attachments'][0]['fields'].append({"value": j["cidrIp"]})
            template['attachments'][0]['fields'].append({"title": "Username"})
            template['attachments'][0]['fields'].append({"value": user_name})
            template['attachments'][0]['fields'].append({"title": " Event Name"})
            template['attachments'][0]['fields'].append({"value": event_name})
            json_template = json.dumps(template)
            print(json_template)
            requests.post(url='slack incoming webhook url', data=json_template)


# lambda_handler
# 
# This is the main handle for the Lambda function.  AWS Lambda passes the function an event and a context.

def lambda_handler(event, context):
    security_group(event)
