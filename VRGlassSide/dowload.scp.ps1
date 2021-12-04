while(1){
scp -i ../FTPServer/ece-697-aws-key.pem ec2-user@ec2-34-235-116-199.compute-1.amazonaws.com:~/data/$args".zip"  $args".zip"
rm $args".ply"
rm "temp\"$args".ply"
Expand-Archive -Path out.zip -DestinationPath temp/
mv "temp\"$args".ply" .\
}
