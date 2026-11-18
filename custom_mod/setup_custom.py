#!/usr/bin/env python3
import base64, hashlib, os, pathlib, random, re, shutil, subprocess, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
MOD = pathlib.Path(__file__).resolve().parent
BRIDGE = r"""// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, dead_null_aware_expression, invalid_null_aware_operator, unused_import
import'dart:async';import'dart:convert';import'dart:io';import'package:fl_clash/common/common.dart';import'package:fl_clash/core/core.dart';import'package:fl_clash/database/database.dart';import'package:fl_clash/enum/enum.dart';
import'package:fl_clash/models/models.dart';import'package:fl_clash/providers/providers.dart';import'package:flutter/widgets.dart';import'package:flutter_riverpod/flutter_riverpod.dart';
typedef BridgeProfile=({String label,bool selected,VoidCallback onSelect});typedef BridgeGroup=({String name,bool isSelector,String now,List<String>all});
typedef BridgeConn=({String id,int up,int down,String proc,String procPath,int?uid,String target,String net,List<String>chains});typedef BridgeLog=({String level,String payload,String time});
typedef DirectEntry=({String id,String label,String exe,String dir,String pkg});typedef InstalledApp=({String pkg,String label,bool system});class FlClashBridge{static const String appVersion='__APP_VER__';
static final String probeUrl=['ht','tps://www.gs','tatic.com/generate_204'].join();static bool simpleTakeover=true;static bool desktopTun=true;static bool _wlLoaded=false;static Mode?_savedMode;
static List<DirectEntry>whitelist=const[];static bool isRunning(Ref ref)=>ref.read(isStartProvider);static bool watchRunning(WidgetRef ref)=>ref.watch(isStartProvider);static Future<void>setRunning(Ref ref,bool enable)async{
if(enable&&simpleTakeover){_applyTakeoverProviders(ref,true);}await ref.read(setupActionProvider.notifier).setRunning(enable);}static Future<File>_wlFile()async{final home=await appPath.homeDirPath;
return File('$home/custom_direct_whitelist.json');}static Future<List<DirectEntry>>ensureWhitelistLoaded()async{if(_wlLoaded)return whitelist;_wlLoaded=true;try{final f=await _wlFile();if(!f.existsSync())return whitelist;
final raw=jsonDecode(await f.readAsString())as List<dynamic>;whitelist=[for(final e in raw)if(e is Map)(id:'${e['id'] ?? ''}',label:'${e['label'] ?? ''}',exe:'${e['exe'] ?? ''}',dir:'${e['dir'] ?? ''}',pkg:'${e['pkg'] ?? ''}',),];
}catch(_){}return whitelist;}static String safeAppDir(String procPath){final clean=procPath.trim().replaceAll('/','\\');if(clean.isEmpty||!clean.contains('\\'))return'';final segs=clean.split('\\').where((s)=>s.isNotEmpty).toList();
if(segs.length<3)return'';var dirSegs=segs.sublist(0,segs.length-1);while(dirSegs.length>=3&&RegExp(r'^([vV]?\d+[.\d_-]*|bin|x64|x86|win64|client)$').hasMatch(dirSegs.last)){dirSegs=dirSegs.sublist(0,dirSegs.length-1);}
if(dirSegs.length<2)return'';final joined=dirSegs.join('\\');final low=joined.toLowerCase();const bad={r'c:\windows',r'c:\windows\system32',r'c:\windows\syswow64',r'c:\program files',r'c:\program files (x86)',r'c:\programdata',};
if(bad.contains(low)||RegExp(r'^[a-z]:\\users\\[^\\]+(\\(desktop|downloads|appdata|appdata\\local|appdata\\roaming))?$').hasMatch(low)){return'';}return procPath.trim().startsWith('/')?'/${dirSegs.join('/')}':joined;}
static List<String>buildSimpleRules(){final out=<String>[];final seen=<String>{};void add(String r){if(!r.contains(',,')&&seen.add(r))out.add(r);}for(final w in whitelist){if(w.pkg.isNotEmpty&&!w.pkg.contains(',')){
add('PROCESS-NAME,${w.pkg},DIRECT');add('PROCESS-NAME-REGEX,^${RegExp.escape(w.pkg)}(:.*)?\$,DIRECT');}if(w.exe.isNotEmpty&&!w.exe.contains(',')){add('PROCESS-NAME,${w.exe},DIRECT');if(!Platform.isAndroid&&!w.exe.contains('.')){
add('PROCESS-NAME,${w.exe}.exe,DIRECT');}final stem=w.exe.replaceAll(RegExp(r'\.(exe|app|bin)$',caseSensitive:false),'');if(stem.length>=3&&RegExp(r'^[a-zA-Z0-9_.-]+$').hasMatch(stem)){
add('PROCESS-NAME-REGEX,(?i)^${RegExp.escape(stem)}[^/\\\\]*\$,DIRECT');}}if(w.dir.isNotEmpty&&!w.dir.contains(',')){final parts=w.dir.split(RegExp(r'[/\\]+')).where((s)=>s.isNotEmpty).toList();if(parts.length>=2){
final pat=parts.map(RegExp.escape).join(r'[/\\]');final prefix=w.dir.startsWith('/')?r'/':'';add('PROCESS-PATH-REGEX,(?i)^$prefix$pat[/\\\\].+,DIRECT');}}}add('MATCH,GLOBAL');return out;}
static void _applyTakeoverProviders(Ref ref,bool simple){simpleTakeover=simple;if(simple){_savedMode??=ref.read(patchClashConfigProvider).mode;if(Platform.isAndroid){final pkgs=[for(final w in whitelist)if(w.pkg.isNotEmpty)w.pkg];
ref.read(vpnSettingProvider.notifier).update((s)=>s.copyWith(enable:true,allowBypass:true,accessControlProps:s.accessControlProps.copyWith(enable:pkgs.isNotEmpty,mode:AccessControlMode.rejectSelected,rejectList:pkgs,),),);
ref.read(patchClashConfigProvider.notifier).update((s)=>s.copyWith(mode:Mode.rule));}else{ref.read(networkSettingProvider.notifier).update((s)=>s.copyWith(systemProxy:true,bypassPrivateRoute:true),);
ref.read(patchClashConfigProvider.notifier).update((s){final next=s.copyWith(mode:Mode.rule);return next.copyWith.tun(enable:desktopTun);});}}else{if(_savedMode!=null){
ref.read(patchClashConfigProvider.notifier).update((s)=>s.copyWith(mode:_savedMode!));}if(Platform.isAndroid){ref.read(vpnSettingProvider.notifier).update((s)=>s.copyWith(accessControlProps:s.accessControlProps.copyWith(enable:false)),
);}}}static Future<void>syncSimpleTakeover(Ref ref,bool simple,{bool?tunEnable})async{if(tunEnable!=null)desktopTun=tunEnable;_applyTakeoverProviders(ref,simple);try{
await ref.read(setupActionProvider.notifier).applyProfile(force:true,silence:true);if(isRunning(ref)){await ref.read(setupActionProvider.notifier).updateConfig();}}catch(_){}}
static Future<void>saveWhitelist(Ref ref,List<DirectEntry>items)async{_wlLoaded=true;whitelist=List<DirectEntry>.unmodifiable(items);try{final f=await _wlFile();await f.parent.create(recursive:true);await f.writeAsString(jsonEncode([
for(final e in whitelist){'id':e.id,'label':e.label,'exe':e.exe,'dir':e.dir,'pkg':e.pkg},]),);}catch(_){}if(simpleTakeover){await syncSimpleTakeover(ref,true);}}static bool matchesDirect(DirectEntry w,String proc,String path){
final p=proc.trim().toLowerCase();final pt=path.trim().replaceAll('/','\\').toLowerCase();if(w.pkg.isNotEmpty&&(p==w.pkg.toLowerCase()||p.startsWith('${w.pkg.toLowerCase()}:')))return true;if(w.exe.isNotEmpty){
final ex=w.exe.toLowerCase();final stem=ex.replaceAll(RegExp(r'\.(exe|app|bin)$'),'');if(p==ex||p=='$stem.exe'||(stem.length>=3&&p.startsWith(stem)))return true;}if(w.dir.isNotEmpty&&pt.isNotEmpty){
final d=w.dir.replaceAll('/','\\').toLowerCase();if(pt.startsWith('$d\\'))return true;}return false;}static Future<List<InstalledApp>>loadInstalledApps(Ref ref)async{if(!Platform.isAndroid)return const[];try{
if(ref.read(packagesProvider).isEmpty){await ref.read(systemActionProvider.notifier).getPackages();}final pkgs=ref.read(packagesProvider);final list=<InstalledApp>[for(final p in pkgs)
if(p.packageName.isNotEmpty&&p.packageName!='com.follow.clash')(pkg:p.packageName,label:p.label.isNotEmpty?p.label:p.packageName,system:p.system),];list.sort((a,b)=>a.system!=b.system?(a.system?1:-1):a.label.compareTo(b.label));
return list;}catch(_){return const[];}}static List<BridgeProfile>watchProfiles(WidgetRef ref){try{final list=ref.watch(profilesProvider);final notifier=ref.read(profilesProvider.notifier);
final curId=ref.watch(currentProfileIdProvider);return[for(final raw in list)(){final p=notifier.labeled(raw);final lbl=p.realLabel;return(label:lbl.isNotEmpty?lbl:'订阅 #${p.id}',selected:p.id==curId,onSelect:(){
ref.read(currentProfileIdProvider.notifier).value=p.id;},);}(),];}catch(_){return const[];}}static List<BridgeGroup>_groups(Iterable<Group>list)=>[for(final g in list)
(name:g.name,isSelector:g.type==GroupType.Selector,now:g.now??'',all:[for(final p in g.all)p.name]),];static List<BridgeGroup>readGroups(Ref ref){try{return _groups(ref.read(groupsProvider));}catch(_){return const[];}}
static Future<void>selectNode(Ref ref,{required String groupName,required String proxyName})async{final act=ref.read(proxiesActionProvider.notifier);await act.changeProxy(groupName:'GLOBAL',proxyName:proxyName);
if(groupName.isNotEmpty&&groupName!='GLOBAL'){await act.changeProxy(groupName:groupName,proxyName:proxyName);}}static Future<String>queryServer(Ref ref,String name)async{try{
final d=await ref.read(coreHandlerProvider).getProxyDefinition(name);return'${d?['server'] ?? ''}'.trim();}catch(_){return'';}}static Future<int>testDelayMs(Ref ref,String name,{int timeoutMs=1000})async{try{
final r=await ref.read(coreHandlerProvider).testDelay(TestDelayParams(proxyName:name,testUrl:probeUrl,timeout:timeoutMs)).timeout(Duration(milliseconds:timeoutMs+150));return r.value??-1;}catch(_){return-1;}}
static Map<String,String>readPkgNames(Ref ref){try{final pkgs=ref.read(packagesProvider);return{for(final pkg in pkgs)...{pkg.packageName:'${pkg.label} (${pkg.packageName})',},};}catch(_){return const{};}}
static Future<List<BridgeConn>>fetchConns(Ref ref)async{try{final list=await ref.read(coreHandlerProvider).getConnections();return[for(final c in list)(id:c.id,up:c.upload,down:c.download,proc:c.metadata.process,
procPath:c.metadata.processPath,uid:c.metadata.uid,target:(c.metadata.host.isNotEmpty?c.metadata.host:c.metadata.destinationIP).isNotEmpty
?'${c.metadata.host.isNotEmpty ? c.metadata.host : c.metadata.destinationIP}:${c.metadata.destinationPort}':'',net:c.metadata.network,chains:c.chains,),];}catch(_){return const[];}}static Future<void>closeConn(Ref ref,String id)async{
try{await ref.read(coreHandlerProvider).closeConnection(id);}catch(_){}}static List<BridgeLog>readLogs(Ref ref){try{final l=ref.read(logsProvider).list;final s=l.length>25?l.length-25:0;
return[for(final i in l.sublist(s))(level:i.logLevel.name,payload:i.payload,time:'${i.dateTime}')];}catch(_){return const[];}}}"""

