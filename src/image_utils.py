from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

from src.utils import generate_id


def open_image(image_path: str):
    return Image.open(image_path)

def save_image(image: Image, path: str):
        image.save(path)

def create_image(width, height):
    return Image.new("RGB", (width, height), "white")

def resize_image(image: Image, width: int, height: int):
    return image.resize((width, height))


# ---------- Изменение размера ----------

def resize_keep_aspect(image: Image, max_size: int):
    """Уменьшает с сохранением пропорций, чтобы большая сторона = max_size."""
    img = image.copy()
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return img

def resize_exact_quality(image: Image, width: int, height: int):
    """Ресайз с высоким качеством (LANCZOS)."""
    return image.resize((width, height), Image.Resampling.LANCZOS)


# ---------- Трансформации ----------

def rotate_image(image: Image, degrees: float, expand: bool = True):
    return image.rotate(degrees, expand=expand)

def flip_horizontal(image: Image):
    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

def flip_vertical(image: Image):
    return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

def crop_image(image: Image, left: int, upper: int, right: int, lower: int):
    return image.crop((left, upper, right, lower))


# ---------- Цвет ----------

def to_grayscale(image: Image):
    return image.convert("L")

def to_rgb(image: Image):
    return image.convert("RGB")

def invert_colors(image: Image):
    return ImageOps.invert(image.convert("RGB"))


# ---------- Фильтры ----------

def blur_image(image: Image, radius: float = 2.0):
    return image.filter(ImageFilter.GaussianBlur(radius))

def sharpen_image(image: Image):
    return image.filter(ImageFilter.SHARPEN)

def find_edges(image: Image):
    return image.filter(ImageFilter.FIND_EDGES)


# ---------- Рисование ----------
def draw_rectangle(image: Image, box: tuple, outline="red", width: int = 2):
    img = image.copy()
    ImageDraw.Draw(img).rectangle(box, outline=outline, width=width)
    return img


# ---------- Наложение ----------

