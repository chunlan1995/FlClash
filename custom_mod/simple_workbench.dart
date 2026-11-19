// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import 'dart:async';import 'dart:io';import 'dart:math' as math;import 'package:fl_clash/ui/icons/icons.dart';import 'package:fl_clash/views/profiles/add.dart';import 'package:fl_clash/widgets/widgets.dart';
import 'package:flutter/services.dart';import 'package:flutter/widgets.dart';import 'package:flutter_riverpod/flutter_riverpod.dart';import 'package:prism_ui/prism_ui.dart';import 'flclash_bridge.dart';import 'smart_guardian.dart';
part 'simple_workbench_cards.dart';
const _cB = Color(0xFF2563EB);const _cP = Color(0xFF10B981);const _cD = Color(0xFF0EA5E9);const _cV = Color(0xFF8B5CF6);const _cW = Color(0xFFD97706);const _cN = Color(0xFF64748B);const _cWht = Color(0xFFFFFFFF);
const _vendorExitOpts = <String>['US','JP','SG','HK','TW','KR','FOLLOW']; const _browserExitOpts = <String>['SG','HK','TW','JP','KR','US','GB','DE','FR','NL','CA','AU','FOLLOW'];
const _subExitOpts = <String>['US','JP','SG','HK','TW','KR','DIRECT']; bool _isCust(VendorSpec v) => v.id.startsWith('custom_'); bool _isDel(VendorSpec v) => v.id.startsWith('custom_grp_');
class SimpleModeHost extends ConsumerWidget { const SimpleModeHost({super.key, required this.originalChild}); final Widget originalChild; @override Widget build(BuildContext context, WidgetRef ref) {
try { ref.watch(guardianProvider.select((s) => s.auto)); } catch (_) {} final simple = ref.watch(simpleModeProvider); final cs = context.colorScheme; final width = MediaQuery.sizeOf(context).width;
final topOff = width < 600 ? 11.0 : 10.0; final rightOff = width < 600 ? 106.0 : 148.0; return Stack(children: <Widget>[ Offstage(offstage: simple, child: originalChild),
if (simple) const Positioned.fill(child: SimpleWorkbenchView()), if (!simple) Positioned( top: topOff, right: rightOff, child: SafeArea( bottom: false, child: GestureDetector(
onTap: () => unawaited(ref.read(guardianProvider.notifier).setUi(true)), child: Container( padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 6), decoration: ShapeDecoration(
color: SurfaceLevel.page.colorOf(cs).withValues(alpha: 0.94), shape: RoundedSuperellipseBorder( borderRadius: BorderRadius.circular(99), side: BorderSide(color: _cB.withValues(alpha: 0.55), width: 1.1), ),
shadows: <BoxShadow>[BoxShadow(color: _cB.withValues(alpha: 0.14), blurRadius: 8, offset: const Offset(0, 2))], ), child: Text( '⚡ 返回极简台', style: AppTextStyle.caption1.of(context, emphasized: true).copyWith(color: _cB), ), ), ),
), ), ]); } } class _WavePainter extends CustomPainter { const _WavePainter({required this.points, required this.showFallback, required this.gridColor}); final List<WavePt> points;final bool showFallback;final Color gridColor;
void _drawTrack(Canvas canvas, Size size, List<int> vals, double maxV, Color color) { if (vals.length < 2) return; final path = Path();final h = size.height;final w = size.width; double xAt(int i) => (i / (vals.length - 1)) * w;
double yAt(int i) => h - 6 - ((vals[i] / maxV).clamp(0.0, 1.0) * (h - 14)); path.moveTo(xAt(0), yAt(0)); for (var i = 1; i < vals.length; i++) {
final x0 = xAt(i - 1);final y0 = yAt(i - 1);final x1 = xAt(i);final y1 = yAt(i);final cx = (x0 + x1) * 0.5; path.cubicTo(cx, y0, cx, y1, x1, y1); }
final stroke = Paint()..color = color..style = PaintingStyle.stroke..strokeWidth = 2.1..strokeCap = StrokeCap.round; canvas.drawPath(path, stroke); final fillPath = Path.from(path)..lineTo(w, h)..lineTo(0, h)..close();
final shader = LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: <Color>[color.withValues(alpha: 0.22), color.withValues(alpha: 0.0)]).createShader(Rect.fromLTWH(0, 0, w, h));
canvas.drawPath(fillPath, Paint()..shader = shader); } @override void paint(Canvas canvas, Size size) { final gp = Paint()..color = gridColor..strokeWidth = 1.0;
for (var i = 1; i <= 2; i++) { final y = (size.height / 3.0) * i; canvas.drawLine(Offset(0, y), Offset(size.width, y), gp); } var peak = 64 * 1024;
for (final p in points) { peak = math.max(peak, math.max(p.vBps, math.max(showFallback ? p.fBps : 0, p.dBps))); } final maxV = peak * 1.15; _drawTrack(canvas, size, <int>[for (final p in points) p.dBps], maxV, _cD);
if (showFallback) _drawTrack(canvas, size, <int>[for (final p in points) p.fBps], maxV, _cP); _drawTrack(canvas, size, <int>[for (final p in points) p.vBps], maxV, _cV); } @override
bool shouldRepaint(covariant _WavePainter old) => true; } class SimpleWorkbenchView extends ConsumerStatefulWidget { const SimpleWorkbenchView({super.key}); @override
ConsumerState<SimpleWorkbenchView> createState() => _SimpleWorkbenchState(); } class _SimpleWorkbenchState extends ConsumerState<SimpleWorkbenchView> {
final _ipCtrl = TextEditingController();final _vSC = TextEditingController();final _cDomCtrl = TextEditingController();
final _bAddCtrl = TextEditingController();final _wAddCtrl = TextEditingController();final _aSC = TextEditingController(); final _ngNameCtrl = TextEditingController();final _ngBadgeCtrl = TextEditingController(text: '自');
final _grpAppCtrl = TextEditingController();final _rnCtrl = TextEditingController(); final _ipFocus = FocusNode();final _vSF = FocusNode();final _cDomFocus = FocusNode();
final _bAddFocus = FocusNode();final _wAddFocus = FocusNode();final _aSF = FocusNode(); final _ngNameFocus = FocusNode();final _ngBadgeFocus = FocusNode();final _grpAppFocus = FocusNode();final _rnFocus = FocusNode();
bool _busy = false;bool _vTl = false;bool _bAddOpen = false;bool _addAppOpen = false;bool _aPk = false;bool _rPv = false;bool _newGrpOpen = false;
String _ipQ = '';String _vQ = '';String _cDom = '';String _bIn = '';String _wIn = '';String _appQ = ''; String _ngName = '';String _ngBadge = '自';String _ngExit = 'SG';
String _openAddCatId = 'custom_default';String _grpAppIn = '';String _renamingCatId = '';String _rnIn = ''; String _customExit = 'US';String _newBrowserExit = 'SG';String _targetVendorId = 'custom_default';LogCat? _logCat;
void _upd(VoidCallback fn) { if (mounted) setState(fn); } @override void dispose() {
for (final c in <TextEditingController>[_ipCtrl,_vSC,_cDomCtrl,_bAddCtrl,_wAddCtrl,_aSC,_ngNameCtrl,_ngBadgeCtrl,_grpAppCtrl,_rnCtrl]) { c.dispose(); }
for (final f in <FocusNode>[_ipFocus,_vSF,_cDomFocus,_bAddFocus,_wAddFocus,_aSF,_ngNameFocus,_ngBadgeFocus,_grpAppFocus,_rnFocus]) { f.dispose(); } super.dispose(); } Future<void> _toggleRun(bool run) async { if (_busy) return;
setState(() => _busy = true); try { await ref.read(guardianProvider.notifier).togRun(run); } finally { if (mounted) setState(() => _busy = false); } }
Color _fg(BuildContext c) => DefaultTextStyle.of(c).style.color ?? const Color(0xFF0F172A); Color _mu(BuildContext c) => _fg(c).withValues(alpha: 0.58); Color _cardBg(BuildContext c) => _fg(c).withValues(alpha: 0.042);
Color _subBg(BuildContext c) => _fg(c).withValues(alpha: 0.068); ShapeDecoration _rBox(Color bg, double r, {Color? border}) => ShapeDecoration( color: bg,
shape: RoundedSuperellipseBorder(borderRadius: BorderRadius.circular(r < 1 ? 1 : r), side: border != null ? BorderSide(color: border, width: 1) : BorderSide.none), );
Widget _txt(BuildContext c, String s, {bool b = false, bool cap = false, Color? col, int maxLines = 1}) { final st = cap ? AppTextStyle.caption1.of(c, emphasized: b) : AppTextStyle.subheadline.of(c, emphasized: b);
return Text(s, maxLines: maxLines, overflow: TextOverflow.ellipsis, style: st.copyWith(color: col ?? (cap && !b ? _mu(c) : _fg(c)))); } Widget _badge(BuildContext c, String text, Color accent) => Container(
padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3), decoration: _rBox(accent.withValues(alpha: 0.14), 99), child: Text(text, style: AppTextStyle.caption1.of(c, emphasized: true).copyWith(color: accent)), );
Widget _pBtn(BuildContext c, String label, VoidCallback? onTap, {bool active = false, Color? activeColor}) { final ac = activeColor ?? _cB; return GestureDetector( onTap: onTap, child: Container(
padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5), decoration: _rBox(active ? ac.withValues(alpha: 0.15) : _subBg(c), 99, border: active ? ac.withValues(alpha: 0.5) : null),
child: Text(label, style: AppTextStyle.caption1.of(c, emphasized: true).copyWith(color: active ? ac : _fg(c).withValues(alpha: onTap == null ? 0.38 : 0.86))), ), ); }
Widget _sw(bool value, Color activeColor, VoidCallback onTap) => GestureDetector( onTap: onTap, child: AnimatedContainer( duration: const Duration(milliseconds: 170), width: 40, height: 23, padding: const EdgeInsets.all(2.5),
alignment: value ? Alignment.centerRight : Alignment.centerLeft, decoration: _rBox(value ? activeColor : const Color(0xFF94A3B8).withValues(alpha: 0.38), 99), child: Container(width: 18, height: 18, decoration: _rBox(_cWht, 99)),
), ); Widget _inp(BuildContext c, TextEditingController tc, FocusNode fn, String hint, String val, ValueChanged<String> onChanged) { final fg = _fg(c); return GestureDetector( onTap: fn.requestFocus, child: Container(
padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 7), decoration: _rBox(_subBg(c), 11, border: _fg(c).withValues(alpha: 0.10)), child: Row(spacing: 8, children: <Widget>[
Expanded(child: Stack(alignment: Alignment.centerLeft, children: <Widget>[ if (val.isEmpty) _txt(c, hint, cap: true, col: _mu(c)),
EditableText(controller: tc, focusNode: fn, autocorrect: false, onChanged: onChanged, style: AppTextStyle.subheadline.of(c).copyWith(color: fg), cursorColor: fg, backgroundCursorColor: _mu(c)), ])),
if (val.isNotEmpty) GestureDetector(onTap: () { tc.clear(); onChanged(''); }, child: Text('×', style: AppTextStyle.body.of(c, emphasized: true).copyWith(color: _mu(c)))), ]), ), ); }
Widget _exPill(BuildContext c, String currentCode, List<String> codes, ValueChanged<String> onPick, {bool active = false, Color? activeColor}) => PopupAnchor(
targetBuilder: (open) => _pBtn(c, '${FlClashBridge.regLblOf(currentCode)} ▾', open, active: active, activeColor: activeColor), popupBuilder: (_) => PopupMenu(items: <PopupMenuItem>[
for (final code in codes) PopupMenuItem(glyph: code == currentCode ? AppGlyphs.check : null, label: FlClashBridge.regLblOf(code), onPressed: () => onPick(code)), ]), );
Widget _buildFallbackDispatchPopup(GuardianState st, {required String label, required String exe, required String path, required String pkg, required bool fixedDirect}) { final ntf = ref.read(guardianProvider.notifier);
final bSlot = FlClashBridge.findCandidateBrowserSlot(exe, path, pkg); final custCats = st.vendors.where(_isCust).toList(); final builtinCats = st.vendors.where((v) => !_isCust(v)).toList(); return PopupMenu(items: <PopupMenuItem>[
for (final cv in custCats) PopupMenuItem( label: '🧩 投送至「${cv.name}」(${FlClashBridge.regLblOf(cv.defEx).split(" ").last})',
onPressed: () => unawaited(ntf.dispatchToVendor(vendorId: cv.id, label: label, exe: exe, path: path, pkg: pkg)), ), PopupMenuItem( label: '✨ + 新建自定义分组并投送...', onPressed: () async { final baseLbl = label.split(' ').first;
final gid = await ntf.createCustomGroup(name: '$baseLbl 专享组', badge: baseLbl, exitCode: 'SG'); await ntf.dispatchToVendor(vendorId: gid, label: label, exe: exe, path: path, pkg: pkg); }, ), if (bSlot != null) ...<PopupMenuItem>[
for (final rc in const <String>['SG', 'HK', 'US', 'JP', 'TW']) PopupMenuItem( label: '🌐 开启「${bSlot.name}」专享代理 → ${FlClashBridge.regLblOf(rc)}',
onPressed: () => unawaited(ntf.enableBrowserForFallbackProc(label: label, exitCode: rc, exe: exe, path: path, pkg: pkg)), ), ], for (final v in builtinCats) PopupMenuItem(
label: '🏢 投送至 ${v.name} (${FlClashBridge.regLblOf(v.defEx).split(" ").last})', onPressed: () => unawaited(ntf.dispatchToVendor(vendorId: v.id, label: label, exe: exe, path: path, pkg: pkg)), ),
for (final rc in const <String>['SG', 'HK', 'US', 'JP']) if (bSlot == null) PopupMenuItem( label: '🌐 独立整包锁定 → ${FlClashBridge.regLblOf(rc)}',
onPressed: () => unawaited(ntf.setStandaloneAppProxy(label: label, exitCode: rc, exe: exe, path: path, pkg: pkg)), ), PopupMenuItem( label: '🌐 独立代理 · 走主干出口',
onPressed: () => unawaited(ntf.setStandaloneAppProxy(label: label, exitCode: 'FOLLOW', exe: exe, path: path, pkg: pkg)), ), if (!st.fbDir && !fixedDirect) PopupMenuItem( label: '🛡 锁定兜底物理直连 (不走代理)',
onPressed: () => unawaited(ntf.moveAppToFallback(label: label, exe: exe, path: path, pkg: pkg, forceDirectBypass: true)), ), if (fixedDirect) PopupMenuItem( label: '↩ 取消固定直连 (恢复默认兜底)',
onPressed: () => unawaited(ntf.moveAppToFallback(label: label, exe: exe, path: path, pkg: pkg)), ), ]); }
Widget _dispatchMenuForFallback(BuildContext c, GuardianState st, {required String label, required String exe, required String path, required String pkg, required bool fixedDirect, String btnText = '🎯 投送代理 ▾'}) => PopupAnchor(
targetBuilder: (open) => _pBtn(c, btnText, open, active: true, activeColor: _cB), popupBuilder: (_) => _buildFallbackDispatchPopup(st, label: label, exe: exe, path: path, pkg: pkg, fixedDirect: fixedDirect), );
Widget _manageMenuForProxied(BuildContext c, GuardianState st, ProcStat p) { final ntf = ref.read(guardianProvider.notifier); final isComp = p.companionId.isNotEmpty; final isBrowser = !isComp && p.browserId.isNotEmpty;
final isCustV = !isComp && !isBrowser && p.vendorId.startsWith('custom_'); final bItem = isBrowser ? st.browserEnvs.where((x) => x.id == p.browserId).firstOrNull : null; final custCats = st.vendors.where(_isCust).toList();
final builtinCats = st.vendors.where((v) => !_isCust(v)).toList(); final btnLabel = isComp ? '🧬 伴生 · 调整 ▾' : (isBrowser ? '🌐 专享地区 · 调整 ▾' : (isCustV ? '🧩 自定义分类 · 调整 ▾' : (p.dispatched ? '📌 已投送 · 调整 ▾' : '⚙️ 调整 / 移至兜底 ▾')));
final btnCol = isComp ? _cP : (isBrowser ? _cD : (isCustV ? _cW : _cV)); return PopupAnchor( targetBuilder: (open) => _pBtn(c, btnLabel, open, active: p.dispatched || isBrowser || isComp || isCustV, activeColor: btnCol),
popupBuilder: (_) => PopupMenu(items: <PopupMenuItem>[ if (isComp) ...<PopupMenuItem>[ PopupMenuItem(label: '🛡 移出伴生白名单并锁定直连 (不再自动纳管)', onPressed: () => unawaited(ntf.rmCompanionRule(p.companionId, pinDirect: true))),
PopupMenuItem(label: '× 仅删除此条伴生白名单记录', onPressed: () => unawaited(ntf.rmCompanionRule(p.companionId))), ] else PopupMenuItem( label: isBrowser ? '↩ 关闭专享浏览器代理 (移回兜底)' : '↩ 移回兜底分类 (解除代理保存记录)',
onPressed: () => unawaited(ntf.moveAppToFallback(label: p.name, browserId: p.browserId, companionId: p.companionId, exe: p.rawExe, path: p.path, pkg: p.pkg)), ), if (isBrowser && bItem != null)
for (final rc in _browserExitOpts) PopupMenuItem(glyph: bItem.exit == rc ? AppGlyphs.check : null, label: '🌐 切换专享出口 → ${FlClashBridge.regLblOf(rc)}', onPressed: () => unawaited(ntf.setBrowserEnvExit(bItem.id, rc)))
else ...<PopupMenuItem>[
for (final cv in custCats) PopupMenuItem(glyph: p.vendorId == cv.id ? AppGlyphs.check : null, label: '🧩 改投至「${cv.name}」(${FlClashBridge.regLblOf(cv.defEx).split(" ").last})', onPressed: () => unawaited(ntf.dispatchToVendor(vendorId: cv.id, label: p.name, exe: p.rawExe, path: p.path, pkg: p.pkg))),
for (final v in builtinCats) PopupMenuItem(glyph: p.vendorId == v.id ? AppGlyphs.check : null, label: '🏢 改投至 ${v.name} (${FlClashBridge.regLblOf(v.defEx).split(" ").last})', onPressed: () => unawaited(ntf.dispatchToVendor(vendorId: v.id, label: p.name, exe: p.rawExe, path: p.path, pkg: p.pkg))),
], ]), ); } Widget _hdr(BuildContext c, GuardianState st, bool run, bool isDesktop, List<BridgeProfile> profs) { final ntf = ref.read(guardianProvider.notifier); final curP = profs.where((p) => p.selected).firstOrNull;
return Container( padding: EdgeInsets.symmetric(horizontal: isDesktop ? 18 : 14, vertical: 10), color: _fg(c).withValues(alpha: 0.025),
child: Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 6, children: <Widget>[ Row(mainAxisSize: MainAxisSize.min, spacing: 9, children: <Widget>[
Container(width: 30, height: 30, alignment: Alignment.center, decoration: _rBox(_cB, 9), child: Text('B', style: AppTextStyle.subheadline.of(c, emphasized: true).copyWith(color: _cWht))),
Text('${FlClashBridge.brandName} v${FlClashBridge.appVersion}', style: AppTextStyle.headline.of(c, emphasized: true)), if (curP != null) PopupAnchor( targetBuilder: (open) => _pBtn(c, '${curP.label} ▾', open),
popupBuilder: (_) => PopupMenu(items: <PopupMenuItem>[for (final p in profs) PopupMenuItem(glyph: p.selected ? AppGlyphs.check : null, label: p.label, onPressed: p.onSelect)]), ), if (st.syncing) _badge(c, '同步规则中', _cB), ]),
Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[ AddProfileMenu(builder: (open) => _pBtn(c, '+ 订阅', open)),
_pBtn(c, '完整原版 ↗', () => unawaited(ntf.setUi(false)), active: true, activeColor: _cB),
if (isDesktop) FilledButton(onPressed: _busy ? null : () => _toggleRun(run), child: Text(_busy ? '切换中...' : (run ? '● 运行中 ${fmtDur(st.runSec)}' : '▶ 开启接管'))), ]), ]), ); } @override Widget build(BuildContext context) {
final cs = context.colorScheme; try { final st = ref.watch(guardianProvider); final ntf = ref.read(guardianProvider.notifier); final run = FlClashBridge.watchRunning(ref); final sysPx = FlClashBridge.watchSystemProxy(ref);
final tunOn = FlClashBridge.watchTunEnabled(ref); final profs = FlClashBridge.watchProfiles(ref); return Surface( color: SurfaceLevel.page.colorOf(cs), child: SafeArea( child: LayoutBuilder(builder: (ctx, box) {
final isDesktop = box.maxWidth >= 820; final isCompact = box.maxWidth < 560; final cockpit = isDesktop
? Row(crossAxisAlignment: CrossAxisAlignment.start, spacing: 12, children: <Widget>[Expanded(flex: 11, child: _tCard(ctx, st, run, sysPx, tunOn)), Expanded(flex: 10, child: _fCard(ctx, st))])
: Column(spacing: 12, children: <Widget>[_tCard(ctx, st, run, sysPx, tunOn), _fCard(ctx, st)]); final quietFooter = Padding( padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
child: Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 6, children: <Widget>[ _txt(ctx, 'BlueClash 全进程树守护 · 支持自定义分类整包代理、主进程线程与伴生子进程白名单自动继承', cap: true),
Wrap(spacing: 6, children: <Widget>[ _pBtn(ctx, '全部展开', () => ntf.setAllDrw(true)), _pBtn(ctx, '仅看座舱', () => ntf.setAllDrw(false)), _pBtn(ctx, '恢复默认布局', () => unawaited(ntf.rstLay())), ]), ]), ); return Column(children: <Widget>[
_hdr(ctx, st, run, isDesktop, profs), Expanded(child: Align(alignment: Alignment.topCenter, child: ConstrainedBox( constraints: const BoxConstraints(maxWidth: 1060), child: SingleChildScrollView(
padding: EdgeInsets.fromLTRB(isDesktop ? 18 : 12, 8, isDesktop ? 18 : 12, 18), child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, spacing: 12, children: <Widget>[
cockpit, _bDrw(ctx, st, isCompact), _vDrw(ctx, st, isCompact), _aDrw(ctx, st, isCompact), _lDrw(ctx, st), quietFooter, ]), ), ))), if (!isDesktop) _mBar(ctx, st, run), ]); }), ), ); } catch (err) {
return Surface(color: SurfaceLevel.page.colorOf(cs), child: SafeArea(child: Center(child: Padding(padding: const EdgeInsets.all(20), child: Column(mainAxisSize: MainAxisSize.min, spacing: 12, children: <Widget>[
Text('BlueClash 界面渲染异常: $err', style: AppTextStyle.subheadline.of(context, emphasized: true)), FilledButton(onPressed: () => ref.read(simpleModeProvider.notifier).setMode(false), child: const Text('切回完整原版面板')), ]))))); } } }
