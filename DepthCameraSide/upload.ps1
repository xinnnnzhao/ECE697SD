while(1){
rm $args".zip"
Compress-Archive -Path $args".ply" -DestinationPath $args".zip"
scp -i ../FTPServer/ece-697-aws-key.pem $args".zip" ec2-user@ec2-34-235-116-199.compute-1.amazonaws.com:~/data/
}
