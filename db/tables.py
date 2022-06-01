from db.instance import DB


class Item(DB.Model):
    __tablename__ = 'Items'

    _id = DB.Column(DB.Integer, primary_key=True)
    _name = DB.Column(DB.String, unique=True, nullable=False)

    def __init__(self, item_id: int, name: str):
        self._id = item_id
        self._name = name


class User(DB.Model):
    __tablename__ = 'Users'

    vk_id = DB.Column(DB.Integer, primary_key=True)
    is_active = DB.Column(DB.Boolean, nullable=False)
    profile_key = DB.Column(DB.String, unique=True, nullable=False)
    equipment = DB.Column(DB.String)
    class_id = DB.Column(DB.Integer, nullable=False)
    is_leader = DB.Column(DB.Boolean, nullable=False)
    is_officer = DB.Column(DB.Boolean, nullable=False)

    def __init__(self, vk_id: int, prof_key: str, equip: str, class_id: int):
        self.vk_id = vk_id
        self.is_active = True
        self.profile_key = prof_key
        self.equipment = equip
        self.class_id = class_id
        self.is_leader = False
        self.is_officer = False

    def __repr__(self):
        return f"vk_id: {self.vk_id}\n" \
               f"is_active: {self.is_active}\n" \
               f"profile_key: {self.profile_key}\n" \
               f"equipment: {self.equipment}\n" \
               f"class_id: {self.class_id}\n" \
               f"is_leader: {self.is_leader}\n" \
               f"is_officer: {self.is_officer}\n"

    def __str__(self):
        return f"vk_id: {self.vk_id}\n" \
               f"is_active: {self.is_active}\n" \
               f"profile_key: {self.profile_key}\n" \
               f"equipment: {self.equipment}\n" \
               f"class_id: {self.class_id}\n" \
               f"is_leader: {self.is_leader}\n" \
               f"is_officer: {self.is_officer}\n" \
