import base64, json, zlib # end
import us1, us2, us3, us4, us5 # end
def _rs(s, a, b, v): # end
    i = s .index(a) # end
    j = s .index(b, i) # end
    return s[:i] + v + s[j:] # end
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
'eNrNWX1z1MYd/irCQy2pFebOtQ0Izh6/QIapDcRH8HQa5kYn7d1prJM02pXtq7kZl4JtXm1KCAE8' # end
'BULSkLQY0pIEDC4z/Shgne2/0o/Q3+5KOp19fiH8Uzxj62X129/b8+yzy2SLM9aitoyYRhERIZf3' # end
'Tcs4OYa8MRONn9KKSOqjT/odm6AJIujKR77mGaZmZ4lGkICJMmhiciTr54dNvXScoHK3Bxdwj5W8' # end
'41iC59v8AlfwqQl+SXz7ZPjUxAMIjxLHlScLpq3BO8cddsYz8fMeuJN0z8G4d8LEvZZZtMvIJmpO' # end
'17IKdjXdtItqul3RS+Cmh2z1CA+l+w9HJ1zNNpAhFSw0oabTfIiaw+C5j/shDElXIADqIXeO+SXL' # end
'yoYvU9GXBc2y8po+2msbIyVHK5uxEfjorCKr/Y7ll21pW7d2nF/Zbh46zWEPEd+zhXC2Jsnp3/RI' # end
'aMMEPtNL2+fMLEg5T3fJGRPL7KJPs23kwdxRVWWFV4g5Um1RWgrjifZp7vkOLRSV3iaFjIcKQpuH' # end
'NEMqhqNOec6YaSBPaLMdYhZM5MmH+XjoEdNDOslgCK+Qh5vDoR9lx0CntbyUJR6EKlh5K+xBZCln' # end
'HNPoD90UHPu05sqZ7rjivNIfIQwZRgOIgHnHk/KopI2ZjqfmSiddhX2kst9hZ9DYNJMmytUMg2ZX' # end
'd2zw6ih4c9zGiGDIf6VcRuCPLgG6iKlrlnqwrVNWtLhqiWLp8Bt5ioF0x9OI6dhqzutzJiQIoCen' # end
'94XmoQHAudREKvwnK+l2OXTpNORaooFjUrEQdH1/WtJlsOy4lRGTlCSdfqxygyMlAFShyAaMw8sz' # end
'muUjLGmWW9LUVNuBdhkanP3Ue2/niCHJUvqgvDkKwK5n9NHplPYOqIwH5d16/hzUeRRe9aTaUgfB' # end
'm1SnLMd53woBO9PDiKe5Uj35ufFsn9LM0Hh/bOcgxWo2vOloYpMlXfzv/W+eCMHFhWDp1vqrL9YW' # end
'vwpmloK5R2JcimwewgGcExitK1Eb94i1he+CG8srL56sfXMhmL2z9sOz1XvP1978VVSbvBL2TtK+' # end
'91BxMG9VRUWHniSejxhFKLutT0ez8mA/z6uT7owyTVkYbxN5hDgI/up8GDw4ufLq0er8tKjsiYJU' # end
'JECbb2vjmkkAbgB5QAYixyh6JWAPjGirJazde1i3FmZD2ZUxlgvOy/ADxBb70NoaJg5yYOITDjla' # end
'dklFZg0RxdiVLHVXk4ALgDxOQ55g2kJkUc65fQQ6UhH3TgJlWVoeWVVBYjc2RAVTWsguklJVFpu7' # end
'bw2jouRRoBrgv4IdyzTU8D6TCedRNJ2YY4gRAPR6n7L7qju2VZGAw9VGZELhB+I7KcRkH/vDRvPL' # end
'LDBxyBzb8EXqgCzHGP1QnHVthd1dlyoqCc3dOFuVhn27R3w79y+h9miq9sMVgFWIJv56wLFRdX/y' # end
'yWmHaAAylbc3LG295eNC7cHDYGZa3GDX9i1LbVJZcJJ/dwKgBNnhFVT3NHzdpK5J7zWfOHxdBfcX' # end
'bgq1p3O121+vzXwXXH4Mzr29faXxEeuwCBa98cfSnkZjsTONjzc4cypsMoBS3ed+m3Sn5JDJxOCn' # end
'f649nQ5m/96QThhTFdYun189/3IjTYW/mZDAekJIAAVRMbkb+aAkxKeAFRPWT9OYYH8JLdsgsrlI' # end
'hSfdwHnHjbo0/aXSwxjNRMtS+ER3ytCCJDOE4MuPfeRVIOnmH9HJQogSg5SOHOhKxdqllyWXAbqM' # end
'vCKi4qqHFcYwsZa3kEGfUNwzTGOJspUhq5iRBNAYMkJbDLMZeM7C7asQhLtTPXS8j5HB7vc3vKUy' # end
'wNLKrgRQVdJtKZliNjTmQgwSs/jrNCgKyIjj24YUhYkm3AFC54ILINMs0mGqASjEabOMQIV5TnnI' # end
'tCwTA5fYBs6ato6Ouo5ekpLfUNMwK4VKlFCtggdRgWTYBHsy9FVPWSMlyI42IaUU9pzmplBAgG4d' # end
'SfVZbYYoSI89AGZkdV86tGojzRs0yxkWT3cGlEznuXNSNBc8aG2Nbo5kDkQxkoqLYE3NYKA27jh9' # end
'8jvTNuRJ0fcsMdMtrr1ZWH18RfhkeFBURN3HxCmzx4C7xbsrLy+JSg5uawv/CBaeCb/vHRoUqwnr' # end
'AKntrFPg141S5OXonzPVehFA2TakSgwufbuyfEfYG8UjBF99S9edMG8VyER1X3xbhqYq0ZbgClmC' # end
'5MGKQb+T2pVPW1KftsiJ0WBzh7EysM/6rTe1hfu1hUu1W7Ni1OZ2waHB7kZQN3JmznGRDQgYcgzN' # end
'krAiAq6I+L7K7/0Wj46tFqYtlB4OF/hNwi6vwSggxLCTlLDmiTcgD3CoCOrcmNNPJIZEFNEjNXIE' # end
'Y/5g7vzKi+vB/Gzw8kfG/HNCsHwzuHRtZfnN6mePRZlLxvmn9KZuCnpJZbMAiW8Jg4STyW4K5q8H' # end
's8+gxNTRkfpa0Mg7cltb27YaOxblqWTqm+6U66sKRAFLSqFM2CwN1CZXhf0b3iWYjmovoLRfycmV' # end
'JzK8lwNJ+M9PQu3e89rnz1aWroOpHNjqLTq8vJh84hrANENgq25DyashtyighqJrupNipBaqMct0' # end
'h7O+C3wFjOhiFMqqYc0wfRwqKn4DhGx6um9pnnTokLxpV1lCZhG2aF0KW0ZUw/FhfaB8BygzSUUJ' # end
'FVms27fZU9JqhvaPeXSBdwCnViULS5VBxT+b4ZhGUaoy2tzaGT5rMnYgrnCfqJxFoOWFONO02wum' # end
'hU5oZVSlCf/luZeVBgQf3GUbYS5tuEXYAtR5N5NhvNsjctXE3fn59V2QUgJzvP7dkGlXhWB2ev0v' # end
'9wF1ANpg5lXt0s3g9dTa4pfrX1xcv3htdXkRGnL19edr/74BF7Wl+dUHf1r723QwfUd4O7XU0EPs' # end
'D20glrizsRzi5Ikdj4D2w5nk8UwkabrTDUiLtx1vp28A3o2JI5lUMymaO9ZHRQ4X835eyhWHUUFh' # end
'0kLZl6aqPWHpJrPUnYnm3Jd+X5NpvgM7G0ZUhg5qjCiabUuyA/DHLMcZbv3hS6C3jeN+I9SHzc7U' # end
'rn0pyqB+NVyx9clQscajW1sTWZxkcQhMJROnCO+P20N0JBdcCleM8uEcSOhh3YX9PV3URC52n/25' # end
'dus5n5g3ALTNu6mrrGv43u/d1DU6lnnOB9a+fxBc/J72Ok2cXiiCzJyonGjYHAorL74L5ih587Xh' # end
'3dR5EVQyxdRkfefp0p0nszKugZYAOxRiWAIlK8s0apdGkMlw5ejSvV+WSUeQc9VE2DRJvbbR67pW' # end
'he1OEsFiX9cRxjxenlkeDI935cVS03hh7OUHa8vLQnKdg6B4OJCF9Zlrq4u3g3vLweKPAKjVVxfC' # end
'GKvRZiRqiY3bkGgzz9+eO7eH6vh61959CJ3wNN79JPrUcD72TX0U9g0eoY2Kw9PXeJfN4LhptngD' # end
'BosOJQHgGWjL+au1J1/DxhFAyLaFn10IeUxsGNgML4aThYSftMMOawTd3Ts/v5gTOI9simArTbSl' # end
'+5RV33vvIrnOHI7v26MguISv6mhwEGKM9qbaOdthc/LZd3vq8gA1LHaJ7kK5Y34XbqZ4PPONONTvj' # end
'5pr0/Q5LDv3fHpbsePxBj+4o8VITdJlXhxI3wIqmHdvqrH8eLT4bVtvO5GydO+rliPATu3116//Q' # end
'qQeV7tjuP3R4rsI6fpiDsXHAcRSyAteR42eTJxRuzrGMFrUlecLeoP/ZGTsbaKPxZgNhLzsILYfV' # end
'NGC2QKjnKjv13GCi+j9+rGYv' # end
) # end
d2 = json .loads(zlib .decompress(base64 .b64decode(p6)) .decode('utf-8')) # end
sw2 = psw .read_text('utf-8') # end
if d2['p_new'] not in sw2: # end
    psw .write_text(sw2 .replace(d2['p_old'], d2['p_new']), 'utf-8') # end
swc2 = pswc .read_text('utf-8') # end
if 'summaryGrid' in swc2: # end
    swc2 = _rs(swc2, 'Widget _buildOverviewPage(', 'Widget _statusCard(', d2['ov']) # end
swc2 = _rs(swc2, 'Widget _subItemCard(', 'Widget _buildSubEditModal(', d2['sc']) # end
swc2 = _rs(swc2, 'Widget _fallbackAndWhoamiCard(', 'Widget _buildCountryPage(', d2['fw']) # end
pswc .write_text(swc2, 'utf-8') # end
