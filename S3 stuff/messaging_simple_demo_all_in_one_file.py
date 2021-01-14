import logging
import boto3
from botocore.exceptions import ClientError

import json
    
''' 
    A simple demo on how to perform core operation with the SQS queue.
    
    !!! Please note that typically the different methods included in this class correspond to operations performed by different 
    entities/components (e.g. a producer would deliver messages to a queue, a consumer would retrieve messages from the queue, etc.)
    and they would not be declared within the same class!!! Recall that a message queue enables asynchronous communication between
    different components/services!
    
    For simplicity, as this is an educational example, all the methods are included in one single class. Please consult the Moodle page 
    for a simplified example where there is one class declared per component/entity, and multiple threads are used to simulate the 
    interaction of the different components (i.e. producer and consumer) with the queue.
'''

class MessagingDemo:
    
    
    def create_queue(self, queue_name, region):
        
        try:
            sqs_client = boto3.client('sqs')
            print('\ncreating the queue {}...'.format(queue_name))
            response = sqs_client.create_queue(QueueName=queue_name)
            print(response) # this is not really needed
        
        except ClientError as e:
            logging.error(e)
            return False
        return True
        
    
    def delete_queue(self, queue_name):
        
        try:
            sqs_client = boto3.client('sqs')
            # retrive the URL of an existing Amazon SQS queue
            response = sqs_client.get_queue_url(QueueName=queue_name)
            print(response) # this is not really needed
            queue_url = response['QueueUrl']
            response = sqs_client.delete_queue(QueueUrl=queue_url)
        
            
        except ClientError as e:
            logging.error(e)
            return False
        return True
        
     
    ''' this method would be a method of the producer component'''
    def send_message(self, queue_name, message):
        
        try:
            sqs_client = boto3.client('sqs')
            # retrive the URL of an existing Amazon SQS queue
            response = sqs_client.get_queue_url(QueueName=queue_name)
            queue_url = response['QueueUrl']
            
            response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
            
        
            
        except ClientError as e:
            logging.error(e)
            return False
        return True


    ''' this method would be a method of the consumer component'''
    def consume_message(self, queue_name):
        
        try:
            sqs_client = boto3.client('sqs')
            # retrive the URL of an existing Amazon SQS queue
            response = sqs_client.get_queue_url(QueueName=queue_name)
            queue_url = response['QueueUrl']
            
            print('\nrequesting messages from the queue...\n')
            # receive a message from the specified queue
            response = sqs_client.receive_message(QueueUrl=queue_url,
                            MaxNumberOfMessages=1, # a number between 1 and 10
                            VisibilityTimeout=10, #default 30 seconds
                        )
            print(response) # this is not really needed
            print('\n')
          
            messages = response.get('Messages')
            if messages != None:
                # consume the message(s) according to the specific processing you'd like to perform
                messages = response['Messages'] # a list with all the messages
                # in this example we only retrieved one message, so the list contains only one element
                current_message = messages[0] # retrieve the message from the list
                print(current_message)
                print("\nThe message I'm proccessing is:\n", current_message['Body'])
                
              
                ''' 
                    once the message has been processed, ensure that the message is deleted from the queue.
                    deletes the specified message from the specified queue. 
                    the message to be deleted is identified by the message ReceiptHandle
                '''
                receipt_handle = current_message['ReceiptHandle']
                response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            else:
                print('No message has been received, you should repeat the request...')
            
            
        except ClientError as e:
            logging.error(e)
            return False
        return True
        

   
    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('queue_name', help='The name of the queue to work with or to create.')
    parser.add_argument('--create_queue', help='Create the queue. When not specified, the create_queue method is not executed.', action='store_true')
    parser.add_argument('--delete_queue', help='Delete the queue. The messages in the queues will no longer be available!!  When not specified, the queue is not deleted.', action='store_true')

  
    args = parser.parse_args()
    
    region = 'us-east-1'
    
    md = MessagingDemo()
    
    if args.create_queue:
        md.create_queue(args.queue_name, region)
    
    message1 = "Hi there!"
    md.send_message(args.queue_name, message1)
    
    message2 = '{"artist": "Pink Floyd","song": "Us and Them"}'
    md.send_message(args.queue_name, message2)
    
    md.consume_message(args.queue_name)
    
    if args.delete_queue:
        print('\n{} is being deleted!.'.format(args.queue_name))
        md.delete_queue(args.queue_name)
    else:
        print('\n{} will not be deleted.'.format(args.queue_name))
    
      
    
    
if __name__ == '__main__':
 main()
