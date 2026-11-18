import base64, hashlib, os, pathlib, random, re, shutil, subprocess, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parent.parent
MOD = pathlib.Path(__file__).resolve().parent
BRIDGE = r"""// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, dead_null_aware_expression, invalid_null_aware_operator, unused_import, unnecessary_import, unawaited_futures, curly_braces_in_flow_control_structures
import'dart:async';import'dart:convert';import'dart:io';import'package:fl_clash/common/common.dart';import'package:fl_clash/core/core.dart';import'package:fl_clash/database/database.dart';import'package:fl_clash/enum/enum.dart';
import'package:fl_clash/models/models.dart';import'package:fl_clash/providers/providers.dart';import'package:flutter/widgets.dart';import'package:flutter_riverpod/flutter_riverpod.dart';
typedef BridgeProfile=({String label,bool selected,VoidCallback onSelect});typedef BridgeGroup=({String name,bool isSelector,String now,List<String>all});
typedef BridgeConn=({String id,int up,int down,String proc,String procPath,int?uid,String host,String ip,String port,String target,String net,List<String>chains});typedef BridgeLog=({String level,String payload,String time});
typedef DirectEntry=({String id,String label,String exe,String dir,String pkg});typedef InstalledApp=({String pkg,String label,bool system});typedef SublaneSpec=({String id,String name,List<String>domains,String exit});
typedef VendorSpec=({String id,String badge,int colVal,String name,bool enabled,String defEx,List<String>procs,List<String>pathRx,List<String>cidrs,List<String>hIps,List<SublaneSpec>subs});class FlClashBridge{
static const String appVersion='__APP_VER__';static const String defGroup='🎯 极简-默认';static String regGroup(String rc)=>'🎯 极简-$rc';static const List<String>mRegs=['HK','TW','SG','JP','KR','US','GB','DE','FR','NL','CA','AU'];
static const List<String>iKws=['剩余流量','距离下次','到期','有效期','官网','群组','公告','重置','订阅','客服','网址','traffic:','expire:'];static final String probeUrl=['ht','tps://www.gs','tatic.com/generate_204'].join();
static final List<(String,String,List<String>)>rDefs='HK|🇭🇰 香港|hong kong,hongkong,香港,港,hkg,hk;TW|🇹🇼 台湾|taiwan,taipei,台湾,台北,新北,彰化,高雄,tpe,tw;SG|🇸🇬 新加坡|singapore,新加坡,狮城,sin,sgp,sg;JP|🇯🇵 日本|japan,tokyo,osaka,日本,东京,大阪,名古屋,沪日,nrt,kix,tyo,jp;KR|🇰🇷 韩国|korea,seoul,韩国,首尔,春川,釜山,icn,sel,kr;US|🇺🇸 美国|america,los angeles,san jose,seattle,silicon,dallas,new york,美国,洛杉矶,圣何塞,西雅图,硅谷,芝加哥,纽约,lax,sjc,sea,ord,ewr,us;GB|🇬🇧 英国|britain,london,英国,伦敦,lhr,uk,gb;DE|🇩🇪 德国|germany,frankfurt,德国,法兰克福,慕尼黑,fra,de;FR|🇫🇷 法国|france,paris,法国,巴黎,cdg,fr;NL|🇳🇱 荷兰|netherlands,amsterdam,荷兰,阿姆斯特丹,ams,nl;CA|🇨🇦 加拿大|canada,toronto,vancouver,加拿大,温哥华,多伦多,yyz,yvr,ca;AU|🇦🇺 澳洲|australia,sydney,澳大利亚,澳洲,悉尼,墨尔本,syd,au;RU|🇷🇺 俄罗斯|russia,moscow,俄罗斯,莫斯科,伯力,svo,ru;IN|🇮🇳 印度|india,mumbai,印度,孟买,bom,ind;MY|🇲🇾 马来西亚|malaysia,kuala,马来西亚,大马,吉隆坡,kul,mys;TH|🇹🇭 泰国|thailand,bangkok,泰国,曼谷,bkk,th;VN|🇻🇳 越南|vietnam,越南,河内,胡志明,sgn,vn;PH|🇵🇭 菲律宾|philippines,菲律宾,马尼拉,mnl,ph;ID|🇮🇩 印尼|indonesia,jakarta,印尼,雅加达,cgk,idn;TR|🇹🇷 土耳其|turkey,istanbul,土耳其,ist,tr;BR|🇧🇷 巴西|brazil,巴西,圣保罗,gru,br;AR|🇦🇷 阿根廷|argentina,阿根廷,eze,ar;AE|🇦🇪 阿联酋|dubai,emirates,阿联酋,迪拜,dxb,ae;CH|🇨🇭 瑞士|switzerland,zurich,瑞士,苏黎世,zrh,ch'.split(';').map((s){final p=s.split('|');return(p[0],p[1],[p[1].split(' ').first,...p[2].split(',')]);}).toList();
static const String _vSpecRaw=r'google|G|FF2563EB|Google 生态|1|US|Antigravity.exe,antigravity|(?i).*[/\\]antigravity[/\\].*|142.250.0.0/15,172.217.0.0/16|ag:Antigravity IDE & CLI:US:antigravity.google,rep.googleapis.com;gemini:Gemini & AI Studio:US:gemini.google.com,aistudio.google.com,generativelanguage.googleapis.com,ai.google.dev,notebooklm.google.com,deepmind.google,makersuite.google.com;yt:YouTube 流媒体:HK:youtube.com,youtu.be,googlevideo.com,ytimg.com,ggpht.com;gcore:Google 搜索与云盘:JP:google.com,googleapis.com,gstatic.com,googleusercontent.com,gmail.com,1e100.net~openai|OA|FF059669|OpenAI 生态|1|US|codex,codex.exe,ChatGPT.exe|(?i).*([/\\]|@)openai[/\\]codex.*||codex:Codex CLI & API:US:api.openai.com,developers.openai.com,learn.chatgpt.com,platform.openai.com;chatgpt:ChatGPT 网页与桌面:US:chatgpt.com,openai.com,oaistatic.com,oaiusercontent.com,oaipro.com;sora:Sora 视频生成:US:sora.com~anthropic|C|FFD97706|Anthropic 生态|1|US|claude,claude.exe,Claude.exe|(?i).*(claude-code|@anthropic-ai).*|160.79.104.0/23|ccode:Claude Code 终端与 API:US:api.anthropic.com,platform.claude.com,downloads.claude.ai,statsig.anthropic.com;cweb:Claude Web & 验证链:US:claude.ai,claude.com,anthropic.com,hcaptcha.com~xai|X|FF334155|xAI & X 生态|1|US|grok,grok.exe,grok-cli||104.244.42.0/24|grok:Grok 网页 / API / CLI:US:grok.com,x.ai,api.x.ai,auth.x.ai,cli-chat-proxy.grok.com;xmedia:X (Twitter) 媒体流:JP:x.com,twitter.com,twimg.com,t.co~aiide|ID|FF7C3AED|AI 编程 IDE|1|US|Cursor.exe,cursor,Windsurf.exe,windsurf|(?i).*[/\\]\.(cursor|windsurf|codeium)[/\\].*||cursor:Cursor 编辑器推理:US:cursor.com,cursor.sh,cursorapi.com,cursor-cdn.com;windsurf:Windsurf & Codeium:US:windsurf.com,codeium.com,codeiumdata.com,supermaven.com~msgh|GH|FF1E293B|Microsoft & GitHub|1|HK|gh.exe,GitHubDesktop.exe||140.82.112.0/20|github:GitHub & Copilot:HK:github.com,githubusercontent.com,githubassets.com,githubcopilot.com,ghcr.io;office:Office 365 & OneDrive:DIRECT:office.com,office365.com,live.com,sharepoint.com,onedrive.com~gateway|GW|FF0284C7|AI 搜索与模型网关|0|US||||pplx:Perplexity 搜索:US:perplexity.ai,pplx.ai;hub:OpenRouter & HuggingFace:US:openrouter.ai,huggingface.co,hf.co,replicate.com,together.ai,groq.com~collab|DV|FF4F46E5|开发协作与镜像源|0|SG|Telegram.exe,Discord.exe||91.108.4.0/22,91.108.56.0/22,149.154.160.0/20|pkg:Docker / NPM / PyPI / Vercel:SG:docker.io,docker.com,registry.npmjs.org,pypi.org,vercel.app;im:Telegram / Discord / Notion / Linear:SG:telegram.org,t.me,discord.com,discordapp.com,notion.so,linear.app';
static List<VendorSpec>defVendors()=>[for(final ln in _vSpecRaw.split('~'))if(ln.isNotEmpty)(){final p=ln.split('|');return(id:p[0],badge:p[1],colVal:int.parse(p[2],radix:16),name:p[3],enabled:p[4]=='1',defEx:p[5],
procs:p[6].isEmpty?const<String>[]:p[6].split(','),pathRx:p[7].isEmpty?const<String>[]:p[7].split(';'),cidrs:p[8].isEmpty?const<String>[]:p[8].split(','),hIps:const<String>[],
subs:[for(final s in p[9].split(';'))(){final sp=s.split(':');return(id:sp[0],name:sp[1],exit:sp[2],domains:sp[3].split(','));}()],);}(),];
static bool simpleTakeover=true,dTun=true,fbDir=false,autoFo=true,lkReg=true,autoHeal=true,ipOpen=false,_loaded=false;static int limitMs=1000;static String regCode='HK';static Map<String,String>stkNs=<String,String>{};
static Map<String,bool>drawers=<String,bool>{'vendors':true,'apps':true,'logs':false};static Set<String>expV=<String>{},expA=<String>{};static List<DirectEntry>whitelist=const[];static List<VendorSpec>vendors=defVendors();static Mode?_savedMode;
static(String,String)detReg(String n,String srv){final s='${n.toLowerCase()} ${srv.toLowerCase()}';for(final(c,l,ts)in rDefs){for(final t in ts){
if(t.length<=3&&RegExp(r'^[a-z]+$').hasMatch(t)?RegExp('(^|[^a-z])${RegExp.escape(t)}[0-9]*(?=[^a-z0-9]|\$)').hasMatch(s):s.contains(t))return(c,l);}}return('OTHER','🌐 其他区域');}static String regLblOf(String rc){
for(final(c,l,_)in rDefs)if(c==rc)return l;return rc=='DIRECT'?'🛡 物理直连':(rc=='FOLLOW'?'🌐 跟随兜底':'🌐 $rc');}static bool isInfoNode(String n)=>iKws.any(n.toLowerCase().contains);static bool isRunning(Ref ref)=>ref.read(isStartProvider);
static bool watchRunning(WidgetRef ref)=>ref.watch(isStartProvider);static Future<void>setRunning(Ref ref,bool enable)async{if(enable&&simpleTakeover)_atp(ref,true);await ref.read(setupActionProvider.notifier).setRunning(enable);}
static Future<File>_stateFile()async=>File('${await appPath.homeDirPath}/custom_minimal_v2.json');static Future<File>_legacyWlFile()async=>File('${await appPath.homeDirPath}/custom_direct_whitelist.json');static Future<void>loadSt()async{
if(_loaded)return;_loaded=true;try{final f=await _stateFile();if(f.existsSync()){final m=jsonDecode(await f.readAsString());if(m is Map){fbDir=m['fbDir']==true;dTun=m['dTun']!=false;autoFo=m['autoFo']!=false;lkReg=m['lkReg']!=false;
autoHeal=m['autoHeal']!=false;ipOpen=m['ipOpen']==true;limitMs=(m['limitMs']is int)?(m['limitMs']as int).clamp(400,5000):1000;final rc='${m['regCode'] ?? ''}'.trim();if(rc.isNotEmpty)regCode=rc;
if(m['stkNs']is Map)stkNs={for(final e in(m['stkNs']as Map).entries)if('${e.key}'.isNotEmpty&&'${e.value}'.isNotEmpty)'${e.key}':'${e.value}'};if(m['drawers']is Map)for(final e in(m['drawers']as Map).entries)drawers['${e.key}']=e.value==true;
if(m['expV']is List)expV={for(final x in m['expV']as List)'$x'};if(m['expA']is List)expA={for(final x in m['expA']as List)'$x'};
if(m['whitelist']is List)whitelist=[for(final e in m['whitelist']as List)if(e is Map)(id:'${e['id'] ?? ''}',label:'${e['label'] ?? ''}',exe:'${e['exe'] ?? ''}',dir:'${e['dir'] ?? ''}',pkg:'${e['pkg'] ?? ''}')];if(m['vendors']is Map){
final vm=m['vendors']as Map;vendors=[for(final dv in defVendors())(){final ov=vm[dv.id];if(ov is!Map)return dv;final subExit=ov['subExit']is Map?ov['subExit']as Map:const{};final cSubs=<SublaneSpec>[if(ov['customSubs']is List)
for(final cs in ov['customSubs']as List)if(cs is Map&&'${cs['domains'] ?? ''}'.isNotEmpty)
(id:'${cs['id'] ?? ''}',name:'${cs['name'] ?? ''}',domains:[for(final d in'${cs['domains']}'.split(','))if(d.trim().isNotEmpty)d.trim()],exit:'${cs['exit'] ?? dv.defEx}'),];
final hIps=<String>[if(ov['hIps']is List)for(final ip in ov['hIps']as List)if('$ip'.trim().isNotEmpty)'$ip'.trim()];return(id:dv.id,badge:dv.badge,colVal:dv.colVal,name:dv.name,enabled:ov['enabled']is bool?ov['enabled']as bool:dv.enabled,
defEx:'${ov['defEx'] ?? dv.defEx}',procs:dv.procs,pathRx:dv.pathRx,cidrs:dv.cidrs,hIps:hIps,subs:[...cSubs,for(final sl in dv.subs)(id:sl.id,name:sl.name,domains:sl.domains,exit:'${subExit[sl.id] ?? sl.exit}')],);}(),];}return;}}
final lf=await _legacyWlFile();if(lf.existsSync()){final raw=jsonDecode(await lf.readAsString());
if(raw is List)whitelist=[for(final e in raw)if(e is Map)(id:'${e['id'] ?? ''}',label:'${e['label'] ?? ''}',exe:'${e['exe'] ?? ''}',dir:'${e['dir'] ?? ''}',pkg:'${e['pkg'] ?? ''}')];}}catch(_){}}static Future<void>savePrefs()async{try{
final defIds={for(final dv in defVendors())dv.id:{for(final sl in dv.subs)sl.id}};final vJson=<String,dynamic>{for(final v in vendors)v.id:{'enabled':v.enabled,'defEx':v.defEx,'hIps':v.hIps.take(64).toList(),
'subExit':{for(final sl in v.subs)if((defIds[v.id]??const<String>{}).contains(sl.id))sl.id:sl.exit},
'customSubs':[for(final sl in v.subs)if(!(defIds[v.id]??const<String>{}).contains(sl.id)){'id':sl.id,'name':sl.name,'domains':sl.domains.join(','),'exit':sl.exit}],},};final f=await _stateFile();await f.parent.create(recursive:true);
await f.writeAsString(jsonEncode({'fbDir':fbDir,'dTun':dTun,'autoFo':autoFo,'lkReg':lkReg,'autoHeal':autoHeal,'ipOpen':ipOpen,'limitMs':limitMs,'regCode':regCode,'stkNs':stkNs,'drawers':drawers,'expV':expV.toList(),'expA':expA.toList(),
'whitelist':[for(final e in whitelist){'id':e.id,'label':e.label,'exe':e.exe,'dir':e.dir,'pkg':e.pkg}],'vendors':vJson,}));}catch(_){}}static String safeDir(String pp){final c=pp.trim().replaceAll('/','\\');
if(c.isEmpty||!c.contains('\\'))return'';var ds=c.split('\\').where((s)=>s.isNotEmpty).toList();if(ds.length<3)return'';ds=ds.sublist(0,ds.length-1);
while(ds.length>=3&&RegExp(r'^([vV]?\d+[.\d_-]*|bin|x64|x86|win64|client)$').hasMatch(ds.last))ds=ds.sublist(0,ds.length-1);if(ds.length<2)return'';final j=ds.join('\\'),lw=j.toLowerCase();
const bad={r'c:\windows',r'c:\windows\system32',r'c:\windows\syswow64',r'c:\program files',r'c:\program files (x86)',r'c:\programdata'};
if(bad.contains(lw)||RegExp(r'^[a-z]:\\users\\[^\\]+(\\(desktop|downloads|appdata|appdata\\local|appdata\\roaming))?$').hasMatch(lw))return'';return pp.trim().startsWith('/')?'/${ds.join('/')}':j;}
static String _exitTgt(String c)=>c=='DIRECT'?'DIRECT':(c=='FOLLOW'?(fbDir?'DIRECT':defGroup):(mRegs.contains(c)?regGroup(c):defGroup));static List<String>simpleRules(){final out=<String>[];final sn=<String>{};
void ad(String r){if(!r.contains(',,')&&sn.add(r))out.add(r);}for(final w in whitelist){if(w.pkg.isNotEmpty&&!w.pkg.contains(',')){ad('PROCESS-NAME,${w.pkg},DIRECT');ad('PROCESS-NAME-REGEX,^${RegExp.escape(w.pkg)}(:.*)?\$,DIRECT');}
if(w.exe.isNotEmpty&&!w.exe.contains(',')){ad('PROCESS-NAME,${w.exe},DIRECT');if(!Platform.isAndroid&&!w.exe.contains('.'))ad('PROCESS-NAME,${w.exe}.exe,DIRECT');final st=w.exe.replaceAll(RegExp(r'\.(exe|app|bin)$',caseSensitive:false),'');
if(st.length>=3&&RegExp(r'^[a-zA-Z0-9_.-]+$').hasMatch(st))ad('PROCESS-NAME-REGEX,(?i)^${RegExp.escape(st)}[^/\\\\]*\$,DIRECT');}if(w.dir.isNotEmpty&&!w.dir.contains(',')){
final ps=w.dir.split(RegExp(r'[/\\]+')).where((s)=>s.isNotEmpty).toList();if(ps.length>=2)ad('PROCESS-PATH-REGEX,(?i)^${w.dir.startsWith('/') ? r'/' : ''}${ps.map(RegExp.escape).join(r'[/\\]')}[/\\\\].+,DIRECT');}}
for(final lan in const['127.0.0.0/8','10.0.0.0/8','172.16.0.0/12','192.168.0.0/16','100.64.0.0/10','169.254.0.0/16'])ad('IP-CIDR,$lan,DIRECT,no-resolve');for(final v in vendors){if(!v.enabled)continue;
final vt=_exitTgt(v.defEx),lt=v.subs.isNotEmpty?_exitTgt(v.subs.first.exit):vt;for(final ip in v.hIps)if(ip.trim().isNotEmpty&&!ip.contains(','))ad('IP-CIDR,${ip.trim()}/32,$vt,no-resolve');for(final sl in v.subs){final st=_exitTgt(sl.exit);
for(final rd in sl.domains){final d=rd.trim().replaceAll(RegExp(r'^\*\.'),'');if(d.isNotEmpty&&!d.contains(','))ad(d.contains('.')?'DOMAIN-SUFFIX,$d,$st':'DOMAIN-KEYWORD,$d,$st');}}if(!Platform.isAndroid){
for(final p in v.procs)if(p.isNotEmpty&&!p.contains(','))ad('PROCESS-NAME,$p,$lt');for(final rx in v.pathRx)if(rx.isNotEmpty)ad('PROCESS-PATH-REGEX,$rx,$lt');}
for(final c in v.cidrs)if(c.isNotEmpty&&!c.contains(','))ad('IP-CIDR,$c,$vt,no-resolve');}ad(fbDir?'MATCH,DIRECT':'MATCH,$defGroup');return out;}static Map<String,dynamic>applyCfg(Map<String,dynamic>rawConfig){
final cfg=Map<String,dynamic>.from(rawConfig)..remove('rule-providers');cfg['sniffer']=<String,dynamic>{'enable':true,'override-destination':false,
'sniff':<String,dynamic>{'TLS':<String,dynamic>{'ports':<int>[443,8443]},'HTTP':<String,dynamic>{'ports':<int>[80,8080,8088],'override-destination':true},'QUIC':<String,dynamic>{'ports':<int>[443,8443]}},};
final inAll=<String>[],byR=<String,List<String>>{};if(cfg['proxies']is List){for(final p in cfg['proxies']as List){if(p is Map){final nm='${p['name'] ?? ''}'.trim(),sv='${p['server'] ?? ''}'.trim();if(nm.isEmpty)continue;inAll.add(nm);
if(!isInfoNode(nm))(byR[detReg(nm,sv).$1]??=<String>[]).add(nm);}}}final cln=inAll.where((n)=>!isInfoNode(n)).toList(),uIn=cln.isNotEmpty?cln:inAll;
final origG=<Map<String,dynamic>>[if(cfg['proxy-groups']is List)for(final g in cfg['proxy-groups']as List)if(g is Map&&!'${g['name'] ?? ''}'.startsWith('🎯 极简-'))Map<String,dynamic>.from(g)];String?fbOrig;for(final g in origG){
final gn='${g['name'] ?? ''}'.trim(),gt='${g['type'] ?? ''}'.toLowerCase();if(gn.isNotEmpty&&(gt=='select'||gt=='url-test'||gt=='fallback')){fbOrig=gn;break;}}
List<String>dd(Iterable<String>xs){final s=<String>{};return[for(final x in xs)if(x.isNotEmpty&&s.add(x))x];}final dStk=stkNs[regCode],pNs=byR[regCode]??const<String>[];final dL=uIn.isNotEmpty
?dd([if(fbDir)'DIRECT',if(dStk!=null&&uIn.contains(dStk))dStk,...pNs,...uIn,'DIRECT']):dd([if(fbDir)'DIRECT',if(fbOrig!=null)fbOrig,'DIRECT']);cfg['proxy-groups']=<Map<String,dynamic>>[
<String,dynamic>{'name':defGroup,'type':'select','proxies':dL},for(final rc in mRegs)(){final rNs=byR[rc]??const<String>[],st=stkNs[rc];
return<String,dynamic>{'name':regGroup(rc),'type':'select','proxies':rNs.isNotEmpty?dd([if(st!=null&&rNs.contains(st))st,...rNs,defGroup]):<String>[defGroup]};}(),...origG,];cfg['rules']=simpleRules();return cfg;}
static void _atp(Ref ref,bool simple){simpleTakeover=simple;if(simple){_savedMode??=ref.read(patchClashConfigProvider).mode;if(Platform.isAndroid){final pkgs=[for(final w in whitelist)if(w.pkg.isNotEmpty)w.pkg];
ref.read(vpnSettingProvider.notifier).update((s)=>s.copyWith(enable:true,allowBypass:true,accessControlProps:s.accessControlProps.copyWith(enable:pkgs.isNotEmpty,mode:AccessControlMode.rejectSelected,rejectList:pkgs)));
ref.read(patchClashConfigProvider.notifier).update((s)=>s.copyWith(mode:Mode.rule));}else{ref.read(networkSettingProvider.notifier).update((s)=>s.copyWith(systemProxy:true,bypassPrivateRoute:true));
ref.read(patchClashConfigProvider.notifier).update((s)=>s.copyWith(mode:Mode.rule).copyWith.tun(enable:dTun));}}else{if(_savedMode!=null)ref.read(patchClashConfigProvider.notifier).update((s)=>s.copyWith(mode:_savedMode!));
if(Platform.isAndroid)ref.read(vpnSettingProvider.notifier).update((s)=>s.copyWith(accessControlProps:s.accessControlProps.copyWith(enable:false)));}}static Future<void>syncMode(Ref ref,bool simple,{bool?tunEnable})async{
if(tunEnable!=null)dTun=tunEnable;_atp(ref,simple);await savePrefs();try{await ref.read(setupActionProvider.notifier).applyProfile(force:true,silence:true);if(isRunning(ref))await ref.read(setupActionProvider.notifier).updateConfig();}catch(_){}
}static Future<void>saveWl(Ref ref,List<DirectEntry>items)async{_loaded=true;whitelist=List<DirectEntry>.unmodifiable(items);if(simpleTakeover)await syncMode(ref,true);else await savePrefs();}
static bool matchDir(DirectEntry w,String proc,String path){final p=proc.trim().toLowerCase(),pt=path.trim().replaceAll('/','\\').toLowerCase();if(w.pkg.isNotEmpty&&(p==w.pkg.toLowerCase()||p.startsWith('${w.pkg.toLowerCase()}:')))return true;
if(w.exe.isNotEmpty){final ex=w.exe.toLowerCase(),st=ex.replaceAll(RegExp(r'\.(exe|app|bin)$'),'');if(p==ex||p=='$st.exe'||(st.length>=3&&p.startsWith(st)))return true;}
if(w.dir.isNotEmpty&&pt.isNotEmpty&&pt.startsWith('${w.dir.replaceAll('/', '\\').toLowerCase()}\\'))return true;return false;}static VendorSpec?matchV(String proc,String path,String host){
final p=proc.trim().toLowerCase(),pt=path.trim(),h=host.trim().toLowerCase();for(final v in vendors){if(!v.enabled)continue;
if(h.isNotEmpty)for(final sl in v.subs)for(final d in sl.domains){final c=d.toLowerCase();if(h==c||h.endsWith('.$c'))return v;}if(p.isNotEmpty)for(final vp in v.procs)if(p==vp.toLowerCase())return v;
if(pt.isNotEmpty)for(final rx in v.pathRx)if(RegExp(rx).hasMatch(pt))return v;}return null;}static Future<List<InstalledApp>>loadApps(Ref ref)async{if(!Platform.isAndroid)return const[];try{
if(ref.read(packagesProvider).isEmpty)await ref.read(systemActionProvider.notifier).getPackages();final l=<InstalledApp>[for(final p in ref.read(packagesProvider))
if(p.packageName.isNotEmpty&&p.packageName!='com.follow.clash')(pkg:p.packageName,label:p.label.isNotEmpty?p.label:p.packageName,system:p.system),]..sort((a,b)=>a.system!=b.system?(a.system?1:-1):a.label.compareTo(b.label));return l;
}catch(_){return const[];}}static List<BridgeProfile>watchProfiles(WidgetRef ref){try{final list=ref.watch(profilesProvider),ntf=ref.read(profilesProvider.notifier),curId=ref.watch(currentProfileIdProvider);return[for(final raw in list)(){
final p=ntf.labeled(raw),lbl=p.realLabel;return(label:lbl.isNotEmpty?lbl:'订阅 #${p.id}',selected:p.id==curId,onSelect:()=>ref.read(currentProfileIdProvider.notifier).value=p.id);}(),];}catch(_){return const[];}}
static List<BridgeGroup>readGroups(Ref ref){try{return[for(final g in ref.read(groupsProvider))(name:g.name,isSelector:g.type==GroupType.Selector,now:g.now??'',all:[for(final p in g.all)p.name])];}catch(_){return const[];}}
static Future<void>selRegNode(Ref ref,{required String rc,required String proxyName,String origGroup='',bool isGlobalFallback=false})async{if(rc.isNotEmpty&&proxyName.isNotEmpty&&proxyName!='DIRECT')stkNs[rc]=proxyName;
if(isGlobalFallback&&rc.isNotEmpty)regCode=rc;unawaited(savePrefs());final act=ref.read(proxiesActionProvider.notifier);if(mRegs.contains(rc)){try{await act.changeProxy(groupName:regGroup(rc),proxyName:proxyName);}catch(_){}}
if(isGlobalFallback){try{await act.changeProxy(groupName:defGroup,proxyName:fbDir?'DIRECT':proxyName);}catch(_){}try{await act.changeProxy(groupName:'GLOBAL',proxyName:proxyName);}catch(_){}
if(origGroup.isNotEmpty&&origGroup!='GLOBAL'&&!origGroup.startsWith('🎯 极简-')){try{await act.changeProxy(groupName:origGroup,proxyName:proxyName);}catch(_){}}}}static Future<String>queryServer(Ref ref,String name)async{
try{return'${(await ref.read(coreHandlerProvider).getProxyDefinition(name))?['server'] ?? ''}'.trim();}catch(_){return'';}}static Future<int>testDelayMs(Ref ref,String name,{int timeoutMs=1000})async{
try{return(await ref.read(coreHandlerProvider).testDelay(TestDelayParams(proxyName:name,testUrl:probeUrl,timeout:timeoutMs)).timeout(Duration(milliseconds:timeoutMs+150))).value??-1;}catch(_){return-1;}}
static Map<String,String>readPkgNames(Ref ref){try{return{for(final pkg in ref.read(packagesProvider))pkg.packageName:'${pkg.label} (${pkg.packageName})'};}catch(_){return const{};}}static Future<List<BridgeConn>>fetchConns(Ref ref)async{try{
return[for(final c in await ref.read(coreHandlerProvider).getConnections())(){final h=c.metadata.host.trim(),dip=c.metadata.destinationIP.trim(),dp='${c.metadata.destinationPort}'.trim();
final tgt=(h.isNotEmpty?h:dip).isNotEmpty?'${h.isNotEmpty ? h : dip}:$dp':'';
return(id:c.id,up:c.upload,down:c.download,proc:c.metadata.process,procPath:c.metadata.processPath,uid:c.metadata.uid,host:h,ip:dip,port:dp,target:tgt,net:c.metadata.network,chains:c.chains);}(),];}catch(_){return const[];}}
static Future<void>closeConn(Ref ref,String id)async{try{await ref.read(coreHandlerProvider).closeConnection(id);}catch(_){}}static List<BridgeLog>readLogs(Ref ref){try{final l=ref.read(logsProvider).list,s=l.length>30?l.length-30:0;
return[for(final i in l.sublist(s))(level:i.logLevel.name,payload:i.payload,time:'${i.dateTime}')];}catch(_){return const[];}}}"""
run_tags = lambda cmd: subprocess.run(cmd, text=True, capture_output=True, timeout=15).stdout.splitlines()
if '--calc-version' in sys.argv: tags = [ln.split('refs/tags/')[-1].strip() for c in (['git', 'ls-remote', '--tags', 'origin'], ['git', 'tag', '-l']) for ln in run_tags(c) if ln.strip()]; vals = [93] + [int(m[1]) * 100 + int(m[2]) * 10 + int(m[3]) for tg in tags if (m := re.match(r'^v(\d+)\.(\d)\.(\d)$', tg)) and int(m[1]) * 100 + int(m[2]) * 10 + int(m[3]) >= 94]; n = max(vals) + 1; v = f'{n // 100}.{(n // 10) % 10}.{n % 10}'; c = 2030000000 + n * 100 + (int(os.environ.get('GITHUB_RUN_NUMBER', '1')) % 100); open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8').write(f'ver={v}\ncode={c}\n'); print(f'Next version: v{v} (+{c})'); sys.exit(0)
ver = os.environ.get('APP_VER', '0.9.5').strip() or '0.9.5'
code = os.environ.get('APP_CODE', '2030009501').strip() or '2030009501'
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
it = ia.read_text(encoding='utf-8')
if 'flclash_bridge.dart' not in it:
 it, ni = re.subn(r'^(\s*import\s+)', "import 'package:fl_clash/custom/flclash_bridge.dart';\n\\1", it, count=1, flags=re.MULTILINE)
 assert ni == 1
 ia.write_text(it, encoding='utf-8')
