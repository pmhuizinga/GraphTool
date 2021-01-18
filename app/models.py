from app import db

class node_type(db.Model):

    __tablename__ = 'node_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=False)
    node = db.relationship('node', backref='place', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

class node(db.Model):

    __tablename__ = 'node'

    id = db.Column(db.Integer, primary_key=True)
    node_type_id = db.Column(db.Integer, db.ForeignKey('node_type.id'))
    name = db.Column(db.String(40), index=True, unique=False)

    def __repr__(self):
        return '{}'.format(self.name)

class relation_type(db.Model):

    __tablename__ = 'relation_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=False)
    relation = db.relationship('node', backref='place', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)

class relation(db.Model):

    __tablename__ = 'relation'

    id = db.Column(db.Integer, primary_key=True)
    source_node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    target_node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    relation_type_id = db.Column(db.Integer, db.ForeignKey('relation_type.id'))

    def __repr__(self):
        return '{}'.format(self.id)