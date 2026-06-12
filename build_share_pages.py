# -*- coding: utf-8 -*-
# share ページ生成スクリプト
# index.html / mdn/index.html を更新したら、このスクリプトを再実行して share/ を作り直してください。
# 使い方: python3 build_share_pages.py  （リポジトリのルートで実行）
import os, re

BASE = 'https://mamoridori.com'
BIRDS_JA = {'condle': '鷹', 'canaly': 'カナリア', 'owl': 'フクロウ', 'peac': '孔雀', 'phenix': '鳳凰'}
BIRDS_ZH = {'condle': '老鷹', 'canaly': '金絲雀', 'owl': '貓頭鷹', 'peac': '孔雀', 'phenix': '鳳凰'}
BIRDS_EN = {'condle': 'Hawk', 'canaly': 'Canary', 'owl': 'Owl', 'peac': 'Peacock', 'phenix': 'Phoenix'}
COLORS_JA = {'W': '白', 'R': '赤', 'Y': '黄色', 'B': '青'}
COLORS_ZH = {'W': '白', 'R': '紅', 'Y': '黃', 'B': '藍'}
COLORS_EN = {'W': 'White', 'R': 'Red', 'Y': 'Yellow', 'B': 'Blue'}
RIMG = {'condle': 'R-Hawk', 'canaly': 'R-canary', 'owl': 'R-owl', 'peac': 'R-peacok', 'phenix': 'R-phenix'}


def make(src_path, out_dir, url_prefix, lang):
    src = open(src_path, encoding='utf-8').read()
    os.makedirs(out_dir, exist_ok=True)
    for bk in BIRDS_JA:
        for ck in COLORS_JA:
            key = f'{bk}-{ck}'
            s = src
            if lang == 'ja':
                name = f'{COLORS_JA[ck]}の{BIRDS_JA[bk]}'
                title = f'私の守護鳥は「{name}」でした｜守護鳥占い'
            elif lang == 'zh':
                name = f'{COLORS_ZH[ck]}色{BIRDS_ZH[bk]}'
                title = f'我的守護鳥是「{name}」｜守護鳥占卜'
            else:
                name = f'{COLORS_EN[ck]} {BIRDS_EN[bk]}'
                title = f'My guardian bird is the \u201c{name}\u201d | Mamoridori'
            img = f'{BASE}/images/{RIMG[bk]}-{ck}.webp'
            page_url = f'{BASE}{url_prefix}/{key}.html'
            # OGP 差し替え
            s = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', r'\g<1>' + title + r'\g<2>', s)
            s = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', r'\g<1>' + page_url + r'\g<2>', s)
            s = re.sub(r'(<meta property="og:image" content=")[^"]*(">)', r'\g<1>' + img + r'\g<2>', s)
            s = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="noindex">', s)
            s = re.sub(r'<link rel="alternate"[^>]*>\n?', '', s)
            # 階層が深くなるため相対パスを絶対パスへ
            s = s.replace('src="images/', 'src="/images/')
            s = s.replace("img.src='images/", "img.src='/images/")
            s = s.replace('href="about.html"', 'href="/about.html"')
            s = s.replace('href="privacy.html"', 'href="/privacy.html"')
            # この鳥・色の結果を初期表示（?r 未指定でもプリセット）
            s = s.replace("var r=q.get('r'),ed=q.get('ed');",
                          "var r=q.get('r')||'%s',ed=q.get('ed');" % key)
            open(os.path.join(out_dir, f'{key}.html'), 'w', encoding='utf-8').write(s)
    print(f'{out_dir}: 20 pages written')


make('index.html', 'share', '/share', 'ja')
make('mdn/index.html', 'mdn/share', '/mdn/share', 'zh')
make('en/index.html', 'en/share', '/en/share', 'en')
