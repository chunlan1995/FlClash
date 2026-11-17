// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import'dart:async';import'package:fl_clash/ui/icons/icons.dart';import'package:fl_clash/views/profiles/add.dart';import'package:fl_clash/widgets/widgets.dart';import'package:flutter/services.dart';
import'package:flutter/widgets.dart';import'package:flutter_riverpod/flutter_riverpod.dart';import'package:prism_ui/prism_ui.dart';import'flclash_bridge.dart';import'smart_guardian.dart';
class SimpleModeHost extends ConsumerWidget{const SimpleModeHost({super.key,required this.originalChild});final Widget originalChild;@override Widget build(BuildContext context,WidgetRef ref){
ref.watch(guardianProvider.select((s)=>s.auto));final simple=ref.watch(simpleModeProvider);return Stack(children:[Offstage(offstage:simple,child:originalChild),if(simple)const Positioned.fill(child:SimpleWorkbenchView())else
Positioned(right:18,bottom:20,child:SafeArea(child:FilledButton(onPressed:()=>ref.read(simpleModeProvider.notifier).setMode(true),child:const Text('返回极简模式'),),),),],);}}
class SimpleWorkbenchView extends ConsumerStatefulWidget{const SimpleWorkbenchView({super.key});@override ConsumerState<SimpleWorkbenchView>createState()=>_SWState();}class _SWState extends ConsumerState<SimpleWorkbenchView>{
final _ic=TextEditingController(),_pc=TextEditingController(),_lc=TextEditingController();final _if=FocusNode(),_pf=FocusNode(),_lf=FocusNode();LogCat?_cat;int _mt=0,_rt=0;String _iq='',_pq='',_lq='';bool _busy=false;
@override void dispose(){_ic.dispose();_if.dispose();_pc.dispose();_pf.dispose();_lc.dispose();_lf.dispose();super.dispose();}Future<void>_tog(bool run)async{if(_busy)return;setState(()=>_busy=true);try{
await FlClashBridge.toggleRunning(ref,context,!run);}finally{if(mounted)setState(()=>_busy=false);}}Color _fg(BuildContext c)=>DefaultTextStyle.of(c).style.color??const Color(0xFF1F2937);
Color _mu(BuildContext c)=>_fg(c).withValues(alpha:0.62);ShapeDecoration _rb(Color c,double r)=>ShapeDecoration(color:c,shape:RoundedSuperellipseBorder(borderRadius:BorderRadius.circular(r)));
Widget _ch(BuildContext c,bool sel,String txt,VoidCallback tap){final cs=c.colorScheme;return GestureDetector(onTap:tap,child:Container(padding:const EdgeInsets.symmetric(horizontal:11,vertical:6),alignment:Alignment.center,
decoration:_rb(sel?cs.successContainer:_fg(c).withValues(alpha:0.065),10),child:Text(txt,style:AppTextStyle.subheadline.of(c,emphasized:sel).copyWith(color:sel?cs.onSuccessContainer:_fg(c)),),),);}
Widget _sb(BuildContext c,String lb,String v)=>Container(padding:const EdgeInsets.symmetric(horizontal:10,vertical:6),decoration:_rb(_fg(c).withValues(alpha:0.06),10),child:Column(crossAxisAlignment:CrossAxisAlignment.start,
children:[Text(lb,style:AppTextStyle.caption1.of(c).copyWith(color:_mu(c))),Text(v,style:AppTextStyle.subheadline.of(c,emphasized:true)),],),);
Widget _sch(BuildContext c,TextEditingController tc,FocusNode fn,String hint,String val,ValueChanged<String>chg){final fg=_fg(c);return GestureDetector(onTap:fn.requestFocus,child:Container(
padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),decoration:_rb(fg.withValues(alpha:0.065),10),child:Row(spacing:8,children:[Expanded(child:Stack(alignment:Alignment.centerLeft,children:[
if(val.isEmpty)Text(hint,style:AppTextStyle.subheadline.of(c).copyWith(color:_mu(c))),EditableText(controller:tc,focusNode:fn,autocorrect:false,onChanged:chg,style:AppTextStyle.subheadline.of(c).copyWith(color:fg),
cursorColor:fg,backgroundCursorColor:_mu(c),),],),),if(val.isNotEmpty)GestureDetector(onTap:(){tc.clear();chg('');},child:Text('×',style:AppTextStyle.headline.of(c)),),],),),);}@override Widget build(BuildContext context){
final cs=context.colorScheme;final st=ref.watch(guardianProvider);final run=FlClashBridge.watchRunning(ref);final profs=FlClashBridge.watchProfiles(ref);final curP=profs.where((p)=>p.selected).firstOrNull;
final lsw=st.sws.firstOrNull;final d=st.ms;final dStr=!run?'未启动':(d<0?'超时 (> ${st.lim}ms)':(d==0?'待测速':'${d}ms'));final curIp=(st.meta!=null&&st.meta!.ip.isNotEmpty)?st.meta!.ip
:((st.meta!=null&&st.meta!.raw.isNotEmpty)?st.meta!.raw:(st.node.isEmpty?'未选择':'正在解析 IP...'));final curSub=st.meta?.s24??'自动同段保持';return Surface(color:SurfaceLevel.page.colorOf(cs),child:SafeArea(child:LayoutBuilder(
builder:(ctx,box){final wide=box.maxWidth>=900;final rcs=[for(final r in st.regs)_ch(ctx,r.code==st.reg,'${r.label} (${r.nodes.length})',()=>unawaited(ref.read(guardianProvider.notifier).selectRegion(r.code))),];
return Column(children:[Padding(padding:const EdgeInsets.fromLTRB(16,8,16,4),child:Wrap(alignment:WrapAlignment.spaceBetween,crossAxisAlignment:WrapCrossAlignment.center,spacing:10,runSpacing:6,children:[
Text('FlClash · 极简智控版',style:AppTextStyle.headline.of(ctx,emphasized:true)),Wrap(spacing:6,runSpacing:6,crossAxisAlignment:WrapCrossAlignment.center,children:[if(profs.isNotEmpty)PopupAnchor(
targetBuilder:(open)=>TextButton(onPressed:open,child:Text('订阅: ${curP?.label ?? "选择"} ▾')),popupBuilder:(_)=>PopupMenu(
items:[for(final p in profs)PopupMenuItem(glyph:p.selected?AppGlyphs.check:null,label:p.label,onPressed:p.onSelect)],),),AddProfileMenu(builder:(open)=>TextButton(onPressed:open,child:const Text('+ 导入订阅'))),PopupAnchor(
targetBuilder:(open)=>TextButton(onPressed:open,child:Text('阈值 ${st.lim}ms ▾')),popupBuilder:(_)=>PopupMenu(items:[for(final ms in const[600,800,1000,1500])PopupMenuItem(glyph:st.lim==ms?AppGlyphs.check:null,
label:ms==1000?'1000ms (默认)':'${ms}ms',onPressed:()=>ref.read(guardianProvider.notifier).setLimit(ms),),],),),TextButton(onPressed:()=>ref.read(simpleModeProvider.notifier).setMode(false),child:const Text('完整面板')),],),],),),
Expanded(child:Padding(padding:const EdgeInsets.fromLTRB(16,4,16,12),child:Column(spacing:10,children:[Container(padding:const EdgeInsets.all(12),decoration:_rb(_fg(ctx).withValues(alpha:0.045),18),child:Column(
crossAxisAlignment:CrossAxisAlignment.start,spacing:10,children:[Wrap(alignment:WrapAlignment.spaceBetween,crossAxisAlignment:WrapCrossAlignment.center,spacing:12,runSpacing:8,children:[Row(mainAxisSize:MainAxisSize.min,
spacing:12,children:[FilledButton(onPressed:_busy?null:()=>_tog(run),child:Text(_busy?'切换中...':(run?'● 代理运行中（点击停止）':'▶ 一键开启代理')),),Flexible(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text(
'当前选中 IP: $curIp  ${st.regLbl}',maxLines:1,overflow:TextOverflow.ellipsis,style:AppTextStyle.body.of(ctx,emphasized:true),),Text('线路: ${st.node.isEmpty ? "自动" : st.node} · 延迟: $dStr · 网段: $curSub',maxLines:1,
overflow:TextOverflow.ellipsis,style:AppTextStyle.caption1.of(ctx).copyWith(color:(!run||(d>=0&&d<st.lim))?_mu(ctx):cs.onErrorContainer,),),],),),],),Wrap(spacing:8,runSpacing:6,children:[
_sb(ctx,'实时上行','↑ ${fmtRate(st.upR)}'),_sb(ctx,'实时下行','↓ ${fmtRate(st.dnR)}'),_sb(ctx,'当次总流量','${fmtBytes(st.tot)} (↑${fmtBytes(st.up)}/↓${fmtBytes(st.dn)})'),],),],),if(st.regs.isEmpty)
Text('尚未检测到订阅节点，请点击右上角「+ 导入订阅」载入配置后自动聚合国家与区域',style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx)))else if(wide)Wrap(spacing:8,runSpacing:6,children:rcs)else
SingleChildScrollView(scrollDirection:Axis.horizontal,child:Row(spacing:8,children:rcs)),Wrap(spacing:8,runSpacing:6,crossAxisAlignment:WrapCrossAlignment.center,children:[
_ch(ctx,st.auto,st.auto?'✓ 超时同段无缝转接 (${st.lim}ms)':'超时自动转接已关',()=>ref.read(guardianProvider.notifier).setAuto(!st.auto)),
_ch(ctx,st.lock,st.lock?'✓ 锁定所选国家区域':'允许跨区兜底',()=>ref.read(guardianProvider.notifier).setLock(!st.lock)),
TextButton(onPressed:st.busy?null:()=>unawaited(ref.read(guardianProvider.notifier).manualCheck()),child:Text(st.busy?'检测中...':'检测当前IP')),if(lsw!=null)
Text('最近转接: ${lsw.from} → ${lsw.to} (${lsw.tier.label}, ${lsw.ms}ms)',style:AppTextStyle.caption1.of(ctx,emphasized:true)),],),],),),if(!wide)Row(spacing:6,children:[
Expanded(child:_ch(ctx,_mt==0,'当前区域IP (${st.opts.length})',()=>setState(()=>_mt=0))),Expanded(child:_ch(ctx,_mt==1,'进程流量 (${st.procs.length})',()=>setState(()=>_mt=1))),
Expanded(child:_ch(ctx,_mt==2,'清晰日志 (${st.logs.length})',()=>setState(()=>_mt=2))),],),Expanded(child:wide?Row(spacing:12,children:[Expanded(flex:5,child:_ipP(ctx,st)),Expanded(flex:6,child:_rP(ctx,st))])
:(_mt==0?_ipP(ctx,st):(_mt==1?_pP(ctx,st):_lP(ctx,st))),),],),),),],);},),),);}Widget _rP(BuildContext ctx,GuardianState st)=>Column(spacing:8,children:[Row(spacing:8,children:[
Expanded(child:_ch(ctx,_rt==0,'进程流量监控 (${st.procs.length})',()=>setState(()=>_rt=0))),Expanded(child:_ch(ctx,_rt==1,'明确清晰日志 (${st.logs.length})',()=>setState(()=>_rt=1))),],),Expanded(child:_rt==0?_pP(ctx,st):_lP(ctx,st)),],
);Widget _ipP(BuildContext ctx,GuardianState st){final cs=ctx.colorScheme;final q=_iq.trim().toLowerCase();final list=q.isEmpty?st.opts
:st.opts.where((o)=>o.ip.toLowerCase().contains(q)||o.raw.toLowerCase().contains(q)||o.node.toLowerCase().contains(q)||(o.s24?.toLowerCase().contains(q)??false)).toList();return Container(padding:const EdgeInsets.all(12),
decoration:_rb(_fg(ctx).withValues(alpha:0.045),16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:8,children:[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[Expanded(child:Text(
'${st.regLbl.isEmpty ? "当前区域" : st.regLbl} · 全部可选 IP (${st.opts.length})',maxLines:1,overflow:TextOverflow.ellipsis,style:AppTextStyle.subheadline.of(ctx,emphasized:true),),),TextButton(
onPressed:st.busy?null:()=>unawaited(ref.read(guardianProvider.notifier).probeCurrentRegion()),child:Text(st.busy?'解析测速中...':'测速本区IP'),),],),_sch(ctx,_ic,_if,'搜索本区 IP 地址 / 网段 / 线路名...',_iq,(v)=>setState(()=>_iq=v)),Expanded(
child:list.isEmpty?Center(child:Text(st.regs.isEmpty?'导入订阅后将自动展示对应区域的全部 IP 选项':'未匹配到符合筛选条件的区域 IP',style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx)),textAlign:TextAlign.center,),):ListView.separated(
itemCount:list.length,separatorBuilder:(_,_)=>const SizedBox(height:6),itemBuilder:(_,i){final o=list[i];final ips=o.ip.isNotEmpty?o.ip:(o.raw.isNotEmpty?o.raw:'点击切换或测速解析 IP');final dl=o.ms>0?'${o.ms}ms':(o.ms<0?'超时':'待测');
final bg=o.sel?'✓ 当前选中':(o.sticky?'本区记忆':'点击固定');return GestureDetector(onTap:()=>unawaited(ref.read(guardianProvider.notifier).pickNode(st.grp,o.node)),child:Container(
padding:const EdgeInsets.symmetric(horizontal:11,vertical:9),decoration:_rb(o.sel?cs.successContainer.withValues(alpha:0.55):_fg(ctx).withValues(alpha:0.065),11),child:Column(crossAxisAlignment:CrossAxisAlignment.start,
spacing:3,children:[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[Expanded(child:Text('IP: $ips',maxLines:1,overflow:TextOverflow.ellipsis,
style:AppTextStyle.body.of(ctx,emphasized:true).copyWith(color:o.sel?cs.onSuccessContainer:_fg(ctx)),),),Text('$dl · $bg',style:AppTextStyle.caption1.of(ctx,emphasized:true).copyWith(
color:o.ms<0?cs.onErrorContainer:(o.sel?cs.onSuccessContainer:_fg(ctx)),),),],),Text('线路: ${o.node}${o.s24 != null ? " · 网段: ${o.s24}" : ""}',maxLines:1,overflow:TextOverflow.ellipsis,
style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx)),),],),),);},),),],),);}Widget _pP(BuildContext ctx,GuardianState st){final cs=ctx.colorScheme;final q=_pq.trim().toLowerCase();
final list=q.isEmpty?st.procs:st.procs.where((p)=>p.name.toLowerCase().contains(q)||p.exit.toLowerCase().contains(q)).toList();final tot=st.tot<=0?1:st.tot;return Container(padding:const EdgeInsets.all(12),
decoration:_rb(_fg(ctx).withValues(alpha:0.045),16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:8,children:[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[Expanded(child:Text(
'进程上下行与总量 · ↑${fmtBytes(st.up)} / ↓${fmtBytes(st.dn)}',maxLines:1,overflow:TextOverflow.ellipsis,style:AppTextStyle.subheadline.of(ctx,emphasized:true),),),
TextButton(onPressed:()=>ref.read(guardianProvider.notifier).resetTraffic(),child:const Text('清零')),],),_sch(ctx,_pc,_pf,'搜索进程名 / 应用包名 / 出口节点...',_pq,(v)=>setState(()=>_pq=v)),Expanded(child:list.isEmpty?Center(
child:Text('开启代理产生请求后，将在此按进程实时显示上下行速率与当次累计总量',style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx)),textAlign:TextAlign.center),):ListView.separated(itemCount:list.length,
separatorBuilder:(_,_)=>const SizedBox(height:6),itemBuilder:(_,i){final p=list[i];final sum=p.up+p.dn;return Container(padding:const EdgeInsets.all(10),decoration:_rb(_fg(ctx).withValues(alpha:0.065),10),child:Column(
crossAxisAlignment:CrossAxisAlignment.start,spacing:4,children:[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[Expanded(
child:Text('${p.name} (${p.conns} 连接 · ${p.exit.isEmpty ? "DIRECT" : p.exit})',maxLines:1,overflow:TextOverflow.ellipsis,style:AppTextStyle.body.of(ctx,emphasized:true)),),
Text('↑ ${fmtRate(p.upR)}  ↓ ${fmtRate(p.dnR)}',style:AppTextStyle.caption1.of(ctx,emphasized:true)),],),Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
Text('累计 ↑${fmtBytes(p.up)} · ↓${fmtBytes(p.dn)}',style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx))),Text('总计 ${fmtBytes(sum)}',style:AppTextStyle.caption1.of(ctx,emphasized:true)),],),Container(height:4,
width:double.infinity,decoration:_rb(_fg(ctx).withValues(alpha:0.08),2),child:FractionallySizedBox(alignment:Alignment.centerLeft,widthFactor:(sum/tot).clamp(0.0,1.0),child:Container(decoration:_rb(cs.onSuccessContainer,2))),
),],),);},),),],),);}Widget _lP(BuildContext ctx,GuardianState st){final cs=ctx.colorScheme;final q=_lq.trim().toLowerCase();
final list=st.logs.where((e)=>(_cat==null||e.cat==_cat)&&(q.isEmpty||e.title.toLowerCase().contains(q)||e.detail.toLowerCase().contains(q))).toList();return Container(padding:const EdgeInsets.all(12),
decoration:_rb(_fg(ctx).withValues(alpha:0.045),16),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:6,children:[Row(mainAxisAlignment:MainAxisAlignment.spaceBetween,children:[
Text('明确清晰运行日志',style:AppTextStyle.subheadline.of(ctx,emphasized:true)),Row(mainAxisSize:MainAxisSize.min,children:[TextButton(onPressed:list.isEmpty?null
:()=>unawaited(Clipboard.setData(ClipboardData(text:list.map((e)=>'[${fmtTime(e.time)}][${e.cat.label}] ${e.title} | ${e.detail}').join('\n')))),child:const Text('复制'),),
TextButton(onPressed:()=>ref.read(guardianProvider.notifier).clearLogs(),child:const Text('清空')),],),],),Wrap(spacing:6,runSpacing:6,children:[_ch(ctx,_cat==null,'全部',()=>setState(()=>_cat=null)),
for(final c in LogCat.values)_ch(ctx,_cat==c,c.label,()=>setState(()=>_cat=c)),],),_sch(ctx,_lc,_lf,'筛选节点名、IP段、进程或告警...',_lq,(v)=>setState(()=>_lq=v)),Expanded(child:list.isEmpty
?Center(child:Text('暂无日志',style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx)))):ListView.separated(itemCount:list.length,separatorBuilder:(_,_)=>const SizedBox(height:6),itemBuilder:(_,i){final e=list[i];
return Container(padding:const EdgeInsets.all(8),decoration:_rb(e.hot?cs.successContainer.withValues(alpha:0.45):_fg(ctx).withValues(alpha:0.065),10),child:Column(crossAxisAlignment:CrossAxisAlignment.start,spacing:2,
children:[Text('[${fmtTime(e.time)}][${e.cat.label}] ${e.title}',style:AppTextStyle.caption1.of(ctx,emphasized:true)),Text(e.detail,style:AppTextStyle.caption1.of(ctx).copyWith(color:_mu(ctx))),],),);},),),],),);}}'; import 'package:fl_clash/views/profiles/add.dart';
import 'package:fl_clash/widgets/widgets.dart'; import 'package:flutter/services.dart'; import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart'; import 'package:prism_ui/prism_ui.dart'; import 'flclash_bridge.dart'; import 'smart_guardian.dart';
class SimpleModeHost extends ConsumerWidget { const SimpleModeHost({super.key, required this.originalChild}); final Widget originalChild; @override
Widget build(BuildContext context, WidgetRef ref) { ref.watch(guardianProvider.select((s) => s.autoSwitch)); final simple = ref.watch(simpleModeProvider);
return Stack(children: [ Offstage(offstage: simple, child: originalChild), if (simple) const Positioned.fill(child: SimpleWorkbenchView())
else Positioned(right: 18, bottom: 20, child: SafeArea(child: FilledButton(onPressed: () => ref.read(simpleModeProvider.notifier).setMode(true), child: const Text('返回极简模式')))),
]); } } class SimpleWorkbenchView extends ConsumerStatefulWidget { const SimpleWorkbenchView({super.key});
@override ConsumerState<SimpleWorkbenchView> createState() => _SimpleWorkbenchViewState(); }
class _SimpleWorkbenchViewState extends ConsumerState<SimpleWorkbenchView> { final _pCtrl = TextEditingController(), _lCtrl = TextEditingController();
final _pFoc = FocusNode(), _lFoc = FocusNode(); LogCat? _cat; int _tab = 0; String _pq = '', _lq = ''; bool _busy = false; @override
void dispose() { _pCtrl.dispose(); _pFoc.dispose(); _lCtrl.dispose(); _lFoc.dispose(); super.dispose(); } Future<void> _toggle(bool run) async { if (_busy) return;
setState(() => _busy = true); try { await FlClashBridge.toggleRunning(ref, context, !run); } finally { if (mounted) setState(() => _busy = false); } }
Color _fg(BuildContext ctx) => DefaultTextStyle.of(ctx).style.color ?? const Color(0xFF1F2937); Color _muted(BuildContext ctx) => _fg(ctx).withValues(alpha: 0.64);
ShapeDecoration _rbox(Color c, double r) => ShapeDecoration(color: c, shape: RoundedSuperellipseBorder(borderRadius: BorderRadius.circular(r)));
Widget _chip(BuildContext ctx, bool sel, String txt, VoidCallback tap) { final cs = ctx.colorScheme; return GestureDetector( onTap: tap, child: Container(
padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7), alignment: Alignment.center,
decoration: _rbox(sel ? cs.successContainer : _fg(ctx).withValues(alpha: 0.065), 10),
child: Text(txt, style: AppTextStyle.subheadline.of(ctx).copyWith(color: sel ? cs.onSuccessContainer : _fg(ctx))), ), ); }
Widget _search(BuildContext ctx, TextEditingController c, FocusNode f, String hint, String val, ValueChanged<String> onChg) { final fg = _fg(ctx);
return GestureDetector( onTap: f.requestFocus, child: Container(
padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8), decoration: _rbox(fg.withValues(alpha: 0.065), 10), child: Row(spacing: 8, children: [
Expanded(child: Stack(alignment: Alignment.centerLeft, children: [ if (val.isEmpty) Text(hint, style: AppTextStyle.subheadline.of(ctx).copyWith(color: _muted(ctx))),
EditableText(controller: c, focusNode: f, autocorrect: false, onChanged: onChg, style: AppTextStyle.subheadline.of(ctx).copyWith(color: fg), cursorColor: fg, backgroundCursorColor: _muted(ctx)),
])), if (val.isNotEmpty) GestureDetector(onTap: () { c.clear(); onChg(''); }, child: Text('×', style: AppTextStyle.headline.of(ctx))), ]), ), ); } @override
Widget build(BuildContext context) { final cs = context.colorScheme; final st = ref.watch(guardianProvider);
final run = FlClashBridge.watchRunning(ref); final profs = FlClashBridge.watchProfiles(ref); final grps = FlClashBridge.watchGroups(ref);
final curP = profs.where((p) => p.selected).firstOrNull; final grp = grps.where((g) => g.isSelector && g.all.isNotEmpty).firstOrNull;
final lastSw = st.switches.firstOrNull; final d = st.delayMs; final dStr = !run ? '未启动' : (d < 0 ? '超时 (> ${st.limitMs}ms)' : (d == 0 ? '待测速' : '${d}ms'));
final ep = st.meta == null ? '等待解析网段' : '${st.meta!.ip.isNotEmpty ? "${st.meta!.ip} · " : ""}${st.meta!.regLabel}'; return Surface(
color: SurfaceLevel.page.colorOf(cs), child: SafeArea(child: LayoutBuilder(builder: (ctx, box) { final wide = box.maxWidth >= 880; return Column(children: [ Padding(
padding: const EdgeInsets.fromLTRB(16, 10, 16, 6),
child: Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 10, runSpacing: 8, children: [
Text('FlClash · 极简智控版', style: AppTextStyle.headline.of(ctx, emphasized: true)),
Wrap(spacing: 8, runSpacing: 8, crossAxisAlignment: WrapCrossAlignment.center, children: [ if (profs.isNotEmpty) PopupAnchor(
targetBuilder: (open) => TextButton(onPressed: open, child: Text('订阅: ${curP?.label ?? "选择"} ▾')),
popupBuilder: (_) => PopupMenu(items: [for (final p in profs) PopupMenuItem(glyph: p.selected ? AppGlyphs.check : null, label: p.label, onPressed: p.onSelect)]), ),
AddProfileMenu(builder: (open) => TextButton(onPressed: open, child: const Text('+ 导入订阅'))),
TextButton(onPressed: () => ref.read(simpleModeProvider.notifier).setMode(false), child: const Text('完整面板')), ]), ]), ), Expanded(child: Padding(
padding: const EdgeInsets.fromLTRB(16, 6, 16, 14), child: Column(spacing: 10, children: [ Container(
padding: const EdgeInsets.all(14), decoration: _rbox(_fg(ctx).withValues(alpha: 0.045), 18),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 10, children: [
Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 14, runSpacing: 10, children: [
Row(mainAxisSize: MainAxisSize.min, spacing: 12, children: [
FilledButton(onPressed: _busy ? null : () => _toggle(run), child: Text(_busy ? '切换中...' : (run ? '● 代理运行中（点击停止）' : '▶ 一键开启代理'))),
Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
Text('节点: ${st.node.isEmpty ? "自动选择" : st.node}', style: AppTextStyle.body.of(ctx, emphasized: true)),
Text('延迟: $dStr · $ep', style: AppTextStyle.caption1.of(ctx).copyWith(color: (!run || (d > 0 && d < st.limitMs)) ? _muted(ctx) : cs.onErrorContainer)), ]), ]),
Wrap(spacing: 12, runSpacing: 6, children: [ Text('↑ ${fmtRate(st.upRate)}', style: AppTextStyle.subheadline.of(ctx, emphasized: true)),
Text('↓ ${fmtRate(st.downRate)}', style: AppTextStyle.subheadline.of(ctx, emphasized: true)),
Text('当次累计: ${fmtBytes(st.sumTotal)}', style: AppTextStyle.subheadline.of(ctx)), ]), ]),
Wrap(spacing: 8, runSpacing: 8, crossAxisAlignment: WrapCrossAlignment.center, children: [
_chip(ctx, st.autoSwitch, st.autoSwitch ? '✓ 超时无缝转接 (${st.limitMs}ms)' : '自动转接已暂停', () => ref.read(guardianProvider.notifier).setAuto(!st.autoSwitch)), PopupAnchor(
targetBuilder: (open) => TextButton(onPressed: open, child: Text('阈值 ${st.limitMs}ms ▾')),
popupBuilder: (_) => PopupMenu(items: [for (final ms in const [600, 800, 1000, 1500]) PopupMenuItem(glyph: st.limitMs == ms ? AppGlyphs.check : null, label: ms == 1000 ? '1000ms (默认)' : '${ms}ms', onPressed: () => ref.read(guardianProvider.notifier).setLimit(ms))]),
), TextButton(onPressed: st.probing ? null : () => unawaited(ref.read(guardianProvider.notifier).manualCheck()), child: Text(st.probing ? '探测中...' : '立即测速择优')),
if (grp != null) PopupAnchor( targetBuilder: (open) => TextButton(onPressed: open, child: const Text('手动选节点 ▾')),
popupBuilder: (_) => PopupMenu(items: [for (final n in grp.all.take(45)) PopupMenuItem(glyph: n == grp.now ? AppGlyphs.check : null, label: n, onPressed: () => unawaited(ref.read(guardianProvider.notifier).pickNode(grp.name, n)))]),
), if (lastSw != null) Text('最近转接: ${lastSw.from} → ${lastSw.to} (${lastSw.tier.label}, ${lastSw.ms}ms)', style: AppTextStyle.caption1.of(ctx, emphasized: true)),
]), ]), ), if (!wide) Row(spacing: 8, children: [ Expanded(child: _chip(ctx, _tab == 0, '进程流量 (${st.procs.length})', () => setState(() => _tab = 0))),
Expanded(child: _chip(ctx, _tab == 1, '清晰日志 (${st.logs.length})', () => setState(() => _tab = 1))), ]),
Expanded(child: wide ? Row(spacing: 12, children: [Expanded(flex: 6, child: _procPane(ctx, st)), Expanded(flex: 5, child: _logPane(ctx, st))]) : (_tab == 0 ? _procPane(ctx, st) : _logPane(ctx, st))),
]), )), ]); })), ); } Widget _procPane(BuildContext ctx, GuardianState st) { final cs = ctx.colorScheme; final q = _pq.trim().toLowerCase();
final list = q.isEmpty ? st.procs : st.procs.where((p) => p.name.toLowerCase().contains(q) || p.exit.toLowerCase().contains(q)).toList();
final tot = st.sumTotal <= 0 ? 1 : st.sumTotal; return Container( padding: const EdgeInsets.all(12), decoration: _rbox(_fg(ctx).withValues(alpha: 0.045), 16),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 8, children: [ Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
Expanded(child: Text('进程上下行与总量 · ↑${fmtBytes(st.sumUp)} / ↓${fmtBytes(st.sumDown)}', maxLines: 1, overflow: TextOverflow.ellipsis, style: AppTextStyle.subheadline.of(ctx, emphasized: true))),
TextButton(onPressed: () => ref.read(guardianProvider.notifier).resetTraffic(), child: const Text('清零')), ]),
_search(ctx, _pCtrl, _pFoc, '搜索进程名 / 应用包名 / 出口节点...', _pq, (v) => setState(() => _pq = v)), Expanded(child: list.isEmpty
? Center(child: Text('代理运行产生请求后，将在此按进程实时显示上下行速率与当次累计总量', style: AppTextStyle.caption1.of(ctx).copyWith(color: _muted(ctx)), textAlign: TextAlign.center))
: ListView.separated( itemCount: list.length, separatorBuilder: (_, _) => const SizedBox(height: 6), itemBuilder: (_, i) {
final p = list[i]; final sum = p.sumUp + p.sumDown; return Container( padding: const EdgeInsets.all(10), decoration: _rbox(_fg(ctx).withValues(alpha: 0.065), 10),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 4, children: [ Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
Expanded(child: Text('${p.name} (${p.conns} 连接 · ${p.exit.isEmpty ? "DIRECT" : p.exit})', maxLines: 1, overflow: TextOverflow.ellipsis, style: AppTextStyle.body.of(ctx, emphasized: true))),
Text('↑ ${fmtRate(p.upRate)}  ↓ ${fmtRate(p.downRate)}', style: AppTextStyle.caption1.of(ctx, emphasized: true)), ]),
Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
Text('累计 ↑${fmtBytes(p.sumUp)} · ↓${fmtBytes(p.sumDown)}', style: AppTextStyle.caption1.of(ctx).copyWith(color: _muted(ctx))),
Text('总计 ${fmtBytes(sum)}', style: AppTextStyle.caption1.of(ctx, emphasized: true)), ]),
Container(height: 4, width: double.infinity, decoration: _rbox(_fg(ctx).withValues(alpha: 0.08), 2), child: FractionallySizedBox(alignment: Alignment.centerLeft, widthFactor: (sum / tot).clamp(0.0, 1.0), child: Container(decoration: _rbox(cs.onSuccessContainer, 2)))),
]), ); }, )), ]), ); } Widget _logPane(BuildContext ctx, GuardianState st) { final cs = ctx.colorScheme; final q = _lq.trim().toLowerCase();
final list = st.logs.where((e) => (_cat == null || e.cat == _cat) && (q.isEmpty || e.title.toLowerCase().contains(q) || e.detail.toLowerCase().contains(q))).toList();
return Container( padding: const EdgeInsets.all(12), decoration: _rbox(_fg(ctx).withValues(alpha: 0.045), 16),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 6, children: [ Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
Text('明确清晰运行日志', style: AppTextStyle.subheadline.of(ctx, emphasized: true)), Row(mainAxisSize: MainAxisSize.min, children: [
TextButton(onPressed: list.isEmpty ? null : () => unawaited(Clipboard.setData(ClipboardData(text: list.map((e) => '[${fmtTime(e.time)}][${e.cat.label}] ${e.title} | ${e.detail}').join('\n')))), child: const Text('复制')),
TextButton(onPressed: () => ref.read(guardianProvider.notifier).clearLogs(), child: const Text('清空')), ]), ]), Wrap(spacing: 6, runSpacing: 6, children: [
_chip(ctx, _cat == null, '全部', () => setState(() => _cat = null)), for (final c in LogCat.values) _chip(ctx, _cat == c, c.label, () => setState(() => _cat = c)), ]),
_search(ctx, _lCtrl, _lFoc, '筛选节点名、IP段、进程或告警...', _lq, (v) => setState(() => _lq = v)), Expanded(child: list.isEmpty
? Center(child: Text('暂无日志', style: AppTextStyle.caption1.of(ctx).copyWith(color: _muted(ctx)))) : ListView.separated(
itemCount: list.length, separatorBuilder: (_, _) => const SizedBox(height: 6), itemBuilder: (_, i) { final e = list[i]; return Container(
padding: const EdgeInsets.all(8), decoration: _rbox(e.hot ? cs.successContainer.withValues(alpha: 0.45) : _fg(ctx).withValues(alpha: 0.065), 10),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: [
Text('[${fmtTime(e.time)}][${e.cat.label}] ${e.title}', style: AppTextStyle.caption1.of(ctx, emphasized: true)),
Text(e.detail, style: AppTextStyle.caption1.of(ctx).copyWith(color: _muted(ctx))), ]), ); }, )), ]), ); } }
