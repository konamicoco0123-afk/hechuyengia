import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
from PIL import ImageTk, Image
import os
from machines_desc import machine_descriptions
from data import rules, machines, brands, purposes, specials, cpus, rams, ssds, prices
def get_description(code, mapping):
    return mapping.get(code.upper(), 'Không xác định')

def get_key_from_value(mapping, value):
    for k, v in mapping.items():
        if v == value:
            return k
    return None

def recommend(user_inputs):
    key_parts = []
    for cat in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        if cat in user_inputs:
            key_parts.append(user_inputs[cat])
        else:
            return None
    key = '^'.join(key_parts)
    return rules.get(key, None)
def show_detail_window(p_code, machine_name, description):
    """Mở cửa sổ chi tiết với ảnh + mô tả"""
    detail_win = Toplevel()
    detail_win.title(f"Chi tiết: {machine_name} ({p_code})")
    detail_win.geometry("700x700")
    detail_win.resizable(False, False)
    p_num = p_code[1:]
    image_path = os.path.join("anhmay", f"{p_num}.png")
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((600, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label_img = tk.Label(detail_win, image=photo)
            label_img.image = photo
            label_img.pack(pady=10)
        except Exception as e:
            tk.Label(detail_win, text=f"Lỗi load ảnh: {e}").pack(pady=10)
    else:
        tk.Label(detail_win, text="Không tìm thấy ảnh minh họa").pack(pady=10)
    tk.Label(detail_win, text=machine_name, font=("Arial", 14, "bold")).pack(pady=5)
    desc_text = description if description else "Hiện chưa có mô tả chi tiết cho máy này."
    tk.Label(detail_win, text=desc_text, wraplength=650, justify="left").pack(pady=10, padx=20)
def on_consult():
    user_inputs = {}
    brand_name = brand_var.get()
    if brand_name:
        brand_code = get_key_from_value(brands, brand_name)
        if brand_code:
            user_inputs['A'] = brand_code
    purpose_name = purpose_var.get()
    if purpose_name:
        purpose_code = get_key_from_value(purposes, purpose_name)
        if purpose_code:
            user_inputs['B'] = purpose_code
    special_name = special_var.get()
    if special_name:
        special_code = get_key_from_value(specials, special_name)
        if special_code:
            user_inputs['C'] = special_code 
    cpu_name = cpu_var.get()
    if cpu_name:
        cpu_code = get_key_from_value(cpus, cpu_name)
        if cpu_code:
            user_inputs['D'] = cpu_code
    ram_name = ram_var.get()
    if ram_name:
        ram_code = get_key_from_value(rams, ram_name)
        if ram_code:
            user_inputs['E'] = ram_code
    ssd_name = ssd_var.get()
    if ssd_name:
        ssd_code = get_key_from_value(ssds, ssd_name)
        if ssd_code:
            user_inputs['F'] = ssd_code 
    price_name = price_var.get()
    if price_name:
        price_code = get_key_from_value(prices, price_name)
        if price_code:
            user_inputs['G'] = price_code
    
    if len(user_inputs) < 7:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ các yêu cầu để hệ thống có thể tư vấn.")
        return
    p_code = recommend(user_inputs)
    if p_code is None:
        messagebox.showinfo("Kết quả", "Hiện tại không có máy phù hợp với yêu cầu của bạn.")
        return
    if p_code not in machines:
        messagebox.showinfo("Kết quả", "Không tìm thấy thông tin máy này.")
        return
    machine_name = machines[p_code]
    description = machine_descriptions.get(p_code, "Hiện chưa có mô tả chi tiết cho máy này.")
    result_text = f"Bạn nên chọn máy: {machine_name}\n\n"
    result_text += f"**Mô tả ngắn:**\n{description[:200]}...\n\n"
    result_text += f"Thương hiệu: {brand_name}\n"
    result_text += f"Mục đích: {purpose_name}\n"
    result_text += f"Yêu cầu đặc biệt: {special_name}\n"
    result_text += f"CPU: {cpu_name}\n"
    result_text += f"RAM: {ram_name}\n"
    result_text += f"SSD: {ssd_name}\n"
    result_text += f"Giá: {price_name}\n"
    if messagebox.askyesno("Kết quả tư vấn", result_text + "\n\nBạn muốn xem ảnh minh họa và mô tả đầy đủ không?"):
        show_detail_window(p_code, machine_name, description)
def show_contact_info():
    contact_win = Toplevel()
    contact_win.title("Thông tin liên hệ")
    contact_win.geometry("400x200")
    contact_text = """
Email: konamicoco0123@gmail.com
SĐT: 0329339523
Địa chỉ: Cao Lãnh, Đồng Tháp, Việt Nam
Website: www.hechuyengia.com
"""
    tk.Label(contact_win, text=contact_text, justify="left", padx=10, pady=10).pack()
    tk.Button(contact_win, text="Đóng", command=contact_win.destroy).pack(pady=10)
def show_terms():
    terms_win = Toplevel()
    terms_win.title("Điều khoản sử dụng")
    terms_win.geometry("500x300")
    terms_text = """
Hệ thống tư vấn chỉ mang tính tham khảo dựa trên dữ liệu có sẵn.
Không đảm bảo 100% chính xác hoặc phù hợp tuyệt đối.
Người dùng chịu trách nhiệm cuối cùng cho quyết định mua hàng.
Không chịu trách nhiệm về bất kỳ thiệt hại nào phát sinh.
Cập nhật dữ liệu đến năm 2026.
"""
    text_widget = tk.Text(terms_win, wrap=tk.WORD, font=("Arial", 10))
    text_widget.insert(tk.END, terms_text)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tk.Button(terms_win, text="Đóng", command=terms_win.destroy).pack(pady=10)
def on_close():
    messagebox.showinfo("Cảm ơn", "Cảm ơn bạn đã sử dụng hệ chuyên gia tư vấn máy tính để bàn!")
    root.destroy()
root = tk.Tk()
root.title("Hệ Chuyên Gia Tư Vấn Máy Tính Để Bàn")
root.geometry("700x800")
root.protocol("WM_DELETE_WINDOW", on_close)
image_path = os.path.join("bia.png")
if os.path.exists(image_path):
    img = Image.open(image_path)
    img = img.resize((600, 300), Image.Resampling.LANCZOS) 
    photo = ImageTk.PhotoImage(img)
    label_image = tk.Label(root, image=photo)
    label_image.pack(pady=0)
brand_var = tk.StringVar()
purpose_var = tk.StringVar()
special_var = tk.StringVar()
cpu_var = tk.StringVar()
ram_var = tk.StringVar()
ssd_var = tk.StringVar()
price_var = tk.StringVar()
tk.Label(root, text="Thương hiệu:").pack(anchor="w", padx=10)
brand_combo = ttk.Combobox(root, textvariable=brand_var, values=list(brands.values()), state="readonly")
brand_combo.pack(fill="x", padx=10, pady=5)
tk.Label(root, text="Mục đích sử dụng:").pack(anchor="w", padx=10)
purpose_combo = ttk.Combobox(root, textvariable=purpose_var, values=list(purposes.values()), state="readonly")
purpose_combo.pack(fill="x", padx=10, pady=5)
tk.Label(root, text="Yêu cầu đặc biệt:").pack(anchor="w", padx=10)
special_combo = ttk.Combobox(root, textvariable=special_var, values=list(specials.values()), state="readonly")
special_combo.pack(fill="x", padx=10, pady=5)
tk.Label(root, text="CPU:").pack(anchor="w", padx=10)
cpu_combo = ttk.Combobox(root, textvariable=cpu_var, values=list(cpus.values()), state="readonly")
cpu_combo.pack(fill="x", padx=10, pady=5)
tk.Label(root, text="RAM:").pack(anchor="w", padx=10)
ram_combo = ttk.Combobox(root, textvariable=ram_var, values=list(rams.values()), state="readonly")
ram_combo.pack(fill="x", padx=10, pady=5)
tk.Label(root, text="SSD:").pack(anchor="w", padx=10)
ssd_combo = ttk.Combobox(root, textvariable=ssd_var, values=list(ssds.values()), state="readonly")
ssd_combo.pack(fill="x", padx=10, pady=5)
tk.Label(root, text="Giá dao động:").pack(anchor="w", padx=10)
price_combo = ttk.Combobox(root, textvariable=price_var, values=list(prices.values()), state="readonly")
price_combo.pack(fill="x", padx=10, pady=5)
button_frame = tk.Frame(root)
button_frame.pack(pady=5, fill="x")
contact_button = tk.Button(button_frame, text="Thông tin liên hệ", command=show_contact_info)
contact_button.pack(side=tk.LEFT, padx=10)
terms_button = tk.Button(button_frame, text="Điều khoản sử dụng", command=show_terms)
terms_button.pack(side=tk.LEFT, padx=10)
consult_button = tk.Button(button_frame, text="Tư vấn", command=on_consult)
consult_button.pack(side=tk.LEFT, padx=10)
root.mainloop()
