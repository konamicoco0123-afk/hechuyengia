from app import app, get_brand_code, get_purpose_code, get_special_code, get_cpu_code, get_ram_code, get_ssd_code, get_price_code, recommend
from models import Machine

with app.app_context():
    print("=" * 70)
    print("Testing brand selection fix:")
    print("=" * 70)
    
    # Test: ASUS selection
    print("\n1. Testing ASUS (A3) selection:")
    user_inputs = {
        'A': 'A3',  # ASUS
        'B': 'B1',  # Văn phòng
        'C': 'C1',  # Cần nhiều cổng kết nối
        'D': 'D1',  # i5
        'E': 'E1',  # 16GB
        'F': 'F1',  # 256GB
        'G': 'G1',  # Dưới 30 triệu
    }
    result = recommend(user_inputs)
    machine = Machine.query.filter_by(code=result).first()
    print(f"   Result: {result} - {machine.name if machine else 'Not found'}")
    if machine and 'ASUS' in machine.name:
        print("   ✓ Correct! Got an ASUS machine")
    else:
        print("   ✗ Error! Should be ASUS machine")
    
    # Test: HP selection
    print("\n2. Testing HP (A2) selection:")
    user_inputs['A'] = 'A2'  # HP
    result = recommend(user_inputs)
    machine = Machine.query.filter_by(code=result).first()
    print(f"   Result: {result} - {machine.name if machine else 'Not found'}")
    if machine and 'HP' in machine.name:
        print("   ✓ Correct! Got an HP machine")
    else:
        print("   ✗ Error! Should be HP machine")
    
    # Test: Dell selection
    print("\n3. Testing Dell (A1) selection:")
    user_inputs['A'] = 'A1'  # Dell
    result = recommend(user_inputs)
    machine = Machine.query.filter_by(code=result).first()
    print(f"   Result: {result} - {machine.name if machine else 'Not found'}")
    if machine and 'Dell' in machine.name:
        print("   ✓ Correct! Got a Dell machine")
    else:
        print("   ✗ Error! Should be Dell machine")
    
    # Test: Acer selection
    print("\n4. Testing Acer (A4) selection:")
    user_inputs['A'] = 'A4'  # Acer
    result = recommend(user_inputs)
    machine = Machine.query.filter_by(code=result).first()
    print(f"   Result: {result} - {machine.name if machine else 'Not found'}")
    if machine and 'Acer' in machine.name:
        print("   ✓ Correct! Got an Acer machine")
    else:
        print("   ✗ Error! Should be Acer machine")
