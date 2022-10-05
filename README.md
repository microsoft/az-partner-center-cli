# az-partner-center-cli
This application wraps the swagger generate client of the partner ingestion apis. 
The documentation can be found [here](https://ingestionapi-swagger.azureedge.net/#/)

## Requirements.

- Python 3.7+ (Expected to work with Python 3.6+)
- Java JDK 8

## Command Line
### Install
```shell script
# Must not use -e when doing pip install

# From Production Release PyPi
pip install az-partner-center-cli

# From Release Candidate PyPi
pip install --pre az-partner-center-cli

# From Source
git clone https://github.com/microsoft/az-partner-center-cli
cd az-partner-center-cli
pip install .
```

## Azure Partner Center (azpc) CLI Usage
### Create Manifest File
1. Copy `template.manifest.yml` and create new file `manifest.yml`.
1. Copy `template.config.yml` and create new file `config.yml`.
1. Complete `manifest.yml` with pointers to required files.
    1. managed_app.zip
    1. app_listing_config.json
    1. Small Logo Image (png) - 48x48
    1. Medium Logo Image (png) - 90x90
    1. Large Logo Image (png) - 216x216
    1. Wide Logo Image (png) - 255x115
1. Complete `config.yml`.
    * **tenant_id**: Who will publish the managed app
    * **azure_preview_subscription**: Who will be the preview audience
    * **aad_id** and **aad_secret**: Service principal used for calling partner API
    * **access_id**: Service principal will have access to managed resource group

#### config.yml
```yaml
tenant_id                   : "<Azure Tenant ID>"
azure_preview_subscription  : "<Azure Subscription>"
aad_id                      : "<Service Principal ID>"
aad_secret                  : "<Service Principal Secret>"
access_id                   : "<Service Principal ID>"
```

#### manifest.yml
```yaml
name                : "dciborow-submission"
plan_name           : "test-plan"
app_path            : "tests/sample_app"
app                 : "sample-app.zip"
json_listing_config : "sample_app_listing_config.json"
```

When the name, and plan name are provided in the manifest.yml, they do not have to be provided in the CLI commands. 
They are in the below examples for clarity on which commands use each value.

#### Managed Application
```shell
ma_name='dciborow-managed-app'
plan_name='test-plan'

cat manifest.yml

azpc ma list
azpc ma create --name $name
azpc ma show   --name $name
azpc ma update --name $name
# azpc ma delete --name $name

azpc ma plan list   --name $name
azpc ma plan create --name $name --plan-name $plan_name 
azpc ma plan show   --name $name --plan-name $plan_name
azpc ma plan update --name $name --plan-name $plan_name
# azpc ma plan delete --name $name --plan-name $plan_name

azpc ma publish --name $name
```

#### Solution Template
```shell script
name='dciborow-solution-template'
plan_name='test-plan'

cat manifest.yml

azpc st list
azpc st create --name $name
azpc st show   --name $name
azpc st update --name $name
# azpc st delete --name $name

azpc st plan list   --name $name
azpc st plan create --name $name --plan-name $plan_name 
azpc st plan show   --name $name --plan-name $plan_name
azpc st plan update --name $name --plan-name $plan_name
# azpc st plan delete --name $name --plan-name $plan_name

azpc st publish --name $name
```

#### Virtual Machine
```shell script
vm_name='dciborow-vm'
plan_name='test-plan'
config_yml='config.yml'
config_json='vm_config.json'
app_path='sample_app'
notificationEmails='default@microsoft.com'

cat manifest.yml

azpc vm list
azpc vm create --name $name --config-yml $config_yml --config-json $config_json --app-path $app_path
azpc vm show --name $name --config-yml $config_yml --config-json $config_json --app-path $app_path
azpc vm update --name $name
azpc vm publish --name $name --config-yml $config_yml --config-json $config_json --app-path $app_path
#  azpc vm delete --name $name

azpc vm plan list   --name $name
azpc vm plan create --name $name --plan-name $plan_name 
azpc vm plan show   --name $name --plan-name $plan_name
azpc vm plan update --name $name --plan-name $plan_name
# azpc vm plan delete --name $name --plan-name $plan_name

azpc vm publish --name $name --notification-emails $notificationEmails
azpc vm status --name $name
```

#### Container Image
```shell script
vm_name='dciborow-vm'
plan_name='test-plan'

cat manifest.yml

azpc co list
azpc co create --name $name
azpc co show   --name $name
azpc co update --name $name
# azpc vm delete --name $name

azpc co plan list   --name $name
azpc co plan create --name $name --plan-name $plan_name 
azpc co plan show   --name $name --plan-name $plan_name
azpc co plan update --name $name --plan-name $plan_name
# azpc co plan delete --name $name --plan-name $plan_name

azpc co publish --name $name
```

## Developer Setup
### Create Configuration File
1. Copy `template.config.yml` and create new file `config.yml`
1. Fill in tenant_id, typically `72f988bf-86f1-41af-91ab-2d7cd011db47` for Microsoft's tenant.
1. Fill in the Subscription that will have Preview access `azure_preview_subscription`
1. Create a Service Principal and provide the id `aad_id` and key `aad_secret`


### Generate Swagger Python Client
Insure Java in installed on the machine with `java -v` Download current stable 3.x.x branch (OpenAPI version 3)

```shell script
pip install -e .
```

This runs the following commands are part of the setup.py. You can also run these commands individually. 

```shell script
wget https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.22/swagger-codegen-cli-3.0.22.jar -O swagger-codegen-cli.jar
java -jar swagger-code-get-cli.jar generate -i Partner_Ingestion_SwaggerDocument.json -l python -o temp
cp temp/swagger_client ./
```

# Python SDK Usage

## 
```python
""" Create New Azure Managed Application """
from  azureiai.managed_apps.managed_app import ManagedApplication 
ama_name="Sample-App"
config_yaml="src/azureiai-managed-apps/config.yml"

ama = ManagedApplication(
    ama_name,
    config_yaml,
)
ama.create()
```

##
```python
""" Get Existing Azure Managed Application """
from azureiai.managed_apps.managed_app import ManagedApplication 

ama_name="Sample-App"
config_yaml="src/azureiai-managed-apps/config.yml"
product_id = "3d00b4ab-50e5-49af-a2e6-5d800b8979cf"

ama = ManagedApplication(
    ama_name,
    config_yaml,
)
ama.set_product_id(product_id)

```

##
```python
""" Get List of Azure Managed Applications """
from azureiai.managed_apps.managed_app import ManagedApplication 

ama_name="Sample-App"
config_yaml="src/azureiai-managed-apps/config.yml"

ama = ManagedApplication(
    ama_name,
    config_yaml,
)
offers = ama.get_offers()
for offer in offers.values:
    print(offer.name)
```

## 
```python
""" Publish Azure Managed Applications """
from azureiai.managed_apps.managed_app import ManagedApplication 

ama_name="Sample-App"
config_yaml="src/azureiai-managed-apps/config.yml"
manifest_yml="src/azureiai-managed-apps/manifest.yml"

ama = ManagedApplication(
    ama_name,
    config_yaml
)
ama.manifest_publish(
    manifest_yml=manifest_yml,
    config_yml=config_yml
)
ama.publish()
ama.promote()
```


## 
```python
""" Publish Azure Managed Applications """
from azureiai.managed_apps.managed_app import ManagedApplication 

ama_name="Sample-App"
config_yaml="src/azureiai-managed-apps/config.yml"
plan_name="FirstOffer"

app_path = "src/azureiai-managed-apps/"
app = "App.zip"
logo_small = "r_48_48.png"
logo_medium = "r_90_90.png"
logo_large = "r_216_216.png"
logo_wide = "r_255_155.png"

ama = ManagedApplication(
    ama_name,
    config_yaml,
)
ama.prepare_publish(
    plan_name=plan_name,
    app_path=app_path,
    app=app
)
ama.publish()
ama.promote()
```
