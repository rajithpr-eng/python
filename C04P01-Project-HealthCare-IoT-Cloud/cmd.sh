#python BedSideMonitor.py -e a3ueika12ovvbq-ats.iot.us-east-1.amazonaws.com -r AmazonRootCA1.pem -c 2bd0358e9671d124a650b93f4f9cb7002a12172611c6e60c5091bfc1eee5775a-certificate.pem.crt -k 2bd0358e9671d124a650b93f4f9cb7002a12172611c6e60c5091bfc1eee5775a-private.pem.key -id client1 -t iot/bsm -n 5

python BedSideMonitor.py -e <> -r root-CA.crt -c 7716bb5042d33071a6235db489ead83e923b4813b7e7b2fa6bfadaea3aa943fc-certificate.pem.crt -k 7716bb5042d33071a6235db489ead83e923b4813b7e7b2fa6bfadaea3aa943fc-private.pem.key -d client1 -t iot/bsm -d BSM_G000

python BedSideMontor.py -e <> -r root-CA.crt -c 80c7b85557f8add3edda3b0659a3e2b79c88e03c9603e9b60300032fc9865bc0-certificate.pem.crt -k 80c7b85557f8add3edda3b0659a3e2b79c88e03c9603e9b60300032fc9865bc0-private.pem.key -d client2 -t iot/bsm -d BSM_G001
