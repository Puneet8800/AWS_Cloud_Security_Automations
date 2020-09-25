### Purpose
 The purpose of this automation is to block/release ip from your AWS WAF.

### Prerequisites
IAM role with full AWS WAF access.

### Configuration Steps
Configure iam role with full permission over AWS WAF.
### How to run
go run Waf_Ip_Block.go ip_address ins env_name

go run Waf_Ip_Block.go ip_address del env_name
### References
1. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_change-permissions.html
