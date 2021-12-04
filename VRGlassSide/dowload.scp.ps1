while(1){
scp -i ece-697-aws-key.pem ec2-user@ec2-34-235-116-199.compute-1.amazonaws.com:~/data/out.zip  out.zip
rm .\temp\out.ply
Expand-Archive -Path out.zip -DestinationPath temp
rm out.ply
cp temp/out.ply ./
}
