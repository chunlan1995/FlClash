// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import'dart:async';import'dart:io';import'package:flutter_riverpod/flutter_riverpod.dart';import'flclash_bridge.dart';enum MatchTier{sameIp('同IP线路'),s24('同/24网段'),s16('同/16网段'),region('同国家/区域'),global('全局低延迟');
const MatchTier(this.label);final String label;}enum LogCat{failover('无缝转接'),conn('进程连接'),warn('延迟预警'),core('系统核心');const LogCat(this.label);final String label;}
typedef EndpointMeta=({String ip,String?s24,String?s16,String rc,String rl,String raw});typedef RegionBucket=({String code,String label,List<String>nodes});
typedef RegionIpOpt=({String node,String ip,String raw,String?s24,int ms,bool sel,bool sticky});typedef ProcStat=({String name,int upR,int dnR,int up,int dn,int conns,String exit});
typedef LogItem=({int id,DateTime time,LogCat cat,String title,String detail,bool hot});typedef SwitchRec=({DateTime time,String from,String to,int ms,MatchTier tier,String det,int rst});typedef GuardianState=({bool auto,
bool lock,int lim,bool busy,String grp,String node,String reg,String regLbl,int ms,EndpointMeta?meta,List<RegionBucket>regs,List<RegionIpOpt>opts,int up,int dn,int tot,int upR,int dnR,List<ProcStat>procs,List<SwitchRec>sws,
List<LogItem>logs,});String fmtBytes(int b){if(b<=0)return'0 B';const u=['B','KB','MB','GB','TB'];var v=b.toDouble();var i=0;while(v>=1024&&i<4){v/=1024;i++;}
return'${v.toStringAsFixed(i == 0 ? 0 : (v >= 100 ? 1 : 2))} ${u[i]}';}String fmtRate(int bps)=>'${fmtBytes(bps)}/s';String fmtTime(DateTime d)=>
'${d.hour.toString().padLeft(2, '0')}:${d.minute.toString().padLeft(2, '0')}:${d.second.toString().padLeft(2, '0')}';final simpleModeProvider=NotifierProvider<SimpleModeNotifier,bool>(SimpleModeNotifier.new);
class SimpleModeNotifier extends Notifier<bool>{@override bool build()=>true;void setMode(bool v)=>state=v;}final guardianProvider=NotifierProvider<GuardianNotifier,GuardianState>(GuardianNotifier.new);
class GuardianNotifier extends Notifier<GuardianState>{Timer?_t1,_t2;DateTime?_la,_ls;bool _b1=false,_b2=false,_br=false,_auto=true,_lock=true,_busy=false;int _seq=1,_lim=1000,_ms=0,_up=0,_dn=0,_upR=0,_dnR=0;
String _lg='',_ll='',_grp='',_node='',_reg='';EndpointMeta?_meta;List<RegionBucket>_regs=const[];List<RegionIpOpt>_opts=const[];List<ProcStat>_procsL=const[];List<SwitchRec>_sws=const[];List<LogItem>_logs=const[];
final Map<String,EndpointMeta>_ec={},_sm={};final Map<String,DateTime>_er={},_cl={};final Map<String,int>_dc={};final Map<String,String>_sn={};final Map<String,(int,int)>_cu={};final Set<String>_si={};
final Map<String,ProcStat>_pr={};static const _ps={'DIRECT','REJECT','REJECT-DROP','PASS','COMPATIBLE'};static const _ik=['剩余流量','距离下次','到期','有效期','官网','群组','公告','重置','订阅','客服','网址','traffic:','expire:'];
static final _rg='HK|🇭🇰 香港|hong kong,hongkong,香港,港,hkg,hk;''TW|🇹🇼 台湾|taiwan,taipei,台湾,台北,新北,彰化,高雄,tpe,tw;''SG|🇸🇬 新加坡|singapore,新加坡,狮城,sin,sgp,sg;''JP|🇯🇵 日本|japan,tokyo,osaka,日本,东京,大阪,名古屋,沪日,nrt,kix,tyo,jp;'
'KR|🇰🇷 韩国|korea,seoul,韩国,首尔,春川,釜山,icn,sel,kr;''US|🇺🇸 美国|america,los angeles,san jose,seattle,silicon,dallas,new york,美国,洛杉矶,圣何塞,西雅图,硅谷,芝加哥,纽约,lax,sjc,sea,ord,ewr,us;''GB|🇬🇧 英国|britain,london,英国,伦敦,lhr,uk,gb;'
'DE|🇩🇪 德国|germany,frankfurt,德国,法兰克福,慕尼黑,fra,de;''FR|🇫🇷 法国|france,paris,法国,巴黎,cdg,fr;''NL|🇳🇱 荷兰|netherlands,amsterdam,荷兰,阿姆斯特丹,ams,nl;''CA|🇨🇦 加拿大|canada,toronto,vancouver,加拿大,温哥华,多伦多,yyz,yvr,ca;'
'AU|🇦🇺 澳洲|australia,sydney,澳大利亚,澳洲,悉尼,墨尔本,syd,au;''RU|🇷🇺 俄罗斯|russia,moscow,俄罗斯,莫斯科,伯力,svo,ru;''IN|🇮🇳 印度|india,mumbai,印度,孟买,bom,ind;''MY|🇲🇾 马来西亚|malaysia,kuala,马来西亚,大马,吉隆坡,kul,mys;''TH|🇹🇭 泰国|thailand,bangkok,泰国,曼谷,bkk,th;'
'VN|🇻🇳 越南|vietnam,越南,河内,胡志明,sgn,vn;''PH|🇵🇭 菲律宾|philippines,菲律宾,马尼拉,mnl,ph;''ID|🇮🇩 印尼|indonesia,jakarta,印尼,雅加达,cgk,idn;''TR|🇹🇷 土耳其|turkey,istanbul,土耳其,ist,tr;''BR|🇧🇷 巴西|brazil,巴西,圣保罗,gru,br;''AR|🇦🇷 阿根廷|argentina,阿根廷,eze,ar;'
'AE|🇦🇪 阿联酋|dubai,emirates,阿联酋,迪拜,dxb,ae;''CH|🇨🇭 瑞士|switzerland,zurich,瑞士,苏黎世,zrh,ch'.split(';').map((s){final p=s.split('|');return(p[0],p[1],[p[1].split(' ').first,...p[2].split(',')]);}).toList();GuardianState _snap()=>(
auto:_auto,lock:_lock,lim:_lim,busy:_busy,grp:_grp,node:_node,reg:_reg,regLbl:_regs.where((r)=>r.code==_reg).firstOrNull?.label??(_meta?.rl??''),ms:_ms,meta:_meta,regs:_regs,opts:_opts,up:_up,dn:_dn,tot:_up+_dn,upR:_upR,
dnR:_dnR,procs:_procsL,sws:_sws,logs:_logs,);void _emit()=>state=_snap();@override GuardianState build(){ref.onDispose((){_t1?.cancel();_t2?.cancel();});Future<void>.microtask((){
_t1=Timer.periodic(const Duration(seconds:1),(_)=>unawaited(_tf()));_t2=Timer.periodic(const Duration(seconds:4),(_)=>unawaited(_tp(false)));
_log(LogCat.core,'极简区域聚合与一致IP守护已启动','自动聚合国家/区域 · 区域粘性固定IP · 1000ms同IP/同网段无缝容灾',true);unawaited(_tf());});return _snap();}void setAuto(bool v){_auto=v;_log(LogCat.core,v?'已开启超时自动无缝转接':'已暂停超时自动无缝转接','阈值: ${_lim}ms');}
void setLock(bool v){_lock=v;_log(LogCat.core,v?'已开启所选国家/区域锁定':'已允许跨区域全局兜底',v?'容灾优先保持在所选区域内':'本区全灭时允许切往其他低延迟区');}void setLimit(int ms){_lim=ms;_log(LogCat.core,'超时阈值已设为 ${ms}ms','探测 >= ${ms}ms 或无响应触发同IP/同段转接');}
void resetTraffic(){_pr.clear();_up=_dn=_upR=_dnR=0;_procsL=const[];_log(LogCat.core,'已清零当次运行累计流量','进程上下行统计已重新开始');}void clearLogs(){_logs=const[];_emit();}Future<void>manualCheck()=>_tp(true);
void _log(LogCat cat,String title,String detail,[bool hot=false]){_logs=[(id:_seq++,time:DateTime.now(),cat:cat,title:title,detail:detail,hot:hot),..._logs.take(219)];_emit();}(String,String)_dr(String n,String srv){
final s='${n.toLowerCase()} ${srv.toLowerCase()}';for(final(c,l,ts)in _rg){for(final t in ts){if(t.length<=3&&RegExp(r'^[a-z]+$').hasMatch(t)){
if(RegExp('(^|[^a-z])${RegExp.escape(t)}[0-9]*(?=[^a-z0-9]|\$)').hasMatch(s))return(c,l);}else if(s.contains(t))return(c,l);}}return('OTHER','🌐 其他区域');}EndpointMeta _pm(String n){final c=_ec[n];if(c!=null)return c;
final(rc,rl)=_dr(n,'');return(ip:'',s24:null,s16:null,rc:rc,rl:rl,raw:'');}Future<EndpointMeta>_rm(String n,[bool force=false])async{final pv=_ec[n];final now=DateTime.now();if(!force&&pv!=null&&pv.ip.isNotEmpty)return pv;
if(!force&&_er[n]!=null&&now.isBefore(_er[n]!))return pv??_pm(n);final srv=await FlClashBridge.queryServer(ref,n);final(rc,rl)=_dr(n,srv);if(srv.isEmpty){_er[n]=now.add(const Duration(seconds:4));
return _ec[n]=(ip:'',s24:null,s16:null,rc:rc,rl:rl,raw:'');}var a=InternetAddress.tryParse(srv);if(a==null){try{final r=await InternetAddress.lookup(srv).timeout(const Duration(milliseconds:1200));
if(r.isNotEmpty)a=r.firstWhere((x)=>x.type==InternetAddressType.IPv4,orElse:()=>r.first);}catch(_){}}String?s24,s16;if(a!=null&&a.type==InternetAddressType.IPv4&&a.rawAddress.length==4){final b=a.rawAddress;
s24='${b[0]}.${b[1]}.${b[2]}.0/24';s16='${b[0]}.${b[1]}.0.0/16';}else if(a!=null&&a.type==InternetAddressType.IPv6&&a.rawAddress.length==16){final b=a.rawAddress;
String h(int i)=>((b[i]<<8)|b[i+1]).toRadixString(16).padLeft(4,'0');s24='${h(0)}:${h(2)}:${h(4)}:${h(6)}::/64';s16='${h(0)}:${h(2)}:${h(4)}::/48';}if(a==null)_er[n]=now.add(const Duration(seconds:8));
return _ec[n]=(ip:a?.address??'',s24:s24,s16:s16,rc:rc,rl:rl,raw:srv);}Future<Map<String,EndpointMeta>>_resB(List<String>ns,[bool force=false])async{final out=<String,EndpointMeta>{};for(var i=0;i<ns.length;i+=8){
final ch=ns.skip(i).take(8).toList();final rs=await Future.wait(ch.map((n)=>_rm(n,force)));for(var j=0;j<ch.length;j++)out[ch[j]]=rs[j];}return out;}(MatchTier,String)_tier(EndpointMeta?r,EndpointMeta m,String tr){
if(r!=null&&r.ip.isNotEmpty&&m.ip==r.ip)return(MatchTier.sameIp,m.ip);if(r!=null&&r.s24!=null&&m.s24==r.s24)return(MatchTier.s24,m.s24!);if(r!=null&&r.s16!=null&&m.s16==r.s16)return(MatchTier.s16,m.s16!);
if(m.rc==tr)return(MatchTier.region,m.ip.isNotEmpty?'${m.rl} ${m.ip}':m.rl);return(MatchTier.global,m.rl);}(BridgeGroup?,String)_lf(List<BridgeGroup>gs){if(gs.isEmpty)return(null,'');final m={for(final g in gs)g.name:g};
var sel=gs.firstWhere((g)=>g.isSelector&&g.all.isNotEmpty,orElse:()=>gs.first);var leaf=sel.now;for(var i=0;i<6&&m.containsKey(leaf);i++){final sub=m[leaf]!;if(sub.isSelector&&sub.all.isNotEmpty)sel=sub;
if(sub.now.isEmpty||sub.now==leaf)break;leaf=sub.now;}return(sel,leaf);}List<String>_rn(BridgeGroup sel,Set<String>gSet){final b=sel.all.where((n)=>!_ps.contains(n.toUpperCase())&&!gSet.contains(n)).toList();
final f=b.where((n)=>!_ik.any(n.toLowerCase().contains)).toList();return f.isNotEmpty?f:b;}void _rb(BridgeGroup sel,String leaf,Set<String>gSet){final ns=_rn(sel,gSet);final by=<String,List<String>>{};
final lb=<String,String>{};for(final n in ns){final m=_pm(n);(by[m.rc]??=[]).add(n);lb[m.rc]=m.rl;}final ord={for(var i=0;i<_rg.length;i++)_rg[i].$1:i};
final cs=by.keys.toList()..sort((a,b)=>a=='OTHER'?1:(b=='OTHER'?-1:(ord[a]??99).compareTo(ord[b]??99)));_regs=[for(final c in cs)(code:c,label:lb[c]??c,nodes:by[c]!)];final lm=leaf.isNotEmpty?_pm(leaf):null;
if(leaf.isNotEmpty&&leaf!=_ll){_ll=leaf;if(lm!=null&&by.containsKey(lm.rc))_sn[_reg=lm.rc]=leaf;}if(_reg.isEmpty||!by.containsKey(_reg))_reg=(lm!=null&&by.containsKey(lm.rc))?lm.rc:(_regs.isNotEmpty?_regs.first.code:'');
final cns=by[_reg]??const<String>[];final stk=_sn[_reg];_grp=sel.name;_node=leaf;_meta=lm;_opts=[for(final n in cns)(){final m=_pm(n);
return(node:n,ip:m.ip,raw:m.raw,s24:m.s24,ms:_dc[n]??(n==leaf?_ms:0),sel:n==leaf,sticky:n==stk);}(),];_emit();unawaited(_bg(cns,ns));}Future<void>_bg(List<String>prioNs,List<String>allNs)async{if(_br)return;_br=true;try{
final now=DateTime.now();bool need(String n)=>(_ec[n]?.ip.isEmpty??true)&&(_er[n]==null||!now.isBefore(_er[n]!));final p=prioNs.where(need).take(16).toList();
final q=[...p,...allNs.where((n)=>!p.contains(n)&&need(n)).take(10)];if(q.isEmpty)return;await _resB(q);final gs=FlClashBridge.readGroups(ref);final(sel,leaf)=_lf(gs);if(sel!=null)_rb(sel,leaf,{for(final g in gs)g.name});
}catch(_){}finally{_br=false;}}Future<int>_mig(String grp,String oldL,String newL)async{await FlClashBridge.selectNode(ref,groupName:grp,proxyName:newL);if(oldL.isEmpty||oldL==newL||!FlClashBridge.isRunning(ref))return 0;
var c=0;try{for(final x in await FlClashBridge.fetchConns(ref)){if(x.chains.contains(oldL)){await FlClashBridge.closeConn(ref,x.id);c++;}}}catch(_){}return c;}
Future<(String,int,EndpointMeta,MatchTier,String)?>_bestOf(List<String>pool,EndpointMeta?refM,String tr,bool lockReg)async{final batch=pool.take(22).toList();if(batch.isEmpty)return null;final metas=await _resB(batch);
batch.sort((a,b)=>_tier(refM,metas[a]!,tr).$1.index.compareTo(_tier(refM,metas[b]!,tr).$1.index));final prb=await Future.wait(batch.take(18).map((n)async=>(n,_dc[n]=await FlClashBridge.testDelayMs(ref,n,timeoutMs:_lim))));
final ok=<(String,int,EndpointMeta,MatchTier,String)>[];for(final(n,ms)in prb){if(ms<=0||ms>=_lim)continue;final m=metas[n]!;if(lockReg&&m.rc!=tr)continue;final(t,det)=_tier(refM,m,tr);ok.add((n,ms,m,t,det));}
if(ok.isEmpty)return null;ok.sort((a,b)=>a.$4.index!=b.$4.index?a.$4.index.compareTo(b.$4.index):a.$2.compareTo(b.$2));return ok.first;}Future<void>selectRegion(String rc)async{final gs=FlClashBridge.readGroups(ref);
final(sel,leaf)=_lf(gs);if(sel==null)return;final gSet={for(final g in gs)g.name};_rb(sel,leaf,gSet);final bk=_regs.where((b)=>b.code==rc).firstOrNull;if(bk==null||bk.nodes.isEmpty)return;_reg=rc;_busy=true;
_rb(sel,leaf,gSet);try{final run=FlClashBridge.isRunning(ref);final ps=_sn[rc];if(leaf.isNotEmpty&&bk.nodes.contains(leaf)){if(!run){_sn[rc]=leaf;_rb(sel,leaf,gSet);return;}
final d=_dc[leaf]=await FlClashBridge.testDelayMs(ref,leaf,timeoutMs:_lim);if(d>0&&d<_lim){_meta=_sm[rc]=await _rm(leaf);_sn[rc]=leaf;_ms=d;_rb(sel,leaf,gSet);
_log(LogCat.core,'保持当前 ${bk.label} 一致 IP','节点: $leaf · IP: ${_meta!.ip.isNotEmpty ? _meta!.ip : _meta!.raw} (${d}ms)');return;}}if(!run){final pick=(ps!=null&&bk.nodes.contains(ps))?ps:bk.nodes.first;_ll=_sn[rc]=pick;
await FlClashBridge.selectNode(ref,groupName:sel.name,proxyName:pick);_meta=_sm[rc]=await _rm(pick);_ms=0;_rb(sel,pick,gSet);
_log(LogCat.core,'已选定 ${bk.label}: $pick','IP: ${_meta!.ip.isNotEmpty ? _meta!.ip : (_meta!.raw.isNotEmpty ? _meta!.raw : "开启后解析")} · 已固定为本区首选');return;}if(ps!=null&&bk.nodes.contains(ps)){
final sd=_dc[ps]=await FlClashBridge.testDelayMs(ref,ps,timeoutMs:_lim);if(sd>0&&sd<_lim){_meta=_sm[rc]=await _rm(ps);_ll=ps;await _mig(sel.name,leaf,ps);_ms=sd;_rb(sel,ps,gSet);
_log(LogCat.core,'切回 ${bk.label} 固定一致 IP: ${_meta!.ip.isNotEmpty ? _meta!.ip : ps}','复用记忆节点 $ps (${sd}ms)，出口 IP 保持一致',true);return;}}final hit=await _bestOf(bk.nodes,_sm[rc],rc,false);
final ch=hit?.$1??((ps!=null&&bk.nodes.contains(ps))?ps:bk.nodes.first);_ms=hit?.$2??(_dc[ch]??-1);_meta=_sm[rc]=hit?.$3??await _rm(ch);_ll=_sn[rc]=ch;await _mig(sel.name,leaf,ch);_rb(sel,ch,gSet);
_log(LogCat.core,'已切换至 ${bk.label} · IP: ${_meta!.ip.isNotEmpty ? _meta!.ip : ch}','节点: $ch · 延迟: ${_ms > 0 ? "${_ms}ms" : "待重试"} · 后续持续固定该 IP',true);}finally{_busy=false;_emit();}}
Future<void>pickNode(String grp,String node)async{final prev=_node;_ll=node;final m=await _rm(node,true);_sn[m.rc]=node;_sm[m.rc]=m;await _mig(grp,prev,node);
final d=FlClashBridge.isRunning(ref)?await FlClashBridge.testDelayMs(ref,node,timeoutMs:_lim):0;if(d!=0)_dc[node]=d;_reg=m.rc;_ms=d;_meta=m;final gs=FlClashBridge.readGroups(ref);final(sel,_)=_lf(gs);
if(sel!=null)_rb(sel,node,{for(final g in gs)g.name});_log(LogCat.core,'手动固定 IP: ${m.ip.isNotEmpty ? m.ip : node}','区域: ${m.rl} · 节点: $node · 延迟: ${d > 0 ? "${d}ms" : (d < 0 ? "超时" : "待测")} · 已设为本区粘性首选',true);}
Future<void>probeCurrentRegion()async{if(_busy||_opts.isEmpty)return;_busy=true;_emit();try{final ns=[for(final o in _opts)o.node];await _resB(ns,true);if(FlClashBridge.isRunning(ref)){for(var i=0;i<ns.length;i+=8){
await Future.wait(ns.skip(i).take(8).map((n)async=>_dc[n]=await FlClashBridge.testDelayMs(ref,n,timeoutMs:_lim)));}}final gs=FlClashBridge.readGroups(ref);final(sel,leaf)=_lf(gs);if(sel!=null){
if(_dc[leaf]!=null)_ms=_dc[leaf]!;_rb(sel,leaf,{for(final g in gs)g.name});}_log(LogCat.core,'已完成 ${state.regLbl} 全部 IP 解析与测速','共检测 ${ns.length} 个候选 IP，当前选中 IP 保持不变');}finally{_busy=false;_emit();}}Future<void>_tf()async{
if(_b1)return;_b1=true;try{final cLogs=FlClashBridge.readLogs(ref);if(cLogs.isNotEmpty){final last=cLogs.last;final sig='${last.time}|${last.payload}';if(sig!=_lg){_lg=sig;final low=last.payload.toLowerCase();
if(low.contains('i/o timeout')||low.contains('deadline exceeded')||(low.contains('dial')&&low.contains('timeout'))){_log(LogCat.warn,'捕获底层连接超时',last.payload,true);
if(_auto&&FlClashBridge.isRunning(ref))unawaited(_tp(false,true));}}}final gs=FlClashBridge.readGroups(ref);final(sel,leaf)=_lf(gs);if(sel!=null){if(leaf.isNotEmpty&&(_ec[leaf]?.ip.isEmpty??true))await _rm(leaf);
_rb(sel,leaf,{for(final g in gs)g.name});}if(!FlClashBridge.isRunning(ref)){_cu.clear();_la=null;if(_upR!=0||_dnR!=0){_upR=_dnR=0;
_procsL=[for(final p in _pr.values)(name:p.name,upR:0,dnR:0,up:p.up,dn:p.dn,conns:0,exit:p.exit)];_emit();}return;}final now=DateTime.now();final dt=_la==null?1000:now.difference(_la!).inMilliseconds.clamp(250,5000);_la=now;
final conns=await FlClashBridge.fetchConns(ref);final pkg=FlClashBridge.readPkgNames(ref);final live=<String>{};final duM=<String,int>{},ddM=<String,int>{},cntM=<String,int>{};var gU=0,gD=0;for(final c in conns){
live.add(c.id);final pv=_cu[c.id];final du=pv==null?c.up:(c.up>=pv.$1?c.up-pv.$1:0);final dd=pv==null?c.down:(c.down>=pv.$2?c.down-pv.$2:0);_cu[c.id]=(c.up,c.down);final raw=c.proc.trim().replaceAll('\\','/');
final pn=raw.isNotEmpty?(pkg[raw]??raw.split('/').last):((c.uid!=null&&c.uid!>0)?(pkg['uid:${c.uid}']??'App (UID:${c.uid})'):'系统/未知进程');final ex=c.chains.isNotEmpty?c.chains.first:leaf;
if(!_si.contains(c.id)&&c.target.isNotEmpty){_si.add(c.id);if(_si.length>1200)_si.remove(_si.first);_log(LogCat.conn,'$pn → ${c.target}','${c.net.toUpperCase()} · 出口: ${ex.isEmpty ? "DIRECT" : ex}');}cntM[pn]=(cntM[pn]??0)+1;
duM[pn]=(duM[pn]??0)+du;ddM[pn]=(ddM[pn]??0)+dd;gU+=du;gD+=dd;final old=_pr[pn];_pr[pn]=(name:pn,upR:0,dnR:0,up:(old?.up??0)+du,dn:(old?.dn??0)+dd,conns:cntM[pn]!,exit:ex.isNotEmpty?ex:(old?.exit??''));}
_cu.removeWhere((k,_)=>!live.contains(k));final k=1000.0/dt;final list=<ProcStat>[];for(final e in _pr.entries){
final it=(name:e.key,upR:((duM[e.key]??0)*k).round(),dnR:((ddM[e.key]??0)*k).round(),up:e.value.up,dn:e.value.dn,conns:cntM[e.key]??0,exit:e.value.exit);_pr[e.key]=it;list.add(it);}
list.sort((a,b)=>(a.upR+a.dnR>0||b.upR+b.dnR>0)?(b.upR+b.dnR).compareTo(a.upR+a.dnR):(b.up+b.dn).compareTo(a.up+a.dn));_up+=gU;_dn+=gD;_upR=(gU*k).round();_dnR=(gD*k).round();_procsL=list;_emit();}catch(_){}finally{_b1=false;
}}Future<void>_tp(bool manual,[bool fromLog=false])async{if(_b2||(!manual&&(!FlClashBridge.isRunning(ref)||!_auto)))return;if(!manual&&_ls!=null&&DateTime.now().difference(_ls!).inSeconds<4)return;_b2=_busy=true;_emit();try{
final gs=FlClashBridge.readGroups(ref);final(sel,leaf)=_lf(gs);if(sel==null||leaf.isEmpty||_ps.contains(leaf.toUpperCase()))return;final gSet={for(final g in gs)g.name};final cur=await _rm(leaf);
var d=await FlClashBridge.testDelayMs(ref,leaf,timeoutMs:_lim);if(!manual&&d>=_lim){await Future<void>.delayed(const Duration(milliseconds:200));d=await FlClashBridge.testDelayMs(ref,leaf,timeoutMs:_lim);}_dc[leaf]=_ms=d;
_meta=cur;if(d>0&&d<_lim){_sn[cur.rc]=leaf;_sm[cur.rc]=cur;_rb(sel,leaf,gSet);if(manual)_log(LogCat.core,'当前 IP 稳定健康: ${cur.ip.isNotEmpty ? cur.ip : leaf} (${d}ms)','节点: $leaf · ${cur.rl} · 保持一致不切换');return;}
final why=d<=0?(fromLog?'拨号超时 & 无响应':'探测超时 (> ${_lim}ms)'):'延迟 ${d}ms >= ${_lim}ms';_cl[leaf]=DateTime.now().add(const Duration(seconds:30));final tr=_reg.isNotEmpty?_reg:cur.rc;
_log(LogCat.warn,'节点超时触发一致转接: $leaf','$why · 检索 ${cur.rl} 同IP/同网段(${cur.s24 ?? cur.ip})候选',true);final all=_rn(sel,gSet).where((n)=>n!=leaf).toList();if(all.isEmpty)return;final now=DateTime.now();
var srp=all.where((n)=>_pm(n).rc==tr&&(_cl[n]==null||!_cl[n]!.isAfter(now))).toList();if(srp.isEmpty)srp=all.where((n)=>_pm(n).rc==tr).toList();
final pool=_lock&&srp.isNotEmpty?srp:[...srp,...all.where((n)=>!srp.contains(n)&&(_cl[n]==null||!_cl[n]!.isAfter(now)))];final hit=await _bestOf(pool,cur,tr,_lock&&srp.isNotEmpty);if(hit==null){_rb(sel,leaf,gSet);
_log(LogCat.warn,'当前区域暂无 < ${_lim}ms 可用 IP','保持区域不乱跳，稍后自动重试本区节点',true);return;}final(best,bMs,bm,tier,det)=hit;_ll=_sn[bm.rc]=best;_meta=_sm[bm.rc]=bm;_ms=bMs;final rst=await _mig(sel.name,leaf,best);_ls=DateTime.now();
_sws=[(time:_ls!,from:leaf,to:best,ms:bMs,tier:tier,det:det,rst:rst),..._sws.take(25)];_rb(sel,best,gSet);
_log(LogCat.failover,'一致无缝转接: $leaf → $best (${bMs}ms)','新IP: ${bm.ip.isNotEmpty ? bm.ip : best} · 匹配: ${tier.label} [$det] · 重置 $rst 条旧连接',true);}finally{_b2=_busy=false;_emit();}}}
