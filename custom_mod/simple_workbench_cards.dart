// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
part of 'simple_workbench.dart'; extension _SimpleWorkbenchCardsExt on _SimpleWorkbenchState { Widget _tCard(BuildContext c, GuardianState st, bool run, bool sysPx, bool tunOn) { final ntf = ref.read(guardianProvider.notifier);
final probeStr = !run ? '--' : (st.ms < 0 ? '超时' : (st.ms == 0 ? '待测' : '${st.ms} ms')); final probeBad = run && (st.ms < 0 || st.ms >= st.lim);
Widget dotLeg(String lbl, Color col, double op) => Opacity(opacity: op, child: Row(mainAxisSize: MainAxisSize.min, spacing: 4, children: <Widget>[Container(width: 7, height: 7, decoration: _rBox(col, 99)), _txt(c, lbl, cap: true)]));
return Container( padding: const EdgeInsets.all(15), decoration: _rBox(_cardBg(c), 20, border: _fg(c).withValues(alpha: 0.07)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 10, children: <Widget>[
Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 10, runSpacing: 6, children: <Widget>[
Row(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.end, spacing: 12, children: <Widget>[ Text('↓ ${fmtRate(st.dnR)}', style: AppTextStyle.title2.of(c, emphasized: true)),
_txt(c, '↑ ${fmtRate(st.upR)}', cap: true, b: true), ]), Wrap(spacing: 8, children: <Widget>[dotLeg('被代理(含自定义/伴生)', _cV, 1.0), dotLeg('兜底代理', _cP, st.fbDir ? 0.35 : 1.0), dotLeg('物理直连', _cD, 1.0)]), ]),
SizedBox(height: 98, width: double.infinity, child: CustomPaint(painter: _WavePainter(points: st.wave, showFallback: !st.fbDir, gridColor: _fg(c).withValues(alpha: 0.06)))),
Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 6, children: <Widget>[
Row(mainAxisSize: MainAxisSize.min, spacing: 6, children: <Widget>[_txt(c, '代理 ${fmtBytes(st.pxB)} · 直连 ${fmtBytes(st.drB)}', cap: true, b: true), _pBtn(c, '清零', ntf.rstTrf)]),
Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[ _txt(c, '内存 ${st.memMB} MB · 204探测 ', cap: true),
_txt(c, probeStr, cap: true, b: true, col: probeBad ? const Color(0xFFEF4444) : _cP), _pBtn(c, st.busy ? '...' : '测速', st.busy ? null : () => unawaited(ntf.chkNow())), if (!Platform.isAndroid) ...<Widget>[
_pBtn(c, sysPx ? '✓ 系统代理' : '系统代理', () => ntf.setSysProxy(!sysPx), active: sysPx, activeColor: _cB), _pBtn(c, tunOn ? '✓ TUN网卡' : 'TUN网卡', () => ntf.setTun(!tunOn), active: tunOn, activeColor: _cP), ], ]), ]), ]), ); }
Widget _fCard(BuildContext c, GuardianState st) { final ntf = ref.read(guardianProvider.notifier); final isDirect = st.fbDir;final meta = st.meta;
final curIp = (meta != null && meta.ip.isNotEmpty) ? meta.ip : ((meta != null && meta.raw.isNotEmpty) ? meta.raw : (st.node.isEmpty ? '待选节点' : st.node));
Widget modeTab(String title, bool active, Color activeCol, VoidCallback tap) => Expanded(child: GestureDetector( onTap: tap, child: Container(
padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 8), alignment: Alignment.center,
decoration: _rBox(active ? _fg(c).withValues(alpha: 0.09) : const Color(0x00000000), 10, border: active ? activeCol.withValues(alpha: 0.55) : null),
child: Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: AppTextStyle.caption1.of(c, emphasized: true).copyWith(color: active ? activeCol : _mu(c))), ), )); final q = _ipQ.trim().toLowerCase();
final filteredOpts = q.isEmpty ? st.opts : st.opts.where((o) => o.ip.toLowerCase().contains(q) || o.node.toLowerCase().contains(q) || (o.s24?.toLowerCase().contains(q) ?? false)).toList(); return Container(
padding: const EdgeInsets.all(15), decoration: _rBox(_cardBg(c), 20, border: _fg(c).withValues(alpha: 0.07)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 10, children: <Widget>[
Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: <Widget>[_txt(c, '🧭 兜底分类默认出口', b: true), _badge(c, isDirect ? 'MATCH,DIRECT' : 'MATCH,${st.reg}-STICKY', isDirect ? _cD : _cP)]),
Container(padding: const EdgeInsets.all(3), decoration: _rBox(_subBg(c), 13), child: Row(spacing: 4, children: <Widget>[ modeTab('🌐 兜底走粘滞代理', !isDirect, _cP, () => unawaited(ntf.setFbDir(false))),
modeTab('🛡 兜底走物理直连', isDirect, _cD, () => unawaited(ntf.setFbDir(true))), ])), if (isDirect)
Container(padding: const EdgeInsets.all(12), decoration: _rBox(_cD.withValues(alpha: 0.11), 14, border: _cD.withValues(alpha: 0.30)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 4, children: <Widget>[
_txt(c, '🛡 兜底分类已设为物理直连（已收起基准国家选择）', b: true, col: const Color(0xFF0284C7)), _txt(c, '「自定义分类」、厂商主进程、动态伴生子进程与专享浏览器 100% 统一走各自代理；其余兜底流量全部走物理直连。', cap: true, maxLines: 3), ])) else ...<Widget>[
if (st.regs.isEmpty) _txt(c, '尚未加载订阅节点，请点击右上角「+ 订阅」导入配置', cap: true) else Wrap(spacing: 6, runSpacing: 6, children: <Widget>[ for (final r in st.regs) GestureDetector( onTap: () => unawaited(ntf.selReg(r.code)), child: Container(
padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7), decoration: _rBox(r.code == st.reg ? _cP.withValues(alpha: 0.15) : _subBg(c), 11, border: r.code == st.reg ? _cP.withValues(alpha: 0.6) : null),
child: Row(mainAxisSize: MainAxisSize.min, spacing: 6, children: <Widget>[ Text(r.label, style: AppTextStyle.caption1.of(c, emphasized: true).copyWith(color: r.code == st.reg ? _cP : _fg(c))),
_txt(c, r.bestMs > 0 ? '${r.bestMs}ms' : '${r.nodes.length}', cap: true), ]), ), ), ]),
Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: _rBox(_subBg(c), 12), child: Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 6, children: <Widget>[
Row(mainAxisSize: MainAxisSize.min, spacing: 6, children: <Widget>[_badge(c, '粘滞IP', _cP), Flexible(child: _txt(c, '$curIp · ${st.ms > 0 ? "${st.ms}ms" : "同段容灾"}', b: true))]),
_pBtn(c, '同区 IP (${st.opts.length}) ${st.ipOpen ? "▴" : "▾"}', ntf.togIpP, active: st.ipOpen, activeColor: _cP), ])),
if (st.ipOpen) Container(padding: const EdgeInsets.only(top: 6), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 7, children: <Widget>[
Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
PopupAnchor(targetBuilder: (open) => _pBtn(c, '容灾阈值 ${st.lim}ms ▾', open), popupBuilder: (_) => PopupMenu(items: <PopupMenuItem>[for (final ms in const <int>[600, 800, 1000, 1500]) PopupMenuItem(glyph: st.lim == ms ? AppGlyphs.check : null, label: '${ms}ms', onPressed: () => ntf.setLimit(ms))])),
_pBtn(c, st.auto ? '✓ 超时同段秒切' : '超时秒切已关', () => ntf.setAuto(!st.auto), active: st.auto, activeColor: _cP), _pBtn(c, st.busy ? '测速中...' : '测速本区', st.busy ? null : () => unawaited(ntf.probReg())), ]),
_inp(c, _ipCtrl, _ipFocus, '搜索本区 IP / /24网段 / 节点名...', _ipQ, (v) => _upd(() => _ipQ = v)),
ConstrainedBox(constraints: const BoxConstraints(maxHeight: 190), child: SingleChildScrollView(child: Column(spacing: 5, children: <Widget>[ for (final o in filteredOpts) GestureDetector(
onTap: () => unawaited(ntf.pickNode(o.node)),
child: Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7), decoration: _rBox(o.sel ? _cP.withValues(alpha: 0.16) : _subBg(c), 10), child: Row(children: <Widget>[
Expanded(child: _txt(c, '${o.ip.isNotEmpty ? o.ip : o.node} · ${o.node}', cap: true, b: o.sel)),
_txt(c, '${o.ms > 0 ? "${o.ms}ms" : (o.ms < 0 ? "超时" : "待测")}${o.sel ? " · 当前" : ""}', cap: true, b: true, col: o.sel ? _cP : _mu(c)), ])), ), ]))), ])), ], ]), ); }
Widget _dSh(BuildContext c, {required String drawerKey, required bool open, required String title, required String summary, Widget? trailingAction, required List<Widget> bodyChildren}) {
final ntf = ref.read(guardianProvider.notifier); return Container( decoration: _rBox(_cardBg(c), 20, border: _fg(c).withValues(alpha: 0.07)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: <Widget>[
GestureDetector( behavior: HitTestBehavior.opaque, onTap: () => ntf.togDrw(drawerKey), child: Padding(padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 13), child: Row(spacing: 8, children: <Widget>[
Expanded(child: Wrap(crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 3, children: <Widget>[Text(title, style: AppTextStyle.subheadline.of(c, emphasized: true)), _txt(c, summary, cap: true)])),
if (trailingAction != null) trailingAction, Text(open ? '▴' : '▾', style: AppTextStyle.subheadline.of(c).copyWith(color: _mu(c))), ])), ),
if (open) Padding(padding: const EdgeInsets.fromLTRB(15, 2, 15, 15), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 8, children: bodyChildren)), ]), ); }
Widget _bDrw(BuildContext c, GuardianState st, bool isCompact) { final ntf = ref.read(guardianProvider.notifier); final activeBrowsers = st.browserEnvs.where((b) => b.enabled).toList();
final summaryText = activeBrowsers.isEmpty ? '未开启专享浏览器（如开启 Edge → 🇸🇬 新加坡 / 🇭🇰 香港，该浏览器及子内核将 100% 锁定该国）' : '已锁定 ${activeBrowsers.map((b) => "${b.name.split(" ").first}→${FlClashBridge.regLblOf(b.exit).split(" ").last}").join(" · ")}';
return _dSh( c, drawerKey: 'browsers', open: st.drawers['browsers'] ?? true, title: '🌐 浏览器特定环境代理', summary: summaryText,
trailingAction: _pBtn(c, '+ 自定义浏览器', () { if (!(st.drawers['browsers'] ?? true)) ntf.togDrw('browsers'); _upd(() => _bAddOpen = !_bAddOpen); }, active: _bAddOpen, activeColor: _cD), bodyChildren: <Widget>[
if (_bAddOpen) Container(padding: const EdgeInsets.all(10), decoration: _rBox(_subBg(c), 12), child: Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
SizedBox(width: isCompact ? 260 : 350, child: _inp(c, _bAddCtrl, _bAddFocus, Platform.isAndroid ? '输入浏览器包名...' : '输入浏览器进程名 / .app / 便携版目录...', _bIn, (v) => _upd(() => _bIn = v))),
_exPill(c, _newBrowserExit, _browserExitOpts, (code) => _upd(() => _newBrowserExit = code), active: true, activeColor: _cD),
_pBtn(c, '+ 锁定专享环境', _bIn.trim().isEmpty ? null : () { final raw = _bIn; _bAddCtrl.clear(); _upd(() => _bIn = ''); unawaited(ntf.addCustomBrowserEnv(raw, _newBrowserExit)); }, active: _bIn.trim().isNotEmpty, activeColor: _cD),
])), for (final b in st.browserEnvs) () { final bComps = st.companions.where((cp) => cp.ownerKind == 'browser' && cp.ownerId == b.id).toList();
final brandBox = Container(width: 30, height: 30, alignment: Alignment.center, decoration: _rBox(Color(b.colVal), 9), child: Text(b.badge, style: AppTextStyle.caption1.of(c, emphasized: true).copyWith(color: _cWht)));
final titleBlock = Expanded(child: GestureDetector(behavior: HitTestBehavior.opaque, onTap: () => unawaited(ntf.togBrowserEnv(b.id)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[
Wrap(spacing: 6, runSpacing: 4, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[ Text(b.name, style: AppTextStyle.subheadline.of(c, emphasized: true)),
_badge(c, b.enabled ? '已锁定 → ${FlClashBridge.regLblOf(b.exit)}' : '普通按域分流', b.enabled ? _cD : _cN), if (bComps.isNotEmpty) _badge(c, '🧬 伴生 +${bComps.length}', _cP), ]), _txt(c, b.hint, cap: true), ])));
final ctrls = Row(mainAxisSize: MainAxisSize.min, spacing: 6, children: <Widget>[ _exPill(c, b.exit, _browserExitOpts, (code) => unawaited(ntf.setBrowserEnvExit(b.id, code)), active: b.enabled, activeColor: _cD),
if (b.custom) _pBtn(c, '移除 ×', () => unawaited(ntf.rmCustomBrowserEnv(b.id))), _sw(b.enabled, _cD, () => unawaited(ntf.togBrowserEnv(b.id))), ]); return Opacity(opacity: b.enabled ? 1.0 : 0.72, child: Container(
padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
decoration: _rBox(b.enabled ? _cD.withValues(alpha: 0.09) : _fg(c).withValues(alpha: 0.028), 14, border: b.enabled ? _cD.withValues(alpha: 0.35) : _fg(c).withValues(alpha: 0.06)),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 7, children: <Widget>[ if (isCompact) ...<Widget>[
Row(spacing: 10, children: <Widget>[brandBox, titleBlock, _sw(b.enabled, _cD, () => unawaited(ntf.togBrowserEnv(b.id)))]),
Row(mainAxisAlignment: MainAxisAlignment.end, spacing: 6, children: <Widget>[_exPill(c, b.exit, _browserExitOpts, (code) => unawaited(ntf.setBrowserEnvExit(b.id, code)), active: b.enabled, activeColor: _cD), if (b.custom) _pBtn(c, '移除 ×', () => unawaited(ntf.rmCustomBrowserEnv(b.id)))]),
] else Row(spacing: 10, children: <Widget>[brandBox, titleBlock, ctrls]), if (bComps.isNotEmpty) Wrap(spacing: 6, runSpacing: 5, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
_txt(c, '🧬 伴生内核白名单:', cap: true, b: true, col: _cP), for (final cp in bComps.take(8)) _pBtn(c, '${cp.exe} (←${cp.rootExe}) ×', () => unawaited(ntf.rmCompanionRule(cp.id)), active: true, activeColor: _cP), ]), ]), )); }(), ], ); }
String _vSum(VendorSpec v, int compCnt) { if (!v.enabled) return '未启用独立代理（归属兜底策略）'; final appEx = FlClashBridge.regLblOf(v.defEx); final parts = <String>['整包 → $appEx'];
if (v.customApps.isNotEmpty) parts.add(_isCust(v) ? '已保存软件 ${v.customApps.length} 款' : '已投送 +${v.customApps.length}'); if (compCnt > 0) parts.add('伴生白名单 +$compCnt');
for (final sl in v.subs.take(2)) { parts.add('${sl.name.split(" ").first}→${FlClashBridge.regLblOf(sl.exit).split(" ").last}'); } if (v.learnedDirs.isNotEmpty) parts.add('目录继承 ${v.learnedDirs.length} 处'); return parts.join(' · ');
} Widget _catCard(BuildContext c, GuardianState st, VendorSpec v, bool isCompact) { final ntf = ref.read(guardianProvider.notifier);
final isC = _isCust(v);final exp = st.expV.contains(v.id);final addOpen = isC && _openAddCatId == v.id; final vComps = st.companions.where((cp) => cp.ownerKind == 'vendor' && cp.ownerId == v.id).toList();
final treeStat = FlClashBridge.liveRootStats['vendor:${v.id}']; final accent = isC ? _cW : _cV; final exitChoices = isC ? _browserExitOpts : _vendorExitOpts; final fbCandidates = st.procs.where((p) => !p.proxied).take(2).toList();
final brandBox = Container(width: 30, height: 30, alignment: Alignment.center, decoration: _rBox(Color(v.colVal), 9), child: Text(v.badge, style: AppTextStyle.caption1.of(c, emphasized: true).copyWith(color: _cWht)));
final titleBlock = Expanded(child: GestureDetector(behavior: HitTestBehavior.opaque, onTap: () => ntf.togVExp(v.id), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[
Wrap(spacing: 6, runSpacing: 4, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[ Text(v.name, style: AppTextStyle.subheadline.of(c, emphasized: true)),
if (isC) _badge(c, '🧩 自定义分类', _cW) else _badge(c, '整包优先', _cV), if (v.customApps.isNotEmpty) _badge(c, isC ? '📌 已保存 ${v.customApps.length} 款' : '📌 +${v.customApps.length}', isC ? _cW : _cB),
if (vComps.isNotEmpty) _badge(c, '🧬 伴生 +${vComps.length}', _cP), if (treeStat != null && treeStat.rootCount > 0) _badge(c, '🧵 ${treeStat.totalThreads}线程${treeStat.childCount > 0 ? " · 活跃伴生${treeStat.childCount}" : ""}', _cD), ]),
_txt(c, _vSum(v, vComps.length), cap: true), ]))); final ctrls = Wrap(spacing: 6, runSpacing: 4, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
if (isC) _pBtn(c, '+ 添加软件', () => _upd(() { _openAddCatId = addOpen ? '' : v.id; _grpAppCtrl.clear(); _grpAppIn = ''; }), active: addOpen, activeColor: _cW),
_exPill(c, v.defEx, exitChoices, (code) => unawaited(ntf.setVEx(v.id, code)), active: isC && v.enabled, activeColor: accent), _pBtn(c, '明细 ${exp ? "▴" : "▾"}', () => ntf.togVExp(v.id), active: exp, activeColor: accent),
_sw(v.enabled, accent, () => unawaited(ntf.togVEn(v.id))), ]); return Opacity(opacity: v.enabled ? 1.0 : 0.58, child: Container( padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
decoration: _rBox(isC ? _cW.withValues(alpha: exp ? 0.10 : 0.065) : (exp ? _subBg(c) : _fg(c).withValues(alpha: 0.028)), 14, border: isC ? _cW.withValues(alpha: 0.34) : _fg(c).withValues(alpha: exp ? 0.13 : 0.06)),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 8, children: <Widget>[ if (isCompact) ...<Widget>[
Row(spacing: 10, children: <Widget>[brandBox, titleBlock, _sw(v.enabled, accent, () => unawaited(ntf.togVEn(v.id)))]), Align(alignment: Alignment.centerRight, child: Wrap(spacing: 6, runSpacing: 4, children: <Widget>[
if (isC) _pBtn(c, '+ 添加软件', () => _upd(() { _openAddCatId = addOpen ? '' : v.id; _grpAppCtrl.clear(); _grpAppIn = ''; }), active: addOpen, activeColor: _cW),
_exPill(c, v.defEx, exitChoices, (code) => unawaited(ntf.setVEx(v.id, code)), active: isC && v.enabled, activeColor: accent), _pBtn(c, '明细 ${exp ? "▴" : "▾"}', () => ntf.togVExp(v.id), active: exp, activeColor: accent), ])),
] else Row(spacing: 10, children: <Widget>[brandBox, titleBlock, ctrls]),
if (addOpen) Container(padding: const EdgeInsets.all(9), decoration: _rBox(_subBg(c), 11), child: Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
SizedBox(width: isCompact ? 250 : 340, child: _inp(c, _grpAppCtrl, _grpAppFocus, Platform.isAndroid ? '输入安卓包名单独保存至本分类...' : '输入软件进程名 / .app / 安装目录单独保存至本分类...', _grpAppIn, (val) => _upd(() => _grpAppIn = val))),
_pBtn(c, '+ 保存至本分类', _grpAppIn.trim().isEmpty ? null : () { final raw = _grpAppIn; _grpAppCtrl.clear(); _upd(() => _grpAppIn = ''); unawaited(ntf.addSoftwareToCategory(v.id, raw)); }, active: _grpAppIn.trim().isNotEmpty, activeColor: _cW),
if (fbCandidates.isNotEmpty) ...<Widget>[ _txt(c, '快选兜底:', cap: true),
for (final fb in fbCandidates) _pBtn(c, '+ ${fb.name}', () => unawaited(ntf.dispatchToVendor(vendorId: v.id, label: fb.name, exe: fb.rawExe, path: fb.path, pkg: fb.pkg))), ], ])),
if (v.customApps.isNotEmpty) Wrap(spacing: 6, runSpacing: 5, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[ _txt(c, isC ? '📌 已保存软件/主进程:' : '📌 已投送主进程:', cap: true, b: true, col: isC ? _cW : _cB),
for (final ca in v.customApps) _pBtn(c, '${ca.label} ×', () => unawaited(ntf.rmVendorCustomApp(v.id, ca.id)), active: true, activeColor: isC ? _cW : _cB),
]) else if (isC) _txt(c, '尚未添加软件 — 点击「+ 添加软件」单独录入，或在下方「🧭 兜底」列表一键投送至此自定义分类并自动保存。', cap: true, maxLines: 2), if (vComps.isNotEmpty) Wrap(spacing: 6, runSpacing: 5, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
_txt(c, '🧬 伴生白名单:', cap: true, b: true, col: _cP), for (final cp in vComps.take(10)) _pBtn(c, '${cp.exe} (←${cp.rootExe}) ×', () => unawaited(ntf.rmCompanionRule(cp.id)), active: true, activeColor: _cP),
if (vComps.length > 1) _pBtn(c, '清空伴生', () => unawaited(ntf.clearOwnerCompanions('vendor', v.id))), ]), if (exp) ...<Widget>[
Container(width: double.infinity, padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6), decoration: _rBox(accent.withValues(alpha: 0.10), 9), child: _txt(c, '✓ 本分类旗下所有主进程、多线程及拉起的伴生进程 100% 统一走 ${FlClashBridge.regLblOf(v.defEx)}（重启自动恢复保存记录）', cap: true, b: true, col: accent, maxLines: 2)),
if (_renamingCatId == v.id) Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
SizedBox(width: 220, child: _inp(c, _rnCtrl, _rnFocus, '输入新分组名称...', _rnIn, (val) => _upd(() => _rnIn = val))),
_pBtn(c, '✓ 保存名称', _rnIn.trim().isEmpty ? null : () { final nm = _rnIn; _upd(() => _renamingCatId = ''); unawaited(ntf.renameCustomGroup(v.id, nm)); }, active: true, activeColor: _cW),
_pBtn(c, '取消', () => _upd(() => _renamingCatId = '')), ]),
for (final sl in v.subs) Container(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7), decoration: _rBox(_cardBg(c), 10), child: Row(spacing: 8, children: <Widget>[
Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[_txt(c, sl.name, cap: true, b: true), _txt(c, sl.domains.join(', '), cap: true)])),
_exPill(c, sl.exit, _subExitOpts, (code) => unawaited(ntf.setSEx(v.id, sl.id, code))), ])), Wrap(spacing: 6, runSpacing: 5, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
if (v.procs.isNotEmpty) _badge(c, '内置主进程: ${v.procs.take(4).join("/")}', _cN), _badge(c, '目录继承: ${v.learnedDirs.isEmpty ? "自动学习目录" : "${v.learnedDirs.length} 目录"}', v.learnedDirs.isEmpty ? _cN : accent),
_badge(c, '阻断补录: ${v.hIps.isEmpty ? "0 IP" : "${v.hIps.length} IP"}', v.hIps.isEmpty ? _cN : _cW), if (v.hIps.isNotEmpty || v.learnedDirs.isNotEmpty) _pBtn(c, '清空动态缓存', () => unawaited(ntf.clrHIps(v.id))),
if (isC) _pBtn(c, '✎ 重命名分组', () => _upd(() { _renamingCatId = v.id; _rnCtrl.text = v.name; _rnIn = v.name; })), if (_isDel(v)) _pBtn(c, '🗑 删除此分组', () => unawaited(ntf.deleteCustomGroup(v.id))), ]), ], ]), )); }
Widget _vDrw(BuildContext c, GuardianState st, bool isCompact) { final ntf = ref.read(guardianProvider.notifier); final allCust = st.vendors.where(_isCust).toList(); final allBuilt = st.vendors.where((v) => !_isCust(v)).toList();
final totalSavedApps = st.vendors.fold<int>(0, (s, v) => s + v.customApps.length); final q = _vQ.trim().toLowerCase(); bool matchV(VendorSpec v) { if (q.isEmpty) return true;
final vComps = st.companions.where((cp) => cp.ownerKind == 'vendor' && cp.ownerId == v.id).map((cp) => '${cp.exe} ${cp.chain}').join(' ');
final hay = '${v.name} ${v.procs.join(" ")} ${v.pkgs.join(" ")} $vComps ${v.customApps.map((a) => "${a.label} ${a.exe} ${a.pkg}").join(" ")}'.toLowerCase(); return hay.contains(q); }
final custList = allCust.where(matchV).toList(); final builtList = allBuilt.where(matchV).toList(); return _dSh( c, drawerKey: 'vendors', open: st.drawers['vendors'] ?? true, title: '🧩 自定义分类与厂商代理配置中心',
summary: '自定义分组 ${allCust.where((v) => v.enabled).length}/${allCust.length} · 内置厂商 ${allBuilt.where((v) => v.enabled).length}/${allBuilt.length}${totalSavedApps > 0 ? " · 已保存软件 $totalSavedApps 项" : ""}',
trailingAction: Wrap(spacing: 6, children: <Widget>[ _pBtn(c, '+ 新建自定义分组', () { if (!(st.drawers['vendors'] ?? true)) ntf.togDrw('vendors'); _upd(() => _newGrpOpen = !_newGrpOpen); }, active: _newGrpOpen, activeColor: _cW),
_pBtn(c, '🔍 筛选', () { if (!(st.drawers['vendors'] ?? true)) ntf.togDrw('vendors'); _upd(() => _vTl = !_vTl); }, active: _vTl), ]), bodyChildren: <Widget>[
if (_newGrpOpen) Container(padding: const EdgeInsets.all(10), decoration: _rBox(_cW.withValues(alpha: 0.09), 13, border: _cW.withValues(alpha: 0.40)), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 8, children: <Widget>[
Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: <Widget>[ Flexible(child: _txt(c, '✨ 新建自定义代理分组（支持单独添加软件、接收兜底投送、伴生树继承与持久化保存）', cap: true, b: true, col: _cW)),
_pBtn(c, '收起 ×', () => _upd(() => _newGrpOpen = false)), ]), Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
SizedBox(width: 72, child: _inp(c, _ngBadgeCtrl, _ngBadgeFocus, '角标', _ngBadge, (v) => _upd(() => _ngBadge = v))),
SizedBox(width: isCompact ? 210 : 300, child: _inp(c, _ngNameCtrl, _ngNameFocus, '输入分组名 (如 跨境办公 / 游戏专享)...', _ngName, (v) => _upd(() => _ngName = v))),
_exPill(c, _ngExit, _browserExitOpts, (code) => _upd(() => _ngExit = code), active: true, activeColor: _cW), _pBtn(c, '✓ 创建并保存分组', () async { final nm = _ngName;final bg = _ngBadge;final ex = _ngExit; _ngNameCtrl.clear();
_upd(() { _ngName = ''; _newGrpOpen = false; }); final id = await ntf.createCustomGroup(name: nm, badge: bg, exitCode: ex); _upd(() { _openAddCatId = id; _targetVendorId = id; }); }, active: true, activeColor: _cW), ]), ])),
if (_vTl) Container(padding: const EdgeInsets.all(10), decoration: _rBox(_subBg(c), 12), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 8, children: <Widget>[
_inp(c, _vSC, _vSF, '搜索自定义分组 / 厂商 / 已保存软件 / 伴生进程...', _vQ, (v) => _upd(() => _vQ = v)), Row(spacing: 6, children: <Widget>[ Expanded(child: _inp(c, _cDomCtrl, _cDomFocus, '新增普通浏览器自定义域名...', _cDom, (v) => _upd(() => _cDom = v))),
_exPill(c, _customExit, _subExitOpts, (code) => _upd(() => _customExit = code)),
_pBtn(c, '+ 加入', _cDom.trim().isEmpty ? null : () { final dom = _cDom; _cDomCtrl.clear(); _upd(() => _cDom = ''); unawaited(ntf.addCDom(dom, _customExit)); }, active: _cDom.trim().isNotEmpty), ]), ])),
Padding(padding: const EdgeInsets.only(top: 2), child: _txt(c, '🧩 自定义分类（支持单独添加软件、接收兜底投送、伴生子进程自动继承并持久化记录）', cap: true, b: true, col: _cW)), for (final v in custList) _catCard(c, st, v, isCompact),
Padding(padding: const EdgeInsets.only(top: 4), child: _txt(c, '🏢 内置大厂与 Harness 分类（整包及伴生守护逻辑与自定义分类一致）', cap: true, b: true)), for (final v in builtList) _catCard(c, st, v, isCompact), ], ); }
Widget _procRow(BuildContext c, GuardianState st, ProcStat p, bool isCompact) { final ntf = ref.read(guardianProvider.notifier); final exp = st.expA.contains(p.key);
final isComp = p.companionId.isNotEmpty || p.lineageHint.isNotEmpty; final isBrw = !isComp && p.browserId.isNotEmpty; final isCustV = !isComp && !isBrw && p.vendorId.startsWith('custom_');
final speedInfo = _txt(c, '↓ ${fmtRate(p.dnR)} · 累计 ${fmtBytes(p.up + p.dn)}', cap: true, b: p.dnR + p.upR > 0);
final actionBtn = p.proxied ? _manageMenuForProxied(c, st, p) : _dispatchMenuForFallback(c, st, label: p.name, exe: p.rawExe, path: p.path, pkg: p.pkg, fixedDirect: p.fixedDirect);
final actRow = Row(mainAxisSize: MainAxisSize.min, spacing: 6, children: <Widget>[actionBtn, _pBtn(c, '连接 (${p.conns.length}) ${exp ? "▴" : "▾"}', () => ntf.togAExp(p.key), active: exp)]);
final rowBg = p.proxied ? (isComp ? _cP.withValues(alpha: 0.08) : (isBrw ? _cD.withValues(alpha: 0.09) : (isCustV ? _cW.withValues(alpha: 0.09) : _cV.withValues(alpha: p.dispatched ? 0.10 : 0.06)))) : (p.fixedDirect ? _cD.withValues(alpha: 0.08) : _fg(c).withValues(alpha: 0.032));
final badgeColor = p.proxied ? (isComp ? _cP : (isBrw ? _cD : (isCustV ? _cW : (p.dispatched ? _cB : _cV)))) : (p.fixedDirect ? _cD : _cN);
final dispBadge = isCustV && p.rLbl.startsWith('📌 ') ? '🧩 ${p.rLbl.substring(2).trimLeft()}' : p.rLbl;
final subLineParts = <String>[if (p.lineageHint.isNotEmpty) '拉起链路: ${p.lineageHint}', if (p.path.isNotEmpty) p.path else if (p.pkg.isNotEmpty) p.pkg else if (p.rawExe.isNotEmpty) p.rawExe];
final subLine = subLineParts.join(' · '); return Container(
padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9), decoration: _rBox(rowBg, 13, border: isCustV ? _cW.withValues(alpha: 0.28) : _fg(c).withValues(alpha: 0.06)),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 6, children: <Widget>[ Row(spacing: 8, children: <Widget>[ Expanded(child: p.proxied
? GestureDetector(behavior: HitTestBehavior.opaque, onTap: () => ntf.togAExp(p.key), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[
Wrap(spacing: 6, runSpacing: 4, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[Text(p.name, style: AppTextStyle.subheadline.of(c, emphasized: true)), _badge(c, dispBadge, badgeColor), if (p.treeBadge.isNotEmpty) _badge(c, p.treeBadge, _cD)]),
if (subLine.isNotEmpty) _txt(c, subLine, cap: true), ])) : PopupAnchor(
targetBuilder: (open) => GestureDetector(behavior: HitTestBehavior.opaque, onTap: open, child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[
Wrap(spacing: 6, runSpacing: 4, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[Text(p.name, style: AppTextStyle.subheadline.of(c, emphasized: true)), _badge(c, dispBadge, badgeColor)]),
if (subLine.isNotEmpty) _txt(c, subLine, cap: true), ])), popupBuilder: (_) => _buildFallbackDispatchPopup(st, label: p.name, exe: p.rawExe, path: p.path, pkg: p.pkg, fixedDirect: p.fixedDirect), )),
if (!isCompact) ...<Widget>[speedInfo, actRow], ]), if (isCompact) Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: <Widget>[Flexible(child: speedInfo), actRow]),
if (exp) Container(padding: const EdgeInsets.all(8), decoration: _rBox(_subBg(c), 10), child: p.conns.isEmpty ? _txt(c, '当前无活跃连接套接字（已保存在自定义分类/伴生白名单记录中）', cap: true) : Column(spacing: 4, children: <Widget>[
for (final cn in p.conns) Row(children: <Widget>[Expanded(child: _txt(c, '${cn.target} (${cn.net})', cap: true, b: true)), _txt(c, '${cn.dim} → ${cn.chain}', cap: true)]), ])), ]), ); }
Widget _subBucket(BuildContext c, {required String drawerKey, required bool open, required String title, required String subtitle, required int count, required Color accent, required String emptyHint, required List<Widget> rows, Widget? headerExtra}) {
final ntf = ref.read(guardianProvider.notifier); return Container( decoration: _rBox(accent.withValues(alpha: 0.04), 15, border: accent.withValues(alpha: 0.22)),
child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: <Widget>[
GestureDetector(behavior: HitTestBehavior.opaque, onTap: () => ntf.togDrw(drawerKey), child: Padding(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10), child: Row(spacing: 8, children: <Widget>[
_badge(c, '$count', accent),
Expanded(child: Wrap(spacing: 8, runSpacing: 2, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[Text(title, style: AppTextStyle.subheadline.of(c, emphasized: true).copyWith(color: accent)), _txt(c, subtitle, cap: true)])),
if (headerExtra != null) headerExtra, Text(open ? '▴' : '▾', style: AppTextStyle.subheadline.of(c).copyWith(color: _mu(c))), ]))),
if (open) Padding(padding: const EdgeInsets.fromLTRB(10, 0, 10, 10), child: rows.isEmpty ? Padding(padding: const EdgeInsets.symmetric(vertical: 10), child: Center(child: _txt(c, emptyHint, cap: true))) : Column(spacing: 6, children: rows)),
]), ); } Widget _aDrw(BuildContext c, GuardianState st, bool isCompact) { final ntf = ref.read(guardianProvider.notifier); final q = _appQ.trim().toLowerCase();
final matched = q.isEmpty ? st.procs : st.procs.where((p) => p.name.toLowerCase().contains(q) || p.rawExe.toLowerCase().contains(q) || p.pkg.toLowerCase().contains(q) || p.path.toLowerCase().contains(q) || p.lineageHint.toLowerCase().contains(q) || p.rLbl.toLowerCase().contains(q)).toList();
final proxiedList = matched.where((p) => p.proxied).toList(); final fallbackList = matched.where((p) => !p.proxied).toList(); final selVendor = st.vendors.where((v) => v.id == _targetVendorId).firstOrNull ?? st.vendors.first;
final custCats = st.vendors.where(_isCust).toList(); final builtinCats = st.vendors.where((v) => !_isCust(v)).toList(); final unlaunchedFallbackApps = Platform.isAndroid && _aPk ? st.apps.where((a) {
if (st.procs.any((p) => p.pkg == a.pkg)) return false;
final isProxiedPkg = FlClashBridge.findAppRule(a.pkg, '', a.pkg)?.exit != 'DIRECT' && (FlClashBridge.findAppRule(a.pkg, '', a.pkg) != null || FlClashBridge.findEnabledBrowserEnv(a.pkg, '', a.pkg) != null || FlClashBridge.matchVendorProcess(a.pkg, '', a.pkg) != null);
if (isProxiedPkg) return false; return q.isEmpty || a.label.toLowerCase().contains(q) || a.pkg.toLowerCase().contains(q); }).take(60).toList() : const <InstalledApp>[];
final pcTreeSummary = (!Platform.isAndroid && !Platform.isIOS) ? ' · 活跃主进程 ${st.liveRoots} / 伴生 ${st.liveChildren} (${st.liveThreads}线程)' : ''; return _dSh(
c, drawerKey: 'apps', open: st.drawers['apps'] ?? true, title: '📱 应用流量与伴生整包控制', summary: '仅分两类：被代理 ${proxiedList.length} · 兜底 ${fallbackList.length}$pcTreeSummary',
trailingAction: _pBtn(c, '+ 手动投送', () { if (!(st.drawers['apps'] ?? true)) ntf.togDrw('apps'); _upd(() => _addAppOpen = !_addAppOpen); }, active: _addAppOpen, activeColor: _cB), bodyChildren: <Widget>[
if (!Platform.isAndroid && !Platform.isIOS) Container(padding: const EdgeInsets.symmetric(horizontal: 11, vertical: 8), decoration: _rBox(_subBg(c), 12), child: Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 6, children: <Widget>[
Row(mainAxisSize: MainAxisSize.min, spacing: 6, children: <Widget>[_badge(c, '🧬 进程树守护', _cP), Flexible(child: _txt(c, '主进程 ${st.liveRoots} · 活跃伴生 ${st.liveChildren} · 覆盖 ${st.liveThreads} 线程 · 已存白名单 ${st.companions.length} 项', cap: true, b: true))]),
Wrap(spacing: 6, children: <Widget>[ _pBtn(c, st.autoCompanion ? '✓ 首次伴生自动入白名单' : '伴生自动入库已关', () => ntf.setAutoCompanion(!st.autoCompanion), active: st.autoCompanion, activeColor: _cP),
_pBtn(c, '立即扫描查漏', () => unawaited(ntf.scanProcessTreeNow())), ]), ])),
if (_addAppOpen) Container(padding: const EdgeInsets.all(10), decoration: _rBox(_subBg(c), 12), child: Wrap(spacing: 6, runSpacing: 6, crossAxisAlignment: WrapCrossAlignment.center, children: <Widget>[
SizedBox(width: isCompact ? 260 : 320, child: _inp(c, _wAddCtrl, _wAddFocus, Platform.isAndroid ? '输入包名直接投送...' : '输入主进程名 / .app / 安装目录直接投送...', _wIn, (v) => _upd(() => _wIn = v))), PopupAnchor(
targetBuilder: (open) => _pBtn(c, '${_isCust(selVendor) ? "🧩" : "🏢"} ${selVendor.name} ▾', open, active: _isCust(selVendor), activeColor: _cW), popupBuilder: (_) => PopupMenu(items: <PopupMenuItem>[
for (final cv in custCats) PopupMenuItem(glyph: cv.id == selVendor.id ? AppGlyphs.check : null, label: '🧩 ${cv.name} (${FlClashBridge.regLblOf(cv.defEx)})', onPressed: () => _upd(() => _targetVendorId = cv.id)),
for (final v in builtinCats) PopupMenuItem(glyph: v.id == selVendor.id ? AppGlyphs.check : null, label: '🏢 ${v.name} (${FlClashBridge.regLblOf(v.defEx)})', onPressed: () => _upd(() => _targetVendorId = v.id)), ]), ),
_pBtn(c, '🎯 投送并保存', _wIn.trim().isEmpty ? null : () { final raw = _wIn; _wAddCtrl.clear(); _upd(() => _wIn = ''); unawaited(ntf.addSoftwareToCategory(selVendor.id, raw)); }, active: _wIn.trim().isNotEmpty, activeColor: _cW), ])),
_inp(c, _aSC, _aSF, '筛选被代理主进程、自定义分类软件、伴生子进程或兜底进程...', _appQ, (v) => _upd(() => _appQ = v)),
_subBucket(c, drawerKey: 'apps_px', open: st.drawers['apps_px'] ?? true, title: '🚀 被代理', subtitle: '含自定义分类软件、厂商主进程、自动伴生白名单及专享浏览器 · 100% 统一走代理', count: proxiedList.length, accent: _cV, emptyHint: '当前暂无被代理应用；添加至自定义分类或启动厂商主进程后，其本身与伴生进程均会自动在此显现', rows: <Widget>[for (final p in proxiedList.take(40)) _procRow(c, st, p, isCompact)]),
_subBucket(
c, drawerKey: 'apps_fb', open: st.drawers['apps_fb'] ?? true, title: '🧭 兜底（待捕获漏网之鱼）', subtitle: '未归入整包代理的应用与普通浏览器 · 点击任意行即可一键投送至「自定义分类」或对应厂商分组并保存', count: fallbackList.length + unlaunchedFallbackApps.length, accent: _cB,
headerExtra: Platform.isAndroid ? _pBtn(c, _aPk ? '仅看活跃 ▴' : '+未启动App (${st.apps.length}) ▾', () { if (st.apps.isEmpty) unawaited(ntf.ldApps()); _upd(() => _aPk = !_aPk); }, active: _aPk, activeColor: _cB) : null,
emptyHint: '当前暂无兜底进程；任何未识别的新应用产生网络请求后将立即在此显现', rows: <Widget>[ for (final p in fallbackList.take(40)) _procRow(c, st, p, isCompact),
for (final a in unlaunchedFallbackApps) Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8), decoration: _rBox(_fg(c).withValues(alpha: 0.025), 12, border: _fg(c).withValues(alpha: 0.05)), child: Row(spacing: 8, children: <Widget>[
Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[_txt(c, a.label, b: true), _txt(c, '${a.pkg} · 未启动兜底应用', cap: true)])),
_dispatchMenuForFallback(c, st, label: a.label, exe: a.pkg, path: '', pkg: a.pkg, fixedDirect: false), ])), ], ), ], ); } Widget _lDrw(BuildContext c, GuardianState st) { final ntf = ref.read(guardianProvider.notifier);
final latest = st.logs.firstOrNull; final list = _logCat == null ? st.logs : st.logs.where((e) => e.cat == _logCat).toList(); final rulesTxt = FlClashBridge.simpleRules().join('\n'); return _dSh(
c, drawerKey: 'logs', open: st.drawers['logs'] ?? false, title: '🛡 自定义分类记录与伴生自愈动态', summary: latest != null ? '最近：${latest.title}' : '实时记录自定义分类投送、伴生进程入白名单、专享浏览器锁定与阻断补录', trailingAction: _badge(c, '${st.logs.length} 条', _cN),
bodyChildren: <Widget>[ Wrap(alignment: WrapAlignment.spaceBetween, crossAxisAlignment: WrapCrossAlignment.center, spacing: 8, runSpacing: 6, children: <Widget>[ Wrap(spacing: 6, runSpacing: 6, children: <Widget>[
_pBtn(c, '全部', () => _upd(() => _logCat = null), active: _logCat == null), for (final ct in LogCat.values) _pBtn(c, ct.label, () => _upd(() => _logCat = ct), active: _logCat == ct), ]),
Wrap(spacing: 6, runSpacing: 6, children: <Widget>[ _pBtn(c, st.autoHeal ? '✓ 阻断自愈' : '阻断自愈已关', () => ntf.setAutoHeal(!st.autoHeal), active: st.autoHeal, activeColor: _cW),
_pBtn(c, _rPv ? '收起规则链 ▴' : '编译规则链 ▾', () => _upd(() => _rPv = !_rPv), active: _rPv), _pBtn(c, '复制规则', () => unawaited(Clipboard.setData(ClipboardData(text: rulesTxt)))), _pBtn(c, '清空', ntf.clrLog), ]), ]),
if (_rPv) Container(width: double.infinity, constraints: const BoxConstraints(maxHeight: 180), padding: const EdgeInsets.all(10), decoration: _rBox(const Color(0xFF0F172A), 12), child: SingleChildScrollView(child: Text(rulesTxt, style: AppTextStyle.caption1.of(c).copyWith(color: const Color(0xFFE2E8F0))))),
ConstrainedBox(constraints: const BoxConstraints(maxHeight: 240), child: list.isEmpty ? Padding(padding: const EdgeInsets.all(12), child: Center(child: _txt(c, '暂无记录', cap: true))) : SingleChildScrollView(child: Column(spacing: 5, children: <Widget>[
for (final e in list.take(40)) Container(width: double.infinity, padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7), decoration: _rBox(e.hot ? _cP.withValues(alpha: 0.10) : _subBg(c), 10), child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[
_txt(c, '[${fmtTime(e.time)}][${e.cat.label}] ${e.title}', cap: true, b: true), if (e.detail.isNotEmpty) _txt(c, e.detail, cap: true, maxLines: 2), ])), ]))), ], ); } Widget _mBar(BuildContext c, GuardianState st, bool run) {
final pxCnt = st.procs.where((p) => p.proxied).length; final fbCnt = st.procs.where((p) => !p.proxied).length; final routeSummary = st.fbDir ? '🛡 兜底直连 · 被代理 $pxCnt · 兜底 $fbCnt' : '${st.regLbl}粘滞 · 被代理 $pxCnt · 兜底 $fbCnt';
return Container(padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9), decoration: _rBox(_cardBg(c), 2, border: _fg(c).withValues(alpha: 0.10)), child: Row(spacing: 10, children: <Widget>[
Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, spacing: 2, children: <Widget>[ _txt(c, routeSummary, b: true),
_txt(c, run ? '↓ ${fmtRate(st.dnR)} · ${st.ms > 0 ? "${st.ms}ms" : "全进程守护中"}' : '接管未启动', cap: true), ])),
FilledButton(onPressed: _busy ? null : () => _toggleRun(run), child: Text(_busy ? '切换中...' : (run ? '● 运行中 ${fmtDur(st.runSec)}' : '▶ 开启接管'))), ])); } }
