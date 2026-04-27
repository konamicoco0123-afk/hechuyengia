from flask import Flask, render_template, request, jsonify
from models import db, Brand, Purpose, Special, CPU, RAM, SSD, Price, Machine, RecommendationRule, SearchHistory
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hechuyengia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db.init_app(app)

def get_brand_code(brand_name):
    """Lấy code từ tên brand"""
    brand = Brand.query.filter_by(name=brand_name).first()
    return brand.code if brand else None

def get_purpose_code(purpose_name):
    """Lấy code từ tên purpose"""
    purpose = Purpose.query.filter_by(name=purpose_name).first()
    return purpose.code if purpose else None

def get_special_code(special_name):
    """Lấy code từ tên special"""
    special = Special.query.filter_by(name=special_name).first()
    return special.code if special else None

def get_cpu_code(cpu_name):
    """Lấy code từ tên cpu"""
    cpu = CPU.query.filter_by(name=cpu_name).first()
    return cpu.code if cpu else None

def get_ram_code(ram_name):
    """Lấy code từ tên ram"""
    ram = RAM.query.filter_by(name=ram_name).first()
    return ram.code if ram else None

def get_ssd_code(ssd_name):
    """Lấy code từ tên ssd"""
    ssd = SSD.query.filter_by(name=ssd_name).first()
    return ssd.code if ssd else None

def get_price_code(price_name):
    """Lấy code từ tên price"""
    price = Price.query.filter_by(name=price_name).first()
    return price.code if price else None

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
    
    # Map display names back to codes
    if data.get('brand'):
        code = get_brand_code(data['brand'])
        if code:
            user_inputs['A'] = code
    
    if data.get('purpose'):
        code = get_purpose_code(data['purpose'])
        if code:
            user_inputs['B'] = code
    
    if data.get('special'):
        code = get_special_code(data['special'])
        if code:
            user_inputs['C'] = code
    
    if data.get('cpu'):
        code = get_cpu_code(data['cpu'])
        if code:
            user_inputs['D'] = code
    
    if data.get('ram'):
        code = get_ram_code(data['ram'])
        if code:
            user_inputs['E'] = code
    
    if data.get('ssd'):
        code = get_ssd_code(data['ssd'])
        if code:
            user_inputs['F'] = code
    
    if data.get('price'):
        code = get_price_code(data['price'])
        if code:
            user_inputs['G'] = code
    
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

if __name__ == '__main__':
    app.run(debug=True)
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
