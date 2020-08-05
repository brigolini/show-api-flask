from data import alchemy

class EpisodeModel(alchemy.Model):
    __tablename__ = 'episode'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(80))
    season = alchemy.Column(alchemy.Float(precision=2))

    show_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('shows.id'))
    #episode = alchemy.relationship('show.ShowModel')

    def __init__(self, name, season, show_id):
        self.name = name
        self.season = season
        self.show_id = show_id

    def json(self):
        return {'name': self.name, 'season': self.season}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    def delete_from_db(self):
        alchemy.session.delete(self)
        alchemy.session.commit()