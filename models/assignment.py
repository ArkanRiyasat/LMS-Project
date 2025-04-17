from ..extensions import db  # Changed to relative import with double dots

class Assignment(db.Model):
    __tablename__ = 'assignments'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)