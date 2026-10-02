#!/usr/bin/env python3
"""生成网站自托管字体（woff2）和对应的 @font-face 样式。

网站使用两套开源字体（SIL OFL 1.1 许可）：
  - Source Serif 4   西文衬线体（正体 + 斜体，可变字重 400–700）
  - Noto Serif SC    思源宋体（可变字重 400–700）

思源宋体完整文件约 25 MB，不能整个放到网页上。这个脚本把它完整地切成一百多个
小文件（每个几十 KB），并为每个文件写上它包含的字符范围（unicode-range）。浏览器
只下载当前页面实际用到的那几个文件。字体里的全部汉字都在，所以以后增删、修改文字
都不需要重新运行这个脚本。

切片方式见 bin/noto-serif-sc-slices.txt（取自 Google Fonts 对同一字体按字频的切分）；
字体里不在其中的生僻字，脚本会另外补成若干切片。

什么时候需要运行：升级字体版本、修改切片方式或西文字符范围的时候。

用法：
  pip install fonttools brotli
  python3 bin/build-fonts.py

源字体第一次运行时从 GitHub 下载到 .cache/fonts/（不提交到仓库），并校验 SHA-256。
输出：assets/fonts/*.woff2、_sass/_fonts.scss 和 _data/fonts.yml（都提交到仓库）。
"""

from __future__ import annotations

import glob
import hashlib
import os
import sys
import urllib.request
from concurrent.futures import ProcessPoolExecutor

try:
    from fontTools import subset
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
except ImportError:
    sys.exit("缺少依赖，请先运行：pip install fonttools brotli")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", "fonts")
OUT_DIR = os.path.join(ROOT, "assets", "fonts")
OUT_SCSS = os.path.join(ROOT, "_sass", "_fonts.scss")
OUT_DATA = os.path.join(ROOT, "_data", "fonts.yml")
SLICES = os.path.join(ROOT, "bin", "noto-serif-sc-slices.txt")

RAW = "https://raw.githubusercontent.com/google/fonts"
SOURCES = {
    "SourceSerif4.ttf": (
        f"{RAW}/08dc85da6bca7ae308a6f1d38d0b137465646071/ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf",
        "97b2d4da6e3cb494b5a1e66ae176914d852ccabef49e0c02c0df25f3e39aca0b",
    ),
    "SourceSerif4-Italic.ttf": (
        f"{RAW}/08dc85da6bca7ae308a6f1d38d0b137465646071/ofl/sourceserif4/SourceSerif4-Italic%5Bopsz%2Cwght%5D.ttf",
        "15fbc7e4679489a501998c3669272637a6646388ef7e4bd77eebb5bf967a1f42",
    ),
    "NotoSerifSC.ttf": (
        f"{RAW}/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifsc/NotoSerifSC%5Bwght%5D.ttf",
        "050080d9255a86808f2945bffac582b31ef32bc36411ce29563b4961670c66f9",
    ),
}

WEIGHTS = (400, 700)

# 西文字符：基本拉丁、Latin-1、拉丁扩展 A（如 č、ł、ő）、常用标点与符号、箭头、数学符号
LATIN = (
    "U+0020-007E,U+00A0-017F,U+0192,U+0218-021B,U+02C6-02C7,U+02D8-02DD,"
    "U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2202,U+2206,U+220F,U+2211-2212,U+2215,"
    "U+221A,U+221E,U+222B,U+2248,U+2260,U+2264-2265,U+25CA,U+03C0"
)
LATIN_FEATURES = [
    "kern", "liga", "calt", "locl", "ccmp", "mark", "mkmk",
    "lnum", "onum", "pnum", "tnum", "sups", "frac", "case", "zero", "ordn",
]  # fmt: skip

# 中文排版里应当用中文字形的标点：破折号、引号、省略号、间隔号
CJK_PUNCT = "—‘’“”…·"

# 不在 Google 切片里的生僻字，每多少个字切成一个文件
EXTRA_SLICE_SIZE = 1200


def fetch_sources() -> None:
    os.makedirs(CACHE, exist_ok=True)
    for name, (url, sha256) in SOURCES.items():
        path = os.path.join(CACHE, name)
        if not os.path.exists(path):
            print(f"下载 {name} …")
            urllib.request.urlretrieve(url, path)
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        if digest != sha256:
            os.remove(path)
            sys.exit(f"{name} 校验失败（文件已删除，请重新运行）。")


def instanced_noto() -> str:
    """把思源宋体的字重范围限定为网站用到的 400–700，结果缓存起来（约 40 秒，只做一次）。"""
    sha = SOURCES["NotoSerifSC.ttf"][1][:8]
    path = os.path.join(CACHE, f"NotoSerifSC-{WEIGHTS[0]}-{WEIGHTS[1]}-{sha}.ttf")
    if not os.path.exists(path):
        print("准备思源宋体（限定字重范围，约 40 秒）…")
        font = TTFont(os.path.join(CACHE, "NotoSerifSC.ttf"))
        font = instancer.instantiateVariableFont(font, {"wght": WEIGHTS})
        font.save(path)
    return path


def parse_ranges(text: str) -> set[int]:
    cps: set[int] = set()
    for part in text.replace(" ", "").split(","):
        if not part:
            continue
        part = part[2:] if part.upper().startswith("U+") else part
        if "-" in part:
            a, b = part.split("-")
            cps.update(range(int(a, 16), int(b, 16) + 1))
        else:
            cps.add(int(part, 16))
    return cps