sa = ROOT / 'lib/providers/actions/setup.dart'
st = sa.read_text(encoding='utf-8')
if 'FlClashBridge.simpleTakeover' not in st:
 st, n1 = re.subn(r'final\s+profileBase\s*=\s*!isCustom\s*&&\s*!hasScript\s*\?\s*await\s+_core\.getProfileBase\(profileId\)\s*:\s*null;', 'final profileBase = !FlClashBridge.simpleTakeover && !isCustom && !hasScript ? await _core.getProfileBase(profileId) : null;', st, count=1)
 hk = "if (FlClashBridge.simpleTakeover) { await FlClashBridge.loadSt(); rawConfig = FlClashBridge.applyCfg(rawConfig); patchConfig = patchConfig.copyWith(mode: Mode.rule); }\n    final directory = await appPath.profilesPath;"
 st = st.replace('final directory = await appPath.profilesPath;', hk, 1)
 st, n2 = re.subn(r'(\bMakeRealProfileState\(\s*rules:\s*)rules,', r'\1FlClashBridge.simpleTakeover ? const <Rule>[] : rules,', st, count=1)
 st, n3 = re.subn(r'(\baddedRules:\s*)setupState\.addedRules,', r'\1FlClashBridge.simpleTakeover ? const <Rule>[] : setupState.addedRules,', st, count=1)
 st, n4 = re.subn(r'(PatchClashConfig\s+_effectivePatchConfig\(\s*PatchClashConfig\s+patchConfig\s*,?\s*\)\s*\{)', r'\1 if (FlClashBridge.simpleTakeover) { patchConfig = patchConfig.copyWith(mode: Mode.rule); }', st, count=1)
 assert n1 == 1 and n2 == 1 and n3 == 1 and n4 == 1
 sa.write_text(st, encoding='utf-8')
hp = ROOT / 'lib/pages/home.dart'
hs = hp.read_text(encoding='utf-8')
if 'SimpleModeHost(' not in hs:
 hs = hs.replace("import 'package:prism_ui/prism_ui.dart';", "import 'package:fl_clash/custom/simple_workbench.dart';\nimport 'package:prism_ui/prism_ui.dart';", 1).replace('  @override\n  Widget build(BuildContext context, WidgetRef ref) {', '  @override\n  Widget build(BuildContext context, WidgetRef ref) {\n    return SimpleModeHost(originalChild: _buildOriginalHome(context, ref));\n  }\n\n  Widget _buildOriginalHome(BuildContext context, WidgetRef ref) {', 1)
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
