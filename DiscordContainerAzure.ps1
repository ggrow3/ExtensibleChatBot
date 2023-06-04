#https://swimburger.net/blog/azure/how-to-create-a-discord-bot-using-the-dotnet-worker-template-and-host-it-on-azure-container-instances

az group create --location eastus --resource-group discordbotrg

az acr create --name discordbotrg --resource-group discordbotrg --sku Basic --location eastus

az acr login --name discordbotrg

docker tag test_bot:latest kmacneel/test_bot:latest
docker push kmacneel/test_bot:latest



$ACR_REGISTRY_ID=$(az acr show --name discordbotrg --query id --output tsv)

$SP_PASSWD=$(az ad sp create-for-rbac --name acr-service-principal --scopes $ACR_REGISTRY_ID --role acrpull --query password --output tsv)
$SP_APP_ID=$(az ad sp list --display-name acr-service-principal --query [0].appId -o tsv)


az container create --resource-group discordbotrg --name discord-bot-container --image kmacneel/test_bot:latest --registry-username $SP_APP_ID --registry-password $SP_PASSWD --location eastus