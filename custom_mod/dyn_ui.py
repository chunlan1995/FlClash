def patch_dyn_ui(name: str, txt: str) -> str:
    if name == 'simple_workbench.dart':
        for s in ("const _vendorExitOpts = <String>['US','JP','SG','HK','TW','KR','FOLLOW']; ", "const _browserExitOpts = <String>['SG','HK','TW','JP','KR','US','GB','DE','FR','NL','CA','AU','FOLLOW'];\n", "const _subExitOpts = <String>['US','JP','SG','HK','TW','KR','DIRECT']; "):
            assert s in txt, s
            txt = txt.replace(s, "", 1)
        reps = [
            ("bool _isDel(VendorSpec v) => v.id.startsWith('custom_grp_');", "bool _isDel(VendorSpec v) => v.id.startsWith('custom_grp_');\nList<String> _cfgRegs(GuardianState st, [String cur = '']) { final b = st.regs.isNotEmpty ? <String>[for (final r in st.regs) r.code] : FlClashBridge.mRegs; return <String>[...b, if (FlClashBridge.isValidRegCode(cur) && !b.contains(cur)) cur]; } List<String> _exitOpts(GuardianState st, [String cur = '', String tail = 'FOLLOW']) => <String>[..._cfgRegs(st, cur), if (tail.isNotEmpty) tail];"),
            ("Widget _bakPill(BuildContext c, String hiCode,", "String _menuRegLbl(GuardianState st, String code) { if (code == 'FOLLOW') return '🌐 跟随主干出口'; if (code == 'DIRECT') return '🛡 物理直连'; final h = st.regs.where((r) => r.code == code).firstOrNull; if (h != null) return '${h.label} (${h.nodes.length}节点${h.bestMs > 0 ? \" · ${h.bestMs}ms\" : \"\"})'; return st.regs.isEmpty ? FlClashBridge.regLblOf(code) : '${FlClashBridge.regLblOf(code)} (当前配置无节点)'; } String _pillRegLbl(GuardianState st, String code) { final base = FlClashBridge.regLblOf(code); if (!FlClashBridge.isValidRegCode(code) || st.regs.isEmpty || st.regs.any((r) => r.code == code)) return base; return '$base(无节点)'; } Widget _bakPill(BuildContext c, GuardianState st, String hiCode,"),
            ("final lbl = hasB ? '低优: ${FlClashBridge.regLblOf(bakCode)} ▾' : '低优备选: 未设 ▾'; return PopupAnchor(", "final lbl = hasB ? '低优: ${_pillRegLbl(st, bakCode)} ▾' : '低优备选: 未设 ▾'; final opts = _cfgRegs(st, hasB ? bakCode : ''); return PopupAnchor("),
            ("for (final code in FlClashBridge.mRegs) if (code != hiCode) PopupMenuItem(glyph: bakCode == code ? AppGlyphs.check : null, label: '低优备选 → ${FlClashBridge.regLblOf(code)}'", "for (final code in opts) if (code != hiCode) PopupMenuItem(glyph: bakCode == code ? AppGlyphs.check : null, label: '低优备选 → ${_menuRegLbl(st, code)}'"),
            ("Widget _exPill(BuildContext c, String currentCode,", "Widget _exPill(BuildContext c, GuardianState st, String currentCode,"),
            ("'$prefix${FlClashBridge.regLblOf(currentCode)} ▾'", "'$prefix${_pillRegLbl(st, currentCode)} ▾'"),
            ("label: FlClashBridge.regLblOf(code), onPressed: () => onPick(code))", "label: _menuRegLbl(st, code), onPressed: () => onPick(code))"),
            ("final gid = await ntf.createCustomGroup(name: '$baseLbl 专享组', badge: baseLbl, exitCode: 'SG', bakExitCode: 'HK');", "final defHi = st.regs.isNotEmpty ? st.regs.first.code : 'SG'; final defLo = st.regs.length > 1 ? st.regs[1].code : ''; final gid = await ntf.createCustomGroup(name: '$baseLbl 专享组', badge: baseLbl, exitCode: defHi, bakExitCode: defLo);"),
            ("for (final rc in const <String>['SG', 'HK', 'US', 'JP', 'TW']) PopupMenuItem( label: '🌐 开启「${bSlot.name}」专享代理 → ${FlClashBridge.regLblOf(rc)}'", "for (final rc in _cfgRegs(st)) PopupMenuItem( label: '🌐 开启「${bSlot.name}」专享代理 → ${_menuRegLbl(st, rc)}'"),
            ("for (final rc in const <String>['SG', 'HK', 'US', 'JP']) if (bSlot == null) PopupMenuItem( label: '🌐 独立整包锁定 → ${FlClashBridge.regLblOf(rc)}'", "for (final rc in _cfgRegs(st)) if (bSlot == null) PopupMenuItem( label: '🌐 独立整包锁定 → ${_menuRegLbl(st, rc)}'"),
            ("for (final rc in _browserExitOpts) PopupMenuItem(glyph: bItem.exit == rc ? AppGlyphs.check : null, label: '🌐 切换专享出口 → ${FlClashBridge.regLblOf(rc)}'", "for (final rc in _exitOpts(st, bItem.exit)) PopupMenuItem(glyph: bItem.exit == rc ? AppGlyphs.check : null, label: '🌐 切换专享出口 → ${_menuRegLbl(st, rc)}'"),
        ]
        for a, b in reps:
            assert txt.count(a) == 1, (a, txt.count(a))
            txt = txt.replace(a, b, 1)
    elif name == 'simple_workbench_cards.dart':
        reps = [
            ("_upd(() => _bAddOpen = !_bAddOpen);", "_upd(() { _bAddOpen = !_bAddOpen; if (_bAddOpen && st.regs.isNotEmpty && !st.regs.any((r) => r.code == _newBrowserExit)) _newBrowserExit = st.regs.first.code; });"),
            ("_exPill(c, _newBrowserExit, _browserExitOpts,", "_exPill(c, st, _newBrowserExit, _exitOpts(st, _newBrowserExit),"),
            ("_exPill(c, b.exit, _browserExitOpts,", "_exPill(c, st, b.exit, _exitOpts(st, b.exit),"),
            ("final exitChoices = isC ? _browserExitOpts : _vendorExitOpts;", "final exitChoices = _exitOpts(st, v.defEx);"),
            ("_exPill(c, v.defEx, exitChoices,", "_exPill(c, st, v.defEx, exitChoices,"),
            ("_bakPill(c, v.defEx,", "_bakPill(c, st, v.defEx,"),
            ("_exPill(c, sl.exit, _subExitOpts,", "_exPill(c, st, sl.exit, _exitOpts(st, sl.exit, 'DIRECT'),"),
            ("_upd(() => _newGrpOpen = !_newGrpOpen);", "_upd(() { _newGrpOpen = !_newGrpOpen; if (_newGrpOpen && st.regs.isNotEmpty) { if (!st.regs.any((r) => r.code == _ngExit)) _ngExit = st.regs.first.code; if (_ngBakExit.isNotEmpty && (!st.regs.any((r) => r.code == _ngBakExit) || _ngBakExit == _ngExit)) _ngBakExit = st.regs.length > 1 ? st.regs.firstWhere((r) => r.code != _ngExit).code : ''; } });"),
            ("_exPill(c, _ngExit, _browserExitOpts,", "_exPill(c, st, _ngExit, _cfgRegs(st, _ngExit),"),
            ("_bakPill(c, _ngExit, _ngBakExit,", "_bakPill(c, st, _ngExit, _ngBakExit,"),
            ("_exPill(c, _customExit, _subExitOpts,", "_exPill(c, st, _customExit, _exitOpts(st, _customExit, 'DIRECT'),"),
        ]
        for a, b in reps:
            assert a in txt, a
            txt = txt.replace(a, b)
    return txt
