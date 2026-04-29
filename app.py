from flask import Flask, render_template, request, jsonify
from models import db, Brand, Purpose, Special, CPU, RAM, SSD, Price, Machine, RecommendationRule, SearchHistory
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hechuyengia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db.init_app(app)

# Create tables on startup
with app.app_context():
    db.create_all()
    
    # Only reset database if explicitly requested via environment variable
    # To reset: set RESET_DB=1 before running
    if os.getenv('RESET_DB', 'false').lower() == 'true':
        print("⚠️  Resetting database...")
        db.drop_all()
        db.create_all()
    
    # Populate initial data
    from machines_desc import machine_descriptions
    from data import rules
    
    # Add categories
    brands = [
        Brand(code='A1', name='Dell'),
        Brand(code='A2', name='HP'),
        Brand(code='A3', name='ASUS'),
        Brand(code='A4', name='Acer'),
    ]
    purposes = [
        Purpose(code='B1', name='Văn phòng'),
        Purpose(code='B2', name='Gaming'),
        Purpose(code='B3', name='Đồ họa'),
    ]
    specials = [
        Special(code='C1', name='Cần nhiều cổng kết nối'),
        Special(code='C2', name='Độ bền, ổn định cao'),
    ]
    cpus = [
        CPU(code='D1', name='i5/Ryzen5'),
        CPU(code='D2', name='i7/Ryzen7'),
    ]
    rams = [
        RAM(code='E1', name='16GB'),
        RAM(code='E2', name='32GB trở lên'),
    ]
    ssds = [
        SSD(code='F1', name='256GB'),
        SSD(code='F2', name='512GB trở lên'),
    ]
    prices = [
        Price(code='G1', name='Dưới 30 triệu VND', min_price=0, max_price=30000000),
        Price(code='G2', name='30 triệu VND trở lên', min_price=30000000, max_price=999999999),
    ]
    
    db.session.add_all(brands + purposes + specials + cpus + rams + ssds + prices)
    db.session.commit()
    
    # Add machines
    machine_names = {
        'P1': 'Dell Precision 3660 Tower',
        'P2': 'PC ASUS B760 / i7-13700',
        'P3': 'HP Z2 Tower G9',
        'P4': 'Acer Predator Orion 5000',
        'P5': 'Dell OptiPlex 7010 Tower',
        'P6': 'HP ProTower 400 G9',
        'P7': 'Asus ProArt Station PD5',
        'P8': 'Acer Aspire TC-1780',
        'P9': 'Asus ExpertCenter D5',
        'P10': 'Dell Vostro 3020 Tower',
        'P11': 'HP Z4 G5 Workstation Tower',
        'P12': 'Acer Veriton M6700G Tower',
        'P13': 'Asus ExpertCenter D7 Tower',
        'P14': 'HP EliteTower 800 G9',
        'P15': 'Acer Veriton M4690G',
        'P16': 'Acer Nitro 50 (N50-650)',
        'P17': 'Acer ConceptD 300',
        'P18': 'Dell OptiPlex Small Form Factor',
        'P19': 'Dell Inspiron Desktop (3020 MT)',
        'P20': 'Asus ExpertCenter D7 SFF',
        'P21': 'HP Pro SFF 400 G9',
        'P22': 'HP Victus 15L',
        'P23': 'Acer Veriton S6690G',
        'P24': 'Dell XPS 8960'
    }
    
    for code, desc in machine_descriptions.items():
        machine = Machine(
            code=code,
            name=machine_names.get(code, code),
            brand='',
            description=desc,
            price=0,
            image_path=''
        )
        db.session.add(machine)
    db.session.commit()
    
    # Add recommendation rules
    for rule_key, machine_code in rules.items():
        parts = rule_key.split('^')
        if len(parts) == 7:
            rule = RecommendationRule(
                rule_key=rule_key,
                brand_code=parts[0],
                purpose_code=parts[1],
                special_code=parts[2],
                cpu_code=parts[3],
                ram_code=parts[4],
                ssd_code=parts[5],
                price_code=parts[6],
                machine_code=machine_code
            )
            db.session.add(rule)
    db.session.commit()

# Mapping giữa category code và model class
CODE_MODEL_MAP = {
    'A': Brand,
    'B': Purpose,
    'C': Special,
    'D': CPU,
    'E': RAM,
    'F': SSD,
    'G': Price
}

def get_code_by_category(category, display_name):
    """Lấy code từ tên display dựa vào category (A-G)"""
    if category not in CODE_MODEL_MAP:
        return None
    model_class = CODE_MODEL_MAP[category]
    obj = model_class.query.filter_by(name=display_name).first()
    return obj.code if obj else None

def recommend(user_inputs):
    """Generate recommendation based on user inputs"""
    key_parts = []
    for cat in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        if cat in user_inputs:
            key_parts.append(user_inputs[cat])
        else:
            return None
    key = '^'.join(key_parts)
    
    # Tìm trong database
    rule = RecommendationRule.query.filter_by(rule_key=key).first()
    return rule.machine_code if rule else None

