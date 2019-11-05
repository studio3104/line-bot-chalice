# LINE Bot example on AWS serverless services

This is a sample implementation of LINE Bot that detects labels on sent images by Amazon Rekognition.  

![image](https://user-images.githubusercontent.com/1546363/67685365-4822c080-f9d8-11e9-9627-bc7eceba62ef.png)

## Workflow Overview

![image](https://user-images.githubusercontent.com/1546363/67685218-03972500-f9d8-11e9-98b7-e7417dd076e6.png)

1. User sends a picture to the Bot
1. LINE server make a callback request to the associated endpoint
1. Amazon API Gateway invokes the associated AWS Lambda function
1. AWS Lambda validates the request, and then enqueues the payload into Amazon SQS
1. Responsing 200 OK
1. Ditto
1. Invoking the function triggered by SQS events
1. Download the image that user sent from LINE server
1. Calling the detect label API of Amazon Rekognition
1. Replying the labels of the sent image

## Dependencies

- Python 3.6+
  - The implementation contains,
    - type hinting
    - f-string
- [AWS Chalice](https://github.com/aws/chalice)
- [LINE Messaging API SDK for Python](https://github.com/line/line-bot-sdk-python)

## Prerequisite

### LINE Messaging API

https://developers.line.biz/en/services/messaging-api/

You need to sign up and register your API via the site above.  
And take a copy of `channel secret` and `channel access token`.  

### AWS Services

#### AWS CLI

Install and configure AWS CLI referring the following guides.  
AWS Chalice depends on the credential settings configured by the procedre.  

- https://docs.aws.amazon.com/en_pv/cli/latest/userguide/cli-chap-install.html
- https://docs.aws.amazon.com/en_pv/cli/latest/userguide/cli-chap-configure.html

#### Amazon SQS

Create Amazon SQS queue, and take a copy of its queue name.  
**Note that the visivility timeout of the queue have to be more than 60**, otherwise the queue cannot integrate with AWS Lambda function.  

## Deployment

### Configuration

This sample project has an example configuration file.  
You need to copy (or rename) the file and configure appropriately.  

```sh
$ cp .chalice/config.json.exapmle .chalice/config.json
$ cat .chalice/config.json
{
  "version": "2.0",
  "app_name": "LINEBotWorkshop",
  "autogen_policy": false,
  "iam_policy_file": "policy.json",
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "environment_variables": {
        "SQS_QUEUE_NAME": "",
        "LINE_CHANNEL_SECRET": "",
        "LINE_CHANNEL_ACCESS_TOKEN": ""
      }
    }
  }
}
```

### Installing dependencies

Activate the virtual environment as needed before performing this procedure

```sh
$ pip install requirements.txt
```

### Deploy

Once dependencies are successfully installed, you can run `chalice deploy` command

```sh
$ chalice deploy
```

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