def paste_image(base: Image, overlay: Image, position: tuple, opacity: int = 255):
    """Накладывает overlay (RGBA) на base с прозрачностью 0..255."""
    base = base.convert("RGBA")
    overlay = overlay.convert("RGBA")
    if opacity < 255:
        alpha = overlay.split()[3].point(lambda p: p * opacity // 255)
        overlay.putalpha(alpha)
    base.paste(overlay, position, overlay)
    return base


# ---------- Метаданные ----------

def get_image_info(image: Image):
    return {
        "size": image.size,
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "format": image.format,
    }


# ---------- Пакетная обработка ----------

def batch_thumbnail(paths: list[str], output_dir: str,
                    max_size: int = 800, quality: int = 85):
    """Уменьшает список файлов и сохраняет в output_dir."""
    from pathlib import Path
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for p in paths:
        img = open_image(p)
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        save_image(img, str(out / Path(p).name), )


from PIL import Image, ImageDraw


def tile_image_to_polygon(image_path: str,
                          points: list[tuple[int, int]],
                          background=None) -> Image:
    """
    Заполняет полигон (массив точек [(x, y), ...]) повторяющейся картинкой.

    :param image_path: путь к текстуре
    :param points: вершины полигона; порядок — по/против часовой (замкнётся сам)
    :param background: цвет фона вне полигона (None → прозрачный RGBA)
    :return: изображение размером с bounding box полигона
    """
    if len(points) < 3:
        raise ValueError("Полигон должен содержать минимум 3 точки")

    src = Image.open(image_path)
    src = src.convert("RGBA") if src.mode in ("RGBA", "LA", "P") else src.convert("RGB")

    # 1. Bounding box полигона
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    w, h = max_x - min_x, max_y - min_y
    if w <= 0 or h <= 0:
        raise ValueError("Полигон вырожден (нулевая площадь)")

    # 2. Тайлим текстуру на весь bbox
    tile_w, tile_h = src.size
    cols = (w + tile_w - 1) // tile_w
    rows = (h + tile_h - 1) // tile_h

    tiled = Image.new(src.mode, (cols * tile_w, rows * tile_h))
    for r in range(rows):
        for c in range(cols):
            tiled.paste(src, (c * tile_w, r * tile_h))
    tiled = tiled.crop((0, 0, w, h))

    # 3. Маска полигона (в локальных координатах bbox)
    local_points = [(x - min_x, y - min_y) for x, y in points]
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(local_points, fill=255)

    # 4. Применяем маску
    if background is None:
        # прозрачный фон вне полигона
        tiled = tiled.convert("RGBA")
        tiled.putalpha(mask)
        result = tiled
    else:
        # заливаем фон и накладываем замаскированную текстуру
        if isinstance(background, str):
            bg = Image.new("RGB", (w, h), background)
        else:
            bg = Image.new("RGB", (w, h), tuple(background))
        tiled_rgba = tiled.convert("RGBA")
        tiled_rgba.putalpha(mask)
        result = bg.convert("RGBA")
        result.alpha_composite(tiled_rgba)
        result = result.convert("RGB")

    return result


def build_outer_polygon(walls: list[dict]) -> list[tuple[int, int]]:
    """
    Собирает внешний контур из массива стен.
    walls: [{'c': [x1, y1, x2, y2], ...}, ...]
    Возвращает список вершин [(x, y), ...] в порядке обхода (замкнутый).
    """
    # 1. Собираем все отрезки (двери НЕ исключаем — они часть контура)
    segments = []
    for w in walls:
        x1, y1, x2, y2 = w["c"]
        segments.append(((x1, y1), (x2, y2)))

    # 2. Строим граф: вершина -> список соседей (по отрезкам)
    from collections import defaultdict
    adj = defaultdict(list)
    for a, b in segments:
        adj[a].append(b)
        adj[b].append(a)

    # 3. Идём по контуру: стартуем с любой вершины степени >= 1,
    #    каждый шаг — берём соседа, кроме того, откуда пришли
    start = segments[0][0]
    polygon = [start]
    prev = None
    current = start

    while True:
        neighbors = [n for n in adj[current] if n != prev]
        if not neighbors:
            break
        nxt = neighbors[0]
        if nxt == start:          # замкнулись
            break
        polygon.append(nxt)
        prev, current = current, nxt

    return polygon


def get_top_left_point(polygon):
    xs = [p[0] for p in polygon]
    ys = [p[1] for p in polygon]
    return (min(xs), min(ys), max(xs), max(ys))

def gen_tile_wall(data):
    import math

    import math

    def line_to_polygon(line: list, offset: float,
                        extend: float = 0) -> list[tuple[int, int]]:
        """
        Строит полигон (полосу) из линии.

        :param line: [x1, y1, x2, y2]
        :param offset: отступ в стороны от линии (половина толщины)
        :param extend: удлинение за каждую конечную точку вдоль линии
        :return: 4 вершины полигона (целые координаты)
        """
        x1, y1, x2, y2 = line
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            raise ValueError("Линия вырождена (точки совпадают)")

        # единичный вектор вдоль линии
        ux = dx / length
        uy = dy / length
        # единичный перпендикуляр
        nx = -uy
        ny = ux

        # смещения: перпендикуляр и продольное
        ox = nx * offset
        oy = ny * offset
        ex = ux * extend
        ey = uy * extend

        # удлинённые концы
        x1e, y1e = x1 - ex, y1 - ey
        x2e, y2e = x2 + ex, y2 + ey

        return [
            (round(x1e + ox), round(y1e + oy)),
            (round(x2e + ox), round(y2e + oy)),
            (round(x2e - ox), round(y2e - oy)),
            (round(x1e - ox), round(y1e - oy)),
        ]

    path = data["path"]
    path_ = data["path_"]
    wall = data["wall"]
    key = data['key']
    range_top = data['range_top']
    input_image = data['input_image']
    elevation = data['elevation']
    polygon = line_to_polygon(wall,offset= 5,extend=5)
    left_top = get_top_left_point(polygon)
    img = tile_image_to_polygon(input_image,
                                points=polygon)
    info = get_image_info(img)

    save_image(img, path)
    print(polygon)
    gen_tile = generate_id(16)

    js_tile = {
        "texture": {
            "src": path_,
            "anchorX": 0.5,
            "anchorY": 0.5,
            "offsetX": 0,
            "offsetY": 0,
            "fit": "fill",
            "scaleX": 1,
            "scaleY": 1,
            "rotation": 0,
            "tint": "#ffffff",
            "alphaThreshold": 0.75
        },
        "x": left_top[0],
        "y": left_top[1],
        "width": info['width'],
        "height": info['height'],
        "elevation": elevation,
        "sort": 9,
        "occlusion": {
            "mode": 0,
            "alpha": 0
        },
        "_id": gen_tile,
        "rotation": 0,
        "alpha": 1,
        "hidden": False,
        "locked": False,
        "restrictions": {
            "light": False,
            "weather": False
        },
        "video": {
            "loop": True,
            "autoplay": True,
            "volume": 0
        },
        "flags": {
        "betterroofs": {
          "brMode": False
        },
        "levels": {
          "rangeTop": range_top,
          "allWallBlockSight": False
        }
      },
        "_key": f"!scenes.tiles!{key}.{gen_tile}"
    }
    return js_tile

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt


import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt


import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt


def darken_near_walls(img: Image.Image,
                      walls: list[dict],
                      left_top: tuple[int, int],
                      distance: float = 40,
                      max_darkening: float = 0.7,
                      falloff: str = "smooth",
                      wall_offset: int = 0,
                      scene_padding: int = 0) -> Image.Image:
    """
    Затемняет пиксели img по мере приближения к стенам сцены.

    Пиксель (x, y) картинки имеет глобальную координату
    (left_top[0] + x, left_top[1] + y).
    Расстояние считается до ближайшего отрезка стены в ГЛОБАЛЬНЫХ координатах.

    :param img: картинка (обычно bbox комнаты)
    :param walls: [{'c': [x1,y1,x2,y2]}, ...] в глобальных координатах сцены
    :param left_top: (gx, gy) — глобальная координата пикселя (0,0) картинки
    :param distance: радиус тени от стены (пиксели)
    :param max_darkening: максимальное затемнение у стены (0..1)
    :param falloff: 'linear' | 'smooth' | 'quadratic'
    :param wall_offset: половина толщины стены (0 = тонкая линия)
    :param scene_padding: запас вокруг окна картинки (чтобы стены
                          за краем тоже давали тень)
    """
    if not walls or max_darkening <= 0 or distance <= 0:
        return img.copy()

    base = img.convert("RGBA") if img.mode in ("RGBA", "LA") else img.convert("RGB")
    w, h = base.size
    ox, oy = int(left_top[0]), int(left_top[1])

    # --- 1. Границы «локальной сцены» = картинка + padding ---
    pad = max(0, int(scene_padding))
    lx, ly = -pad, -pad                  # локальные границы окна
    lw, lh = w + 2 * pad, h + 2 * pad    # размер окна

    # --- 2. Маска стен в локальных координатах окна ---
    # глобальная точка (gx, gy) -> локальная в окне (gx - (ox+lx), gy - (oy+ly))
    # у нас lx=-pad, значит смещение = (ox - pad, oy - pad)
    shift_x = ox + lx   # = ox - pad
    shift_y = oy + ly   # = oy - pad

    wall_mask = Image.new("L", (lw, lh), 0)
    draw = ImageDraw.Draw(wall_mask)

    for wall in walls:
        x1, y1, x2, y2 = wall["c"]
        # в координаты окна
        wx1, wy1 = x1 - shift_x, y1 - shift_y
        wx2, wy2 = x2 - shift_x, y2 - shift_y

        if wall_offset > 0:
            # толстая стена — полигон
            # (line_to_polygon работает и в глобальных, и в локальных — важен offset)
            from math import hypot
            dx, dy = wx2 - wx1, wy2 - wy1
            length = hypot(dx, dy)
            if length == 0:
                continue
            nx, ny = -dy / length * wall_offset, dx / length * wall_offset
            draw.polygon([
                (wx1 + nx, wy1 + ny),
                (wx2 + nx, wy2 + ny),
                (wx2 - nx, wy2 - ny),
                (wx1 - nx, wy1 - ny),
            ], fill=255)
        else:
            # тонкая линия
            draw.line([(wx1, wy1), (wx2, wy2)], fill=255, width=1)

    mask = np.array(wall_mask, dtype=bool)
    if mask.sum() == 0:
        # ни одна стена не попала в окно
        return img

    # --- 3. Расстояние до ближайшего пикселя стены (в координатах окна) ---
    dist = distance_transform_edt(~mask)

    # --- 4. Вырезаем окно, соответствующее картинке ---
    # картинка занимает [pad : pad+w, pad : pad+h]
    dist_img = dist[pad:pad + h, pad:pad + w]

    # --- 5. Коэффициент затемнения ---
    t = np.clip(1.0 - dist_img / float(distance), 0.0, 1.0)

    if falloff == "smooth":
        t = t * t * (3 - 2 * t)
    elif falloff == "quadratic":
        t = t * t

    factor = 1.0 - t * float(max_darkening)
    factor = factor[..., None]

    arr = np.array(base, dtype=np.float32)
    arr[..., :3] *= factor
    out = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode=base.mode)



