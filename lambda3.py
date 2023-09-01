import json

# Look what threshold I've got
THRESHOLD = .85


def lambda_handler(event, context):
    # Grab the inferences from the event
    body = json.loads(event["body"])
    inferences_str = body["body"]["inferences"]
    inferences = json.loads(inferences_str)

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(inferences) > THRESHOLD

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