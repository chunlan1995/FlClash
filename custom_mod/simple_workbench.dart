// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import 'dart:async'; import 'package:fl_clash/common/common.dart'; import 'package:fl_clash/ui/icons/icons.dart'; import 'package:fl_clash/views/profiles/add.dart';
import 'package:fl_clash/widgets/widgets.dart'; import 'package:flutter/services.dart'; import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart'; import 'package:prism_ui/prism_ui.dart'; import 'flclash_bridge.dart'; import 'smart_guardian.dart';
class SimpleModeHost extends ConsumerWidget { const SimpleModeHost({super.key, required this.originalChild}); final Widget originalChild; @override
Widget build(BuildContext context, WidgetRef ref) { ref.watch(guardianProvider.select((s) => s.autoSwitch)); final simple = ref.watch(simpleModeProvider);
return Stack(children: [ Offstage(offstage: simple, child: originalChild), if (simple) const Positioned.fill(child: SimpleWorkbenchView())
else Positioned(right: 18, bottom: 20, child: SafeArea(child: FilledButton.tonal(onPressed: () => ref.read(simpleModeProvider.notifier).setMode(true), child: const Text('返回极简模式')))),
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
targetBuilder: (open) => FilledButton.tonal(onPressed: open, child: Text('订阅: ${curP?.label ?? "选择"} ▾')),
popupBuilder: (_) => PopupMenu(items: [for (final p in profs) PopupMenuItem(glyph: p.selected ? AppGlyphs.check : null, label: p.label, onPressed: p.onSelect)]), ),
AddProfileMenu(builder: (open) => FilledButton.tonal(onPressed: open, child: const Text('+ 导入订阅'))),
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
targetBuilder: (open) => FilledButton.tonal(onPressed: open, child: Text('阈值 ${st.limitMs}ms ▾')),
popupBuilder: (_) => PopupMenu(items: [for (final ms in const [600, 800, 1000, 1500]) PopupMenuItem(glyph: st.limitMs == ms ? AppGlyphs.check : null, label: ms == 1000 ? '1000ms (默认)' : '${ms}ms', onPressed: () => ref.read(guardianProvider.notifier).setLimit(ms))]),
), TextButton(onPressed: st.probing ? null : () => unawaited(ref.read(guardianProvider.notifier).manualCheck()), child: Text(st.probing ? '探测中...' : '立即测速择优')),
if (grp != null) PopupAnchor( targetBuilder: (open) => FilledButton.tonal(onPressed: open, child: const Text('手动选节点 ▾')),
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
