while(1){
scp -i ece-697-aws-key.pem ec2-user@ec2-34-235-116-199.compute-1.amazonaws.com:~/data/out.zip  out.zip
rm .\temp\out.xyz
Expand-Archive -Path out.zip -DestinationPath temp
rm out.xyz
cp temp/out.xyz ./
}
