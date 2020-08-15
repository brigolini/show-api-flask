from data import alchemy


class UserModel(alchemy.Model):
    __tablename__ = 'user'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(80))
    password = alchemy.Column(alchemy.String(80))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def json(self):
        return {'name': self.name, 'password': self.password}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    def delete_from_db(self):
        alchemy.session.delete(self)
        alchemy.session.commit()
