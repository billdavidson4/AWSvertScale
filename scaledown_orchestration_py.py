# the AWS SDK for Python
import boto3
import json

aws_session = boto3.Session()
LAMBDA_CLIENT = aws_session.client('lambda')
config_data = '{"region":"us-east-1","targetGroup":"arn:aws:elasticloadbalancing:us-east-1:966491901056:targetgroup/scalingGroup/e3c4afb3152a9daf","instanceId":"i-047b90c92357e47f8","targetSize":"t2.micro"}'

def lambda_handler(event, context):
    # De-register the instance
    LAMBDA_CLIENT.invoke(FunctionName="elb_deregister_ec2_py",
                               InvocationType='RequestResponse',
                               Payload=config_data)

    invoke_response = LAMBDA_CLIENT.invoke(FunctionName="ec2_resizer_py",
                               InvocationType='RequestResponse',
                               Payload=config_data)
    
    data = invoke_response['Payload'].read()
    
    if data == "\"The resize request completed successfully.\"":
        return ("it resized and was remove from the ELB")
    else:
        return ("it did not resize")