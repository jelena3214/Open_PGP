from KeyRings.PublicKey import PublicKey


class PublicKeyRing:
    def __init__(self):
        self.public_keys = {}

    def add_new_public_key(self, name, email, public_key):
        new_key = PublicKey(public_key, name, email)
        self.public_keys[new_key.key_id] = new_key

    def delete_public_key(self, key_id):
        if key_id in self.public_keys:
            del self.public_keys[key_id]

    def get_key_by_key_id(self, key_id):
        return self.private_keys.get(key_id)

    def get_key_by_email(self, email) -> PublicKey:
        for key in self.public_keys.values():
            if key.email == email:
                return key
        return None

    def get_all_keys(self):
        return list(self.public_keys.values())
