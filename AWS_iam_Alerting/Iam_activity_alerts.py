import json
import boto3
import os
from botocore.vendored import requests

def lambda_handler(event, context):
    if event["detail"]['eventSource'] == 'iam.amazonaws.com' and 'requestParameters' in event["detail"]:
        event_name = event["detail"]['eventName']
        if event_name == "CreatePolicy":
            createpolicy(event,event_name)
        elif event_name == "CreatePolicyVersion":
            createpolicyversion(event,event_name)
        elif event_name == "AttachGroupPolicy":
            attach_group_policy(event,event_name)
        elif event_name == "DetachGroupPolicy":
            detach_group_policy(event,event_name)
        elif event_name == "AttachUserPolicy":
            attach_user_policy(event,event_name)
        elif event_name == "DetachUserPolicy":
            detach_user_policy(event,event_name)
        elif event_name == "AttachRolePolicy":
            attach_role_policy(event,event_name)
        elif event_name == "DetachRolePolicy":
            detach_role_policy(event,event_name)
        else:
            print("No event Found")


def createpolicy(event, event_name):
    p_name = event['detail']['requestParameters']['policyName']
    p_arn = event['detail']['responseElements']['policy']['arn']
    name=" "
    public_alert(event,p_name,p_arn,name)
def createpolicyversion(event, event_name):
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    name =" "
    public_alert(event,p_name,p_arn,name)
def attach_group_policy(event, event_name):
    g_name = event['detail']['requestParameters']['groupName']
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    public_alert(event,p_name,p_arn,g_name)
def detach_group_policy(event, event_name):
    g_name = event['detail']['requestParameters']['groupName']
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    public_alert(event,p_name,p_arn,g_name)
def attach_user_policy(event, event_name):
    u_name = event['detail']['requestParameters']['userName']
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    public_alert(event,p_name,p_arn,u_name)
def detach_user_policy(event, event_name):
    u_name = event['detail']['requestParameters']['userName']
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    public_alert(event,p_name,p_arn,u_name)
def attach_role_policy(event, event_name):
    r_name = event['detail']['requestParameters']['roleName']
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    public_alert(event,p_name,p_arn,r_name)
def detach_role_policy(event, event_name):
    r_name = event['detail']['requestParameters']['roleName']
    p_name = event['detail']['requestParameters']['policyArn'].split(':')[5]
    p_arn = event['detail']['requestParameters']['policyArn']
    public_alert(event,p_name,p_arn,r_name)

def public_alert(event,p_name,p_arn,name):
    event_name = event["detail"]['eventName']
    user_name = event["detail"]['userIdentity']['principalId']
    template = {}
    template['attachments'] = [{}]
    template['attachments'][0]['fallback'] = 'unable to display this message !'
    template['attachments'][0]['color'] = '#AF0000'
    template['attachments'][0]['pretext'] = "IAM Alerts"

    template['attachments'][0]['fields'] = [{"title": "IAM Alerts"}]
    template['attachments'][0]['fields'].append({"title": "Event Name"})
    template['attachments'][0]['fields'].append({"value":event_name })
    template['attachments'][0]['fields'].append({"title": "Username"})
    template['attachments'][0]['fields'].append({"value": user_name})
    template['attachments'][0]['fields'].append({"title": "Policy Attached To"})
    template['attachments'][0]['fields'].append({"value":name })
    template['attachments'][0]['fields'].append({"title": "Policy Name"})
    template['attachments'][0]['fields'].append({"value": p_name})
    template['attachments'][0]['fields'].append({"title": "Policy ARN"})
    template['attachments'][0]['fields'].append({"value": p_arn})

    json_template = json.dumps(template)
    requests.post(url='Slack incoming webhook url', data=json_template)
