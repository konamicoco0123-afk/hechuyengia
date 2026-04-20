from flask import Flask, render_template, request, jsonify
from data import rules, machines, brands, purposes, specials, cpus, rams, ssds, prices
from machines_desc import machine_descriptions
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def get_key_from_value(mapping, value):
    """Convert display name to code"""
    for k, v in mapping.items():
        if v == value:
            return k
    return None

def recommend(user_inputs):
    """Generate recommendation based on user inputs"""
    key_parts = []
    for cat in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        if cat in user_inputs:
            key_parts.append(user_inputs[cat])
        else:
            return None
    key = '^'.join(key_parts)
    return rules.get(key, None)

@app.route('/')
def index():
    """Home page with recommendation form"""
    context = {
        'brands': list(brands.values()),
        'purposes': list(purposes.values()),
        'specials': list(specials.values()),
        'cpus': list(cpus.values()),
        'rams': list(rams.values()),
        'ssds': list(ssds.values()),
        'prices': list(prices.values()),
    }
    return render_template('index.html', **context)

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for recommendation"""
    data = request.json
    
    user_inputs = {}
    
    # Map display names back to codes
    if data.get('brand'):
        code = get_key_from_value(brands, data['brand'])
        if code:
            user_inputs['A'] = code
    
    if data.get('purpose'):
        code = get_key_from_value(purposes, data['purpose'])
        if code:
            user_inputs['B'] = code
    
    if data.get('special'):
        code = get_key_from_value(specials, data['special'])
        if code:
            user_inputs['C'] = code
    
    if data.get('cpu'):
        code = get_key_from_value(cpus, data['cpu'])
        if code:
            user_inputs['D'] = code
    
    if data.get('ram'):
        code = get_key_from_value(rams, data['ram'])
        if code:
            user_inputs['E'] = code
    
    if data.get('ssd'):
        code = get_key_from_value(ssds, data['ssd'])
        if code:
            user_inputs['F'] = code
    
    if data.get('price'):
        code = get_key_from_value(prices, data['price'])
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
    
    if p_code not in machines:
        return jsonify({
            'success': False,
            'message': 'Không tìm thấy thông tin máy này.'
        }), 404
    
    machine_name = machines[p_code]
    description = machine_descriptions.get(p_code, 'Hiện chưa có mô tả chi tiết cho máy này.')
    
    # Check if image exists
    p_num = p_code[1:]
    image_path = os.path.join('static', 'images', f'{p_num}.png')
    image_exists = os.path.exists(image_path)
    
    return jsonify({
        'success': True,
        'p_code': p_code,
        'machine_name': machine_name,
        'description': description,
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

@app.route('/machines/<machine_code>')
def machine_detail(machine_code):
    """Detailed page for a specific machine"""
    if machine_code not in machines:
        return "Máy không tìm thấy", 404
    
    machine_name = machines[machine_code]
    description = machine_descriptions.get(machine_code, 'Hiện chưa có mô tả chi tiết cho máy này.')
    
    p_num = machine_code[1:]
    image_path = os.path.join('static', 'images', f'{p_num}.png')
    image_exists = os.path.exists(image_path)
    
    return render_template('machine_detail.html',
                          machine_code=machine_code,
                          machine_name=machine_name,
                          description=description,
                          image_exists=image_exists,
                          image_url=f'/static/images/{p_num}.png' if image_exists else None)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
