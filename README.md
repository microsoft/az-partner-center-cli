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
1. Complete `manifest.yml` with pointers to required files.
    1. managed_app.zip
    1. app_listing_config.json
    1. Small Logo Image (png) - 48x48
    1. Medium Logo Image (png) - 90x90
    1. Large Logo Image (png) - 216x216
    1. Wide Logo Image (png) - 255x115
1. Login using `az login`.

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
### Azure Login
1. Login to Azure via `az login`

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
