from database import db
from url_utils import normalize_picture_urls


def default_access_hours():
    """Default 7-day schedule: closed all days."""
    return [["00:00", "00:00"] for _ in range(7)]


class StudySpot(db.Model):
    """
    Study spot model: locations for studying with metadata and amenities.
    """
    __tablename__ = 'study_spots'

    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(50), nullable=False)
    study_spot_name = db.Column(db.String(200), nullable=False)
    building_name = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(500), nullable=False)
    floor = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.JSON, nullable=False, default=lambda: [])
    pictures = db.Column(db.JSON, nullable=False, default=lambda: [])
    noise_level = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    spot_type = db.Column(db.JSON, nullable=False, default=lambda: [])
    access_hours = db.Column(db.JSON, nullable=False, default=default_access_hours)
    near_food = db.Column(db.Boolean, nullable=False, default=False)
    additional_properties = db.Column(db.Text, nullable=True)
    reservable = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """Convert model instance to dictionary for JSON responses."""
        return {
            'id': self.id,
            'abbreviation': self.abbreviation,
            'study_spot_name': self.study_spot_name,
            'building_name': self.building_name,
            'address': self.address,
            'floor': self.floor,
            'tags': self.tags if self.tags is not None else [],
            'pictures': normalize_picture_urls(self.pictures),
            'noise_level': self.noise_level,
            'capacity': self.capacity,
            'spot_type': self.spot_type if self.spot_type is not None else [],
            'access_hours': self.access_hours,
            'near_food': self.near_food,
            'additional_properties': self.additional_properties,
            'reservable': self.reservable,
            'description': self.description,
        }

    def __repr__(self):
        return f'<StudySpot {self.id}: {self.study_spot_name}>'
