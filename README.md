## Secret Retrieval From HCP Vault Using AppRole Authentication 						With Astro

### Step: 1
Storing secrets in your Vault cluster using Vault CLI:

vault kv put secret/variables/<secret-key> value=<secret-value>

### Step: 2
Creating a ACL policy to retrieve secret from your Vault cluster:

path "secret/data/variables/*" {
  capabilities = ["read", "list"]
}




### Step: 3
Creating a AppRole and attaching the created policy with it:

vault write auth/approle/role/<AppRole-name> \
secret_id_ttl=0m \
token_num_uses=10 \
token_ttl=20m \
token_max_ttl=30m \
secret_id_num_uses=0 \
policies=”<your_policy_name>”

### Step: 4
retrieve the role-id and secret-id for your AppRole by running following commands:

vault read auth/approle/role/<your-approle>/role-id
vauld write -f auth/approle/role/<your-approle>/secret-id

### Step: 5
Test if the created AppRole is successfully retrieving your secret.
First to get a client_token for your AppRole use the following command:

curl --request POST
--data '{"role_id": "your_role_id", "secret_id": "your_secret_id"}'
your_cluster_url/v1/admin/auth/approle/login

copy the client_token received in output and use to retrieve your secret by using:
curl --header "X-Vault-Token: client_token_for_your_approle"
your_cluster_url/v1/admin/secret/data/variables/<secret-key>

### Step: 6
Initialize Astro on your machine locally
Create a empty directory and run the following command in it:

1. astro dev init
2. astro dev start

This should initialize your astro project

### Step: 7
Open your requirement.txt file created by astro and paste:

apache-airflow-providers-hashicorp

Then, add the following environment variables to your “Dockerfile”:

ENV AIRFLOW__SECRETS__BACKEND = airflow.providers.hashicorp.secrets.vault.VaultBackend

ENV AIRFLOW__SECRETS__BACKEND_KWARGS = '{"connections_path" :"connections", "variables_path": "variables","namespace": "admin", "mount_point": "secret", "config_path": null, "url": "<your-cluster-url”, "auth_type": "approle", "role_id":"<your-AppRole-role-id>", "secret_id":"<your-AppRole-secret-id>"}' 

### Step: 8

Create your DAG in DAG’s folder created by astro

from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_var():
    my_var = Variable.get("airflow")
    print(f'My variable is: {my_var}')

with DAG('vault_astro_connection', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:
    test_task = PythonOperator(task_id='test-task',python_callable=print_var,)


### Step: 9

To push your configuration changes run:

astro dev restart

After this you can test your DAG using the Airflow UI provided by astro on your local machine. You should be able to see your secret value in your DAG logs



### Step: 10

Before deploying these changes in your astronomer account, remove the environment variables from your Dockerfile and place them as variables marked as secrets in your astronomer deployment.




### Step: 11

Deploy these changes in your Astronomer account.
(a) Login to Astro using CLI
(b) List your deployments by using
      astro deployment list
(c) Copy the deployment ID of your deployment in which you want to push your DAG
(d) deploy your changes in required astronomer deployment by running:
      astro deploy <deployment-id> -f
      
