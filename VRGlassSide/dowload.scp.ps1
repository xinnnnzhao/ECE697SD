while(1){
scp -i ../FTPServer/ece-697-aws-key.pem ec2-user@ec2-34-235-116-199.compute-1.amazonaws.com:~/data/$args".zip"  $args".zip"
rm $args".ply"
rm $args"1.ply"
Expand-Archive -Path $args".zip" -DestinationPath $args"1.ply"
mv $args"1.ply" $args".ply"
}
