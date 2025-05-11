# import json

# # مسیر فایل JSON ورودی
# input_file = "judotv_competitions_2018-2025.json"
# # مسیر فایل خروجی فیلترشده
# output_file = "judotv_competitions_2019-2025.json"

# # خواندن داده‌ها از فایل JSON
# with open(input_file, "r", encoding="utf-8") as f:
#     data = json.load(f)

# # فیلتر کردن تورنمنت‌ها از سال ۲۰۱۹ به بعد
# filtered_data = [item for item in data if int(item.get("year", 0)) == 2019]
# print(len(filtered_data))
# # ذخیره داده‌های فیلترشده در یک فایل جدید
# # with open(output_file, "w", encoding="utf-8") as f:
# #     json.dump(filtered_data, f, indent=2, ensure_ascii=False)

# # print(f"{len(filtered_data)} تورنمنت از سال ۲۰۱۹ به بعد فیلتر و ذخیره شد.")k




import json

# خواندن دو فایل JSON
with open('filtered_competitions_2014_2019.json', 'r', encoding='utf-8') as f1:
    data1 = json.load(f1)

with open('judotv_competitions_2019-2025.json', 'r', encoding='utf-8') as f2:
    data2 = json.load(f2)

# ادغام داده‌ها
from datetime import datetime

# خواندن دو فایل JSON

# ادغام داده‌ها
combined_data = data1 + data2

# حذف موارد تکراری
unique_data = [dict(t) for t in {tuple(sorted(d.items())) for d in combined_data}]

# مرتب‌سازی بر اساس dateFrom
sorted_data = sorted(unique_data, key=lambda x: datetime.fromisoformat(x['dateFrom'].replace('Z', '+00:00')))

# ذخیره در فایل جدید
with open('2016-2025.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=2)

print("فایل‌ها با موفقیت ادغام، مرتب‌سازی و در 'merged_unique_sorted.json' ذخیره شدند.")