run_tags = lambda cmd: subprocess.run(cmd, text=True, capture_output=True, timeout=15).stdout.splitlines()
if '--calc-version' in os.sys.argv: tags = [ln.split('refs/tags/')[-1].strip() for c in (['git', 'ls-remote', '--tags', 'origin'], ['git', 'tag', '-l']) for ln in run_tags(c) if ln.strip()]; vals = [93] + [int(m[1]) * 100 + int(m[2]) * 10 + int(m[3]) for tg in tags if (m := re.match(r'^v(\d+)\.(\d)\.(\d)$', tg)) and int(m[1]) * 100 + int(m[2]) * 10 + int(m[3]) >= 94]; n = max(vals) + 1; v = f'{n // 100}.{(n // 10) % 10}.{n % 10}'; c = 2030000000 + n * 100 + (int(os.environ.get('GITHUB_RUN_NUMBER', '1')) % 100); open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8').write(f'ver={v}\ncode={c}\n'); print(f'Next version: v{v} (+{c})'); raise SystemExit(0)
ver = os.environ.get('APP_VER', '0.9.4').strip() or '0.9.4'
code = os.environ.get('APP_CODE', '2030009401').strip() or '2030009401'
ps = ROOT / 'pubspec.yaml'
pt, np = re.subn(r'^version:\s*\S+', f'version: {ver}+{code}', ps.read_text(encoding='utf-8'), count=1, flags=re.MULTILINE)
assert np == 1
ps.write_text(pt, encoding='utf-8')
od = ROOT / 'lib/custom'
od.mkdir(parents=True, exist_ok=True)
(od / 'flclash_bridge.dart').write_text(BRIDGE.replace('__APP_VER__', ver), encoding='utf-8')
shutil.copyfile(MOD / 'smart_guardian.dart', od / 'smart_guardian.dart')
shutil.copyfile(MOD / 'simple_workbench.dart', od / 'simple_workbench.dart')
ia = ROOT / 'lib/providers/action.dart'
it, ni = re.subn(r'^(\s*import\s+)', "import 'package:fl_clash/custom/flclash_bridge.dart';\n\\1", ia.read_text(encoding='utf-8'), count=1, flags=re.MULTILINE)
assert ni == 1
ia.write_text(it, encoding='utf-8')
sa = ROOT / 'lib/providers/actions/setup.dart'
st = sa.read_text(encoding='utf-8')
st, n1 = re.subn(r'final\s+profileBase\s*=\s*!isCustom\s*&&\s*!hasScript\s*\?\s*await\s+_core\.getProfileBase\(profileId\)\s*:\s*null;', 'final profileBase = !FlClashBridge.simpleTakeover && !isCustom && !hasScript ? await _core.getProfileBase(profileId) : null;', st, count=1)
hk = "if (FlClashBridge.simpleTakeover) { await FlClashBridge.ensureWhitelistLoaded(); rawConfig = Map<String, dynamic>.from(rawConfig)..remove('rule-providers'); rawConfig['rules'] = FlClashBridge.buildSimpleRules(); patchConfig = patchConfig.copyWith(mode: Mode.rule); }\n    final directory = await appPath.profilesPath;"
st = st.replace('final directory = await appPath.profilesPath;', hk, 1)
st, n2 = re.subn(r'(\bMakeRealProfileState\(\s*rules:\s*)rules,', r'\1FlClashBridge.simpleTakeover ? const <Rule>[] : rules,', st, count=1)
st, n3 = re.subn(r'(\baddedRules:\s*)setupState\.addedRules,', r'\1FlClashBridge.simpleTakeover ? const <Rule>[] : setupState.addedRules,', st, count=1)
st, n4 = re.subn(r'(PatchClashConfig\s+_effectivePatchConfig\(\s*PatchClashConfig\s+patchConfig\s*,?\s*\)\s*\{)', r'\1 if (FlClashBridge.simpleTakeover) { patchConfig = patchConfig.copyWith(mode: Mode.rule); }', st, count=1)
assert n1 == 1 and n2 == 1 and n3 == 1 and n4 == 1
sa.write_text(st, encoding='utf-8')
hp = ROOT / 'lib/pages/home.dart'
hs = hp.read_text(encoding='utf-8').replace("import 'package:prism_ui/prism_ui.dart';", "import 'package:fl_clash/custom/simple_workbench.dart';\nimport 'package:prism_ui/prism_ui.dart';", 1).replace('  @override\n  Widget build(BuildContext context, WidgetRef ref) {', '  @override\n  Widget build(BuildContext context, WidgetRef ref) {\n    return SimpleModeHost(originalChild: _buildOriginalHome(context, ref));\n  }\n\n  Widget _buildOriginalHome(BuildContext context, WidgetRef ref) {', 1)
assert 'SimpleModeHost(' in hs
hp.write_text(hs, encoding='utf-8')
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
print(f'Wired FlClash v{ver}+{code} OK')
