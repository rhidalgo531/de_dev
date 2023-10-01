
OVERRIDE=$1 || false 


if [ ! -d "/Users/raify/Development/airbyte" ] || [ "$OVERRIDE" = true ];   
then 
    cd ~/Development/
    git clone https://github.com/airbytehq/airbyte.git --depth 1 
    cd airbyte
    docker-compose up -d 
    echo "Airbyte repository downloaded"
else  
    echo "Directory exists - No Action Taken"
fi 
