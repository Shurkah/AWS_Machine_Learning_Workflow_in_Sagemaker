import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-09-01-17-32-58-596"

def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(
        endpoint_name=ENDPOINT,
        serializer=IdentitySerializer(content_type="image/png"),
        sagemaker_session=sagemaker.Session()
    )

    # Make a prediction using the predictor object
    inferences = predictor.predict(image)

    # Decode the response if necessary (assuming it's JSON)
    inferences_decoded = inferences.decode('utf-8')

    # We return the data back to the Step Function
    event["body"]["inferences"] = inferences_decoded
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
