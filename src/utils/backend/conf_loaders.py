import yaml


def load_config(config_path='app_cfg.yaml', custom_key=None):

    with open(config_path, encoding='utf-8') as file:
        data = file.read()
        data = yaml.safe_load(data)

    if custom_key:
        return data[custom_key]
