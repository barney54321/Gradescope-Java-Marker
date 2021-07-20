apt install curl
apt install zip
apt install unzip
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
apt-get -y install openjdk-11-jdk
apt-get install --reinstall ca-certificates-java
update-ca-certificates -f
apt install python3
sdk install gradle 7.1.1