import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('elbv2')

    targetArn = event['targetGroup']
    instance_ID = event['instanceId']

    response = client.deregister_targets(
    TargetGroupArn = targetArn,
        Targets=[{
                'Id': instance_ID
            }
        ]
    )

    return response