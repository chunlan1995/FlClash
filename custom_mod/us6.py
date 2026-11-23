import base64, io, json, struct, zlib # end
import icon_pack, us1, us2, us3, us4, us5 # end
def _rs(s, a, b, v): # end
    i = s .index(a) # end
    j = s .index(b, i) # end
    return s[:i] + v + s[j:] # end
def _apply_icons_and_ver(od, psw, pswc, d2): # end
    root = od .parent .parent # end
    for rel, content in d2['txt_files'] .items(): # end
        fp = root / rel # end
        if fp .parent .parent .exists(): # end
            fp .parent .mkdir(parents=True, exist_ok=True) # end
            fp .write_text(content, 'utf-8') # end
    Image, ImageDraw, ImageFilter = icon_pack ._pil() # end
    from PIL import ImageEnhance # end
    base = Image .open(io .BytesIO(base64 .b64decode(icon_pack .B64))) .convert('RGBA') .resize((1024, 1024), Image .Resampling .LANCZOS) # end
    msk = Image .new('L', (2048, 2048), 0); ImageDraw .Draw(msk) .rounded_rectangle((8, 8, 2039, 2039), radius=408, fill=255) # end
    sq = base .copy(); sq .putalpha(msk .resize((1024, 1024), Image .Resampling .LANCZOS)) # end
    def png_b(im): # end
        b = io .BytesIO(); im .save(b, format='PNG', optimize=True); return b .getvalue() # end
    def mk_ico(frames): # end
        hdr = struct .pack('<HHH', 0, 1, len(frames)); off = 6 + 16 * len(frames); ents = []; blobs = [] # end
        for sz, pb in frames: # end
            dm = 0 if sz >= 256 else sz; ents .append(struct .pack('<BBBBHHII', dm, dm, 0, 0, 1, 32, len(pb), off)); blobs .append(pb); off += len(pb) # end
        return hdr + b'' .join(ents) + b'' .join(blobs) # end
    def mk_tile(sz): # end
        cp = base .crop((44, 40, 980, 976)) .resize((sz * 2, sz * 2), Image .Resampling .LANCZOS) # end
        tm = Image .new('L', (sz * 2, sz * 2), 0); ImageDraw .Draw(tm) .rounded_rectangle((2, 2, sz * 2 - 3, sz * 2 - 3), radius=round(sz * 2 * 0.24), fill=255); cp .putalpha(tm) # end
        out = cp .resize((sz, sz), Image .Resampling .LANCZOS) # end
        if sz <= 48: # end
            rgb = ImageEnhance .Contrast(out .convert('RGB')) .enhance(1.14) .filter(ImageFilter .UnsharpMask(radius=0.85, percent=115, threshold=2)); rc, gc, bc = rgb .split(); out = Image .merge('RGBA', (rc, gc, bc, out .getchannel('A'))) # end
        return out # end
    def mk_col(st, sz): # end
        im = mk_tile(sz) # end
        if st == 1: # end
            rgb = ImageEnhance .Brightness(ImageEnhance .Color(im .convert('RGB')) .enhance(0.20)) .enhance(0.88); rc, gc, bc = rgb .split(); return Image .merge('RGBA', (rc, gc, bc, im .getchannel('A') .point(lambda v: int(v * 0.86)))) # end
        if st == 2: # end
            return im # end
        ss = sz * 4; ov = Image .new('RGBA', (ss, ss), (0, 0, 0, 0)); drw = ImageDraw .Draw(ov); dr = max(8, round(ss * 0.135)); cx = cy = ss - dr - max(4, round(ss * 0.04)); rr = dr + max(4, round(ss * 0.042)) # end
        drw .ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 255, 255, 252)); drw .ellipse((cx - dr, cy - dr, cx + dr, cy + dr), fill=(16, 185, 129, 255) if st == 3 else (245, 158, 11, 255)) # end
        im .alpha_composite(ov .resize((sz, sz), Image .Resampling .LANCZOS)); return im # end
    def mk_tpl(sz, warn): # end
        ss = sz * 8; im = Image .new('RGBA', (ss, ss), (0, 0, 0, 0)); drw = ImageDraw .Draw(im) # end
        for pts in d2['polys']: # end
            drw .polygon([(x * ss / 240.0, y * ss / 240.0) for x, y in pts], fill=(0, 0, 0, 255)) # end
        if warn: # end
            cx = 206 * ss / 240.0; cy = 54 * ss / 240.0; ro = 28 * ss / 240.0; ri = 19 * ss / 240.0; drw .ellipse((cx - ro, cy - ro, cx + ro, cy + ro), fill=(0, 0, 0, 0)); drw .ellipse((cx - ri, cy - ri, cx + ri, cy + ri), fill=(0, 0, 0, 255)) # end
        return im .resize((sz, sz), Image .Resampling .LANCZOS) # end
    app_ico = mk_ico([(sz, png_b(mk_tile(sz) if sz <= 48 else sq .resize((sz, sz), Image .Resampling .LANCZOS))) for sz in (16, 20, 24, 32, 40, 48, 64, 96, 128, 256)]) # end
    for rk in ('p_ico1', 'p_ico2'): # end
        ip = root / d2[rk] # end
        if ip .parent .exists(): # end
            ip .write_bytes(app_ico) # end
    wt = root / d2['p_win_tray'] # end
    if wt .parent .exists(): # end
        wt .mkdir(parents=True, exist_ok=True) # end
        for st in (1, 2, 3, 4): # end
            (wt / ('status_' + str(st) + '.' + 'ico')) .write_bytes(mk_ico([(sz, png_b(mk_col(st, sz))) for sz in (16, 20, 24, 32, 40, 48, 64)])) # end
    ut = root / d2['p_unix_tray']; mt = root / d2['p_mac_tray'] # end
    if ut .parent .exists(): # end
        for sc_i in (1, 2, 3, 4): # end
            du = ut if sc_i == 1 else (ut / (str(sc_i) + '.0x')); dm = mt if sc_i == 1 else (mt / (str(sc_i) + '.0x')); du .mkdir(parents=True, exist_ok=True); dm .mkdir(parents=True, exist_ok=True); px = 18 * sc_i # end
            for st in (1, 2, 3, 4): # end
                fn = 'status_' + str(st) + '.' + 'png'; mk_col(st, px) .save(du / fn, format='PNG', optimize=True); mk_tpl(px, st == 4) .save(dm / fn, format='PNG', optimize=True) # end
    sw2 = psw .read_text('utf-8') # end
    if d2['chk_g'] not in sw2: # end
        sw2 = d2['imp_g'] + sw2 # end
    if '_bcIslandGlyph' not in sw2: # end
        sw2 = sw2 .replace(d2['t_fb'], d2['t_fb'] + '\n' + d2['bc_glyph'], 1) # end
    sw2 = sw2 .replace(d2['p_old'], d2['p_new']) .replace(d2['dock_old'], d2['dock_new']) .replace(d2['hdr_old'], d2['hdr_new']) .replace(d2['ret_old'], d2['ret_new']) # end
    psw .write_text(sw2, 'utf-8') # end
    swc2 = pswc .read_text('utf-8') # end
    if 'summaryGrid' in swc2: # end
        pswc .write_text(_rs(_rs(_rs(swc2, 'Widget _buildOverviewPage(', 'Widget _statusCard(', d2['ov']), 'Widget _subItemCard(', 'Widget _buildSubEditModal(', d2['sc']), 'Widget _fallbackAndWhoamiCard(', 'Widget _buildCountryPage(', d2['fw']), 'utf-8') # end
