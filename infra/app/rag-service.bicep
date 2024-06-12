param name string
param location string = resourceGroup().location
param tags object = {}

param apiUrls array
param identityName string
param containerRegistryName string
param containerAppsEnvironmentName string
param applicationInsightsName string
param allowedOrigins array
param exists bool
param azureOpenAiApiKey string
param azureOpenAiEndpoint string
param azureOpenDeploymentName string
@secure()
param appDefinition object
@secure()
param cosmosDbConnectionString string
@secure()
param azureSearchKey string
param azureSearchEndpoint string
param azureSearchIndex string = 'default'
param azureSearchEmbeddingModel string = 'text-embedding-ada-002'

var appSettingsArray = filter(array(appDefinition.settings), i => i.name != '')
var secrets = map(filter(appSettingsArray, i => i.?secret != null), i => {
  name: i.name
  value: i.value
  secretRef: i.?secretRef ?? take(replace(replace(toLower(i.name), '_', '-'), '.', '-'), 32)
})
var env = map(filter(appSettingsArray, i => i.?secret == null), i => {
  name: i.name
  value: i.value
})

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: containerRegistryName
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' existing = {
  name: containerAppsEnvironmentName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: containerRegistry
  name: guid(subscription().id, resourceGroup().id, identity.id, 'acrPullRole')
  properties: {
    roleDefinitionId:  subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalType: 'ServicePrincipal'
    principalId: identity.properties.principalId
  }
}

module fetchLatestImage '../modules/fetch-container-image.bicep' = {
  name: '${name}-fetch-image'
  params: {
    exists: exists
    name: name
  }
}

resource app 'Microsoft.App/containerApps@2023-05-02-preview' = {
  name: name
  location: location
  tags: union(tags, {'azd-service-name':  'rag-service' })
  dependsOn: [ acrPullRole ]
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: { '${identity.id}': {} }
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress:  {
        external: false
        targetPort: 80
        transport: 'auto'
        corsPolicy: {
          allowedOrigins: union(allowedOrigins, [
            // define additional allowed origins here
          ])
        }
      }
      registries: [
        {
          server: '${containerRegistryName}.azurecr.io'
          identity: identity.id
        }
      ]
      secrets: union([
          {
            name: 'azure-cosmos-connection-string'
            value: cosmosDbConnectionString
          }
          {
            name: 'azure-search-key'
            value: azureSearchKey
          }
      ],
      map(secrets, secret => {
        name: secret.secretRef
        value: secret.value
      }))
    }
    template: {
      containers: [
        {
          image: fetchLatestImage.outputs.?containers[?0].?image ?? 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
          name: 'main'
          env: union([
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: applicationInsights.properties.ConnectionString
            }
            {
              name: 'MONGODB_CONNECTION_STRING'
              secretRef: 'azure-cosmos-connection-string'
             }
            {
              name: 'PORT'
              value: '80'
            }
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: azureOpenAiEndpoint
            }
            {
              name: 'AZURE_OPENAI_API_KEY'
              value: azureOpenAiApiKey
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT_NAME'
              value: azureOpenDeploymentName
            }
            {
                          name: 'AZURE_SEARCH_KEY'
                          secretRef: 'azure-search-key'
            }
            {
                          name: 'AZURE_SEARCH_ENDPOINT'
                          value: azureSearchEndpoint
            }
            {
                          name: 'AZURE_SEARCH_INDEX'
                          value: azureSearchIndex
            }
            {
                          name: 'AZURE_SEARCH_EMBEDDING_MODEL'
                          value: azureSearchEmbeddingModel
            }
          ],
          env,
          map(secrets, secret => {
            name: secret.name
            secretRef: secret.secretRef
          }))
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}

output defaultDomain string = containerAppsEnvironment.properties.defaultDomain
output name string = app.name
output uri string = 'https://${app.properties.configuration.ingress.fqdn}'
output id string = app.id
