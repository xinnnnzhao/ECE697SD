#while(1){
rm out.zip
Compress-Archive -Path out.xyz -DestinationPath out.zip
scp -i ece-697-aws-key.pem out.zip ec2-user@ec2-34-235-116-199.compute-1.amazonaws.com:~/data/
#}
