import functools, hashlib, us13a
SWC13 = [
('// v127_skia_smooth_cards', '=', '// v128_sub_del_and_settings\n// v127_skia_smooth_cards'),
('shadows: DashboardShadows~e2(c),', '=', 'shadows: _e2Shadows(c),'),
('_badge(\n          ', '\n                        )',
"Row(mainAxisSize: MainAxisSize~min, spacing: 6, children: <Widget>[\n_badge(c, '${ms~nodes}节点', inMix ? _cB : _cN),\nGestureDetector(behav"
'ior: _hOp, onTap: () => _askDeleteSub(ms~id, ms~label), child: DecoratedBox(\ndecoration: _rBox(_cR~withValues(alpha: dk ? 0~14 : 0~09), '
'8),\nchild: const SizedBox~square(dimension: 24, child: Center(child: GlyphIcon(AppGlyphs~close, size: 13, color: _cR))),\n)),\n]),\n       '
'                   ],'),
('AddProfileMenu(\nbu', '\n],\n),\n),\n)\n', "_pBtn(c, '导入订阅', _openImportModal, glyph: AppGlyphs~add, solid: true, height: 38),"),
('_iconBtn(\nc,\nisExp', '\n),\n],\n),\n),',
'_iconBtn(c, isExpanded ? AppGlyphs~chevronUp : AppGlyphs~chevronDown, toggleExpand, active: isExpanded, activeColor: _cD),\n_iconBtn(c, A'
'ppGlyphs~close, () => _askDeleteSub(s~id, s~label), activeColor: _cR),\n],'),
('shadows: DashboardShadows~e2(c),', '=', 'shadows: _e2Shadows(c),'),
('Expanded(\nchild: _bentoActionTile(\nc,\nglyph: AppGlyphs~e', '\nExpanded(\nc',
"Expanded(child: _bentoActionTile(c, glyph: AppGlyphs~code, label: '查看源码', onTap: () => _upd(() => _subTab = 'extend'), height: 46)),"),
('Row(\nspacing: 8,\nchildren: <Widget>[\nif (cur~', 'Column(\ncros', ''),
('shadows: DashboardShadows~e2(c),', '=', 'shadows: _e2Shadows(c),'),
('shadows: DashboardShadows~e2(c),', '=', 'shadows: _e2Shadows(c),'),
]
SWC13_EXT = (
"\nFuture<void> _doImportUrl() async {\nif (_impBusy) return;\nfinal u = _impUrlCtrl~text~trim();\nif (u~isEmpty) { _upd(() => _impErr = '请粘贴"
"订阅 URL 或 vless/vmess/hy2/ss 分享链接'); return; }\n_upd(() { _impBusy = true; _impErr = ''; });\nfinal res = await _FB~importSubFromUrl(_gRef,"
' url: u, label: _impNameCtrl~text~trim(), ageKey: _impAgeCtrl~text~trim());\nif (!mounted) return;\nif (res~ok) {\nFocusManager~instance~pr'
"imaryFocus?~unfocus();\n_upd(() { _impBusy = false; _impOpen = false; });\n_showBottomToast(res~msg, 'success');\n} else {\n_upd(() { _impBu"
'sy = false; _impErr = res~msg; });\n}\n}\nFuture<void> _doBackupExport() async {\nif (_bakBusy) return;\n_upd(() => _bakBusy = true);\nfinal r'
'es = await _FB~exportFullBackupZip(_gRef);\nif (!mounted) return;\n_upd(() => _bakBusy = false);\nif (res~msg~isNotEmpty) _showBottomToast('
"res~msg, res~ok ? 'success' : 'error');\n}\nFuture<void> _doBackupRestore() async {\nif (_bakBusy) return;\n_upd(() => _bakBusy = true);\nfin"
'al res = await _FB~restoreFullBackupZip(_gRef);\nif (!mounted) return;\nif (res~ok) await ref~read(guardianProvider~notifier)~reloadAfterR'
"estore();\nif (!mounted) return;\n_upd(() => _bakBusy = false);\nif (res~msg~isNotEmpty) _showBottomToast(res~msg, res~ok ? 'success' : 'er"
"ror');\n}\nWidget _buildSubDelConfirmModal(BuildContext c) {\nfinal dk = _isDk(c), subId = _delSubId, subLbl = _delSubLbl;\nreturn Stack(chi"
'ldren: <Widget>[\nPositioned~fill(child: GestureDetector(behavior: _hOp, onTap: _delSubBusy ? null : () => _upd(() => _delSubId = 0), chi'
'ld: const ColoredBox(color: Color(0xB3000000)))),\nCenter(child: Padding(padding: const EdgeInsets~all(18), child: ConstrainedBox(constra'
'ints: const BoxConstraints(maxWidth: 400), child: Surface(color: _cardBg(c), child: DecoratedBox(\ndecoration: _rBox(_cardBg(c), 24, bord'
'er: _cR~withValues(alpha: dk ? 0~36 : 0~28), shadows: _e2Shadows(c)),\nchild: Padding(padding: const EdgeInsets~all(20), child: Column(ma'
'inAxisSize: MainAxisSize~min, crossAxisAlignment: _caS, spacing: 14, children: <Widget>[\nRow(spacing: 10, children: <Widget>[\nDecoratedB'
'ox(decoration: _rBox(_cR~withValues(alpha: 0~14), 12), child: const SizedBox~square(dimension: 36, child: Center(child: GlyphIcon(AppGly'
"phs~delete, size: 18, color: _cR)))),\nExpanded(child: Text('删除订阅', style: AppTextStyle~headline~of(c, emphasized: true))),\n_iconBtn(c, A"
"ppGlyphs~close, _delSubBusy ? null : () => _upd(() => _delSubId = 0)),\n]),\nText('确定要删除订阅「$subLbl」吗？删除后将同步移除该订阅的本地节点缓存及国家优先绑定。', style: A"
'ppTextStyle~body~of(c)~copyWith(color: _mu(c), height: 1~45)),\nRow(mainAxisAlignment: MainAxisAlignment~end, spacing: 10, children: <Wid'
"get>[\n_pBtn(c, '取消', _delSubBusy ? null : () => _upd(() => _delSubId = 0), height: 38),\n_pBtn(c, _delSubBusy ? '删除中~~~' : '确认删除', _delSu"
'bBusy ? null : () async {\n_upd(() => _delSubBusy = true);\nawait _FB~deleteSubById(_gRef, subId);\nif (!mounted) return;\n_expandedSubIds~r'
"emove(subId);\nif (_bindPopSubId == subId) _bindPopSubId = 0;\n_upd(() { _delSubBusy = false; _delSubId = 0; });\n_showBottomToast('已删除订阅「$"
"subLbl」', 'info');\n}, glyph: AppGlyphs~delete, solid: true, activeColor: _cR, height: 38, padding: _ehv(16, 0)),\n]),\n])),\n))))),\n]);\n}\nW"
'idget _buildSubImportModal(BuildContext c) {\nfinal dk = _isDk(c), kbB = MediaQuery~viewInsetsOf(c)~bottom, isMob = Platform~isAndroid ||'
' Platform~isIOS;\nreturn Stack(children: <Widget>[\nPositioned~fill(child: GestureDetector(behavior: _hOp, onTap: _impBusy ? null : () { F'
'ocusManager~instance~primaryFocus?~unfocus(); _upd(() => _impOpen = false); }, child: const ColoredBox(color: Color(0xB3000000)))),\nAnim'
'atedPadding(duration: const Duration(milliseconds: 160), padding: EdgeInsets~fromLTRB(12, 12, 12, math~max(12~0, kbB + 8)), child: Cente'
'r(child: ConstrainedBox(constraints: const BoxConstraints(maxWidth: 520, maxHeight: 620), child: Surface(color: _cardBg(c), child: Decor'
'atedBox(\ndecoration: _rBox(_cardBg(c), 28, border: _fg(c)~withValues(alpha: dk ? 0~12 : 0~08), shadows: _e2Shadows(c)),\nchild: Column(ma'
'inAxisSize: MainAxisSize~min, crossAxisAlignment: CrossAxisAlignment~stretch, children: <Widget>[\nPadding(padding: const EdgeInsets~from'
'LTRB(18, 15, 18, 10), child: Row(mainAxisAlignment: _mSB, children: <Widget>[\nRow(spacing: 8, children: <Widget>[\nDecoratedBox(decoratio'
'n: _rBox(_cB~withValues(alpha: dk ? 0~18 : 0~10), 10), child: SizedBox~square(dimension: 30, child: Center(child: GlyphIcon(AppGlyphs~cl'
"oudDownload, size: 16, color: dk ? _cD : _cB)))),\nText('新增订阅', style: AppTextStyle~headline~of(c, emphasized: true)),\n]),\n_iconBtn(c, Ap"
'pGlyphs~close, _impBusy ? null : () { FocusManager~instance~primaryFocus?~unfocus(); _upd(() => _impOpen = false); }),\n])),\nFlexible(chi'
'ld: SingleChildScrollView(padding: const EdgeInsets~fromLTRB(18, 6, 18, 16), child: Column(crossAxisAlignment: CrossAxisAlignment~stretc'
'h, spacing: 12, children: <Widget>[\nif (_impErr~isNotEmpty) DecoratedBox(decoration: _rBox(_cR~withValues(alpha: 0~14), 14, border: _cR~'
'withValues(alpha: 0~36)), child: Padding(padding: _ehv(12, 9), child: Row(spacing: 8, children: <Widget>[\nconst GlyphIcon(AppGlyphs~warn'
'ing, size: 15, color: _cR),\nExpanded(child: Text(_impErr, style: _sC1(c)~copyWith(color: _cR))),\n]))),\nColumn(crossAxisAlignment: _caS, '
"spacing: 6, children: <Widget>[\nRow(mainAxisAlignment: _mSB, children: <Widget>[\nText('订阅地址 / 节点分享链接', style: _sC1(c)),\nGestureDetector("
"behavior: _hOp, onTap: () async {\nfinal data = await Clipboard~getData('text/plain');\nfinal txt = data?~text?~trim() ?? '';\nif (txt~isNo"
"tEmpty && mounted) { _impUrlCtrl~text = txt; _upd(() => _impErr = ''); }\n}, child: Row(mainAxisSize: MainAxisSize~min, spacing: 4, child"
"ren: <Widget>[\nGlyphIcon(AppGlyphs~paste, size: 13, color: dk ? _cD : _cB),\nText('粘贴剪贴板', style: _sC1(c)~copyWith(color: dk ? _cD : _cB)"
'),\n])),\n]),\nDecoratedBox(decoration: _blockDeco(c, r: 14), child: Padding(padding: _ehv(12, 9), child: TextField(\ncontroller: _impUrlCtr'
'l,\nfocusNode: _impUrlFocus,\nminLines: 2,\nmaxLines: 4,\nautocorrect: false,\ncursorColor: _cB,\nonChanged: (_) { if (_impErr~isNotEmpty) _up'
"d(() => _impErr = ''); },\nstyle: AppTextStyle~body~of(c)~copyWith(color: _fg(c)),\ndecoration: InputDecoration~collapsed(\nborder: const N"
"oInputBorder(),\nhintText: 'https://~~~ 或多行 vless:// vmess:// hy2:// ss://',\nhintStyle: AppTextStyle~body~of(c)~copyWith(color: _mu(c)),\n"
"),\n))),\n]),\nRow(spacing: 8, children: <Widget>[\nExpanded(child: Column(crossAxisAlignment: _caS, spacing: 5, children: <Widget>[Text('显示"
"名称（选填）', style: _sC1(c)), _inp(c, _impNameCtrl, _impNameFocus, '自动识别名称', _impNameCtrl~text, (_) {})])),\nExpanded(child: Column(crossAxis"
"Alignment: _caS, spacing: 5, children: <Widget>[Text('Age 私钥（选填）', style: _sC1(c)), _inp(c, _impAgeCtrl, _impAgeFocus, 'AGE-SECRET-KEY~~"
"~', _impAgeCtrl~text, (_) {})])),\n]),\n_bentoActionTile(c, glyph: AppGlyphs~cloudDownload, label: _impBusy ? '正在拉取并校验订阅~~~' : '立即拉取并导入', "
'onTap: _impBusy ? null : () => unawaited(_doImportUrl()), solid: true, activeColor: _cB, height: 46),\nDecoratedBox(decoration: BoxDecora'
'tion(border: Border(top: BorderSide(color: _fg(c)~withValues(alpha: dk ? 0~08 : 0~06)))), child: Padding(padding: const EdgeInsets~only('
"top: 12), child: Column(crossAxisAlignment: _caS, spacing: 8, children: <Widget>[\n_txt(c, '其他导入方式', cap: true, b: true),\nRow(spacing: 8,"
" children: <Widget>[\nExpanded(child: _bentoActionTile(c, glyph: AppGlyphs~importFile, label: '本地 YAML 文件', onTap: _impBusy ? null : () a"
'sync {\n_upd(() => _impOpen = false);\nfinal r = await _FB~importSubFromLocalFile(_gRef);\nif (mounted && r~msg~isNotEmpty) _showBottomToas'
"t(r~msg, r~ok ? 'success' : 'error');\n}, height: 44)),\nif (isMob) Expanded(child: _bentoActionTile(c, glyph: AppGlyphs~camera, label: '相"
"机扫码', onTap: _impBusy ? null : () async {\n_upd(() => _impOpen = false);\nfinal r = await _FB~importSubFromQr(c, _gRef);\nif (mounted && r~"
"msg~isNotEmpty) _showBottomToast(r~msg, r~ok ? 'success' : 'error');\n}, height: 44)),\nExpanded(child: _bentoActionTile(c, glyph: AppGlyp"
"hs~qrCode, label: isMob ? '相册识码' : '识别二维码图', onTap: _impBusy ? null : () async {\n_upd(() => _impOpen = false);\nfinal r = await _FB~impor"
"tSubFromQr(c, _gRef, fromGallery: true);\nif (mounted && r~msg~isNotEmpty) _showBottomToast(r~msg, r~ok ? 'success' : 'error');\n}, height"
': 44)),\n]),\n]))),\n]))),\n]),\n))))),\n]);\n}\nWidget _buildHkRecorderModal(BuildContext c) {\nfinal dk = _isDk(c), act = _hkRecAct;\nif (ac'
't == null) return const SizedBox~shrink();\nfinal labels = ShortcutLabels~host();\nfinal hasKey = _hkRecKey != null, valid = isValidHotKey'
'(_hkRecMods, _hkRecKey);\nfinal invalid = hasKey && !valid;\nfinal conflict = valid ? _FB~checkHotKeyConflictTitle(ref, act, _hkRecMods, _'
'hkRecKey) : null;\nfinal capParts = hasKey ? labels~parts(_hkRecMods, _hkRecKey!) : (_hkRecMods~isNotEmpty ? <String>[~~~labels~modifierP'
"arts(_hkRecMods), '…'] : const <String>[]);\nreturn Stack(children: <Widget>[\nPositioned~fill(child: GestureDetector(behavior: _hOp, onTa"
'p: _closeHkRecorder, child: const ColoredBox(color: Color(0xB3000000)))),\nCenter(child: Padding(padding: const EdgeInsets~all(18), child'
': ConstrainedBox(constraints: const BoxConstraints(maxWidth: 420), child: Focus(autofocus: true, onKeyEvent: (_, _) => KeyEventResult~ha'
'ndled, child: Surface(color: _cardBg(c), child: DecoratedBox(\ndecoration: _rBox(_cardBg(c), 26, border: (invalid ? _cR : _cB)~withValues'
'(alpha: 0~42), shadows: _e2Shadows(c)),\nchild: Padding(padding: const EdgeInsets~all(20), child: Column(mainAxisSize: MainAxisSize~min, '
'crossAxisAlignment: _caS, spacing: 14, children: <Widget>[\nRow(mainAxisAlignment: _mSB, children: <Widget>[\nRow(spacing: 8, children: <W'
'idget>[GlyphIcon(AppGlyphs~keyboard, size: 18, color: dk ? _cD : _cB), Text(_hkRecTitle, style: AppTextStyle~headline~of(c, emphasized: '
'true))]),\n_iconBtn(c, AppGlyphs~close, _closeHkRecorder),\n]),\nDecoratedBox(\ndecoration: _rBox(_blockBg(c), 18, border: (invalid ? _cR : '
'(valid ? _cP : _cB))~withValues(alpha: 0~45), borderWidth: 1~4),\nchild: SizedBox(height: 86, child: Center(child: capParts~isEmpty ? Tex'
"t('请直接按下组合键（如 Ctrl + Alt + S）', style: AppTextStyle~body~of(c)~copyWith(color: _mu(c))) : Wrap(spacing: 8, runSpacing: 8, alignment: Wra"
'pAlignment~center, children: <Widget>[\nfor (final p in capParts) DecoratedBox(decoration: _rBox(invalid ? _cR~withValues(alpha: 0~16) : '
'_cardBg(c), 10, border: _fg(c)~withValues(alpha: dk ? 0~16 : 0~10)), child: Padding(padding: _ehv(12, 8), child: Text(p, style: AppTextS'
"tyle~headline~of(c, emphasized: true)~copyWith(color: invalid ? _cR : _fg(c))))),\n]))),\n),\nif (invalid) Text('全局快捷键必须至少包含一个修饰键（${labels~"
'modifierParts(primaryHotKeyModifiers)~join(" / ")}）\', style: _sC1(c)~copyWith(color: _cR))\nelse if (conflict != null) Text(\'提示：该组合键当前已被「'
"$conflict」使用，保存后将自动接管。', style: _sC1(c)~copyWith(color: _cW)),\nRow(mainAxisAlignment: MainAxisAlignment~end, spacing: 8, children: <Widg"
"et>[\nif (_hkRecHadOld) _pBtn(c, '清除绑定', () {\n_FB~saveHotKeyRow(ref, act, const <KeyboardModifier>{}, null);\n_closeHkRecorder();\n_showBot"
"tomToast('已清除「$_hkRecTitle」快捷键', 'info');\n}, active: true, activeColor: _cR, height: 38),\n_pBtn(c, '取消', _closeHkRecorder, height: 38),\n"
"_pBtn(c, '保存快捷键', valid ? () {\nfinal savedText = labels~text(_hkRecMods, _hkRecKey!);\n_FB~saveHotKeyRow(ref, act, _hkRecMods, _hkRecKey)"
";\n_closeHkRecorder();\n_showBottomToast('已绑定 $_hkRecTitle：$savedText', 'success');\n} : null, glyph: AppGlyphs~check, solid: true, activeC"
'olor: _cB, height: 38, padding: _ehv(15, 0)),\n]),\n])),\n)))))),\n]);\n}\nWidget _buildSettingsPage(BuildContext c, GuardianState st, bool ru'
'n, bool isDesktop) {\nfinal dk = _isDk(c), sysCfg = _FB~watchSysSettings(ref), themeCfg = _FB~watchThemeCfg(ref);\nWidget segTab(String id'
', Glyph glyph, String lbl, {String? badgeTxt}) {\nfinal sel = _setSect == id;\nreturn Expanded(child: ElasticPress(child: GestureDetector('
"\nbehavior: _hOp,\nonTap: () {\nif (_setSect == id) return;\nHapticFeedback~selectionClick();\n_upd(() => _setSect = id);\nif (id == 'conns') "
'unawaited(_refreshConnsSnapshot());\n},\nchild: DecoratedBox(\ndecoration: _rBox(sel ? _cB : const Color(0x00000000), 14, gradient: sel ? _'
'gPri : null),\nchild: SizedBox(height: 40, child: Center(child: Padding(padding: _ehv(6, 0), child: FittedBox(fit: BoxFit~scaleDown, chil'
'd: Row(mainAxisSize: MainAxisSize~min, spacing: 6, children: <Widget>[\nGlyphIcon(glyph, size: 15~5, color: sel ? _cWht : _mu(c)),\nText(l'
'bl, style: _sC1(c)~copyWith(color: sel ? _cWht : _fg(c), fontWeight: sel ? FontWeight~w700 : FontWeight~w600)),\nif (badgeTxt != null && '
'badgeTxt~isNotEmpty) DecoratedBox(decoration: _rBox(sel ? _cWht~withValues(alpha: 0~22) : _fg(c)~withValues(alpha: 0~08), 99), child: Pa'
'dding(padding: _ehv(6, 1~5), child: Text(badgeTxt, style: _sC2(c)~copyWith(color: sel ? _cWht : _mu(c))))),\n]))))),\n),\n)));\n}\nWidget swR'
'ow({required Glyph glyph, required String title, required String sub, required bool val, required VoidCallback onToggle, Color accent = '
'_cP}) {\nreturn DecoratedBox(decoration: _blockDeco(c, r: 16), child: Padding(padding: _ehv(13, 11), child: Row(spacing: 11, children: <W'
'idget>[\nDecoratedBox(decoration: _rBox((val ? accent : _cN)~withValues(alpha: dk ? 0~18 : 0~11), 11), child: SizedBox~square(dimension: '
'34, child: Center(child: GlyphIcon(glyph, size: 17, color: val ? accent : _mu(c))))),\nExpanded(child: Column(crossAxisAlignment: _caS, s'
'pacing: 2, children: <Widget>[\nText(title, style: _sC1(c)~copyWith(fontSize: 13~5)),\nText(sub, style: _sC2(c, b: false)~copyWith(color: '
'_mu(c))),\n])),\n_sw(val, accent, () { HapticFeedback~selectionClick(); onToggle(); }),\n])));\n}\nWidget buildSysAndBackupSection() {\nWidget'
' themeChip(ThemeMode m, Glyph g, String lbl) {\nfinal sel = themeCfg~mode == m;\nreturn Expanded(child: _bentoActionTile(c, glyph: g, labe'
'l: lbl, onTap: () { HapticFeedback~selectionClick(); _FB~updateThemeCfg(ref, mode: m); }, solid: sel, activeColor: _cB, height: 44));\n}\n'
'final themeCard = DecoratedBox(decoration: _cardDeco(c), child: Padding(padding: const EdgeInsets~all(16), child: Column(crossAxisAlignm'
'ent: _caS, spacing: 12, children: <Widget>[\nRow(mainAxisAlignment: _mSB, children: <Widget>[\nRow(spacing: 8, children: <Widget>[GlyphIco'
"n(AppGlyphs~sun, size: 17, color: dk ? _cD : _cB), Text('外观与显示模式', style: _sSb(c))]),\n_badge(c, switch (themeCfg~mode) { ThemeMode~syste"
"m => '跟随系统', ThemeMode~light => '浅色模式', ThemeMode~dark => '深色模式' }, _cB),\n]),\nRow(spacing: 8, children: <Widget>[\nthemeChip(ThemeMode~sy"
"stem, AppGlyphs~devices, '跟随系统'),\nthemeChip(ThemeMode~light, AppGlyphs~sun, '浅色'),\nthemeChip(ThemeMode~dark, AppGlyphs~pureBlack, '深色'),"
"\n]),\nif (themeCfg~mode != ThemeMode~light) swRow(glyph: AppGlyphs~pureBlack, title: '纯黑深色背景 (OLED)', sub: '深色模式下采用纯黑底色，降低屏幕功耗并增强对比度', va"
'l: themeCfg~pureBlack, accent: _cB, onToggle: () => _FB~updateThemeCfg(ref, pureBlack: !themeCfg~pureBlack)),\n])));\nfinal bootCard = Dec'
'oratedBox(decoration: _cardDeco(c), child: Padding(padding: const EdgeInsets~all(16), child: Column(crossAxisAlignment: _caS, spacing: 1'
"0, children: <Widget>[\nRow(spacing: 8, children: <Widget>[GlyphIcon(AppGlyphs~bolt, size: 17, color: dk ? _cD : _cB), Text('启动与系统体验', st"
"yle: _sSb(c))]),\nswRow(glyph: AppGlyphs~bolt, title: '打开软件自动开启代理', sub: 'BlueClash 启动就绪后自动拉起核心分流接管', val: sysCfg~autoRun, onToggle: () ="
"> _FB~updateSysSetting(ref, autoRun: !sysCfg~autoRun)),\nif (_kDesktop) ~~~<Widget>[\nswRow(glyph: AppGlyphs~verified, title: '开机自动启动', su"
"b: '登录桌面系统时自动在后台启动 BlueClash', val: sysCfg~autoLaunch, onToggle: () => _FB~updateSysSetting(ref, autoLaunch: !sysCfg~autoLaunch)),\nswRow"
"(glyph: AppGlyphs~eyeOff, title: '静默最小化启动', sub: '启动时不弹出主窗口，直接驻留系统托盘运行', val: sysCfg~silentLaunch, accent: _cB, onToggle: () => _FB~upda"
"teSysSetting(ref, silentLaunch: !sysCfg~silentLaunch)),\nswRow(glyph: AppGlyphs~pin, title: '关闭窗口最小化到托盘', sub: '点击右上角关闭按钮时隐藏到托盘而非退出核心', v"
'al: sysCfg~minimizeOnExit, accent: _cB, onToggle: () => _FB~updateSysSetting(ref, minimizeOnExit: !sysCfg~minimizeOnExit)),\nswRow(glyph:'
" AppGlyphs~speed, title: '托盘显示实时网速', sub: '在状态栏/托盘菜单同步展示当前上下行速率', val: sysCfg~showTrayTitle, accent: _cD, onToggle: () => _FB~updateSysS"
"etting(ref, showTrayTitle: !sysCfg~showTrayTitle)),\n],\nif (Platform~isAndroid) swRow(glyph: AppGlyphs~vpn, title: '通知栏常驻停止按钮', sub: '在 A"
"ndroid 前台通知栏显示一键停止 VPN 快捷按钮', val: sysCfg~notifStop, accent: _cB, onToggle: () => _FB~updateSysSetting(ref, notifStop: !sysCfg~notifStop"
')),\n])));\nfinal backupCard = DecoratedBox(decoration: _cardDeco(c), child: Padding(padding: const EdgeInsets~all(16), child: Column(cros'
'sAxisAlignment: _caS, spacing: 12, children: <Widget>[\nRow(mainAxisAlignment: _mSB, children: <Widget>[\nRow(spacing: 8, children: <Widge'
"t>[GlyphIcon(AppGlyphs~cloudSync, size: 17, color: dk ? _cD : _cB), Text('本地一键备份与恢复', style: _sSb(c))]),\n_badge(c, '全量 ZIP', _cP),\n]),\nD"
"ecoratedBox(decoration: _blockDeco(c, r: 14), child: Padding(padding: _ehv(12, 10), child: Text('打包保存全部远程/本地订阅、国家白名单、AI 厂商与自定义分流、专享浏览器、伴"
"生白名单、全局限速黑名单以及桌面快捷键与主题配置。', style: _sC2(c, b: false)~copyWith(color: _mu(c), height: 1~45)))),\nRow(spacing: 10, children: <Widget>[\nExpa"
"nded(child: _bentoActionTile(c, glyph: AppGlyphs~export, label: _bakBusy ? '正在打包~~~' : '导出完整备份', onTap: _bakBusy ? null : () => unawaite"
'd(_doBackupExport()), solid: true, activeColor: _cB, height: 46)),\nExpanded(child: _bentoActionTile(c, glyph: AppGlyphs~importFile, labe'
"l: _bakBusy ? '正在恢复~~~' : '从备份文件恢复', onTap: _bakBusy ? null : () => unawaited(_doBackupRestore()), active: true, activeColor: _cP, heigh"
't: 46)),\n]),\n])));\nWidget? hotKeyCard;\nif (_kDesktop) {\nfinal hkRows = _FB~watchHotKeyRows(ref);\nhotKeyCard = DecoratedBox(decoration: _'
'cardDeco(c), child: Padding(padding: const EdgeInsets~all(16), child: Column(crossAxisAlignment: _caS, spacing: 10, children: <Widget>[\n'
'Row(mainAxisAlignment: _mSB, children: <Widget>[\nRow(spacing: 8, children: <Widget>[GlyphIcon(AppGlyphs~keyboard, size: 17, color: dk ? '
"_cD : _cB), Text('桌面全局快捷键', style: _sSb(c))]),\n_badge(c, '点击录制', _cD),\n]),\nfor (final r in hkRows) ElasticPress(child: GestureDetector(\n"
'behavior: _hOp,\nonTap: () => _openHkRecorder(r~action, r~title, r~modifiers, r~key),\nchild: DecoratedBox(decoration: _blockDeco(c, r: 15'
'), child: Padding(padding: _ehv(13, 10), child: Row(spacing: 10, children: <Widget>[\nExpanded(child: Column(crossAxisAlignment: _caS, sp'
"acing: 2, children: <Widget>[\nText(r~title, style: _sC1(c)~copyWith(fontSize: 13~2)),\nText(r~err != null ? '注册冲突：${r~err}' : r~subtitle,"
' maxLines: 1, overflow: TextOverflow~ellipsis, style: _sC2(c, b: false)~copyWith(color: r~err != null ? _cR : _mu(c))),\n])),\nif (r~caps~'
"isEmpty) _badge(c, '未设置', _cN)\nelse Row(mainAxisSize: MainAxisSize~min, spacing: 5, children: <Widget>[\nfor (final cp in r~caps) Decorat"
'edBox(decoration: _rBox(r~err != null ? _cR~withValues(alpha: 0~15) : _cardBg(c), 8, border: _fg(c)~withValues(alpha: dk ? 0~14 : 0~09))'
', child: Padding(padding: _ehv(7, 3~5), child: Text(cp, style: _sC2(c)~copyWith(color: r~err != null ? _cR : _fg(c))))),\nGestureDetector'
"(behavior: _hOp, onTap: () { _FB~saveHotKeyRow(ref, r~action, const <KeyboardModifier>{}, null); _showBottomToast('已清除「${r~title}」快捷键', "
"'info'); }, child: DecoratedBox(decoration: _rBox(_cR~withValues(alpha: 0~12), 8), child: const SizedBox~square(dimension: 24, child: Ce"
'nter(child: GlyphIcon(AppGlyphs~close, size: 13, color: _cR))))),\n]),\n]))),\n)),\n])));\n}\nif (isDesktop && hotKeyCard != null) {\nreturn Co'
'lumn(crossAxisAlignment: CrossAxisAlignment~stretch, spacing: 14, children: <Widget>[\nRow(crossAxisAlignment: CrossAxisAlignment~start, '
'spacing: 14, children: <Widget>[\nExpanded(child: Column(crossAxisAlignment: CrossAxisAlignment~stretch, spacing: 14, children: <Widget>['
'themeCard, backupCard])),\nExpanded(child: bootCard),\n]),\nhotKeyCard,\n]);\n}\nreturn Column(crossAxisAlignment: CrossAxisAlignment~stretch,'
' spacing: 14, children: <Widget>[themeCard, bootCard, backupCard, if (hotKeyCard != null) hotKeyCard]);\n}\nWidget buildLiveConnsSection()'
' {\nfinal q = _connQ~trim()~toLowerCase();\nfinal filtered = q~isEmpty ? _liveConns : <BridgeConn>[for (final cn in _liveConns) if (cn~tar'
'get~toLowerCase()~contains(q) || cn~host~toLowerCase()~contains(q) || cn~ip~toLowerCase()~contains(q) || cn~proc~toLowerCase()~contains('
'q) || cn~net~toLowerCase()~contains(q) || cn~chains~any((x) => x~toLowerCase()~contains(q))) cn];\nreturn DecoratedBox(decoration: _cardD'
'eco(c), child: Padding(padding: const EdgeInsets~all(16), child: Column(crossAxisAlignment: _caS, spacing: 12, children: <Widget>[\nRow(m'
'ainAxisAlignment: _mSB, spacing: 8, children: <Widget>[\nFlexible(child: Row(mainAxisSize: MainAxisSize~min, spacing: 8, children: <Widge'
"t>[\nGlyphIcon(AppGlyphs~connections, size: 17, color: dk ? _cD : _cB),\nFlexible(child: Text('全局实时域名连接流水', maxLines: 1, overflow: TextOve"
"rflow~ellipsis, style: _sSb(c))),\n_badge(c, '${filtered~length}/${_liveConns~length}', run ? _cP : _cN, dot: run && !_connPaused),\n])),\n"
"Row(mainAxisSize: MainAxisSize~min, spacing: 6, children: <Widget>[\n_pBtn(c, _connPaused ? '继续' : '暂停', () { _upd(() => _connPaused = !_"
"connPaused); if (!_connPaused) unawaited(_refreshConnsSnapshot()); }, active: _connPaused, activeColor: _cW, height: 32),\n_pBtn(c, '刷新',"
" () => unawaited(_refreshConnsSnapshot()), glyph: AppGlyphs~refresh, height: 32),\nif (_liveConns~isNotEmpty) _pBtn(c, '全断', () async {\nf"
"inal n = await _FB~closeAllActiveConns(_gRef);\nawait _refreshConnsSnapshot();\nif (mounted) _showBottomToast('已断开 $n 条活跃连接', 'info');\n}, "
"glyph: AppGlyphs~close, active: true, activeColor: _cR, height: 32),\n]),\n]),\n_inp(c, _connSearchCtrl, _connSearchFocus, '搜索域名 / 目标 IP / "
"进程名 / 出口节点 / TCP·UDP~~~', _connQ, (v) => _upd(() => _connQ = v)),\nif (!run && _liveConns~isEmpty) DecoratedBox(decoration: _blockDeco(c,"
" r: 16), child: Padding(padding: const EdgeInsets~all(22), child: Center(child: _txt(c, '代理尚未运行，开启接管后将在此实时显示全局域名与连接流向', cap: true))))\nel"
'se if (filtered~isEmpty) DecoratedBox(decoration: _blockDeco(c, r: 16), child: Padding(padding: const EdgeInsets~all(22), child: Center('
"child: _txt(c, q~isEmpty ? '当前暂无活跃连接' : '无匹配的连接记录', cap: true))))\nelse Column(crossAxisAlignment: CrossAxisAlignment~stretch, spacing: 8"
", children: <Widget>[\nfor (final cn in filtered~take(100)) () {\nfinal isDir = cn~chains~contains('DIRECT'), isRej = cn~chains~any((x) =>"
" x~toUpperCase()~contains('REJECT'));\nfinal routeCol = isRej ? _cR : (isDir ? _cD : _cP);\nfinal chainTxt = cn~chains~isEmpty ? 'DIRECT' "
": cn~chains~reversed~join(' → ');\nfinal procName = cn~proc~trim()~isNotEmpty ? cn~proc~trim()~split(RegExp(r'[/\\\\]'))~last : '系统/未知进程';\n"
'return DecoratedBox(decoration: _blockDeco(c, r: 15), child: Padding(padding: _ehv(12, 10), child: Row(spacing: 10, children: <Widget>[\n'
'Expanded(child: Column(crossAxisAlignment: _caS, spacing: 4, children: <Widget>[\nRow(spacing: 6, children: <Widget>[\n_badge(c, cn~net~to'
"UpperCase(), routeCol),\nExpanded(child: Text(cn~target~isNotEmpty ? cn~target : (cn~ip~isNotEmpty ? cn~ip : '未知目标'), maxLines: 1, overfl"
'ow: TextOverflow~ellipsis, style: _sC1(c)~copyWith(fontSize: 13))),\n]),\nText(\'$procName${cn~ip~isNotEmpty && cn~host~isNotEmpty ? " · ${'
'cn~ip}" : ""} · $chainTxt\', maxLines: 1, overflow: TextOverflow~ellipsis, style: _sC2(c, b: false)~copyWith(color: _mu(c))),\n])),\nText(\''
"↑${fmtBytes(cn~up)}\\n↓${fmtBytes(cn~down)}', textAlign: TextAlign~right, style: _sC2(c)~copyWith(color: _mu(c), fontFeatures: const <Fon"
'tFeature>[FontFeature~tabularFigures()])),\nGestureDetector(behavior: _hOp, onTap: () async { await _FB~closeConn(_gRef, cn~id); await _r'
'efreshConnsSnapshot(); }, child: DecoratedBox(decoration: _rBox(_cR~withValues(alpha: 0~12), 8), child: const SizedBox~square(dimension:'
' 26, child: Center(child: GlyphIcon(AppGlyphs~close, size: 13~5, color: _cR))))),\n])));\n}(),\n]),\n])));\n}\nWidget buildCoreLogsSection() {'
'\nfinal curLv = _FB~watchCoreLogLevel(ref), rawLogs = _FB~watchCoreLogsFull(ref), q = _logQ~trim()~toLowerCase();\nfinal logs = q~isEmpty '
'? rawLogs : <BridgeLog>[for (final lg in rawLogs) if (lg~payload~toLowerCase()~contains(q) || lg~level~toLowerCase()~contains(q)) lg];\nr'
'eturn DecoratedBox(decoration: _cardDeco(c), child: Padding(padding: const EdgeInsets~all(16), child: Column(crossAxisAlignment: _caS, s'
'pacing: 12, children: <Widget>[\nRow(mainAxisAlignment: _mSB, spacing: 8, children: <Widget>[\nRow(mainAxisSize: MainAxisSize~min, spacing'
": 8, children: <Widget>[\nGlyphIcon(AppGlyphs~logs, size: 17, color: dk ? _cD : _cB),\nText('Mihomo 内核日志', style: _sSb(c)),\n_badge(c, '${l"
"ogs~length} 条', _cB),\n]),\nRow(mainAxisSize: MainAxisSize~min, spacing: 6, children: <Widget>[\n_pBtn(c, '复制', logs~isEmpty ? null : () {\n"
"final txt = logs~take(120)~map((e) => '[${e~time}] [${e~level~toUpperCase()}] ${e~payload}')~join('\\n');\nClipboard~setData(ClipboardData"
"(text: txt));\n_showBottomToast('已复制最近 ${math~min(120, logs~length)} 条内核日志', 'success');\n}, glyph: AppGlyphs~copy, height: 32),\n_pBtn(c, "
"'导出', () => unawaited(_FB~exportCoreLogsFile(ref, <String>[for (final g in st~logs) '[${g~time~toIso8601String()}] [${g~cat~name}] ${g~t"
"itle} | ${g~detail}'])), glyph: AppGlyphs~export, solid: true, activeColor: _cB, height: 32),\nif (rawLogs~isNotEmpty) _pBtn(c, '清空', () "
"{ _FB~clearCoreLogs(ref); _showBottomToast('已清空当前日志缓存', 'info'); }, glyph: AppGlyphs~broom, height: 32),\n]),\n]),\nSingleChildScrollView(s"
"crollDirection: Axis~horizontal, child: Row(spacing: 6, children: <Widget>[\n_txt(c, '日志级别：', cap: true, b: true),\nfor (final lv in const"
' <LogLevel>[LogLevel~info, LogLevel~warning, LogLevel~error, LogLevel~debug, LogLevel~silent])\n_pBtn(c, lv~name~toUpperCase(), () => _FB'
'~setCoreLogLevel(ref, lv), solid: curLv == lv, activeColor: _cB, height: 28, padding: _ehv(10, 0)),\n])),\n_inp(c, _logSearchCtrl, _logSea'
"rchFocus, '过滤日志关键词 / 域名 / 错误类型（点击单条可复制）~~~', _logQ, (v) => _upd(() => _logQ = v)),\nif (logs~isEmpty) DecoratedBox(decoration: _blockDeco"
"(c, r: 16), child: Padding(padding: const EdgeInsets~all(22), child: Center(child: _txt(c, rawLogs~isEmpty ? '暂无内核日志输出' : '未匹配到相关日志', ca"
'p: true))))\nelse Column(crossAxisAlignment: CrossAxisAlignment~stretch, spacing: 7, children: <Widget>[\nfor (final lg in logs~take(120))'
" () {\nfinal lvLow = lg~level~toLowerCase();\nfinal lvCol = lvLow~contains('err') ? _cR : (lvLow~contains('warn') ? _cW : (lvLow~contains("
"'debug') ? _cN : _cB));\nfinal shortTime = lg~time~length >= 19 ? lg~time~substring(11, 19) : lg~time;\nreturn GestureDetector(\nbehavior: "
"_hOp,\nonTap: () { Clipboard~setData(ClipboardData(text: '[${lg~time}] [${lg~level~toUpperCase()}] ${lg~payload}')); _showBottomToast('已复"
"制该条日志', 'success'); },\nchild: DecoratedBox(decoration: _blockDeco(c, r: 13), child: Padding(padding: _ehv(11, 8~5), child: Column(crossA"
'xisAlignment: _caS, spacing: 4, children: <Widget>[\nRow(mainAxisAlignment: _mSB, children: <Widget>[\n_badge(c, lg~level~toUpperCase(), l'
'vCol),\nText(shortTime, style: _sC2(c, b: false)~copyWith(color: _mu(c), fontFeatures: const <FontFeature>[FontFeature~tabularFigures()])'
'),\n]),\nText(lg~payload, style: _sC2(c, b: false)~copyWith(color: _fg(c), height: 1~38)),\n]))),\n);\n}(),\n]),\n])));\n}\nreturn Column(cro'
'ssAxisAlignment: CrossAxisAlignment~stretch, spacing: 14, children: <Widget>[\nDecoratedBox(decoration: _cardDeco(c), child: Padding(padd'
"ing: const EdgeInsets~all(6), child: Row(spacing: 4, children: <Widget>[\nsegTab('sys', AppGlyphs~settings, '系统与备份'),\nsegTab('conns', App"
"Glyphs~connections, '实时连接', badgeTxt: _liveConns~isNotEmpty ? '${_liveConns~length}' : null),\nsegTab('logs', AppGlyphs~logs, '内核日志'),\n])"
")),\nif (_setSect == 'conns') buildLiveConnsSection() else if (_setSect == 'logs') buildCoreLogsSection() else buildSysAndBackupSection()"
',\n]);\n}')
def ck_b(): assert hashlib .sha256(repr((SWC13, SWC13_EXT)) .encode('utf-8')) .hexdigest()[:12] == '87b35beadf0e'
_u = lambda x: x .replace('~', '.')
_s = lambda s, h, t, v: (lambda i: s[:i] + v + (s[i + len(h):] if t == '=' else s[s .index(t, i + len(h)):]))(s .index(h))
_r = lambda s, x: _s(s, _u(x[0]), _u(x[1]), _u(x[2]))
def _w(p, ns, tx): p .write_text((ns .rstrip()[:-1] + _u(tx) + '\n}\n') if tx else ns, 'utf-8')
def _p(d, f, m, ps, tx=''): p = d / (f + _u('~dart')); s = p .read_text('utf-8'); _w(p, functools .reduce(_r, ps, s), tx) if _u(m) not in s else 0
HKI13 = "import 'package:fl_clash/custom/flclash_bridge~dart';\nimport 'package:fl_clash/custom/smart_guardian~dart';\n"
def _f(p, s): p .write_text(_u(s), 'utf-8') if p .exists() else 0
HKS13 = "import 'package:fl_clash/providers/state~dart';\n"
def _hk(kp): ks = kp .read_text('utf-8') .replace(_u(HKS13), ''); kp .write_text(_u(HKI13) + ks .replace(_u(us13a .HKO13), _u(us13a .HKN13), 1), 'utf-8') if ('guardianProvider' not in ks and _u(us13a .HKO13) in ks) else 0
def _rt(od): r = od .parent .parent; _f(r / _u('lib/pages/home~dart'), us13a .HOME13); _f(r / _u('lib/views/navigation~dart'), us13a .NAV13); kp = r / _u('lib/manager/hotkey_manager~dart'); _hk(kp) if kp .exists() else 0
def _a1(od): us13a .ck_a(); ck_b(); _p(od, 'flclash_bridge', 'v128_pure_core_bridge', us13a .FB13); _p(od, 'smart_guardian', 'v128_pure_guardian', us13a .SG13)
def apply_v128(od): _a1(od); _p(od, 'simple_workbench', 'v128_eight_tab_pure_ui', us13a .SW13); _p(od, 'simple_workbench_cards', 'v128_sub_del_and_settings', SWC13, SWC13_EXT); _rt(od)
