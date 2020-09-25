package main

import (
	"fmt"
	"os"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/waf"
	"sync"
)
var wg sync.WaitGroup

func insert(ruleid string, s string, env string, region string, a string){
	go func(){
		sess, err := session.NewSession(&aws.Config{
			Region: aws.String(region),
			Credentials: credentials.NewSharedCredentials("", env),
		})
		svc := waf.New(sess)
		ct := &waf.GetChangeTokenInput{}
		result1, err := svc.GetChangeToken(ct)
		input := &waf.UpdateIPSetInput{
			ChangeToken: result1.ChangeToken,
			IPSetId:     aws.String(ruleid),
			Updates: []*waf.IPSetUpdate{
				{
					Action: aws.String(a),
					IPSetDescriptor: &waf.IPSetDescriptor{
						Type:  aws.String("IPV4"),
						Value: aws.String(s),
					},
				},
			},
		}
		result, err := svc.UpdateIPSet(input)
		if err != nil {
			if aerr, ok := err.(awserr.Error); ok {
				switch aerr.Code() {
				case waf.ErrCodeStaleDataException:
					fmt.Println(waf.ErrCodeStaleDataException, aerr.Error())
				case waf.ErrCodeInternalErrorException:
					fmt.Println(waf.ErrCodeInternalErrorException, aerr.Error())
				case waf.ErrCodeInvalidAccountException:
					fmt.Println(waf.ErrCodeInvalidAccountException, aerr.Error())
				case waf.ErrCodeInvalidOperationException:
					fmt.Println(waf.ErrCodeInvalidOperationException, aerr.Error())
				case waf.ErrCodeInvalidParameterException:
					fmt.Println(waf.ErrCodeInvalidParameterException, aerr.Error())
				case waf.ErrCodeNonexistentContainerException:
					fmt.Println(waf.ErrCodeNonexistentContainerException, aerr.Error())
				case waf.ErrCodeNonexistentItemException:
					fmt.Println(waf.ErrCodeNonexistentItemException, aerr.Error())
				case waf.ErrCodeReferencedItemException:
					fmt.Println(waf.ErrCodeReferencedItemException, aerr.Error())
				case waf.ErrCodeLimitsExceededException:
					fmt.Println(waf.ErrCodeLimitsExceededException, aerr.Error())
				default:
					fmt.Println(aerr.Error())
				}
			} else {
				// Print the error, cast err to awserr.Error to get the Code and
				// Message from an error.
				fmt.Println(err.Error())
			}
			return
		}
		fmt.Println(result)
		wg.Done()

	}()
}

const region1 = "global"
const ruleid_1 ="put the rule id for the block rule"
const ruleid_2 = "put the ruleid for the block rule"
const env_1 ="env name in your .aws/credentials"
const env_2 = "env name in your .aws/credentials"
const ins = "INSERT"
const del = "DELETE"

func main() {
	s := os.Args[1]
	wg.Add(1)
	if os.Args[2] == "ins"{
		if os.Args[3] == "env1"{
			insert(ruleid_1, s,env_1,region1, ins)

		}
	}
	if os.Args[2] == "del"{
		if os.Args[3] == "env1"{
			insert(ruleid_1, s,env_1,region1, del)

		}
	}
	if os.Args[2] == "ins"{
		if os.Args[3] == "env2"{
			insert(ruleid_2, s,env_2,region1, ins)

		}
	}
	if os.Args[2] == "del"{
		if os.Args[3] == "env2"{
			insert(ruleid_2, s,env_2,region1, ins)

		}
	}

	wg.Wait()
}
