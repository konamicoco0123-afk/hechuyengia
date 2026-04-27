from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Category Tables
class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Purpose(db.Model):
    __tablename__ = 'purposes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Special(db.Model):
    __tablename__ = 'specials'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CPU(db.Model):
    __tablename__ = 'cpus'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RAM(db.Model):
    __tablename__ = 'rams'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SSD(db.Model):
    __tablename__ = 'ssds'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    min_price = db.Column(db.Integer)  # Giá tối thiểu (VND)
    max_price = db.Column(db.Integer)  # Giá tối đa (VND)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Machine Table
class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer)  # Giá bán (VND)
    image_path = db.Column(db.String(200))  # Đường dẫn ảnh
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'brand': self.brand,
            'description': self.description,
            'price': self.price,
            'image_path': self.image_path
        }

# Recommendation Rule Table
class RecommendationRule(db.Model):
    __tablename__ = 'recommendation_rules'
    id = db.Column(db.Integer, primary_key=True)
    # Rule key format: A1^B1^C1^D1^E1^F1^G1
    rule_key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    brand_code = db.Column(db.String(10), nullable=False)
    purpose_code = db.Column(db.String(10), nullable=False)
    special_code = db.Column(db.String(10), nullable=False)
    cpu_code = db.Column(db.String(10), nullable=False)
    ram_code = db.Column(db.String(10), nullable=False)
    ssd_code = db.Column(db.String(10), nullable=False)
    price_code = db.Column(db.String(10), nullable=False)
    machine_code = db.Column(db.String(10))  # Mã máy được khuyến nghị (có thể NULL)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'rule_key': self.rule_key,
            'machine_code': self.machine_code
        }

# Search History Table (Optional - để track lịch sử tìm kiếm)
class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    brand_code = db.Column(db.String(10))
    purpose_code = db.Column(db.String(10))
    special_code = db.Column(db.String(10))
    cpu_code = db.Column(db.String(10))
    ram_code = db.Column(db.String(10))
    ssd_code = db.Column(db.String(10))
    price_code = db.Column(db.String(10))
    result_machine_code = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
