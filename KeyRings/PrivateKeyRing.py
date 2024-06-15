import json
from typing import List

import context
from KeyRings.PrivateKey import PrivateKey


class PrivateKeyRing:
    def __init__(self):
        self.private_keys = {}

    def add_new_private_key(self, name, email, public_key, private_key, passphrase, timestamp=None):
        new_key = PrivateKey(name, email, passphrase, public_key, private_key, timestamp)
        self.private_keys[new_key.key_id] = new_key

    def delete_private_key(self, key_id):
        if key_id in self.private_keys:
            del self.private_keys[key_id]

    def get_key_by_key_id(self, key_id) -> PrivateKey:
        return self.private_keys.get(key_id)

    def get_key_by_email(self, email) -> PrivateKey:
        for key in self.private_keys.values():
            if key.email == email:
                return key
        return None

    def get_all_data(self) -> List[PrivateKey]:
        return list(self.private_keys.values())

    def export_all_private_keys(self, file_path):
        with open(file_path, 'w') as file:
            json_data = [pk.to_dict() for pk in self.get_all_data()]
            json.dump(json_data, file, default=str, indent=4)

    @classmethod
    def import_all_private_keys(cls, file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            private_keys = [PrivateKey.from_dict(data) for data in json_data]
        for key in private_keys:
            context.private_key_ring.private_keys[key.key_id] = key
