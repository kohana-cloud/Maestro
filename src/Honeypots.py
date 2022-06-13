import yaml
import time

class Honeypot():
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = id
        self.owner = owner
        self.health = 0 #healthy
        self.last_update = int(time.time())
        self.type = None


class HP_EC2(Honeypot):
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_BottleRocket(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_ECS(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_Frost(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_Lambda(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_Deadline(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_Outpost(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_Parallel(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner


class HP_Serverless(Honeypot): 
    def __init__(self, uuid:str, owner:str) -> None:
        self.uuid = uuid
        self.owner = owner




"""LEGACY"""


def ingest_honeypots(config_file:str) -> None:
    honeypots = []

    with open(config_file, "tr") as fio:
        try:
            config_file = yaml.safe_load(fio)

            for id, config in zip(config_file['servers'],
                                  config_file['servers'].values()):
                honeypots.append(
                    VPS(id,
                        owner_email = config['owner-email'],
                        owner_name = config['owner-name'],
                        health = config['health'],
                        last_update = config['last-updated'],
                        os = config['os']
                    )
                )
            
            for id, config in zip(config_file['databases'],
                                  config_file['databases'].values()):
                honeypots.append(
                    Database(id,
                        owner_email = config['owner-email'],
                        owner_name = config['owner-name'],
                        health = config['health'],
                        last_update = config['last-updated'],
                        db_engine = config['db-engine']
                    )
                )

        except yaml.YAMLError as e:
            print(f"Error {e}")

    return honeypots
