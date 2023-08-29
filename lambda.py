# Runtime Python 3.8
# Remember to config role permissions

#####################################################################

# Test object to use for lambdas and step functions

''''
{
  "image_data": "",
  "s3_bucket": MY_BUCKET_NAME, # Fill in with your bucket
  "s3_key": "test/bicycle_s_000513.png"
}
''''

#####################################################################

# SerializeImageData lambda function
import json
import boto3
import base64

s3 = boto3.client('s3')
def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event["s3_key"]
    bucket = event["s3_bucket"]

    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


#####################################################################

# Inference lambda function

import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT =  ## TODO: fill in


def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode(event["image_data"])

    # Instantiate a Predictor
    predictor=  ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences =  sagemaker.invoke_endpoint(
        EndpointName = ENDPOINT,
        Body = image,
        ContentType = 'image/png')

    # We return the data back to the Step Function
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


#####################################################################

# Threshold lambda function

import json

# Look what threshold I've got
THRESHOLD = .8


def lambda_handler(event, context):
    # Grab the inferences from the event
    inferences = event['inferences']

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = (max(inferences) > THRESHOLD)

# The project asks to comment out error handling
# for the function to fail loudly:)

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise ("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


