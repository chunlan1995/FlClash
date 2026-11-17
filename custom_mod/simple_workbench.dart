// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import 'dart:async';
import 'dart:io';
import 'package:fl_clash/ui/icons/icons.dart';
import 'package:fl_clash/views/profiles/add.dart';
import 'package:fl_clash/widgets/widgets.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:prism_ui/prism_ui.dart';
import 'flclash_bridge.dart';
import 'smart_guardian.dart';
class SimpleModeHost extends ConsumerWidget {
 const SimpleModeHost({super.key, required this.originalChild});
 final Widget originalChild;
 @override
 Widget build(BuildContext context, WidgetRef ref) {
  ref.watch(guardianProvider.select((s) => s.auto));
  final simple = ref.watch(simpleModeProvider);
  final backBtn = FilledButton(
   onPressed: () => unawaited(ref.read(guardianProvider.notifier).setUi(true)),
   child: const Text('返回极简模式（全局接管）'),
  );
  return Stack(children: [
   Offstage(offstage: simple, child: originalChild),
   if (simple) const Positioned.fill(child: SimpleWorkbenchView()),
   if (!simple) Positioned(right: 18, bottom: 20, child: SafeArea(child: backBtn)),
  ]);
 }
}
class SimpleWorkbenchView extends ConsumerStatefulWidget {
 const SimpleWorkbenchView({super.key});
 @override
 ConsumerState<SimpleWorkbenchView> createState() => _SWS();
}
class _SWS extends ConsumerState<SimpleWorkbenchView> {
 final _ic = TextEditingController(), _wc = TextEditingController(), _ac = TextEditingController(), _pc = TextEditingController(), _lc = TextEditingController();
 final _if = FocusNode(), _wf = FocusNode(), _af = FocusNode(), _pf = FocusNode(), _lf = FocusNode();
 LogCat? _cat;
 int _mt = 0, _rt = 0;
 String _iq = '', _wq = '', _aq = '', _pq = '', _lq = '';
 bool _busy = false;
 @override
 void dispose() {
  for (final c in [_ic, _wc, _ac, _pc, _lc]) c.dispose();
  for (final f in [_if, _wf, _af, _pf, _lf]) f.dispose();
  super.dispose();
 }
 Future<void> _tog(bool run) async {
  if (_busy) return;
  setState(() => _busy = true);
  try {
   await ref.read(guardianProvider.notifier).togRun(run);
  } finally {
   if (mounted) setState(() => _busy = false);
  }
 }
 Color _fg(BuildContext c) => DefaultTextStyle.of(c).style.color ?? const Color(0xFF1F2937);
 Color _mu(BuildContext c) => _fg(c).withValues(alpha: 0.62);
 ShapeDecoration _rb(Color c, double r) {
  return ShapeDecoration(color: c, shape: RoundedSuperellipseBorder(borderRadius: BorderRadius.circular(r)));
 }
 Widget _tx(BuildContext c, String s, {bool b = false, bool cap = false, Color? col}) {
  final base = cap ? AppTextStyle.caption1.of(c, emphasized: b) : AppTextStyle.body.of(c, emphasized: b);
  final clr = col ?? (cap && !b ? _mu(c) : _fg(c));
  return Text(s, maxLines: 1, overflow: TextOverflow.ellipsis, style: base.copyWith(color: clr));
 }
 Widget _cd(BuildContext c, List<Widget> ch) {
  final col = Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 8, children: ch);
  return Container(padding: const EdgeInsets.all(12), decoration: _rb(_fg(c).withValues(alpha: 0.045), 16), child: col);
 }
 Widget _lv<T>(BuildContext c, List<T> l, String emp, Widget Function(T) fn) {
  if (l.isEmpty) {
   final msg = Text(emp, style: AppTextStyle.caption1.of(c).copyWith(color: _mu(c)), textAlign: TextAlign.center);
   return Expanded(child: Center(child: msg));
  }
  Widget sep(BuildContext _, int __) => const SizedBox(height: 6);
  Widget item(BuildContext _, int i) => fn(l[i]);
  return Expanded(child: ListView.separated(itemCount: l.length, separatorBuilder: sep, itemBuilder: item));
 }
 Widget _ch(BuildContext c, bool sel, String txt, VoidCallback tap) {
  final cs = c.colorScheme;
  final bg = sel ? cs.successContainer : _fg(c).withValues(alpha: 0.065);
  final tc = sel ? cs.onSuccessContainer : _fg(c);
  final st = AppTextStyle.subheadline.of(c, emphasized: sel).copyWith(color: tc);
  final box = Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6), alignment: Alignment.center, decoration: _rb(bg, 10), child: Text(txt, style: st));
  return GestureDetector(onTap: tap, child: box);
 }
 Widget _sb(BuildContext c, String lb, String v) {
  final col = Column(crossAxisAlignment: CrossAxisAlignment.start, children: [_tx(c, lb, cap: true), Text(v, style: AppTextStyle.subheadline.of(c, emphasized: true))]);
  return Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6), decoration: _rb(_fg(c).withValues(alpha: 0.06), 10), child: col);
 }
 Widget _sch(BuildContext c, TextEditingController tc, FocusNode fn, String h, String v, ValueChanged<String> chg) {
  final fg = _fg(c);
  final ed = EditableText(controller: tc, focusNode: fn, autocorrect: false, onChanged: chg, style: AppTextStyle.subheadline.of(c).copyWith(color: fg), cursorColor: fg, backgroundCursorColor: _mu(c));
  final stk = Stack(alignment: Alignment.centerLeft, children: [if (v.isEmpty) _tx(c, h, col: _mu(c)), ed]);
  final clr = GestureDetector(onTap: () { tc.clear(); chg(''); }, child: Text('×', style: AppTextStyle.headline.of(c)));
  final row = Row(spacing: 8, children: [Expanded(child: stk), if (v.isNotEmpty) clr]);
  final box = Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7), decoration: _rb(fg.withValues(alpha: 0.065), 10), child: row);
  return GestureDetector(onTap: fn.requestFocus, child: box);
 }
 Widget _topBar(BuildContext c, GuardianState st, List<BridgeProfile> profs) {
  final ntf = ref.read(guardianProvider.notifier);
  final curP = profs.where((p) => p.selected).firstOrNull;
  final pItems = [for (final p in profs) PopupMenuItem(glyph: p.selected ? AppGlyphs.check : null, label: p.label, onPressed: p.onSelect)];
  final lItems = [for (final ms in const [600, 800, 1000, 1500]) PopupMenuItem(glyph: st.lim == ms ? AppGlyphs.check : null, label: ms == 1000 ? '1000ms(默认)' : '${ms}ms', onPressed: () => ntf.setLimit(ms))];
  final acts = Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: [
   if (profs.isNotEmpty) PopupAnchor(targetBuilder: (o) => TextButton(onPressed: o, child: Text('订阅: ${curP?.label ?? "选择"} ▾')), popupBuilder: (_) => PopupMenu(items: pItems)),
   AddProfileMenu(builder: (o) => TextButton(onPressed: o, child: const Text('+ 导入订阅'))),
   PopupAnchor(targetBuilder: (o) => TextButton(onPressed: o, child: Text('阈值 ${st.lim}ms ▾')), popupBuilder: (_) => PopupMenu(items: lItems)),
   TextButton(onPressed: () => unawaited(ntf.setUi(false)), child: const Text('完整面板')),
  ]);
  final ttl = Text('FlClash · 极简智控版 v${FlClashBridge.appVersion}', style: AppTextStyle.headline.of(c, emphasized: true));
  final row = Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 10, runSpacing: 6, children: [ttl, acts]);
  return Padding(padding: const EdgeInsets.fromLTRB(16, 8, 16, 4), child: row);
 }
 Widget _heroCard(BuildContext c, GuardianState st, bool run, bool wide) {
  final cs = c.colorScheme, ntf = ref.read(guardianProvider.notifier), d = st.ms, lsw = st.sws.firstOrNull;
  final dS = !run ? '未启动' : (d < 0 ? '超时(>${st.lim}ms)' : (d == 0 ? '待测速' : '${d}ms'));
  final cIp = (st.meta != null && st.meta!.ip.isNotEmpty) ? st.meta!.ip : ((st.meta != null && st.meta!.raw.isNotEmpty) ? st.meta!.raw : (st.node.isEmpty ? '未选择' : '解析中...'));
  final btn = FilledButton(onPressed: _busy ? null : () => _tog(run), child: Text(_busy ? '切换中...' : (run ? '● 全局接管中（点击停止）' : '▶ 一键开启全局接管')));
  final subClr = (!run || (d >= 0 && d < st.lim)) ? _mu(c) : cs.onErrorContainer;
  final info = Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
   _tx(c, '当前选中 IP: $cIp  ${st.regLbl}', b: true),
   _tx(c, '线路: ${st.node.isEmpty ? "自动" : st.node} · 延迟: $dS · 网段: ${st.meta?.s24 ?? "同段保持"} · 已无视订阅规则', cap: true, col: subClr),
  ]);
  final left = Row(mainAxisSize: MainAxisSize.min, spacing: 12, children: [btn, Flexible(child: info)]);
  final stats = Wrap(spacing: 8, runSpacing: 6, children: [
   _sb(c, '实时上行', '↑ ${fmtRate(st.upR)}'),
   _sb(c, '实时下行', '↓ ${fmtRate(st.dnR)}'),
   _sb(c, '当次总流量', '${fmtBytes(st.tot)} (↑${fmtBytes(st.up)}/↓${fmtBytes(st.dn)})'),
  ]);
  final head = Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 12, runSpacing: 8, children: [left, stats]);
  final rcs = [for (final r in st.regs) _ch(c, r.code == st.reg, '${r.label} (${r.nodes.length})', () => unawaited(ntf.selReg(r.code)))];
  final regBar = st.regs.isEmpty
    ? _tx(c, '尚未检测到订阅节点，请点击右上角「+ 导入订阅」自动聚合国家与区域', cap: true)
    : (wide ? Wrap(spacing: 8, runSpacing: 6, children: rcs) : SingleChildScrollView(scrollDirection: Axis.horizontal, child: Row(spacing: 8, children: rcs)));
  final ctrls = Wrap(spacing: 8, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: [
   _ch(c, true, '✓ 无视订阅规则·白名单直连 (${st.wl.length})', () => setState(() { _rt = 0; _mt = 1; })),
   if (!Platform.isAndroid) _ch(c, st.tun, st.tun ? '✓ TUN网卡全进程接管' : '仅系统代理', () => unawaited(ntf.setTun(!st.tun))),
   _ch(c, st.auto, st.auto ? '✓ 超时同段转接(${st.lim}ms)' : '超时转接已关', () => ntf.setAuto(!st.auto)),
   _ch(c, st.lock, st.lock ? '✓ 锁定所选区域' : '允许跨区兜底', () => ntf.setLock(!st.lock)),
   TextButton(onPressed: st.busy ? null : () => unawaited(ntf.chkNow()), child: Text(st.busy ? '检测中...' : '检测当前IP')),
   if (lsw != null) _tx(c, '最近转接: ${lsw.from} → ${lsw.to} (${lsw.tier.label}, ${lsw.ms}ms)', cap: true, b: true),
  ]);
  return _cd(c, [head, regBar, ctrls]);
 }
 @override
 Widget build(BuildContext context) {
  final cs = context.colorScheme, st = ref.watch(guardianProvider);
  final run = FlClashBridge.watchRunning(ref), profs = FlClashBridge.watchProfiles(ref);
  Widget builder(BuildContext ctx, BoxConstraints box) {
   final wide = box.maxWidth >= 900;
   final mTabs = Row(spacing: 6, children: [
    Expanded(child: _ch(ctx, _mt == 0, '区域IP(${st.opts.length})', () => setState(() => _mt = 0))),
    Expanded(child: _ch(ctx, _mt == 1, '直连(${st.wl.length})', () => setState(() => _mt = 1))),
    Expanded(child: _ch(ctx, _mt == 2, '进程(${st.procs.length})', () => setState(() => _mt = 2))),
    Expanded(child: _ch(ctx, _mt == 3, '日志(${st.logs.length})', () => setState(() => _mt = 3))),
   ]);
   final wideRow = Row(spacing: 12, children: [Expanded(flex: 5, child: _ipP(ctx, st)), Expanded(flex: 6, child: _rP(ctx, st))]);
   final mobPane = _mt == 0 ? _ipP(ctx, st) : (_mt == 1 ? _wP(ctx, st) : (_mt == 2 ? _pP(ctx, st) : _lP(ctx, st)));
   final bodyCol = Column(spacing: 10, children: [
    _heroCard(ctx, st, run, wide),
    if (!wide) mTabs,
    Expanded(child: wide ? wideRow : mobPane),
   ]);
   final bodyPad = Padding(padding: const EdgeInsets.fromLTRB(16, 4, 16, 12), child: bodyCol);
   return Column(children: [_topBar(ctx, st, profs), Expanded(child: bodyPad)]);
  }
  return Surface(color: SurfaceLevel.page.colorOf(cs), child: SafeArea(child: LayoutBuilder(builder: builder)));
 }
 Widget _rP(BuildContext c, GuardianState st) {
  final tabs = Row(spacing: 8, children: [
   Expanded(child: _ch(c, _rt == 0, '直连放通白名单 (${st.wl.length})', () => setState(() => _rt = 0))),
   Expanded(child: _ch(c, _rt == 1, '进程流量监控 (${st.procs.length})', () => setState(() => _rt = 1))),
   Expanded(child: _ch(c, _rt == 2, '清晰日志 (${st.logs.length})', () => setState(() => _rt = 2))),
  ]);
  final pane = _rt == 0 ? _wP(c, st) : (_rt == 1 ? _pP(c, st) : _lP(c, st));
  return Column(spacing: 8, children: [tabs, Expanded(child: pane)]);
 }
 Widget _wTag(BuildContext c, DirectEntry w) {
  final cs = c.colorScheme, ntf = ref.read(guardianProvider.notifier);
  final box = Container(padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4), decoration: _rb(cs.successContainer, 8), child: _tx(c, '✓ ${w.label} ×', cap: true, b: true, col: cs.onSuccessContainer));
  return GestureDetector(onTap: () => unawaited(ntf.rmDir(w.id)), child: box);
 }
 Widget _appRow(BuildContext c, InstalledApp a) {
  final cs = c.colorScheme, ntf = ref.read(guardianProvider.notifier), on = ntf.isDir(a.pkg, '', a.pkg);
  final bg = on ? cs.successContainer.withValues(alpha: 0.5) : _fg(c).withValues(alpha: 0.065);
  final info = Column(crossAxisAlignment: CrossAxisAlignment.start, children: [_tx(c, a.label, b: true), _tx(c, a.pkg, cap: true)]);
  final row = Row(children: [Expanded(child: info), _tx(c, on ? '✓ 直连放通' : '设为直连', cap: true, b: true, col: on ? cs.onSuccessContainer : _fg(c))]);
  final box = Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: _rb(bg, 10), child: row);
  return GestureDetector(onTap: () => unawaited(ntf.togDir(label: a.label, exe: a.pkg, pkg: a.pkg)), child: box);
 }
 Widget _procPickRow(BuildContext c, ProcStat p) {
  final cs = c.colorScheme, ntf = ref.read(guardianProvider.notifier);
  final bg = p.direct ? cs.successContainer.withValues(alpha: 0.5) : _fg(c).withValues(alpha: 0.065);
  final info = Column(crossAxisAlignment: CrossAxisAlignment.start, children: [_tx(c, p.name, b: true), _tx(c, p.path.isNotEmpty ? p.path : p.rawExe, cap: true)]);
  final row = Row(children: [Expanded(child: info), _tx(c, p.direct ? '✓ 已直连放通' : '设为直连放通', cap: true, b: true, col: p.direct ? cs.onSuccessContainer : _fg(c))]);
  final box = Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: _rb(bg, 10), child: row);
  return GestureDetector(onTap: () => unawaited(ntf.togDir(label: p.name, exe: p.rawExe, path: p.path, pkg: p.pkg)), child: box);
 }
 Widget _wP(BuildContext c, GuardianState st) {
  final ntf = ref.read(guardianProvider.notifier), q = _aq.trim().toLowerCase();
  final hint = Platform.isAndroid ? '输入包名(如 com.tencent.mm)...' : '输入进程名(如 WeChat.exe)或应用目录...';
  final addBtn = FilledButton(onPressed: _wq.trim().isEmpty ? null : () { final v = _wq; _wc.clear(); setState(() => _wq = ''); unawaited(ntf.addDir(v)); }, child: const Text('+ 添加直连'));
  final addRow = Row(spacing: 8, children: [Expanded(child: _sch(c, _wc, _wf, hint, _wq, (v) => setState(() => _wq = v))), addBtn]);
  final tagsWrap = Wrap(spacing: 6, runSpacing: 6, children: [for (final w in st.wl) _wTag(c, w)]);
  final tagsBox = ConstrainedBox(constraints: const BoxConstraints(maxHeight: 84), child: SingleChildScrollView(child: tagsWrap));
  final preChips = [for (final (l, ex) in GuardianNotifier.presets) _ch(c, ntf.isDir(ex, '', ''), ntf.isDir(ex, '', '') ? '✓ $l' : '+ $l', () => unawaited(ntf.togDir(label: l, exe: ex)))];
  final preBar = SingleChildScrollView(scrollDirection: Axis.horizontal, child: Row(spacing: 6, children: preChips));
  final sHint = Platform.isAndroid ? '搜索本机应用勾选直连放通...' : '搜索活跃进程一键设为直连...';
  final sRow = Row(spacing: 8, children: [
   Expanded(child: _sch(c, _ac, _af, sHint, _aq, (v) => setState(() => _aq = v))),
   if (Platform.isAndroid) TextButton(onPressed: () => unawaited(ntf.ldApps()), child: const Text('刷新应用')),
  ]);
  final apps = q.isEmpty ? st.apps : st.apps.where((a) => a.label.toLowerCase().contains(q) || a.pkg.toLowerCase().contains(q)).toList();
  final procs = st.procs.where((p) => p.rawExe.isNotEmpty && (q.isEmpty || p.name.toLowerCase().contains(q) || p.path.toLowerCase().contains(q))).toList();
  final list = Platform.isAndroid
    ? _lv(c, apps, '点击「刷新应用」读取本机应用或在上方输入包名', (a) => _appRow(c, a))
    : _lv(c, procs, '开启代理后产生流量的本地进程及目录会自动列出，也可点击上方常用软件或输入目录添加', (p) => _procPickRow(c, p));
  return _cd(c, [_tx(c, '直连放通白名单 · 已放通应用的进程/子进程/线程流量直连不走代理', b: true), addRow, if (st.wl.isNotEmpty) tagsBox, if (!Platform.isAndroid) preBar, sRow, list]);
 }
 Widget _ipRow(BuildContext c, GuardianState st, RegionIpOpt o) {
  final cs = c.colorScheme, ntf = ref.read(guardianProvider.notifier);
  final ips = o.ip.isNotEmpty ? o.ip : (o.raw.isNotEmpty ? o.raw : '点击切换解析 IP');
  final dl = o.ms > 0 ? '${o.ms}ms' : (o.ms < 0 ? '超时' : '待测');
  final bg = o.sel ? cs.successContainer.withValues(alpha: 0.55) : _fg(c).withValues(alpha: 0.065);
  final stClr = o.ms < 0 ? cs.onErrorContainer : (o.sel ? cs.onSuccessContainer : _fg(c));
  final top = Row(children: [
   Expanded(child: _tx(c, 'IP: $ips', b: true, col: o.sel ? cs.onSuccessContainer : _fg(c))),
   _tx(c, '$dl · ${o.sel ? "✓ 当前选中" : (o.sticky ? "本区记忆" : "点击固定")}', cap: true, b: true, col: stClr),
  ]);
  final sub = _tx(c, '线路: ${o.node}${o.s24 != null ? " · 网段: ${o.s24}" : ""}', cap: true);
  final col = Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: [top, sub]);
  final box = Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: _rb(bg, 10), child: col);
  return GestureDetector(onTap: () => unawaited(ntf.pickNode(st.grp, o.node)), child: box);
 }
 Widget _ipP(BuildContext c, GuardianState st) {
  final ntf = ref.read(guardianProvider.notifier), q = _iq.trim().toLowerCase();
  final l = q.isEmpty ? st.opts : st.opts.where((o) => o.ip.toLowerCase().contains(q) || o.raw.toLowerCase().contains(q) || o.node.toLowerCase().contains(q) || (o.s24?.toLowerCase().contains(q) ?? false)).toList();
  final hdr = Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
   Expanded(child: _tx(c, '${st.regLbl.isEmpty ? "当前区域" : st.regLbl} · 全部可选 IP (${st.opts.length})', b: true)),
   TextButton(onPressed: st.busy ? null : () => unawaited(ntf.probReg()), child: Text(st.busy ? '测速中...' : '测速本区IP')),
  ]);
  final sch = _sch(c, _ic, _if, '搜索本区 IP / 网段 / 线路名...', _iq, (v) => setState(() => _iq = v));
  return _cd(c, [hdr, sch, _lv(c, l, st.regs.isEmpty ? '导入订阅后自动展示区域全部 IP' : '无匹配 IP', (o) => _ipRow(c, st, o))]);
 }
 Widget _pRow(BuildContext c, ProcStat p, int tot) {
  final cs = c.colorScheme, ntf = ref.read(guardianProvider.notifier), sum = p.up + p.dn;
  final bg = p.direct ? cs.successContainer.withValues(alpha: 0.35) : _fg(c).withValues(alpha: 0.065);
  final dBg = p.direct ? cs.successContainer : _fg(c).withValues(alpha: 0.1);
  final dTag = Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3), decoration: _rb(dBg, 7), child: _tx(c, p.direct ? '✓直连' : '直连放通', cap: true, b: true, col: p.direct ? cs.onSuccessContainer : _fg(c)));
  final dBtn = GestureDetector(onTap: () => unawaited(ntf.togDir(label: p.name, exe: p.rawExe, path: p.path, pkg: p.pkg)), child: dTag);
  final top = Row(spacing: 8, children: [
   Expanded(child: _tx(c, '${p.name} (${p.conns}连接 · ${p.exit.isEmpty ? "GLOBAL" : p.exit})', b: true)),
   _tx(c, '↑${fmtRate(p.upR)} ↓${fmtRate(p.dnR)}', cap: true, b: true),
   if (p.rawExe.isNotEmpty || p.pkg.isNotEmpty) dBtn,
  ]);
  final mid = Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [_tx(c, '累计 ↑${fmtBytes(p.up)} · ↓${fmtBytes(p.dn)}', cap: true), _tx(c, '总计 ${fmtBytes(sum)}', cap: true, b: true)]);
  final fill = FractionallySizedBox(alignment: Alignment.centerLeft, widthFactor: (sum / tot).clamp(0.0, 1.0), child: Container(decoration: _rb(cs.onSuccessContainer, 2)));
  final bar = Container(height: 4, width: double.infinity, decoration: _rb(_fg(c).withValues(alpha: 0.08), 2), child: fill);
  return Container(padding: const EdgeInsets.all(10), decoration: _rb(bg, 10), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 4, children: [top, mid, bar]));
 }
 Widget _pP(BuildContext c, GuardianState st) {
  final ntf = ref.read(guardianProvider.notifier), q = _pq.trim().toLowerCase(), tot = st.tot <= 0 ? 1 : st.tot;
  final l = q.isEmpty ? st.procs : st.procs.where((p) => p.name.toLowerCase().contains(q) || p.exit.toLowerCase().contains(q)).toList();
  final hdr = Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Expanded(child: _tx(c, '进程流量 · ↑${fmtBytes(st.up)} / ↓${fmtBytes(st.dn)}', b: true)), TextButton(onPressed: ntf.rstTrf, child: const Text('清零'))]);
  return _cd(c, [hdr, _sch(c, _pc, _pf, '搜索进程名 / 包名 / 出口...', _pq, (v) => setState(() => _pq = v)), _lv(c, l, '开启全局接管后实时显示各进程上下行并支持一键直连', (p) => _pRow(c, p, tot))]);
 }
 Widget _lRow(BuildContext c, LogItem e) {
  final cs = c.colorScheme;
  final bg = e.hot ? cs.successContainer.withValues(alpha: 0.45) : _fg(c).withValues(alpha: 0.065);
  final det = Text(e.detail, style: AppTextStyle.caption1.of(c).copyWith(color: _mu(c)));
  final col = Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: [_tx(c, '[${fmtTime(e.time)}][${e.cat.label}] ${e.title}', cap: true, b: true), det]);
  return Container(padding: const EdgeInsets.all(8), decoration: _rb(bg, 10), child: col);
 }
 Widget _lP(BuildContext c, GuardianState st) {
  final ntf = ref.read(guardianProvider.notifier), q = _lq.trim().toLowerCase();
  final l = st.logs.where((e) => (_cat == null || e.cat == _cat) && (q.isEmpty || e.title.toLowerCase().contains(q) || e.detail.toLowerCase().contains(q))).toList();
  void copyAll() => unawaited(Clipboard.setData(ClipboardData(text: l.map((e) => '[${fmtTime(e.time)}][${e.cat.label}] ${e.title} | ${e.detail}').join('\n'))));
  final btns = Row(mainAxisSize: MainAxisSize.min, children: [TextButton(onPressed: l.isEmpty ? null : copyAll, child: const Text('复制')), TextButton(onPressed: ntf.clrLog, child: const Text('清空'))]);
  final hdr = Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [_tx(c, '明确清晰运行日志', b: true), btns]);
  final cats = Wrap(spacing: 6, runSpacing: 6, children: [_ch(c, _cat == null, '全部', () => setState(() => _cat = null)), for (final ct in LogCat.values) _ch(c, _cat == ct, ct.label, () => setState(() => _cat = ct))]);
  return _cd(c, [hdr, cats, _sch(c, _lc, _lf, '筛选节点名、IP段、直连进程或告警...', _lq, (v) => setState(() => _lq = v)), _lv(c, l, '暂无日志', (e) => _lRow(c, e))]);
 }
}
