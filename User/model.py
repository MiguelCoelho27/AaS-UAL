class User:
    def __init__(self, user_id, name, email, password):
        if user_id and name and email and password:
            self.user_id = user_id
            self.name = name
            self.email = email
            self.password = password
        else:
            self.name = name
            self.email = email
            self.password = password

    def to_json(self):
        if self.user_id and self.name and self.email and self.password:
            return {'user_id': self.user_id,'name': self.name,'email': self.email,self.password:'password'}
        else:
            return {'name': self.name,'email': self.email,self.password:'password'}