@app.route('/')
def index():
    """Home page with recommendation form"""
    brands_list = Brand.query.all()
    purposes_list = Purpose.query.all()
    specials_list = Special.query.all()
    cpus_list = CPU.query.all()
    rams_list = RAM.query.all()
    ssds_list = SSD.query.all()
    prices_list = Price.query.all()
    
    context = {
        'brands': [b.name for b in brands_list],
        'purposes': [p.name for p in purposes_list],
        'specials': [s.name for s in specials_list],
        'cpus': [c.name for c in cpus_list],
        'rams': [r.name for r in rams_list],
        'ssds': [s.name for s in ssds_list],
        'prices': [p.name for p in prices_list],
    }
    return render_template('index.html', **context)

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for recommendation"""
    data = request.json
    
    user_inputs = {}
    categories = {
        'brand': 'A',
        'purpose': 'B',
        'special': 'C',
        'cpu': 'D',
        'ram': 'E',
        'ssd': 'F',
        'price': 'G'
    }
    
    # Map display names back to codes
    for field, category in categories.items():
        if data.get(field):
            code = get_code_by_category(category, data[field])
            if code:
                user_inputs[category] = code
    
    # Check if all fields are filled
    if len(user_inputs) < 7:
        return jsonify({
            'success': False,
            'message': 'Vui lòng chọn đầy đủ các yêu cầu để hệ thống có thể tư vấn.'
        }), 400
    
    # Get recommendation
    p_code = recommend(user_inputs)
    
    if p_code is None:
        return jsonify({
            'success': False,
            'message': 'Hiện tại không có máy phù hợp với yêu cầu của bạn.'
        }), 404
    
    # Lấy thông tin máy từ database
    machine = Machine.query.filter_by(code=p_code).first()
    
    if not machine:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy thông tin máy này.'
        }), 404
    
    # Check if image exists
    p_num = p_code[1:]
    image_path = os.path.join('static', 'images', f'{p_num}.png')
    image_exists = os.path.exists(image_path)
    
    # Save search history
    history = SearchHistory(
        brand_code=user_inputs.get('A'),
        purpose_code=user_inputs.get('B'),
        special_code=user_inputs.get('C'),
        cpu_code=user_inputs.get('D'),
        ram_code=user_inputs.get('E'),
        ssd_code=user_inputs.get('F'),
        price_code=user_inputs.get('G'),
        result_machine_code=p_code
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'p_code': p_code,
        'machine_name': machine.name,
        'description': machine.description,
        'image_exists': image_exists,
        'image_url': f'/static/images/{p_num}.png' if image_exists else None,
        'selections': {
            'brand': data.get('brand'),
            'purpose': data.get('purpose'),
            'special': data.get('special'),
            'cpu': data.get('cpu'),
            'ram': data.get('ram'),
            'ssd': data.get('ssd'),
            'price': data.get('price'),
        }
    })

@app.route('/api/info')
def api_info():
    """API endpoint for contact and terms info"""
    return jsonify({
        'contact': {
            'email': 'konamicoco0123@gmail.com',
            'phone': '0329339523',
            'address': 'Cao Lãnh, Đồng Tháp, Việt Nam',
            'website': 'www.hechuyengia.com'
        },
        'terms': '''
Hệ thống tư vấn chỉ mang tính tham khảo dựa trên dữ liệu có sẵn.
Không đảm bảo 100% chính xác hoặc phù hợp tuyệt đối.
Người dùng chịu trách nhiệm cuối cùng cho quyết định mua hàng.
Không chịu trách nhiệm về bất kỳ thiệt hại nào phát sinh.
Cập nhật dữ liệu đến năm 2026.
'''
    })

@app.route('/machine/<machine_code>')
def machine_detail(machine_code):
    """Detailed page for a specific machine"""
    machine = Machine.query.filter_by(code=machine_code).first()
    
    if not machine:
        return "Máy không tìm thấy", 404
    
    p_num = machine_code[1:]
    image_path = os.path.join('static', 'images', f'{p_num}.png')
    image_exists = os.path.exists(image_path)
    
    return render_template('machine_detail.html',
                          machine_code=machine_code,
                          machine_name=machine.name,
                          description=machine.description,
                          image_exists=image_exists,
                          image_url=f'/static/images/{p_num}.png' if image_exists else None)

@app.route('/api/search-history')
def get_search_history():
    """API endpoint to view search history"""
    history = SearchHistory.query.order_by(SearchHistory.created_at.desc()).limit(50).all()
    return jsonify([{
        'id': h.id,
        'brand_code': h.brand_code,
        'purpose_code': h.purpose_code,
        'special_code': h.special_code,
        'cpu_code': h.cpu_code,
        'ram_code': h.ram_code,
        'ssd_code': h.ssd_code,
        'price_code': h.price_code,
        'result_machine_code': h.result_machine_code,
        'created_at': h.created_at.isoformat()
    } for h in history])

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
