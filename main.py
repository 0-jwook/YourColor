from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import colorsys

app = FastAPI()

# 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 입력 데이터 검증 모델
class ColorRequest(BaseModel):
    hex_color: str

# HEX 색상을 처리하는 함수
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def generate_similar_colors(hex_color):
    rgb = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)

    variations = []
    for adjustment in [-0.2, -0.1, 0.1, 0.2]:
        new_l = min(max(l + adjustment, 0), 1)
        r, g, b = colorsys.hls_to_rgb(h, new_l, s)
        variations.append(rgb_to_hex((int(r * 255), int(g * 255), int(b * 255))))

    return variations

# 추천 API 엔드포인트
@app.post("/recommend")
async def recommend_colors(request: ColorRequest):
    similar_colors = generate_similar_colors(request.hex_color)
    return {"input_color": request.hex_color, "recommended_colors": similar_colors}

# 메인 페이지 렌더링
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