from PIL import Image, ImageDraw


from PIL import Image, ImageDraw

from PIL import Image, ImageDraw

from PIL import Image, ImageDraw


def cut_hole(img, polygon1, polygon2, offset=0.0):
    """Делает дырку (прозрачную область) в изображении по полигону.

    polygon1 задаёт систему координат (опорная рамка), polygon2 —
    что вырезать. offset смещает polygon2 относительно его центра:
    положительное значение расширяет полигон (ближе к краям),
    отрицательное — сжимает (ближе к центру).

    Args:
        img: Изображение (PIL.Image) или путь к файлу.
        polygon1: Вершины [(x, y), ...] опорной рамки в координатах сцены.
        polygon2: Вершины [(x, y), ...] вырезаемой области в координатах сцены.
        offset: Смещение относительно центра polygon2. Значение в тех же
            единицах, что и координаты (пиксели сцены). Положительное —
            наружу (расширение), отрицательное — внутрь (сжатие).
            По умолчанию 0 — без изменений.

    Returns:
        PIL.Image RGBA размером с img: всё, кроме polygon2 (с учётом offset),
        сохранено; внутри polygon2 — alpha=0.
    """
    if isinstance(img, str):
        img = Image.open(img)
    img = img.convert("RGBA")

    # 1. Система координат по polygon1
    xs1 = [p[0] for p in polygon1]
    ys1 = [p[1] for p in polygon1]
    min_x, min_y = min(xs1), min(ys1)
    max_x, max_y = max(xs1), max(ys1)
    box_w, box_h = max_x - min_x, max_y - min_y

    sx = img.width / box_w if box_w else 1
    sy = img.height / box_h if box_h else 1

    # 2. Центроид polygon2 (в координатах сцены)
    cx = sum(p[0] for p in polygon2) / len(polygon2)
    cy = sum(p[1] for p in polygon2) / len(polygon2)

    # 3. Радиус описанной окружности — для перевода offset в коэффициент
    import math
    radius = max(math.hypot(p[0] - cx, p[1] - cy) for p in polygon2)
    if radius == 0:
        k = 1.0
    else:
        k = 1.0 + offset / radius

    # 4. Масштабируем polygon2 относительно центроида, затем -> локальные коорд.
    local_polygon = []
    for x, y in polygon2:
        nx = cx + (x - cx) * k
        ny = cy + (y - cy) * k
        local_polygon.append(((nx - min_x) * sx, (ny - min_y) * sy))

    # 5. Маска: 255 везде, 0 внутри polygon2
    mask = Image.new("L", img.size, 255)
    ImageDraw.Draw(mask).polygon(local_polygon, fill=0)

    out = img.copy()
    out.putalpha(mask)
    return out