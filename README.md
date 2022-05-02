# az-partner-center-cli
This application wraps the swagger generate client of the partner ingestion apis. 
The documentation can be found [here](https://apidocs.microsoft.com/services/partneringestion/#/)

## Requirements.


Python 3.7+ (Expected to work with Python 3.6+)

# Command Line
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


#### Install
```shell script
# Must not use -e when doing pip install

# From Production Release PyPi
pip install az-partner-center-cli

# From Release Candidate PyPi
pip install --extra-index-url=https://test.pypi.com/simple/ az-partner-center-cli

# From Source
git clone https://github.com/microsoft/az-partner-center-cli
pip install az-partner-center-cli
```

#### Usage
```shell script
ama_name='sample-test'
product_id=$(ama create --ama-name $ama_name 2>&1 | jq '.product_id' -r)
ama publish --ama-name $ama_name --product-id $product_id

ama status --product-id $product_id

ama delete --product-id $product_id
```


## Setup
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

# Usage

## 
```python
""" Create New Azure Managed Application """
from  azureiai.managed_apps import ManagedApplication 
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
from azureiai.managed_apps import ManagedApplication 

ama_name="Sample-App"
config_yaml="az-partner-center-cli/config.yml"
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
from azureiai.managed_apps import ManagedApplication 

ama_name="Sample-App"
config_yaml="az-partner-center-cli/config.yml"

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
from azureiai.managed_apps import ManagedApplication 

ama_name="Sample-App"
config_yaml="az-partner-center-cli/config.yml"
manifest_yml="az-partner-center-cli/manifest.yml"

ama = ManagedApplication(
    ama_name,
    config_yml
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
from azureiai.managed_apps import ManagedApplication 

ama_name="Sample-App"
config_yaml="az-partner-center-cli/config.yml"
plan_name="FirstOffer"

app_path = "az-partner-center-cli"
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
    app=app,
    logo_small=logo_small,
    logo_medium=logo_medium,
    logo_large=logo_large,
    logo_wide=logo_wide
)
ama.publish()
ama.promote()
```


# Databricks Deployment

```shell script
ama db create resource \
  --resource-id $DATABRICKS_RESOURCE_ID \
  --host $DATABRICKS_WORKSPACE_URL

ama db create compute \
  --resource-id $DATABRICKS_RESOURCE_ID \
  --host $DATABRICKS_WORKSPACE_URL
```
