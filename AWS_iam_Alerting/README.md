### Purpose
 The purpose of this automation is to trigger an alert whenever an there is an IAM changes regarding user/role/policy.

### Deployment Options
AWS Lambda

### Prerequisites
1. Cloudwatch Events.
2. Cloudtrail events( logging should be enabled).

### Configuration Steps
1. Configure cloudtrail on the account with logging enabled.
2. Configure cloudwatch event rule using the json mention below.
3. Lambda deployement.
4. Enable lambda trigger for the cloudwatch event rule.



### References
1. Cloudtrail Multi Region Configuration: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/receive-cloudtrail-log-files-from-multiple-regions.html
2. Cloudwatch Event Rule: https://github.com/Puneet8800/Cloud_Security_Automations/blob/master/AWS_iam_Alerting/Cloudwatch_eventrule.json
3. Creating Cloudwatch Rule using JSON: https://aws.amazon.com/premiumsupport/knowledge-center/cloudwatch-create-custom-event-pattern/
4. Enabling Cloudwatch trigger on Lambda: https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents.html
