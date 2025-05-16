from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


province_codes = {
    "001": "Hà Nội",
    "002": "Hà Giang",
    "004": "Cao Bằng",
    "006": "Bắc Kạn",
    "008": "Tuyên Quang",
    "010": "Lào Cai",
    "011": "Điện Biên",
    "012": "Lai Châu",
    "014": "Sơn La",
    "015": "Yên Bái",
    "017": "Hòa Bình",
    "019": "Thái Nguyên",
    "020": "Lạng Sơn",
    "022": "Quảng Ninh",
    "024": "Bắc Giang",
    "025": "Phú Thọ",
    "026": "Vĩnh Phúc",
    "027": "Bắc Ninh",
    "030": "Hải Dương",
    "031": "Hải Phòng",
    "033": "Hưng Yên",
    "034": "Thái Bình",
    "035": "Hà Nam",
    "036": "Nam Định",
    "037": "Ninh Bình",
    "038": "Thanh Hóa",
    "040": "Nghệ An",
    "042": "Hà Tĩnh",
    "044": "Quảng Bình",
    "045": "Quảng Trị",
    "046": "Thừa Thiên Huế",
    "048": "Đà Nẵng",
    "049": "Quảng Nam",
    "051": "Quảng Ngãi",
    "052": "Bình Định",
    "054": "Phú Yên",
    "056": "Khánh Hòa",
    "058": "Ninh Thuận",
    "060": "Bình Thuận",
    "062": "Kon Tum",
    "064": "Gia Lai",
    "066": "Đắk Lắk",
    "067": "Đắk Nông",
    "068": "Lâm Đồng",
    "070": "Bình Phước",
    "072": "Tây Ninh",
    "074": "Bình Dương",
    "075": "Đồng Nai",
    "077": "Bà Rịa - Vũng Tàu",
    "079": "TP. Hồ Chí Minh",
    "080": "Long An",
    "082": "Tiền Giang",
    "083": "Bến Tre",
    "084": "Trà Vinh",
    "086": "Vĩnh Long",
    "087": "Đồng Tháp",
    "089": "An Giang",
    "091": "Kiên Giang",
    "092": "Cần Thơ",
    "093": "Hậu Giang",
    "094": "Sóc Trăng",
    "095": "Bạc Liêu",
    "096": "Cà Mau",
}


century_gender_map = {
    "0": ("20", "19", "Nam"),
    "1": ("20", "19", "Nữ"),
    "2": ("21", "20", "Nam"),
    "3": ("21", "20", "Nữ"),
    "4": ("22", "21", "Nam"),
    "5": ("22", "21", "Nữ"),
    "6": ("23", "22", "Nam"),
    "7": ("23", "22", "Nữ"),
    "8": ("24", "23", "Nam"),
    "9": ("24", "23", "Nữ"),
}


class CCCDInput(BaseModel):
    cccd: str = Field(..., min_length=12, max_length=12, pattern=r"^\d{12}$")


@app.get("/")
def root():
    return {"message": "Welcome to VN-ID Finder!"}


@app.post("/lookup")
def analyze_cccd(input: CCCDInput):
    cccd = input.cccd

    province_code = cccd[:3]
    gender_century_code = cccd[3]
    year_suffix = cccd[4:6]
    random_code = cccd[6:]

    province = province_codes.get(
        province_code, "Chưa cập nhật tỉnh/thành của người này"
    )
    century_gender = century_gender_map.get(gender_century_code)

    if not century_gender:
        return {"error": "Mã thế kỷ không hợp lệ"}

    century, year_prefix, gender = century_gender
    birth_year = year_prefix + year_suffix

    return {
        "province": province,
        "gender": gender,
        "century": century,
        "birth_year": birth_year,
        "random_code": random_code,
    }


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, workers=2)
