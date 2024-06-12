targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

param azureOpenAiEndpoint1 string
@secure()
param azureOpenAiApiKey1 string
param azureOpenDeploymentName1 string
param azureOpenAiEndpoint2 string
@secure()
param azureOpenAiApiKey2 string
param azureOpenDeploymentName2 string


@minLength(1)
@description('Primary location for all resources')
param location string

param chatUiExists bool
@secure()
param chatUiDefinition object
param chessApiExists bool
@secure()
param chessApiDefinition object
param stockfishServerExists bool
@secure()
param stockfishServerDefinition object
param gameServiceExists bool
@secure()
param gameServiceDefinition object
@secure()
param azureSearchKey string
param azureSearchEndpoint string

@description('Id of the user or app to assign application roles')
param principalId string

// Tags that should be applied to all resources.
//
// Note that 'azd-service-name' tags should be applied separately to service host resources.
// Example usage:
//   tags: union(tags, { 'azd-service-name': <service name in azure.yaml> })
var tags = {
  'azd-env-name': environmentName
}

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module monitoring './shared/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    tags: tags
    logAnalyticsName: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: '${abbrs.insightsComponents}${resourceToken}'
  }
  scope: rg
}

module dashboard './shared/dashboard-web.bicep' = {
  name: 'dashboard'
  params: {
    name: '${abbrs.portalDashboards}${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    location: location
    tags: tags
  }
  scope: rg
}

module registry './shared/registry.bicep' = {
  name: 'registry'
  params: {
    location: location
    tags: tags
    name: '${abbrs.containerRegistryRegistries}${resourceToken}'
  }
  scope: rg
}

module keyVault './shared/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    location: location
    tags: tags
    name: '${abbrs.keyVaultVaults}${resourceToken}'
    principalId: principalId
  }
  scope: rg
}

module appsEnv './shared/apps-env.bicep' = {
  name: 'apps-env'
  params: {
    name: '${abbrs.appManagedEnvironments}${resourceToken}'
    location: location
    tags: tags
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
  scope: rg
}

resource vault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVault.outputs.name
  scope: rg
}

module cosmosDb './app/db-cosmos-mongo.bicep' = {
  name: 'cosmosDb'
  params: {
    accountName: '${abbrs.documentDBDatabaseAccounts}${resourceToken}'
    location: location
    tags: tags
    keyVaultName: keyVault.outputs.name
  }
  scope: rg
}

module chatUi './app/chat-ui.bicep' = {
  name: 'chat-ui'
  params: {
    name: '${abbrs.appContainerApps}chat-ui-${resourceToken}'
    location: location
    tags: tags
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}chat-ui-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: chatUiExists
    appDefinition: chatUiDefinition
    apiUrls: [
      chessApi.outputs.uri
      stockfishServer.outputs.uri
      gameService.outputs.uri
      ragService.outputs.uri
    ]
  }
  scope: rg
}

module chessApi './app/chess-api.bicep' = {
  name: 'chess-api'
  params: {
    name: '${abbrs.appContainerApps}chess-api-${resourceToken}'
    location: location
    tags: tags
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}chess-api-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: chessApiExists
    appDefinition: chessApiDefinition
    cosmosDbConnectionString: vault.getSecret(cosmosDb.outputs.connectionStringKey)
    allowedOrigins: [
      'https://${abbrs.appContainerApps}chat-ui-${resourceToken}.${appsEnv.outputs.domain}'
    ]
  }
  scope: rg
}

module stockfishServer './app/stockfish-server.bicep' = {
  name: 'stockfish-server'
  params: {
    name: '${abbrs.appContainerApps}stockfish-se-${resourceToken}'
    location: location
    tags: tags
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}stockfish-se-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: stockfishServerExists
    appDefinition: stockfishServerDefinition
    allowedOrigins: [
      'https://${abbrs.appContainerApps}chat-ui-${resourceToken}.${appsEnv.outputs.domain}'
    ]
  }
  scope: rg
}

module gameService './app/game-service.bicep' = {
  name: 'game-service'
  params: {
    name: '${abbrs.appContainerApps}game-service-${resourceToken}'
    location: location
    tags: tags
    apiUrls: [
          chessApi.outputs.uri
          stockfishServer.outputs.uri
        ]
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}game-service-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: gameServiceExists
    appDefinition: gameServiceDefinition
    azureOpenAiEndpoint1: azureOpenAiEndpoint1
    azureOpenAiApiKey1: azureOpenAiApiKey1
    azureOpenDeploymentName1: azureOpenDeploymentName1
    cosmosDbConnectionString: vault.getSecret(cosmosDb.outputs.connectionStringKey)
    allowedOrigins: [
      'https://${abbrs.appContainerApps}chat-ui-${resourceToken}.${appsEnv.outputs.domain}'
    ]
  }
  scope: rg
}

module ragService './app/rag-service.bicep' = {
  name: 'rag-service'
  params: {
    name: '${abbrs.appContainerApps}rag-service-${resourceToken}'
    location: location
    tags: tags
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}rag-service-${resourceToken}'
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: appsEnv.outputs.name
    containerRegistryName: registry.outputs.name
    exists: gameServiceExists
    appDefinition: gameServiceDefinition
    azureOpenAiEndpoint: azureOpenAiEndpoint2
    azureOpenAiApiKey: azureOpenAiApiKey2
    azureOpenDeploymentName: azureOpenDeploymentName2
    azureSearchEndpoint: azureSearchEndpoint
    azureSearchKey: azureSearchKey
    apiUrls: []
    cosmosDbConnectionString: vault.getSecret(cosmosDb.outputs.connectionStringKey)
    allowedOrigins: [
      'https://${abbrs.appContainerApps}chat-ui-${resourceToken}.${appsEnv.outputs.domain}'
    ]
  }
  scope: rg
}

output AZURE_CONTAINER_REGISTRY_ENDPOINT string = registry.outputs.loginServer
output AZURE_KEY_VAULT_NAME string = keyVault.outputs.name
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.endpoint
