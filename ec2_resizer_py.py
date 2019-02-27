# the AWS SDK for Python
import boto3

def lambda_handler(event, context):
    
    
    try:
        # set local vars from event arguments 
        region = event['region']
        instance_ID = event['instanceId']
        size = event['targetSize']
    
        # get an EC2 SDK object
        client = boto3.client('ec2', region_name=region)
        
        # Get the current Instance Size
        instance_data = client.describe_instance_attribute(InstanceId = instance_ID, Attribute = 'instanceType')
        
        current_instance_type = instance_data['InstanceType']['Value']
        
        print 'current instance type: ' + current_instance_type

        # Get the current status
        instance_status_data = client.describe_instance_status(InstanceIds = [instance_ID])

        # Passing an array of one, so it should be the first element back
        if len(instance_status_data['InstanceStatuses']) != 0:
            print(instance_status_data)
            current_instance_status = instance_status_data['InstanceStatuses'][0]['InstanceState']['Name'] 
        else:
            current_instance_status = 'unknown'
    
        print 'current instance status: ' + current_instance_status
    
        # check if the instance is currently a difference size and if so, don't resize it
        if current_instance_type != size:
        
            if current_instance_status == 'running':
                # Stop the instance
                client.stop_instances(InstanceIds=[instance_ID])
                waiter=client.get_waiter('instance_stopped')
                waiter.wait(InstanceIds=[instance_ID])
            
            # Change the instance type
            client.modify_instance_attribute(InstanceId=instance_ID, Attribute='instanceType', Value=size)
            
            # Start the instance
            client.start_instances(InstanceIds=[instance_ID])
        
        else:
            # There's nothing to do.  Let the caller determine if this is an issue or not.
			if current_instance_status == 'stopped': client.start_instances(InstanceIds=[instance_ID])
			
			return 'The instance is already the requested size.'
			

    except Exception, e:
        # more detailed error handling can go here.
        # if not...
        # return the error so the caller can take action.
		raise Exception('Error: '+ str(e))
		
    else:
        return 'The resize request completed successfully.'
		