def apply_v118(od): # end
    raw = us1 .P1 + us2 .P2 .replace('4l/9a1Dw1o', '4l/8a1Dw1o') + us3 .P3 + us4 .P4 .replace('TtNtNtNSkno', 'TtNtNSkno') + us5 .P5 # end
    d = json .loads(zlib .decompress(base64 .b64decode(raw)) .decode('utf-8')) # end
    pfb = od / ('flclash_bridge' + '.' + 'dart') # end
    fb = pfb .read_text('utf-8') # end
    if 'SubRichItem' not in fb: # end
        fb = fb .replace(d['fb_imp_old'], d['fb_imp_new'], 1) # end
        fb = fb .replace('typedef BridgeProfile =', d['fb_types'] + 'typedef BridgeProfile =', 1) # end
        fb = fb .replace('class FlClashBridge {', 'class FlClashBridge {\n' + d['fb_body'], 1) # end
        fb = fb .replace(d['a_snc'], d['a_snc_new'], 1) # end
        pfb .write_text(fb, 'utf-8') # end
    psg = od / ('smart_guardian' + '.' + 'dart') # end
    sg = psg .read_text('utf-8') # end
    if 'syncAndApplyNow' not in sg: # end
        sg = sg .replace('极简智控已就绪', '已就绪') # end
        sg = sg .replace('Future<void> togRun(', d['sg_extra'] + 'Future<void> togRun(', 1) # end
        psg .write_text(sg, 'utf-8') # end
    psw = od / ('simple_workbench' + '.' + 'dart') # end
    sw = psw .read_text('utf-8') # end
    if 'wb_sub_modal' not in sw: # end
        sw = sw .replace('final _pkSearchFocus=FocusNode();', d['sw_fields'], 1) # end
        sw = sw .replace(d['a_init'], d['a_init'] + d['sw_init'], 1) # end
        sw = _rs(sw, 'for(final c in<TextEditingController>[_cSearchCtrl', d['a_disp'], d['sw_dispose']) # end
        sw = _rs(sw, 'Future<void>_toggleRun(bool run)async{', 'bool _isDk(BuildContext c)=>', d['sw_helpers']) # end
        sw = _rs(sw, 'Widget _inp(', 'String _menuRegLbl(', d['sw_inp']) # end
        sw = _rs(sw, 'Widget _hdr(BuildContext c,GuardianState st,', '@override Widget build(BuildContext context){', d['sw_hdr']) # end
        sw = _rs(sw, "const titles=<String>['智控'", '}catch(err){', d['sw_build']) # end
        sw = sw .replace("Text('重新加载 BlueClash')", "Text('重新加载')") # end
        psw .write_text(sw, 'utf-8') # end
    pswc = od / ('simple_workbench_cards' + '.' + 'dart') # end
    swc = pswc .read_text('utf-8') # end
    if '_buildSubsPage(' not in swc: # end
        swc = _rs(swc, 'Widget _buildOverviewPage(', 'Widget _fallbackAndWhoamiCard(', d['swc_subs']) # end
        pswc .write_text(swc, 'utf-8') # end
    p6 = ( # end
'eNrtXHuT21SW/yqih43tXcWW5EfbTrt72+k0m1onMOmQLJukXLIk26rIkkqS+7Ghq7IsJOGZsMAwQG' # end
'qAYWaHYZbA7DIzEMhQNR8F4k7nr9mPsL9zryQ/Ync6cWcJtSFV7aurc8/rnvM75153c27GWZ0pCzMn' # end
'Tb1lBEK90TUt/clVw1s1jbWn1JaRrNLMQccOjPVA0MQnuqqnm6q9EqiBIfiBWDP9YG6l2zhmau3Dgd' # end
'GZ9zDAsy82HMcSvK7NB/6G/9Q6HwZd+8lw1vSXDP9s4Lipc03TVvHOcY85a5V4fgFPSc1zfH9x3fQX' # end
'LbNldww7KNc1dUX0XVUz7VZZVkStDTU9wy7PcVPmTx1ad1VbN/Rk0zLWy7LMScp1H5p3/YMwI6mJMI' # end
'A05MoxvVIpcWSlFK1sqpbVULWzi7Z+su2oHTNmgkVnxFT5oGN1O3ZyR7XuKl/cSQ6JOeAZQdezhVDa' # end
'GOccvGNKSPsBlmntnX1mNpN1T3ODE6afYoOqatuGB9nRrqZEvkNMkc0ZUZhprg0G0Hjd7xJE0ebbQb' # end
'PiGU0h7RmqnmyFVE95zqqpG56Qtp3AbJqGlzrA6RElpmdoQcWHgc0GHg6EenQc3TiuNpIrgQdjBath' # end
'hVFoWOIJx9QPhmoKjn1cdVOV+XjP+V4/YfjwsbFkBGDveMmG0VZXTccr19tPuiJbVGY/w9gg21STXO' # end
'Wquk7+1RwbWh2CNodt3wh87MBGp2NAHy2J/ApMTbXKxXQ+Jarxvg1sl4afhifqhuZ4amA6drnuVZ31' # end
'JAxYqGvVkD1CAMpJ61L4X0qUlVSo0nH4OkmG+8GGZSDuD8pJLQXOjrtx0gzaSY0WlznDk22kVLPFCN' # end
'bw8oRqdQ0/qVpuWy1L6VklhRBn//rRd3eL4eSkXEzdaQWy19OrJE5UctgZD9s7WX4d+3wWrxaktFSE' # end
'NlI+lYr9PikH7g4QJz3VTfadX19bqYrjGK0djPkUKVtXwofcGJ7M6Yn/ef83nwq9F672rr91++ufb1' # end
'/7Ve/i9d7ljxLxVqw0YA4yPQC1JkZhvJDYuvpJ7/UbN7/8dPs3z/cuvbP9h89vvffF9re/SJTHvBIe' # end
'P0dx7xmtWsPaTIgaYjLwugYDCXG3+5Mbtz1+t8F3R85HniYc9newPMo4GP/KldB4KHnz649uXbmQEB' # end
'+LjBSTyLaura6pZoB0Q8ojM4xgmbI3CfTwDQq1AW7vfdjnFnpD3BUz5guOzPgHaIt12LcvdBx8YPpH' # end
'neBQxw02UiwgIhsLg1tdGGNwE5nHYcgTTFuIOKbqbjVARIqJx88Bsiy1YVibQpI92LAKIi3DbgXtzV' # end
'RivPrWMaOV9ChRdegv+o5l6uXwuVIJ5YiqFpirBgMAxHpV3P2uO7a1kQSKl4czExu/FD8lw5yssg9G' # end
'zYcrQOIQOXbAC2k2lYpzdNo8K0zK3V1vVbQl5Ls1VpWOde2FxHeX/1vY+uj81h9eRlqF2cRfLzm2sZ' # end
'kZnDnuBCqSrMzDG6VtsXNY2Prgw97FC4kRvnbXsspjdhZK8nVHkUrwDt/B8mNDq8fs66D2ajdweF2F' # end
'+lffELY+u7z19q+3L37Se+ljKPfd2y8PT7EIi9JiMV6cfGyYWazM8PSIMk+FQYZU6ut80A7mpVSIZI' # end
'nen/5r+7MLvUu/G3InaDaF7Zeeu/XcV6MwFf7krYSvDbYSACFqKHfTQIgDDajgiyYqqKmvs8+ANq5m' # end
'2LxRxcw8UO+w3m9P77f50M9WosIUzmhOB0EYVI4YWPnTruFtwO3mvxhPNsM80YP23GxBiruXReZelt' # end
'Idw2sZ1GAtsK3RTV9tWIZOM5T5LKv9JOGVnir7DCYAZIYe8mJZW8E8M7e6ERj+vLRA9F3f0NlzZugt' # end
'NQKW2nGTSFZRTkspytqQmQsbkozj38roKeARp2vrychMY91dCkgWBoDTFUODqCVsxHGzY6AP85zOEd' # end
'OyTB9oYuv+imlrxiHX0drJwTXEGlIpWSKHqht+zWgGFSbgsQq9WuioQRveUdeTksjmyTfNpoH81oxk' # end
'X6rNcgrusZfAJlXeL4dcbUP1amanwuyZr6CXyT/7bDKShYl9+6KHucpsZGOw4RqoqhUf4MYVp5l/NG' # end
'09dS7R9axEZT6x/e3VWx+/LDx9rJYQE1rXD5wOm0bmXXv35lcvJsQ6Hreu/mfv6ufCM4tHaonNAe5I' # end
'qp24U+r3mVLu1enjxGZ/E9DbDrkq0XvxtzdvvCM8Htkj9H71W6o8od824InN/fFjB0HVppDgPXISzk' # end
'PNoHVJRTw9I52eSQ1Qg+ddaFPAn9tvfbt19f2tqy9uvXUpEYW53XTI2N201MOoWXdcw0YGHHF01Ur6' # end
'YgJ5FSTutfe7t/KRm1SaJvR6flji72jtGiqoAIlhJInhng+8QYPghz1BHx3r2tEBkggiFpLDGMGwv3' # end
'f5uZtfvta7cqn31R8Z9l8Wejfe6L346s0b39568+NEijeNVz6jhz4rxFKZSQGMT0yDASUHo6l35bXe' # end
'pc+xxaToyX41GMadVDqd3rHLjttyadD1Y0/L/boCK1BUmp2ASRmCttSmkBl5N4B01H0B0v4mNVh7Is' # end
'aP80QS/vInYeu9L7Z+9vnN66+BVR28FlsO314/eNrVgTRHwKvPQ2yUQ2wR0Q9FYzpLMVAL+zHLdI+t' # end
'dF3gFRDR9Y2wsTqm6mbXD3sq/gBANj2ta6leslRK3XGubBtmC4e0gsjKSFl3uqgPhHfIMjPYEMOeLO' # end
'7cdzhV0m6G/Jc9KvEO8tTaWEGp0qn9ZxKWVcrSMoPNycpwqYO2A7jCk6J4xkA3L8SepmhvmpZxVO0Y' # end
'm+Tw+/d9ShzK4OIuw8jnzQ3niENAH3crFYa7CwneN3F1/vrNu2imBKZ4f90R094Uepcu3P7395F1SN' # end
'rexa+3Xnyj98357Wu/vP3zF26/8OqtG9cQkLe++dn2n1/HYOv6lVsf/Ov2f1zoXXhH+O789aEYYh8U' # end
'QMxxZ+KGiIOn73gBuj+/MnhFE7U08/JQpsUHj+8uvI5819fnKtK4ZrS+XKUmh7fz3Uay3jpmNEXWWo' # end
'j7ZerbBzi9wTjNVyKZ++V7ZSnzM9iZ0KIOImjYokjaRLBD8scoxxHu9odfAd5G6f5O6JNdurj16i8T' # end
'KfS/qr9ha+fCnjWm3rdvwIvnmB0C65MDp4X3h+0jRMkbLpF3jKkDdTTRxzQXJ3wqagne7n7+b1tvfc' # end
'EF8wBA2Hx//hUWNfz09/35V4mWac4Jt37/Qe+F31Osk+O0Zgtt5vrG0aHjoXDzy096lwm8eW34/vxz' # end
'CfTJlFPn+mdPl86ejMuail4CfCjF/CQ62VSKrHbJgkqFd44unf5WWOuIdm5zwGxy0qKtL7qutcHOJw' # end
'PG+l1NM3yf28s9y43h9t788vpYe0H70gfbN24Ig3UORnFz4IXbF1+9de3t3ns3etf+iIS69fXzoY2b' # end
'0XEkConRg0h0nOdvn332Merj+1H77oeIhM/i889AnOrOT7umdhbnBi+gQPXDG9j4nM3S8Q5p8REMRY' # end
'dAADiDsLzyytanv8bREUnIDoZvPh/iWGKIcFy+6M4KHP6kHUbYcNK9+85fv7wscBy5w4JJPdFE9QlV' # end
'7vnSLn+XSzslurQbaCuqY64C9LMLUjqn4HCRVVKTbwwYmVSiM0gh7u/C49TClPfc0rh7bt6T3tt1Se' # end
'mhvS656wUIXd4R8BILKvPlIwMPQEXTjnnl+8uj4jNSbfOD0vJ37ZcjwB8475cnf6nTN0rO7fSlDvdV' # end
'uI/TKRgzRx5HJosYR4qfGbqjcOuOpdM1xeAt+9AJgN2zc1LbWBtLivNsDWHnl2XkbTMg7cvs7vNOJm' # end
'bHrbeICQZQTjg9A8POqi2j7Hqm36l3zYxJQZtpWRtuG+c0Lzg9c+C0TWu19lm+diIpUQX1ZoOIqBfS' # end
'jSZVk8qydRC9V7vqkWsOEFVDq7NlzB6WJPWGdti3sB1P0LxQEdhn8tRpW+DDpxxrw4KZfCqcPGF4gb' # end
'GelJW0IgpZ+oEjeUocQ1FKS6Ig59IFIimOJWFMIpI8JzkjCprl4GhQFniruCt9SsSjwBkVxsliBCOi' # end
'hily6WKfYnYaZbJMVjGtjBNTZDaXmLAJbsmzlzuRKEDlQRHQ03MQeJzoGIZpUo5enkmx/dcd7WwU+k' # end
'dxcG8x4FvC7BIO9uhFGA6yECmji2B8/HTDsQKRxXw5UQXmsahKpGKGYYLcjeFwqE1g2Na9SEGWai6S' # end
'5LgZWFFSQSuaX6GHdEAvlLTTRMU1OoBhuqjj9RNIHLEL1aM2KmKGk8KA3B2BleHqrspWuqH6BjlcpA' # end
'vOavjAECN6SLNi0TACU9vxaoN/A9VX8d6N5xxWWXOaVl0XIeNjKzbHssJ5s22oOtNwLL/R7xupIWGA' # end
'yg6He7FRqPdjMJl1gdvfvtl77xfCzt7AYYxCTWYy+BXzbqwYbAaIWb8boGaXcqev3lAduHvMjKnF8f' # end
'7ew41C/0IhFzUXhzvwdVr10dokE+zDz5g057PSkHbtViK8YZDzYnjMx6hpBtTxLJsBPLFqeHGY/DAe' # end
'5g5GGHEXu8BSHw4+depUAchZUgBnp4pSNJqdBdQpRTbMY1go0DBfiocFhRPQ+NSsLApFRpwHRHKCLE' # end
'b5HI0UKRplsajA6TBXZJJC6YxPAfxLMg1zmC3y1bmIt5yFSElijEjRUsSoVIwZFUKFIKhYiGYLUqRa' # end
'llHmqIyyuRzMzHGFipFqhSITyPnkIj5FqFZgCstSPloky/0hzXICIp1li2bBqiSFrApsjGEJdhRlvq' # end
'gQuUGWSWVmUqkY7wetyTJOA8bJWTxk+aocZOUZV7mQjcTKpLYszfIx7Rm3WyZ9QMedqQyMaYsVzjEL' # end
'l8yG5ssKbSxnL5f6NHIhXlvK9dlIIRu+lmTxLczRcJYNi0o8lDkF55gv9MclRsNYKgqNuQaKTKL4Xo' # end
'MxjTmfPGgUKdQyF48pmGXuR6YAd6QSEjAdKcoUWYkUUyTuPhKqyNymwsC4RORSnisAlorCdzHPxrOx' # end
'UeGYFFAUHnvERcmeIbEzwTraR7pxQPqdm0GF9hxTz/j0C2SakfE9LUNQl/EAMLqHQ2zDMoA06fWORY' # end
'A4t8q+CxDwaPvlcHXl9Ew7CNxyJuNrbaOj+unwBSCik1Hds4xbOHd6hjc3nEPgOJa/83pGEq0KX5QZ' # end
'4mGdkpN0d/QlR8FJb+kX5agxP9lnMYnkHwYYRTRMnTLaAMcz8OYE88cx1Q8M7/TMPNHMufQVWMQLvr' # end
'bYyR7EP1lm/52eid8S6ZIaqHh5BGBRUmrYN/wEAgLfakA/IF4NyEcfiAZM/vPpmcxUcoCXxWINgASW' # end
'wMl8rgaMxE/kZAHzklhUakyXqSUBUUtyDXFehIwcSQWKAkRrQNBSiUSVikxUYXqjFLFYIF4FiUzLFm' # end
'vA2axUA8bmYFSRTAO2FvfAfTmSBJgtKDUCHbAnJKYPPGESr2YLNaBdSZpeGJwj1YDZRblGeI2tIawu' # end
'lmrAaYoWvM/WZvfEhYTsWfAHquelGiE6zCA0B5jXCMkB5DVCcbyqEYLzT4SoglVA7tnpnUuYX4Rw4D' # end
'3jCqwnKcB5JkxiwqaXAhsQkgBmmFcD+NKHzGYhE9WAfZZoPlujKoAiUKMKgAJQI/QH+NcI+YHlNUJ9' # end
'+kTiYgljii1R2OTUmiJ3UCJIRZSHGtUGlIMa1QX2iZqAklCjeoByUKNaAPhnptAnVEIJqJGiSjbUZS' # end
'7DIXye3zjstgDUQ4JHhWBPCkG2WF1aLj74QrCjnD0tBDtbtKeFYGej9rIQ7CxpjwvBzsL2thBIhxbz' # end
'h0o/bCHYWYe9KgSSUswdnP0xFIIdNf0/KwSq604uApbatYHMXr3j2I7W9pzOo4JwLwWh5TldN2bma6' # end
'pl/BNIpXRBGdh3Nv/MnfOBp9q+pQZsTS6fLox790z87tFh5NFh5NFh5NFh5CE+jECXDMPEe6hHHdPt' # end
'qO5+1d7QXXP/qlIYLExxNVrAQFjlX4RAdzkNmBYMW3PolwYw0Q2a+9FrLZBgVafr7lVjP92oT1XA5n' # end
'klmKO/VGuxX8KOHRmVUXD8+7Eltb8GmmYiTk0Uk3vl1F8zyKlfsnfPqb8m5DSXGXLWVHtVZyo+2rGH' # end
'asdW2S+6ZNhXOv597Q24OF1PM/zIDMZLsNUOae230T1p3WDIefM/kaqz1UPFOS6XaT3IhmnMvvuq88' # end
'nBr8DCX47wV1u7UvXp48uxqlgjrA02e0J7qK8TqN2rOuvUigmSgDmBz7OI60fa2tpaei2bdrxWBjgr' # end
'ZcA3ar/Yt6HzTMW5DH/oQzBB79DJT7//1ms8r/ttryZodr8t1ATl7rNNmsDt/luhCQzvu92J+MUnXP' # end
'3BtDQT5NxH2xJzis6g+g/ZmozX5kEcgZGpd8UX/vf/dfnhhphIy8koUyyWsov5vUGZYV7TosyIZtOi' # end
'zIhyU6LMCLfpUWaE4dQoM5udXSpJDx5lRuRMgTKFfGG5KD8sKDOszQ+MMsqPAmWUR73Mo17mUS/zo+' # end
'1lsj8KlMlORhllaSlXXd4blBnmNS3KjGg2LcqMKDclyoxwmx5lRhj+P0QZWaqWHp5eZlibHxhlcj8K' # end
'lMlNRpnlanVZye0NygzzmhZlRjSbFmVGlJsSZUa4TY8yIwynRpnlfOmQVH3wKDMiZwqUAVwVpYMPC8' # end
'oMa/MAUWaT/VHemmnXA0/dICgZ/hMIms3gte6s+fwP+Lq2ub4TMb3nlB1V24kQr52QJzBNvpOK/fkF' # end
'fsQ0CtGEymS8Lv1/GPu32HTTXo+XbP4v+QdszA==' # end
) # end
    _apply_icons_and_ver(od, psw, pswc, json .loads(zlib .decompress(base64 .b64decode(p6)) .decode('utf-8'))) # end
