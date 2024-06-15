from typing import List

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
