import requests
import json

# آدرس فرضی API (باید URL واقعی رو پیدا کنید)
api_url = "https://judotv.com/api/competitions/cont_cup_cad_uzb2022/draw"

# هدرهای درخواست (در صورت نیاز به احراز هویت یا توکن)
headers = {
    "Content-Type": "application/json",
    # اگه API نیاز به کلید داشته باشه: "Authorization": "Bearer YOUR_API_KEY"
}

try:
    # ارسال درخواست GET به API
    response = requests.get(api_url, headers=headers)
    
    # چک کردن وضعیت پاسخ
    if response.status_code == 200:
        # تبدیل پاسخ به JSON
        data = response.json()
        
        # چاپ داده‌ها (مثل قرعه‌کشی، شرکت‌کننده‌ها، و غیره)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # ذخیره داده‌ها تو فایل JSON
        with open("competition_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print(f"خطا در درخواست: کد وضعیت {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"خطا در اتصال به API: {e}")