import json

def process_tournament_data(input_json):
    # کپی داده ورودی برای جلوگیری از تغییر داده اصلی
    output_json = input_json.copy()
    
    # پردازش POOLها و SEMI-FINALS
    for stage in output_json.keys():
        if stage != "REPECHAGE":  # REPECHAGE جداگانه پردازش می‌شه
            # استخراج برنده نهایی از round 1-1
            round_1_1 = output_json[stage]["round 1-1"]
            if round_1_1 and len(round_1_1) > 0:
                final_winner_entry = round_1_1[-1]  # آخرین لیست در round 1-1
                final_winner = final_winner_entry[0]["name"]  # نام برنده
                output_json[stage]["final_winner"] = final_winner
                # حذف آخرین لیست از round 1-1
                output_json[stage]["round 1-1"] = round_1_1[:-1]
    
    # پردازش REPECHAGE
    if "REPECHAGE" in output_json:
        round_1_2 = output_json["REPECHAGE"]["round 1-2"]
        final_winners = []
        if len(round_1_2) >= 2:
            # دو لیست آخر در round 1-2
            for entry in round_1_2[-2:]:
                final_winners.append(entry[0]["name"])  # نام فرد در لیست
        output_json["REPECHAGE"]["final_winners"] = final_winners
    
    return output_json

# تابع برای خواندن و پردازش فایل JSON
def process_json_file(input_file_path, output_file_path):
    try:
        # خواندن فایل JSON
        with open(input_file_path, 'r', encoding='utf-8') as file:
            input_data = json.load(file)
        
        # پردازش داده
        processed_data = process_tournament_data(input_data)
        
        # ذخیره خروجی در فایل جدید
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)
        
        print(f"فایل با موفقیت پردازش و در {output_file_path} ذخیره شد.")
    
    except FileNotFoundError:
        print(f"فایل {input_file_path} یافت نشد.")
    except json.JSONDecodeError:
        print("خطا در خواندن فایل JSON: ساختار فایل معتبر نیست.")
    except Exception as e:
        print(f"خطایی رخ داد: {str(e)}")

# مثال استفاده
if __name__ == "__main__":
    # مسیر فایل ورودی و خروجی
    input_file = "F--63 kg.json"  # فایل JSON ورودی
    output_file = "output.json"  # فایل JSON خروجی
    
    # اجرای تابع
    process_json_file(input_file, output_file)