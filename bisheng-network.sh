sudo iptables -I DOCKER-USER -s 172.30.0.4 -j REJECT
sudo iptables -I DOCKER-USER -s 172.30.0.4 -d 172.30.0.0/16 -j ACCEPT
sudo iptables -I DOCKER-USER -s 172.30.0.4 -d 10.10.42.114 -j ACCEPT
# access bisheng.dataelem.com
sudo iptables -I DOCKER-USER -s 172.30.0.4 -d 110.16.193.170 -j ACCEPT
# minio access form cpolar
sudo iptables -I DOCKER-USER -s 172.30.0.4 -d 61.160.195.206 -j ACCEPT
# access bing.com
sudo iptables -I DOCKER-USER -s 172.30.0.4 -d 13.70.5.32 -j ACCEPT
#sudo docker network disconnect docker_proxy one-api
#sudo docker network connect --ip 172.30.0.12 docker_proxy one-api
#sudo /home/station/Downloads/docker-compose-linux-x86_64 up -d
