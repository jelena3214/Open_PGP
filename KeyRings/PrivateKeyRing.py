from KeyRings.PrivateKey import PrivateKey


class PrivateKeyRing:
    def __init__(self):
        self.private_keys = []

    def add_new_private_key(self, name, email, public_key, private_key, passphrase):
        new_key = PrivateKey(name, email, passphrase, public_key, private_key)
        self.private_keys.append(new_key)

    def delete_private_key(self, key_id):
        for key in self.private_keys:
            if key.key_id == key_id:
                self.private_keys.remove(key)

    def get_key_by_key_id(self, key_id):
        if key_id == 0 and len(self.private_keys) > 0:
            return self.private_keys[0]

        for key in self.private_keys:
            if key.key_id == key_id:
                return key
        return None

    def get_keys_by_user_id(self, user_id):
        user_keys = []
        for key in self.private_keys:
            if key.user_id == user_id:
                user_keys.append(key)
        return user_keys

    def get_all_keys(self):
        return self.private_keys
