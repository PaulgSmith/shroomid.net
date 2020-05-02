def lambda_handler(event, context):
    results = []
    dicObj = eval(event['body'])
    buckets = dicObj['Bucket']
    keys = dicObj['Key']
    locations = dicObj['Location']


    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'wb') as f:
        s3.Bucket(buckets).download_file(keys, tmp.name)
        tmp.flush()
	results = run_inference_on_image(tmp.name)
    results.append({"Location": locations})
    jsonResults = json.dumps(results)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },

        "body": jsonResults
    }
