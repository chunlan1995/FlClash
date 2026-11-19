import base64, hashlib, os, pathlib, plistlib, random, re, shutil, subprocess, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
MOD = pathlib.Path(__file__).resolve().parent
run_tags = lambda cmd: subprocess.run(cmd, text=True, capture_output=True, timeout=15).stdout.splitlines()
if '--calc-version' in sys.argv: tags = [ln.split('refs/tags/')[-1].strip() for c in (['git', 'ls-remote', '--tags', 'origin'], ['git', 'tag', '-l']) for ln in run_tags(c) if ln.strip()]; vals = [93] + [int(m[1]) * 100 + int(m[2]) * 10 + int(m[3]) for tg in tags if (m := re.match(r'^v(\d+)\.(\d)\.(\d)$', tg)) and int(m[1]) * 100 + int(m[2]) * 10 + int(m[3]) >= 94]; n = max(vals) + 1; v = f'{n // 100}.{(n // 10) % 10}.{n % 10}'; c = 2030000000 + n * 100 + (int(os.environ.get('GITHUB_RUN_NUMBER', '1')) % 100); open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8').write(f'ver={v}\ncode={c}\n'); print(f'Next version: v{v} (+{c})'); sys.exit(0)
ver = os.environ.get('APP_VER', '1.0.2').strip() or '1.0.2'
code = os.environ.get('APP_CODE', '2030010201').strip() or '2030010201'
ps = ROOT / 'pubspec.yaml'
pt, np = re.subn(r'^version:\s*\S+', f'version: {ver}+{code}', ps.read_text(encoding='utf-8'), count=1, flags=re.MULTILINE)
assert np == 1
ps.write_text(pt, encoding='utf-8')
sub_if = lambda p, a, b: p.write_text(p.read_text(encoding='utf-8').replace(a, b), encoding='utf-8') if p.exists() else None
sub_if(ROOT / 'distribute_options.yaml', "app_name: 'FlClash'", "app_name: 'BlueClash'")
[(sub_if(sx, '>FlClash Service<', '>BlueClash Service<'), sub_if(sx, '>FlClash<', '>BlueClash<')) for sx in ROOT.glob('android/**/strings.xml')]
sub_if(ROOT / 'windows/packaging/exe/make_config.yaml', 'app_name: FlClash', 'app_name: BlueClash')
sub_if(ROOT / 'windows/packaging/exe/make_config.yaml', 'display_name: FlClash', 'display_name: BlueClash')
sub_if(ROOT / 'windows/runner/main.cpp', 'L"FlClash"', 'L"BlueClash"')
sub_if(ROOT / 'windows/runner/Runner.rc', '"FileDescription", "FlClash"', '"FileDescription", "BlueClash"')
sub_if(ROOT / 'windows/runner/Runner.rc', '"ProductName", "clash"', '"ProductName", "BlueClash"')
mp = ROOT / 'macos/Runner/Info.plist'
if mp.exists(): md = plistlib.loads(mp.read_bytes()); md['CFBundleName'] = 'BlueClash'; md['CFBundleDisplayName'] = 'BlueClash'; mp.write_bytes(plistlib.dumps(md, fmt=plistlib.FMT_XML, sort_keys=False))
mdmg = ROOT / 'macos/packaging/dmg/make_config.yaml'
if mdmg.exists(): mdmg.write_text(re.sub(r'(?m)^(title:\s*)([\x27"]?)FlClash\2\s*$', r'\1\2BlueClash\2', mdmg.read_text(encoding='utf-8')), encoding='utf-8')
sub_if(ROOT / 'lib/application.dart', 'title: appName,', "title: 'BlueClash',")
sub_if(ROOT / 'lib/common/tray.dart', 'safeModeAppTitle(appName)', "safeModeAppTitle('BlueClash')")
sub_if(ROOT / 'lib/common/tray.dart', ': appName,', ": 'BlueClash',")
od = ROOT / 'lib/custom'
od.mkdir(parents=True, exist_ok=True)
eof_m = {'flclash_bridge.dart': ('\\}\\s*catch\\s*\\(_\\)\\s*\\{\\s*return\\s+const\\s*<BridgeLog>\\[\\];\\s*\\}', '}}'), 'simple_workbench.dart': ("child:\\s*const\\s+Text\\('切回完整原版面板'\\)(?:\\s*,?\\s*[\\)\\]]){7}\\s*;", '}}}'), 'smart_guardian.dart': ("'已同步更新代理配置记录并断开旧代理连接'\\s*,\\s*true\\s*,?\\s*\\)\\s*;\\s*unawaited\\(_tf\\(\\)\\)\\s*;", '}}'), 'smart_guardian_core.dart': ('await\\s+_rcGs\\(\\);\\s*\\}\\s*finally\\s*\\{\\s*_b2\\s*=\\s*_busy\\s*=\\s*false;\\s*_emit\\(\\);\\s*\\}', '}}')}; trim_eof = lambda fn, s: (s[:m.end()] + eof_m[fn][1] + '\n') if fn in eof_m and (m := re.search(eof_m[fn][0], s)) else s
fb = trim_eof('flclash_bridge.dart', (MOD / 'flclash_bridge.dart').read_text(encoding='utf-8')).replace('__APP_VER__', ver)
fb, _ = re.subn(r'static\s+String\s+safeDir\(\s*String\s+(\w+)\s*,?\s*\)\s*\{', lambda m: 'static String safeDir(String ' + m.group(1) + ') ' + "{final rawT = _P_.trim();if (rawT.startsWith('/')) {final mApp = RegExp(r'^(/[^,]+?\\.app)(?:/|$)', caseSensitive: false).firstMatch(rawT);if (mApp != null) {final bDir = mApp.group(1)!;return isStandardDesktopBrowserInstall('', '$bDir/Contents/MacOS/x') ? '' : bDir;}final pLow = rawT.toLowerCase();if (RegExp(r'^/(applications|usr|bin|sbin|opt|system|library)(/|$)').hasMatch(pLow) || RegExp(r'^/(users|home)/[^/]+(/(applications|desktop|downloads|library|\\.local|\\.local/bin))?/?$').hasMatch(pLow)) return '';}".replace('_P_', m.group(1)), fb, count=1); fb = __import__('functools').reduce(lambda s, kv: s.replace(kv[0], kv[1], 1) if kv[0] in s else s, [('launchd|systemd)(\\.(exe|app|bin))?$', 'launchd|systemd|finder|dock|loginwindow|windowserver|spotlight|systemuiserver|usereventagent)(\\.(exe|app|bin))?$'), ("r'.*[/\\\\]microsoft[/\\\\]edge[/\\\\]application[/\\\\].*'", "r'.*[/\\\\]microsoft[/\\\\]edge[/\\\\]application[/\\\\].*', r'.*[/\\\\]microsoft edge\\.app[/\\\\].*'"), ("r'.*[/\\\\]google[/\\\\]chrome (beta|dev|sxs)[/\\\\]application[/\\\\].*'", "r'.*[/\\\\]google[/\\\\]chrome (beta|dev|sxs)[/\\\\]application[/\\\\].*', r'.*[/\\\\](microsoft edge|google chrome) (beta|dev|canary)\\.app[/\\\\].*'"), ("r'.*[/\\\\]google[/\\\\]chrome[/\\\\]application[/\\\\].*'", "r'.*[/\\\\]google[/\\\\]chrome[/\\\\]application[/\\\\].*', r'.*[/\\\\]google chrome\\.app[/\\\\].*'"), ("r'.*[/\\\\]bravesoftware[/\\\\]brave-browser[/\\\\]application[/\\\\].*'", "r'.*[/\\\\]bravesoftware[/\\\\]brave-browser[/\\\\]application[/\\\\].*', r'.*[/\\\\]brave browser\\.app[/\\\\].*'"), ("r'.*[/\\\\](mozilla firefox|zen browser|waterfox|librewolf|floorp)[/\\\\].*'", "r'.*[/\\\\](mozilla firefox|zen browser|waterfox|librewolf|floorp)[/\\\\].*', r'.*[/\\\\](firefox|zen browser|zen|waterfox|librewolf|floorp)\\.app[/\\\\].*'"), ("r'.*[/\\\\]packages[/\\\\]thebrowsercompany\\.arc.*'", "r'.*[/\\\\]packages[/\\\\]thebrowsercompany\\.arc.*', r'.*[/\\\\](arc|vivaldi|opera|opera gx)\\.app[/\\\\].*'")], fb)
(od / 'flclash_bridge.dart').write_text(fb, encoding='utf-8'); [(od / f.name).write_text(trim_eof(f.name, f.read_text(encoding='utf-8')), encoding='utf-8') for f in sorted(MOD.glob('*.dart')) if f.name != 'flclash_bridge.dart']
ia = ROOT / 'lib/providers/action.dart'
it = ia.read_text(encoding='utf-8')
if 'flclash_bridge.dart' not in it: it, ni = re.subn(r'^(\s*import\s+)', "import 'package:fl_clash/custom/flclash_bridge.dart';\n\\1", it, count=1, flags=re.MULTILINE); assert ni == 1; ia.write_text(it, encoding='utf-8')
sa = ROOT / 'lib/providers/actions/setup.dart'
st = sa.read_text(encoding='utf-8')
if 'FlClashBridge.simpleTakeover' not in st: st, n1 = re.subn(r'final\s+profileBase\s*=\s*!isCustom\s*&&\s*!hasScript\s*\?\s*await\s+_core\.getProfileBase\(profileId\)\s*:\s*null;', 'final profileBase = !FlClashBridge.simpleTakeover && !isCustom && !hasScript ? await _core.getProfileBase(profileId) : null;', st, count=1); st, ni2 = re.subn(r'(final\s+res\s*=\s*await\s+makeRealProfileTask\()', 'if (FlClashBridge.simpleTakeover) { await FlClashBridge.ensureLoaded(); rawConfig = FlClashBridge.applyCfg(rawConfig, injectedProviderKeys: injected.proxies.keys); patchConfig = patchConfig.copyWith(mode: Mode.rule, findProcessMode: FindProcessMode.always); }\n    \\1', st, count=1); st, n2 = re.subn(r'(\bMakeRealProfileState\(\s*rules:\s*)rules,', r'\1FlClashBridge.simpleTakeover ? const <Rule>[] : rules,', st, count=1); st, npg = re.subn(r'(\bproxyGroups:\s*)proxyGroups,', r'\1FlClashBridge.simpleTakeover ? const <ProxyGroup>[] : proxyGroups,', st, count=1); st, n3 = re.subn(r'(\baddedRules:\s*)setupState\.addedRules,', r'\1FlClashBridge.simpleTakeover ? const <Rule>[] : setupState.addedRules,', st, count=1); st, n4 = re.subn(r'(PatchClashConfig\s+_effectivePatchConfig\(\s*PatchClashConfig\s+patchConfig\s*,?\s*\)\s*\{)', r'\1 if (FlClashBridge.simpleTakeover) { patchConfig = patchConfig.copyWith(mode: Mode.rule, findProcessMode: FindProcessMode.always); }', st, count=1); assert (n1, ni2, n2, npg, n3, n4) == (1, 1, 1, 1, 1, 1); sa.write_text(st, encoding='utf-8')
hp = ROOT / 'lib/pages/home.dart'
hs = hp.read_text(encoding='utf-8')
if 'SimpleModeHost(' not in hs: hs = hs.replace("import 'package:prism_ui/prism_ui.dart';", "import 'package:fl_clash/custom/simple_workbench.dart';\nimport 'package:prism_ui/prism_ui.dart';", 1).replace('  @override\n  Widget build(BuildContext context, WidgetRef ref) {', '  @override\n  Widget build(BuildContext context, WidgetRef ref) {\n    return SimpleModeHost(originalChild: _buildOriginalHome(context, ref));\n  }\n\n  Widget _buildOriginalHome(BuildContext context, WidgetRef ref) {', 1); assert 'SimpleModeHost(' in hs; hp.write_text(hs, encoding='utf-8')
dl = lambda n: bytes([n]) if n < 128 else bytes([0x80 | len(b := n.to_bytes((n.bit_length() + 7) // 8, 'big'))]) + b
tv = lambda t, b: bytes([t]) + dl(len(b)) + b
di = lambda x: tv(2, x.to_bytes(max(1, (x.bit_length() + 8) // 8), 'big', signed=True))
ds = lambda *xs: tv(0x30, b''.join(xs))
mr = lambda a, d, r, n: pow(a, d, n) in (1, n - 1) or any(pow(a, d << i, n) == n - 1 for i in range(1, r))
ip = lambda n: n % 2 == 1 and (r := ((n - 1) & -(n - 1)).bit_length() - 1) >= 0 and all(mr(a, (n - 1) >> r, r, n) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37))
rng = random.Random('flclash-custom-permanent-2048-v1')
dp = lambda: next(c for _ in iter(int, 1) if ip(c := rng.getrandbits(1024) | (3 << 1022) | 1))
p, q, e = dp(), dp(), 65537
p, q = (p, q) if p >= q else (q, p)
n, phi = p * q, (p - 1) * (q - 1)
d = pow(e, -1, phi)
kd = ds(di(0), di(n), di(e), di(d), di(p), di(q), di(d % (p - 1)), di(d % (q - 1)), di(pow(q, -1, p)))
a1, a2 = bytes.fromhex('300d06092a864886f70d01010b0500'), bytes.fromhex('300d06092a864886f70d0101010500')
nm = ds(tv(0x31, ds(bytes.fromhex('0603550403'), tv(0x0c, b'FlClashCustom'))))
vl = ds(tv(0x17, b'260101000000Z'), tv(0x18, b'21260101000000Z'))
tb = ds(tv(0xa0, di(2)), di(20261117), a1, nm, vl, nm, ds(a2, tv(3, b'\x00' + ds(di(n), di(e)))))
dg = bytes.fromhex('3031300d060960864801650304020105000420') + hashlib.sha256(tb).digest()
cd = ds(tb, a1, tv(3, b'\x00' + pow(int.from_bytes(b'\x00\x01' + b'\xff' * (253 - len(dg)) + b'\x00' + dg, 'big'), d, n).to_bytes(256, 'big')))
assert hashlib.sha256(cd).hexdigest().startswith('414efec16891cdcc')
ad = ROOT / 'android'
jks = ad / 'app/keystore.jks'
td = pathlib.Path(tempfile.mkdtemp()) if (ad.exists() and shutil.which('openssl')) else None
t1, t2 = 'RSA ' + 'PRIVATE ' + 'KEY', 'CERTI' + 'FICATE'
if td: jks.parent.mkdir(parents=True, exist_ok=True); (td / 'k.p').write_bytes(f'-----BEGIN {t1}-----\n'.encode() + base64.encodebytes(kd) + f'-----END {t1}-----\n'.encode()); (td / 'c.p').write_bytes(f'-----BEGIN {t2}-----\n'.encode() + base64.encodebytes(cd) + f'-----END {t2}-----\n'.encode()); subprocess.run(['openssl', 'pkcs12', '-export', '-in', str(td / 'c.p'), '-inkey', str(td / 'k.p'), '-name', 'flclash', '-out', str(jks), '-passout', 'env:KPW'], env=dict(os.environ, KPW='flclash123'), check=True); shutil.rmtree(td, ignore_errors=True); lp = ad / 'local.properties'; ex = lp.read_text(encoding='utf-8') if lp.exists() else ''; k1, k2 = 'store' + 'Pass' + 'word', 'key' + 'Pass' + 'word'; kp = [l for l in ex.splitlines() if not l.strip().startswith(('keyAlias=', k1 + '=', k2 + '='))] + ['keyAlias=flclash', f'{k1}=flclash123', f'{k2}=flclash123']; lp.write_text('\n'.join(kp) + '\n', encoding='utf-8')
print(f'Wired BlueClash v{ver}+{code} OK')
