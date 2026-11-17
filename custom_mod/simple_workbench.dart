// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import'dart:async';import'dart:io';import'package:fl_clash/ui/icons/icons.dart';import'package:fl_clash/views/profiles/add.dart';import'package:fl_clash/widgets/widgets.dart';import'package:flutter/services.dart';
import'package:flutter/widgets.dart';import'package:flutter_riverpod/flutter_riverpod.dart';import'package:prism_ui/prism_ui.dart';import'flclash_bridge.dart';import'smart_guardian.dart';class SimpleModeHost extends ConsumerWidget{
const SimpleModeHost({super.key,required this.originalChild});final Widget originalChild;@override Widget build(BuildContext context,WidgetRef ref){ref.watch(guardianProvider.select((s)=>s.auto));final s=ref.watch(simpleModeProvider);
return Stack(children:[Offstage(offstage:s,child:originalChild),if(s)const Positioned.fill(child:SimpleWorkbenchView())
else Positioned(right:18,bottom:20,child:SafeArea(child:FilledButton(onPressed:()=>unawaited(ref.read(guardianProvider.notifier).setUi(true)),child:const Text('返回极简模式（全局接管）')))),]);}}
class SimpleWorkbenchView extends ConsumerStatefulWidget{const SimpleWorkbenchView({super.key});@override ConsumerState<SimpleWorkbenchView>createState()=>_SWS();}class _SWS extends ConsumerState<SimpleWorkbenchView>{
final _ic=TextEditingController(),_wc=TextEditingController(),_ac=TextEditingController(),_pc=TextEditingController(),_lc=TextEditingController();final _if=FocusNode(),_wf=FocusNode(),_af=FocusNode(),_pf=FocusNode(),_lf=FocusNode();
LogCat?_cat;int _mt=0,_rt=0;String _iq='',_wq='',_aq='',_pq='',_lq='';bool _busy=false;@override void dispose(){for(final c in[_ic,_wc,_ac,_pc,_lc])c.dispose();for(final f in[_if,_wf,_af,_pf,_lf])f.dispose();super.dispose();}
Future<void>_tog(bool r)async{if(_busy)return;setState(()=>_busy=true);try{await ref.read(guardianProvider.notifier).togRun(r);}finally{if(mounted)setState(()=>_busy=false);}}
Color _fg(BuildContext c)=>DefaultTextStyle.of(c).style.color??const Color(0xFF1F2937);Color _mu(BuildContext c)=>_fg(c).withValues(alpha:0.62);
ShapeDecoration _rb(Color c,double r)=>ShapeDecoration(color:c,shape:RoundedSuperellipseBorder(borderRadius:BorderRadius.circular(r)));Widget _tx(BuildContext c,String s,{bool b=false,bool cap=false,Color?col})=>Text(
s,maxLines:1,overflow:TextOverflow.ellipsis,style:(cap?AppTextStyle.caption1.of(c,emphasized:b):AppTextStyle.body.of(c,emphasized:b)).copyWith(color:col??(cap&&!b?_mu(c):_fg(c))),);Widget _cd(BuildContext c,List<Widget>ch)=>Container(
padding:const EdgeInsets.all(12),decoration:_rb(_fg(c).withValues(alpha:0.045),16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:8,children:ch),);
Widget _lv<T>(BuildContext c,List<T>l,String emp,Widget Function(T)fn)=>Expanded(child:l.isEmpty?Center(child:Text(emp,style:AppTextStyle.caption1.of(c).copyWith(color:_mu(c)),textAlign:TextAlign.center))
:ListView.separated(itemCount:l.length,separatorBuilder:(_,_)=>const SizedBox(height:6),itemBuilder:(_,i)=>fn(l[i])),);Widget _ch(BuildContext c,bool sel,String txt,VoidCallback tap){final cs=c.colorScheme;return GestureDetector(
onTap:tap,child:Container(padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),alignment:Alignment.center,decoration:_rb(sel?cs.successContainer:_fg(c).withValues(alpha:0.065),10),
child:Text(txt,style:AppTextStyle.subheadline.of(c,emphasized:sel).copyWith(color:sel?cs.onSuccessContainer:_fg(c))),),);}Widget _sb(BuildContext c,String lb,String v)=>Container(
padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),decoration:_rb(_fg(c).withValues(alpha:0.06),10),
child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[_tx(c,lb,cap:true),Text(v,style:AppTextStyle.subheadline.of(c,emphasized:true))]),);
Widget _sch(BuildContext c,TextEditingController tc,FocusNode fn,String h,String v,ValueChanged<String>chg){final fg=_fg(c);return GestureDetector(onTap:fn.requestFocus,child:Container(
padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),decoration:_rb(fg.withValues(alpha:0.065),10),child:Row(spacing:8,children:[Expanded(child:Stack(alignment:Alignment.centerLeft,children:[if(v.isEmpty)_tx(c,h,col:_mu(c)),
EditableText(controller:tc,focusNode:fn,autocorrect:false,onChanged:chg,style:AppTextStyle.subheadline.of(c).copyWith(color:fg),cursorColor:fg,backgroundCursorColor:_mu(c)),])),
if(v.isNotEmpty)GestureDetector(onTap:(){tc.clear();chg('');},child:Text('×',style:AppTextStyle.headline.of(c))),]),),);}@override Widget build(BuildContext context){
final cs=context.colorScheme,st=ref.watch(guardianProvider),ntf=ref.read(guardianProvider.notifier);final run=FlClashBridge.watchRunning(ref),profs=FlClashBridge.watchProfiles(ref);
final curP=profs.where((p)=>p.selected).firstOrNull,lsw=st.sws.firstOrNull,d=st.ms;final dS=!run?'未启动':(d<0?'超时(>${st.lim}ms)':(d==0?'待测速':'${d}ms'));
final cIp=(st.meta!=null&&st.meta!.ip.isNotEmpty)?st.meta!.ip:((st.meta!=null&&st.meta!.raw.isNotEmpty)?st.meta!.raw:(st.node.isEmpty?'未选择':'解析中...'));return Surface(color:SurfaceLevel.page.colorOf(cs),
child:SafeArea(child:LayoutBuilder(builder:(ctx,box){final w=box.maxWidth>=900;final rcs=[for(final r in st.regs)_ch(ctx,r.code==st.reg,'${r.label} (${r.nodes.length})',()=>unawaited(ntf.selReg(r.code)))];return Column(children:[
Padding(padding:const EdgeInsets.fromLTRB(16,8,16,4),child:Wrap(alignment:WrapAlignment.spaceBetween,crossAxisAlignment:WrapCrossAlignment.center,spacing:10,runSpacing:6,children:[
Text('FlClash · 极简智控版 v${FlClashBridge.appVersion}',style:AppTextStyle.headline.of(ctx,emphasized:true)),Wrap(spacing:6,runSpacing:6,crossAxisAlignment:WrapCrossAlignment.center,children:[if(profs.isNotEmpty)PopupAnchor(
targetBuilder:(o)=>TextButton(onPressed:o,child:Text('订阅: ${curP?.label ?? "选择"} ▾')),popupBuilder:(_)=>PopupMenu(items:[for(final p in profs)PopupMenuItem(glyph:p.selected?AppGlyphs.check:null,label:p.label,onPressed:p.onSelect)]),),
AddProfileMenu(builder:(o)=>TextButton(onPressed:o,child:const Text('+ 导入订阅'))),PopupAnchor(targetBuilder:(o)=>TextButton(onPressed:o,child:Text('阈值 ${st.lim}ms ▾')),
popupBuilder:(_)=>PopupMenu(items:[for(final ms in const[600,800,1000,1500])PopupMenuItem(glyph:st.lim==ms?AppGlyphs.check:null,label:ms==1000?'1000ms(默认)':'${ms}ms',onPressed:()=>ntf.setLimit(ms))]),),
TextButton(onPressed:()=>unawaited(ntf.setUi(false)),child:const Text('完整面板')),]),]),),Expanded(child:Padding(padding:const EdgeInsets.fromLTRB(16,4,16,12),child:Column(spacing:10,children:[_cd(ctx,[
  Wrap(alignment:WrapAlignment.spaceBetween,crossAxisAlignment:WrapCrossAlignment.center,spacing:12,runSpacing:8,children:[Row(mainAxisSize:MainAxisSize.min,spacing:12,children:[
FilledButton(onPressed:_busy?null:()=>_tog(run),child:Text(_busy?'切换中...':(run?'● 全局接管中（点击停止）':'▶ 一键开启全局接管'))),Flexible(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[_tx(ctx,'当前选中 IP: $cIp  ${st.regLbl}',b:true),
_tx(ctx,'线路: ${st.node.isEmpty ? "自动" : st.node} · 延迟: $dS · 网段: ${st.meta?.s24 ?? "同段保持"} · 已无视订阅规则',cap:true,col:(!run||(d>=0&&d<st.lim))?_mu(ctx):cs.onErrorContainer),])),]),Wrap(spacing:8,runSpacing:6,children:[
_sb(ctx,'实时上行','↑ ${fmtRate(st.upR)}'),_sb(ctx,'实时下行','↓ ${fmtRate(st.dnR)}'),_sb(ctx,'当次总流量','${fmtBytes(st.tot)} (↑${fmtBytes(st.up)}/↓${fmtBytes(st.dn)})'),]),]),
if(st.regs.isEmpty)_tx(ctx,'尚未检测到订阅节点，请点击右上角「+ 导入订阅」自动聚合国家与区域',cap:true)else if(w)Wrap(spacing:8,runSpacing:6,children:rcs)else SingleChildScrollView(scrollDirection:Axis.horizontal,child:Row(spacing:8,children:rcs)),
Wrap(spacing:8,runSpacing:6,crossAxisAlignment:WrapCrossAlignment.center,children:[_ch(ctx,true,'✓ 无视订阅规则·白名单直连 (${st.wl.length})',()=>setState((){_rt=0;_mt=1;})),
if(!Platform.isAndroid)_ch(ctx,st.tun,st.tun?'✓ TUN网卡全进程接管':'仅系统代理',()=>unawaited(ntf.setTun(!st.tun))),_ch(ctx,st.auto,st.auto?'✓ 超时同段转接(${st.lim}ms)':'超时转接已关',()=>ntf.setAuto(!st.auto)),
_ch(ctx,st.lock,st.lock?'✓ 锁定所选区域':'允许跨区兜底',()=>unawaited(ntf.setLock(!st.lock)),TextButton(onPressed:st.busy?null:()=>unawaited(ntf.chkNow()),child:Text(st.busy?'检测中...':'检测当前IP')),
if(lsw!=null)_tx(ctx,'最近转接: ${lsw.from} → ${lsw.to} (${lsw.tier.label}, ${lsw.ms}ms)',cap:true,b:true),]),]),if(!w)Row(spacing:6,children:[Expanded(child:_ch(ctx,_mt==0,'区域IP(${st.opts.length})',()=>setState(()=>_mt=0))),
Expanded(child:_ch(ctx,_mt==1,'直连(${st.wl.length})',()=>setState(()=>_mt=1))),Expanded(child:_ch(ctx,_mt==2,'进程(${st.procs.length})',()=>setState(()=>_mt=2))),
Expanded(child:_ch(ctx,_mt==3,'日志(${st.logs.length})',()=>setState(()=>_mt=3))),]),Expanded(child:w?Row(spacing:12,children:[Expanded(flex:5,child:_ipP(ctx,st)),Expanded(flex:6,child:_rP(ctx,st))])
:(_mt==0?_ipP(ctx,st):(_mt==1?_wP(ctx,st):(_mt==2?_pP(ctx,st):_lP(ctx,st))))),]),)),]);})),);}Widget _rP(BuildContext c,GuardianState st)=>Column(spacing:8,children:[Row(spacing:8,children:[
Expanded(child:_ch(c,_rt==0,'直连放通白名单 (${st.wl.length})',()=>setState(()=>_rt=0))),Expanded(child:_ch(c,_rt==1,'进程流量监控 (${st.procs.length})',()=>setState(()=>_rt=1))),
Expanded(child:_ch(c,_rt==2,'清晰日志 (${st.logs.length})',()=>setState(()=>_rt=2))),]),Expanded(child:_rt==0?_wP(c,st):(_rt==1?_pP(c,st):_lP(c,st))),]);Widget _wP(BuildContext c,GuardianState st){
final cs=c.colorScheme,ntf=ref.read(guardianProvider.notifier),q=_aq.trim().toLowerCase();return _cd(c,[_tx(c,'直连放通白名单 · 已放通应用的进程/子进程/线程流量直连不走代理',b:true),Row(spacing:8,children:[
Expanded(child:_sch(c,_wc,_wf,Platform.isAndroid?'输入包名(如 com.tencent.mm)...':'输入进程名(如 WeChat.exe)或应用目录...',_wq,(v)=>setState(()=>_wq=v))),
FilledButton(onPressed:_wq.trim().isEmpty?null:(){final v=_wq;_wc.clear();setState(()=>_wq='');unawaited(ntf.addDir(v));},child:const Text('+ 添加直连')),]),if(st.wl.isNotEmpty)ConstrainedBox(constraints:const BoxConstraints(maxHeight:84),
child:SingleChildScrollView(child:Wrap(spacing:6,runSpacing:6,children:[for(final w in st.wl)GestureDetector(onTap:()=>unawaited(ntf.rmDir(w.id)),
child:Container(padding:const EdgeInsets.symmetric(horizontal:9,vertical:4),decoration:_rb(cs.successContainer,8),child:_tx(c,'✓ ${w.label} ×',cap:true,b:true,col:cs.onSuccessContainer)),),])),),
if(!Platform.isAndroid)SingleChildScrollView(scrollDirection:Axis.horizontal,child:Row(spacing:6,children:[
for(final(l,ex)in GuardianNotifier.presets)_ch(c,ntf.isDir(ex,'',''),ntf.isDir(ex,'','')?'✓ $l':'+ $l',()=>unawaited(ntf.togDir(label:l,exe:ex))),])),Row(spacing:8,children:[
Expanded(child:_sch(c,_ac,_af,Platform.isAndroid?'搜索本机应用勾选直连放通...':'搜索活跃进程一键设为直连...',_aq,(v)=>setState(()=>_aq=v))),if(Platform.isAndroid)TextButton(onPressed:()=>unawaited(ntf.ldApps()),child:const Text('刷新应用')),]),
if(Platform.isAndroid)_lv(c,q.isEmpty?st.apps:st.apps.where((a)=>a.label.toLowerCase().contains(q)||a.pkg.toLowerCase().contains(q)).toList(),'点击「刷新应用」读取本机应用或在上方输入包名',(a){final on=ntf.isDir(a.pkg,'',a.pkg);return GestureDetector(
onTap:()=>unawaited(ntf.togDir(label:a.label,exe:a.pkg,pkg:a.pkg)),
child:Container(padding:const EdgeInsets.symmetric(horizontal:11,vertical:8),decoration:_rb(on?cs.successContainer.withValues(alpha:0.5):_fg(c).withValues(alpha:0.065),10),child:Row(children:[
Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[_tx(c,a.label,b:true),_tx(c,a.pkg,cap:true)])),_tx(c,on?'✓ 直连放通':'设为直连',cap:true,b:true,col:on?cs.onSuccessContainer:_fg(c)),])),);})else
_lv(c,st.procs.where((p)=>p.rawExe.isNotEmpty&&(q.isEmpty||p.name.toLowerCase().contains(q)||p.path.toLowerCase().contains(q))).toList(),'开启代理后产生流量的本地进程及目录会自动列出，也可点击上方常用软件或输入目录添加',(p)=>GestureDetector(
onTap:()=>unawaited(ntf.togDir(label:p.name,exe:p.rawExe,path:p.path,pkg:p.pkg)),
child:Container(padding:const EdgeInsets.symmetric(horizontal:11,vertical:8),decoration:_rb(p.direct?cs.successContainer.withValues(alpha:0.5):_fg(c).withValues(alpha:0.065),10),child:Row(children:[
Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[_tx(c,p.name,b:true),_tx(c,p.path.isNotEmpty?p.path:p.rawExe,cap:true)])),
_tx(c,p.direct?'✓ 已直连放通':'设为直连放通',cap:true,b:true,col:p.direct?cs.onSuccessContainer:_fg(c)),])),)),]);}Widget _ipP(BuildContext c,GuardianState st){
final cs=c.colorScheme,ntf=ref.read(guardianProvider.notifier),q=_iq.trim().toLowerCase();
final l=q.isEmpty?st.opts:st.opts.where((o)=>o.ip.toLowerCase().contains(q)||o.raw.toLowerCase().contains(q)||o.node.toLowerCase().contains(q)||(o.s24?.toLowerCase().contains(q)??false)).toList();return _cd(c,[
Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[Expanded(child:_tx(c,'${st.regLbl.isEmpty ? "当前区域" : st.regLbl} · 全部可选 IP (${st.opts.length})',b:true)),
TextButton(onPressed:st.busy?null:()=>unawaited(ntf.probReg()),child:Text(st.busy?'测速中...':'测速本区IP')),]),_sch(c,_ic,_if,'搜索本区 IP / 网段 / 线路名...',_iq,(v)=>setState(()=>_iq=v)),_lv(c,l,st.regs.isEmpty?'导入订阅后自动展示区域全部 IP':'无匹配 IP',(o){
final ips=o.ip.isNotEmpty?o.ip:(o.raw.isNotEmpty?o.raw:'点击切换解析 IP'),dl=o.ms>0?'${o.ms}ms':(o.ms<0?'超时':'待测');return GestureDetector(onTap:()=>unawaited(ntf.pickNode(st.grp,o.node)),
child:Container(padding:const EdgeInsets.symmetric(horizontal:11,vertical:8),decoration:_rb(o.sel?cs.successContainer.withValues(alpha:0.55):_fg(c).withValues(alpha:0.065),10),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:2,children:[
Row(children:[Expanded(child:_tx(c,'IP: $ips',b:true,col:o.sel?cs.onSuccessContainer:_fg(c))),
_tx(c,'$dl · ${o.sel ? "✓ 当前选中" : (o.sticky ? "本区记忆" : "点击固定")}',cap:true,b:true,col:o.ms<0?cs.onErrorContainer:(o.sel?cs.onSuccessContainer:_fg(c))),]),_tx(c,'线路: ${o.node}${o.s24 != null ? " · 网段: ${o.s24}" : ""}',cap:true),])),);}),
]);}Widget _pP(BuildContext c,GuardianState st){final cs=c.colorScheme,ntf=ref.read(guardianProvider.notifier),q=_pq.trim().toLowerCase(),tot=st.tot<=0?1:st.tot;
final l=q.isEmpty?st.procs:st.procs.where((p)=>p.name.toLowerCase().contains(q)||p.exit.toLowerCase().contains(q)).toList();return _cd(c,[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
Expanded(child:_tx(c,'进程流量 · ↑${fmtBytes(st.up)} / ↓${fmtBytes(st.dn)}',b:true)),TextButton(onPressed:ntf.rstTrf,child:const Text('清零')),]),_sch(c,_pc,_pf,'搜索进程名 / 包名 / 出口...',_pq,(v)=>setState(()=>_pq=v)),
_lv(c,l,'开启全局接管后实时显示各进程上下行并支持一键直连',(p){final sum=p.up+p.dn;
return Container(padding:const EdgeInsets.all(10),decoration:_rb(p.direct?cs.successContainer.withValues(alpha:0.35):_fg(c).withValues(alpha:0.065),10),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:4,children:[
Row(spacing:8,children:[Expanded(child:_tx(c,'${p.name} (${p.conns}连接 · ${p.exit.isEmpty ? "GLOBAL" : p.exit})',b:true)),_tx(c,'↑${fmtRate(p.upR)} ↓${fmtRate(p.dnR)}',cap:true,b:true),
if(p.rawExe.isNotEmpty||p.pkg.isNotEmpty)GestureDetector(onTap:()=>unawaited(ntf.togDir(label:p.name,exe:p.rawExe,path:p.path,pkg:p.pkg)),
child:Container(padding:const EdgeInsets.symmetric(horizontal:8,vertical:3),decoration:_rb(p.direct?cs.successContainer:_fg(c).withValues(alpha:0.1),7),child:_tx(c,p.direct?'✓直连':'直连放通',cap:true,b:true,col:p.direct?cs.onSuccessContainer:_fg(c))),
),]),Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[_tx(c,'累计 ↑${fmtBytes(p.up)} · ↓${fmtBytes(p.dn)}',cap:true),_tx(c,'总计 ${fmtBytes(sum)}',cap:true,b:true)]),
Container(height:4,width:double.infinity,decoration:_rb(_fg(c).withValues(alpha:0.08),2),child:FractionallySizedBox(alignment:Alignment.centerLeft,widthFactor:(sum/tot).clamp(0.0,1.0),child:Container(decoration:_rb(cs.onSuccessContainer,2)))),
]));}),]);}Widget _lP(BuildContext c,GuardianState st){final cs=c.colorScheme,ntf=ref.read(guardianProvider.notifier),q=_lq.trim().toLowerCase();
final l=st.logs.where((e)=>(_cat==null||e.cat==_cat)&&(q.isEmpty||e.title.toLowerCase().contains(q)||e.detail.toLowerCase().contains(q))).toList();return _cd(c,[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
_tx(c,'明确清晰运行日志',b:true),Row(mainAxisSize:MainAxisSize.min,children:[
TextButton(onPressed:l.isEmpty?null:()=>unawaited(Clipboard.setData(ClipboardData(text:l.map((e)=>'[${fmtTime(e.time)}][${e.cat.label}] ${e.title} | ${e.detail}').join('\n')))),child:const Text('复制')),
TextButton(onPressed:ntf.clrLog,child:const Text('清空')),]),]),Wrap(spacing:6,runSpacing:6,children:[_ch(c,_cat==null,'全部',()=>setState(()=>_cat=null)),for(final ct in LogCat.values)_ch(c,_cat==ct,ct.label,()=>setState(()=>_cat=ct))]),
_sch(c,_lc,_lf,'筛选节点名、IP段、直连进程或告警...',_lq,(v)=>setState(()=>_lq=v)),
_lv(c,l,'暂无日志',(e)=>Container(padding:const EdgeInsets.all(8),decoration:_rb(e.hot?cs.successContainer.withValues(alpha:0.45):_fg(c).withValues(alpha:0.065),10),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:2,children:[
_tx(c,'[${fmtTime(e.time)}][${e.cat.label}] ${e.title}',cap:true,b:true),Text(e.detail,style:AppTextStyle.caption1.of(c).copyWith(color:_mu(c))),]))),]);}}
