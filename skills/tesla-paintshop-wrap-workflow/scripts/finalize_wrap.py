"""Finalize an engineered 1024px UV canvas without changing official template alpha."""
import argparse
import hashlib
import io
import json
import re
from pathlib import Path
from PIL import Image, ImageColor


def finalize(*, template, design, output, template_sha256, model, base_color,
             allow_rgb_quantization=False):
    template, design, output = Path(template), Path(design), Path(output)
    report_path = output.with_name(output.stem + '-report.json')
    if not re.fullmatch(r'[A-Za-z0-9_ -]+\.png', output.name) or len(output.name) > 30:
        raise ValueError('PNG 文件名须为英文数字、空格、下划线或短横线，含扩展名最多 30 字符')
    if output.exists() or report_path.exists():
        raise FileExistsError('成品或报告已存在，请使用新文件名')
    if not model or not str(model).strip():
        raise ValueError('需明确提供已核实的车型模板标识')
    raw = template.read_bytes()
    template_hash = hashlib.sha256(raw).hexdigest()
    if template_hash != template_sha256.lower():
        raise ValueError('模板哈希与已核实原件不符')
    with Image.open(template) as mask:
        if mask.size != (1024, 1024) or mask.mode != 'RGBA' or mask.format != 'PNG':
            raise ValueError('官方模板必须为 1024×1024 PNG/RGBA；不会自动缩放 UV')
        alpha = mask.getchannel('A').copy()
    if alpha.getextrema() != (0, 255):
        raise ValueError('模板须含透明背景与完整车身件')
    with Image.open(design) as artwork:
        if artwork.size != (1024, 1024):
            raise ValueError('工程化设计画布须与模板同为 1024×1024，不得缩放错位 UV')
        material = artwork.convert('RGBA')
    color = ImageColor.getrgb(base_color)
    if len(color) != 3:
        raise ValueError('基色须为不含透明度的 RGB 颜色')
    composed = Image.new('RGBA', (1024, 1024), color + (255,))
    composed.alpha_composite(material)
    composed.putalpha(alpha)
    # Hidden RGB is normalized for compression; visible RGB and every alpha byte remain meaningful.
    rgb = composed.convert('RGB')
    transparent = alpha.point(lambda value: 255 if value == 0 else 0)
    rgb.paste((0, 0, 0), mask=transparent)
    steps = [1, 2, 4, 8, 16, 32, 64, 128, 256] if allow_rgb_quantization else [1]
    candidate_bytes = None
    for step in steps:
        reduced = rgb if step == 1 else rgb.point([min(255, round(v / step) * step) for v in range(256)] * 3)
        candidate = reduced.convert('RGBA')
        candidate.putalpha(alpha)
        stream = io.BytesIO()
        candidate.save(stream, format='PNG', optimize=True, compress_level=9)
        encoded = stream.getvalue()
        if len(encoded) < 1000000:
            candidate_bytes = encoded
            break
    if candidate_bytes is None:
        raise ValueError('PNG 超过 1 MB；可明确允许 RGB 色阶减少后重试，Alpha 不会被压缩改写')
    with Image.open(io.BytesIO(candidate_bytes)) as check:
        check.load()
        if check.mode != 'RGBA' or check.size != (1024, 1024) or check.getchannel('A').tobytes() != alpha.tobytes():
            raise ValueError('最终编码文件与模板透明度不符')
    report = {
        'model': str(model), 'filename': output.name, 'format': 'PNG', 'mode': 'RGBA',
        'width': 1024, 'height': 1024, 'bytes': len(candidate_bytes),
        'sha256': hashlib.sha256(candidate_bytes).hexdigest(),
        'template_sha256': template_hash, 'alpha_sha256': hashlib.sha256(alpha.tobytes()).hexdigest(),
        'alpha_matches_template': True, 'rgb_quantization_step': step,
        'orientation_verified_by_script': False, 'vehicle_import_verified': False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as file:
        file.write(candidate_bytes)
    with report_path.open('x', encoding='utf-8') as file:
        file.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['template', 'template-sha256', 'model', 'design', 'base-color', 'output']:
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--allow-rgb-quantization', action='store_true')
    args = parser.parse_args()
    try:
        result = finalize(**vars(args))
    except (ValueError, OSError) as error:
        parser.exit(1, f'制作失败：{error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
