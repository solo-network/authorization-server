from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'authorizationstaticfiles' # Must be replaced by your <storage_account_name>
    account_key = 'EtYqoaWQfeHWnF19+Z1VPQit99ReA3M6ue4jPUXZ4LiuLQVTDbPlRwMCPVQd8vYumRLP4Tcmw4zX+AStpqIL0A==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'authorizationstaticfiles' # Must be replaced by your storage_account_name
    account_key = 'EtYqoaWQfeHWnF19+Z1VPQit99ReA3M6ue4jPUXZ4LiuLQVTDbPlRwMCPVQd8vYumRLP4Tcmw4zX+AStpqIL0A==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None