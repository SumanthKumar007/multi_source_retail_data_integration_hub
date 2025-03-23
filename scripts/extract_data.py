import kaggle
def extract():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('olistbr/brazilian-ecommerce',path='./data', unzip=True)