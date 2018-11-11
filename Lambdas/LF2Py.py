from __future__ import print_function
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

import json
import pprint
import requests
import sys
import urllib
import datetime
import boto3
import decimal
import time
import datetime
# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= 'yGvgfy8EatVV5qpVk2SJuKQapFY-iHJ2J0qwKD1-JL05DtDD13epvY6L86aVgLPdwFjx8GTvXZerT6ds7GTdtLHGRg07DUd8Eu6BWJfdyNGvo3-TTq12FbMEuRHmW3Yx'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 1




def lambda_handler(event, context):
    
    
    pollSNS()
    #print('\n',yelpResult)
    # insertIntoDynamo()
    
def pollSNS():
    # create a boto3 client
    client = boto3.client('sqs')
    # create the test queue
    # for a FIFO queue, the name must end in .fifo, and you must pass FifoQueue = True
  #  client.create_queue(QueueName='dinningQueue')
    # get a list of queues, we get back a dict with 'QueueUrls' as a key with a list of queue URLs
    queues = client.list_queues(QueueNamePrefix='dinningQueue') # we filter to narrow down the list
    test_queue_url = queues['QueueUrls'][0]
    
    
    # Receive message from SQS queue
    # response = client.receive_message(
    #     QueueUrl=test_queue_url,
    #     AttributeNames=[
    #         'All'
    #     ],
    #     MaxNumberOfMessages=10,
    #     MessageAttributeNames=[
    #         'All'
    #     ],
    #     VisibilityTimeout=30,
    #     WaitTimeSeconds=0
    # )
    
    # print("Response "+str(response))
    
    # send 100 messages to this queue
    # for i in range(0,100):
    #     # we set a simple message body for each message
    #     # for FIFO queues, a 'MessageGroupId' is required, which is a 128 char alphanumeric string
    #     enqueue_response = client.send_message(QueueUrl=test_queue_url, MessageBody='This is test message #'+str(i))
    #     # the response contains MD5 of the body, a message Id, MD5 of message attributes, and a sequence number (for FIFO queues)
    #     print('Message ID : ',enqueue_response['MessageId'])
    # next, we dequeue these messages - 10 messages at a time (SQS max limit) till the queue is exhausted.
    # in production/real setup, I suggest using long polling as you get billed for each request, regardless of an empty response
    while True:
        #response = client.receive_message(QueueUrl=test_queue_url,AttributeNames=['ALL'],MaxNumberOfMessages=5) # adjust MaxNumberOfMessages if needed
        # Receive message from SQS queue
        response = client.receive_message(
        QueueUrl=test_queue_url,
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=30,
        WaitTimeSeconds=0
        )
    
        if 'Messages' in response: # when the queue is exhausted, the response dict contains no 'Messages' key
            for message in response['Messages']: # 'Messages' is a list
                # process the messages
                #print("Mess"+str(message))
               # print("\n")
                print("-------------------------------")
                print(message['MessageAttributes'])
                # next, we delete the message from the queue so no one else will process it again
                client.delete_message(QueueUrl=test_queue_url,ReceiptHandle=message['ReceiptHandle'])
               #insertIntoDynamo(message['MessageAttributes'])
                
                url_params =  {
                "term":DEFAULT_TERM,
                "location":message['MessageAttributes']['Location']['StringValue'],
                
                "limit":SEARCH_LIMIT
                }
                
                yelpResult = request(API_HOST,SEARCH_PATH,API_KEY,url_params)
                insertIntoDynamo(message['MessageAttributes'],yelpResult)
                #print(yelpResult)
                processYelpSMS(yelpResult,message['MessageAttributes'])
        else:
            print('Queue is now empty')
            break
        
def processYelpSMS(yelpResult,messageAttributes):
    #print("YELP BUSINESSESS")
    #print(yelpResult["businesses"])
    smsContent = yelpResult["businesses"][0]["name"]+"   " +str(yelpResult["businesses"][0]['rating'])+"  "+str(yelpResult["businesses"][0]['display_phone'])
    #print("smsContent")
    print(smsContent)
    sendSMS(smsContent,messageAttributes)
def sendSMS(smsContent,messageAttributes):
    sns = boto3.client('sns')
    number = '+1'+messageAttributes['Phone']['StringValue']
    sns.publish(PhoneNumber = number, Message=smsContent )
def insertIntoDynamo(message,yelprequest):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    table = dynamodb.Table('DINE')
    title = "The Big New Movie"
    year = 2015
    
    response = table.put_item(
       Item={
            'UID': st,
            'body': message,
            'yelpRequest': str(yelprequest)
        }
    )


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    print(response.json())
    return response.json()

