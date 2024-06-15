from typing import List

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
