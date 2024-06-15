import json
from typing import List

import context
from KeyRings.PublicKey import PublicKey


class PublicKeyRing:
    def __init__(self):
        self.public_keys = {}

    def add_new_public_key(self, name, email, public_key, timestamp=None):
        for key in self.public_keys.values():
            if key.email == email:
                return False
        new_key = PublicKey(public_key, name, email, timestamp)
        self.public_keys[new_key.key_id] = new_key
        return True

    def delete_public_key(self, key_id):
        if key_id in self.public_keys:
            del self.public_keys[key_id]
            return True
        else:
            return False

    def get_key_by_key_id(self, key_id):
        return self.public_keys.get(key_id)

    def get_key_by_email(self, email) -> PublicKey:
        for key in self.public_keys.values():
            if key.email == email:
                return key
        return None

    def get_all_data(self) -> List[PublicKey]:
        return list(self.public_keys.values())

    def export_all_public_keys(self, file_path):
        with open(file_path, 'w') as file:
            json_data = [pk.to_dict() for pk in self.get_all_data()]
            json.dump(json_data, file, default=str, indent=4)

    @classmethod
    def import_all_public_keys(cls, file_path):
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            public_keys = [PublicKey.from_dict(data) for data in json_data]
        for key in public_keys:
            context.public_key_ring.public_keys[key.key_id] = key
