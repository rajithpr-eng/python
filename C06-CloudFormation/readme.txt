1. Create a keypair name ec2-ohio

2. Run cloud formation with template m03p02.json

3. SSH to EC2 instance and run commands to install the code deploy agent

Example:
ssh -i "ec2-ohio.pem" ec2-user@ec2-18-216-136-90.us-east-2.compute.amazonaws.com
sudo yum update
wget https://aws-codedeploy-us-east-2.s3.us-east-2.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status
Ref: https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install-linux.html


4. Upload artifacts to s3
s3://m03p02artifacts/backend.zip

5. Create IAM role for code deploy

6. Run code deploy with source pointing to s3 bucket

7. Upload artifacts to s3 after updating lambda.py with SNS ARN
s3://m03p02artifacts/lambda.zip


8. Run cloud formation providing Kinesis ARN