def format_ranges(cps: set[int]) -> str:
    ordered = sorted(cps)
    ranges: list[str] = []
    start = prev = ordered[0]
    for cp in ordered[1:] + [None]:
        if cp is not None and cp == prev + 1:
            prev = cp
            continue
        ranges.append(f"U+{start:04X}" if start == prev else f"U+{start:04X}-{prev:04X}")
        if cp is not None:
            start = prev = cp
    return ", ".join(ranges)


def make_woff2(job: tuple[str, str, list[int], list[str], bool]) -> tuple[str, str, int]:
    """切出一个字体文件。返回（文件名，内容哈希，大小）。"""
    source, out_name, cps, features, limit_weight = job
    font = TTFont(source)
    options = subset.Options()
    options.layout_features = features
    options.name_IDs = [1, 2, 3, 4, 6]
    options.notdef_outline = True
    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=cps)
    subsetter.subset(font)
    if limit_weight:
        font = instancer.instantiateVariableFont(font, {"wght": WEIGHTS})
    font.flavor = "woff2"
    out_path = os.path.join(OUT_DIR, out_name)
    font.save(out_path)
    with open(out_path, "rb") as fh:
        data = fh.read()
    return out_name, hashlib.sha256(data).hexdigest()[:8], len(data)


def font_face(family: str, style: str, file: str, version: str, urange: str) -> str:
    return (
        "@font-face {\n"
        f'  font-family: "{family}";\n'
        f"  font-style: {style};\n"
        f"  font-weight: {WEIGHTS[0]} {WEIGHTS[1]};\n"
        "  font-display: swap;\n"
        f'  src: url("../fonts/{file}?v={version}") format("woff2");\n'
        f"  unicode-range: {urange};\n"
        "}\n"
    )


def main() -> None:
    fetch_sources()
    os.makedirs(OUT_DIR, exist_ok=True)
    noto = instanced_noto()
    noto_cmap = set(TTFont(noto, lazy=True).getBestCmap())

    # 思源宋体的切片：先按 Google 的切分，再把剩下的字补成若干切片
    with open(SLICES, encoding="utf-8") as fh:
        google_slices = [parse_ranges(line) for line in fh if line.strip() and not line.startswith("#")]
    slices: list[set[int]] = []
    covered: set[int] = set()
    for cps in google_slices:
        cps &= noto_cmap
        if cps:
            slices.append(cps)
            covered |= cps
    rest = sorted(noto_cmap - covered)
    for i in range(0, len(rest), EXTRA_SLICE_SIZE):
        slices.append(set(rest[i : i + EXTRA_SLICE_SIZE]))

    for old in glob.glob(os.path.join(OUT_DIR, "noto-serif-sc-*.woff2")):
        os.remove(old)

    latin = sorted(parse_ranges(LATIN))
    jobs = [
        (os.path.join(CACHE, "SourceSerif4.ttf"), "source-serif-4.woff2", latin, LATIN_FEATURES, True),
        (os.path.join(CACHE, "SourceSerif4-Italic.ttf"), "source-serif-4-italic.woff2", latin, LATIN_FEATURES, True),
        (noto, "noto-serif-sc-punct.woff2", [ord(c) for c in CJK_PUNCT], ["*"], False),
    ]
    for n, cps in enumerate(slices):
        jobs.append((noto, f"noto-serif-sc-{n:03d}.woff2", sorted(cps), ["*"], False))

    print(f"生成 {len(jobs)} 个字体文件（思源宋体 {len(slices)} 个切片，共 {len(noto_cmap)} 个字符）…")
    with ProcessPoolExecutor() as pool:
        results = {name: (version, size) for name, version, size in pool.map(make_woff2, jobs)}

    total = sum(size for _, size in results.values())
    print(f"完成，共 {total / 1024 / 1024:.1f} MB（每个页面只下载其中用到的几个文件）")

    css = [
        "// 由 bin/build-fonts.py 生成，请不要手动修改。",
        "// Source Serif 4 与 Noto Serif SC 均以 SIL Open Font License 1.1 发布，见 assets/fonts/OFL-*.txt。",
        "",
    ]
    v = results["source-serif-4.woff2"][0]
    css.append(font_face("Source Serif 4", "normal", "source-serif-4.woff2", v, LATIN))
    v = results["source-serif-4-italic.woff2"][0]
    css.append(font_face("Source Serif 4", "italic", "source-serif-4-italic.woff2", v, LATIN))
    for n, cps in enumerate(slices):
        name = f"noto-serif-sc-{n:03d}.woff2"
        css.append(font_face("Noto Serif SC", "normal", name, results[name][0], format_ranges(cps)))
    css.append("// 中文页面里，引号、破折号、省略号、间隔号使用中文字形")
    v = results["noto-serif-sc-punct.woff2"][0]
    css.append(font_face("Noto Serif SC Punct", "normal", "noto-serif-sc-punct.woff2", v, format_ranges({ord(c) for c in CJK_PUNCT})))

    with open(OUT_SCSS, "w", encoding="utf-8") as fh:
        fh.write("\n".join(css))
    with open(OUT_DATA, "w", encoding="utf-8") as fh:
        fh.write("# 由 bin/build-fonts.py 生成，请不要手动修改。页面用它来提前加载西文字体。\n")
        fh.write(f"latin: source-serif-4.woff2?v={results['source-serif-4.woff2'][0]}\n")
    print(f"已写入 {os.path.relpath(OUT_SCSS, ROOT)} 和 {os.path.relpath(OUT_DATA, ROOT)}")


if __name__ == "__main__":
    main()
