from KeyRings.PublicKey import PublicKey


class PublicKeyRing:
    def __init__(self):
        self.public_keys = []

    def add_new_public_key(self, name, email, public_key):
        new_key = PublicKey(public_key, name, email, )
        self.public_keys.append(new_key)

    def delete_public_key(self, key_id):
        for key in self.public_keys:
            if key.key_id == key_id:
                self.public_keys.remove(key)

    def get_key_by_key_id(self, key_id):
        if key_id == 0 and len(self.public_keys) > 0:
            return self.public_keys[0]

        for key in self.public_keys:
            if key.key_id == key_id:
                return key
        return None

    def get_keys_by_user_id(self, user_id):
        user_keys = []
        for key in self.public_keys:
            if key.user_id == user_id:
                user_keys.append(key)
        return user_keys

    def get_all_keys(self):
        return self.public_keys
