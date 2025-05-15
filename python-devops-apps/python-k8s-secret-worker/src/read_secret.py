import os
from kubernetes import client, config

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    namespace = os.getenv('SECRET_NAMESPACE', 'default')
    secret_name = os.getenv('SECRET_NAME')

    if secret_name:
        try:
            secret = v1.read_namespaced_secret(secret_name, namespace)
            print(f"Secret '{secret_name}' in namespace '{namespace}':")
            print(secret.data)  # Base64-encoded
        except client.exceptions.ApiException as e:
            print(f"Error fetching secret '{secret_name}': {e}")
    else:
        print(f"Listing all secrets in namespace '{namespace}':")
        secrets = v1.list_namespaced_secret(namespace)
        for s in secrets.items:
            print(f"Name: {s.metadata.name}")

if __name__ == '__main__':
    main()
