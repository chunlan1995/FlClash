import functools, hashlib
FB12 = [
('static List<OsProcNode> _scanWin32Ffi() {', '=',
'static bool _scanBusy = false; static List<OsProcNode> _lastScan = const <OsProcNode>[]; static List<OsProcNode> _scanWin32Ffi([Map<int, ('
'int, String, String)>? extCache]) { final cache = extCache ?? _winPathCache;'),
('final cached = _winPathCache[pid];', '=', 'final cached = cache[pid];'),
('_winPathCache[pid] = (ppid, exe, fullPath);', '=', 'cache[pid] = (ppid, exe, fullPath);'),
('_winPathCache~remo', '} catch (_) ', 'cache~removeWhere((k, _) => !alive~contains(k));'),
('static Future<List', 'if (Platform~isM',
'static Future<List<OsProcNode>> scan() async {if (Platform~isAndroid || Platform~isIOS) return const <OsProcNode>[]; if (_scanBusy) return'
' _lastScan; _scanBusy = true; try { if (Platform~isWindows) { final seed = Map<int, (int, String, String)>~from(_winPathCache); final res '
'= await Isolate~run(() { final m = Map<int, (int, String, String)>~from(seed); return (_scanWin32Ffi(m), m); }); _winPathCache~~clear()~~a'
'ddAll(res~$2); return _lastScan = res~$1; } if (Platform~isLinux) return _lastScan = await Isolate~run(_scanLinuxProc);'),
('return out;} catch', '\ntypedef Sub',
'return _lastScan = out;} catch (_) {return _lastScan;}}return const <OsProcNode>[];} finally {_scanBusy = false;}}}'),
('class FlClashBridg', 'var validCnt',
'// v127_win_zero_stall_bridge\nclass FlClashBridge {\nstatic final Map<String, String> resolvedNodeIpCache = <String, String>{};\nstatic fina'
'l Map<String, RegExp> _rxCache = <String, RegExp>{};\nstatic RegExp _cachedRx(String pat, {bool caseSensitive = true}) => _rxCache~putIfAbs'
'ent(\'${caseSensitive ? "1" : "0"}:$pat\', () => RegExp(pat, caseSensitive: caseSensitive));\nstatic bool isAppVisible(Ref ref) { try { retur'
'n ref~read(appVisibleProvider); } catch (_) { return true; } }\nstatic bool watchAppVisible(WidgetRef ref) { try { return ref~watch(appVisi'
'bleProvider); } catch (_) { return true; } }\nstatic Future<(List<Map<String, dynamic>>, Map<String, Map<String, dynamic>>, int, int)> _rea'
'dSubInIsolate(String homeDir, int pid) => Isolate~run(() {\nfinal pxs = <Map<String, dynamic>>[], provs = <String, Map<String, dynamic>>{};'
" var gCnt = 0, rCnt = 0;\nfinal pf = File('$homeDir/profiles/$pid~yaml');\nif (pf~existsSync()) { try { final c = _extractFileProxiesAndCoun"
"ts(pf~readAsStringSync(), pxs, provs); gCnt = c~$1; rCnt = c~$2; } catch (_) {} }\nfinal provDir = Directory('$homeDir/profiles/providers/$"
"pid');\nif (provDir~existsSync()) { try { for (final e in provDir~listSync(recursive: true, followLinks: false)) {\nif (e is! File) continue"
"; final pLow = e~path~replaceAll('\\\\', '/')~toLowerCase();\nif (pLow~contains('/rules/') || pLow~endsWith('~mmdb') || pLow~endsWith('~metad"
"b') || pLow~endsWith('~dat') || pLow~endsWith('~mrs') || e~lengthSync() >= 8388608) continue;\ntry { _extractFileProxiesAndCounts(e~readAsS"
'tringSync(), pxs, <String, Map<String, dynamic>>{}); } catch (_) {}\n} } catch (_) {} }\nreturn (pxs, provs, gCnt, rCnt);\n});\nstatic final M'
'ap<int, ({int nodes, int groups, int rules, int providers, int mtime})> subDiskStats = <int, ({int nodes, int groups, int rules, int provi'
'ders, int mtime})>{};\nstatic bool _scanningStats = false;\nstatic Future<void> refreshAllSubDiskStats(Ref ref, {bool force = false}) async '
'{\nif (_scanningStats && !force) return; _scanningStats = true;\ntry { final h = await appPath~homeDirPath, list = ref~read(profilesProvider'
");\nfor (final p in list) {\nfinal pf = File('$h/profiles/${p~id}~yaml'), mt = pf~existsSync() ? pf~lastModifiedSync()~millisecondsSinceEpoc"
'h : 0, prev = subDiskStats[p~id];\nif (!force && prev != null && prev~mtime == mt && mt > 0 && subRegNodeCounts~containsKey(p~id)) { subNod'
'eCounts[p~id] = prev~nodes; continue; }\nfinal parsed = await _readSubInIsolate(h, p~id), pxs = parsed~$1, provs = parsed~$2, gCnt = parsed'
'~$3, rCnt = parsed~$4;\n'),
("final rc0 = resolveReg(nm, sv, '')~$1;", '=', "final rc0 = resolveReg(nm, sv, resolvedNodeIpCache[nm] ?? '')~$1;"),
('if(targets~isEmpty', 'int rdVar(in',
'if(targets~isEmpty)return;final datPath=_geoDatPath,reqMap=Map<String,Uint8List>~from(targets);try{final hits=await Isolate~run((){final f'
'ound=<String,String>{},buf=File(datPath)~readAsBytesSync(),targets=Map<String,Uint8List>~from(reqMap),tmp=<int>[0];'),
('ipGeoCache[k]=cc~l', 'static Futur',
"found[k]=cc~length==2?cc:'ANYCAST';if(cc~length==2)matched~add(k);});for(final mk in matched){targets~remove(mk);}}}eo+=fLen;}else if(wt=="
'0){eo=rdVar(eo);}else break;}o=eEnd;}return found;});ipGeoCache~addAll(hits);}catch(_){}}'),
("resolveReg(p~$1,p~$2,'')~$1]);await savePrefs();", '=', "resolveReg(p~$1,p~$2,resolvedNodeIpCache[p~$1]??'')~$1]);await savePrefs();"),
('static void _extra', 'void parseLi',
'static void _extractFileProxies(String raw,List<Map<String,dynamic>>pxOut,Map<String,Map<String,dynamic>>provOut){_extractFileProxiesAndCo'
'unts(raw,pxOut,provOut);}static (int,int) _extractFileProxiesAndCounts(String raw,List<Map<String,dynamic>>pxOut,Map<String,Map<String,dyn'
'amic>>provOut){final t=raw~trim();if(t~isEmpty)return (0,0);var gCnt=0,rCnt=0;'),
("if(d is Map){if(d['proxies']is Iterable)", '=',
"if(d is Map){if(d['proxy-groups']is List)gCnt=(d['proxy-groups']as List)~length;if(d['rules']is List)rCnt=(d['rules']as List)~length;if(d["
"'proxies']is Iterable)"),
('if(pxOut~isNotEmpty||provOut~isNotEmpty)return;}', '=', 'if(pxOut~isNotEmpty||provOut~isNotEmpty)return (gCnt,rCnt);}'),
('if(pxOut~isNotEmpty)', 'static Futur', 'if(pxOut~isNotEmpty)return (gCnt,rCnt);}catch(_){}}}catch(_){}parseLines(t);return (gCnt,rCnt);}'),
('final pxs = <Map<String, dynamic>>[];', 'var validSub',
"final pf = File('$h/profiles/$pid~yaml'), mt = pf~existsSync() ? pf~lastModifiedSync()~millisecondsSinceEpoch : 0;\nfinal parsed = await _r"
'eadSubInIsolate(h, pid), pxs = parsed~$1, provs = parsed~$2;\n'),
("final rc0 = resolveReg(nm, sv, '')~$1;", '=', "final rc0 = resolveReg(nm, sv, resolvedNodeIpCache[nm] ?? '')~$1;"),
('subNodeCounts[pid]', '\nif (!isPrim',
'subNodeCounts[pid] = validSubCnt;\nsubRegNodeCounts[pid] = regCnts;\nsubDiskStats[pid] = (nodes: validSubCnt, groups: parsed~$3, rules: pars'
'ed~$4, providers: provs~length, mtime: mt);'),
("resolveReg(p~$1,p~$2,'')~$1]);}return true;", '=', "resolveReg(p~$1,p~$2,resolvedNodeIpCache[p~$1]??'')~$1]);}return true;"),
('static Future<void>sy', '_lastSyncDiskMs=',
'static Future<void>syncProfileNodesFromDisk(Ref ref,{bool force=false,bool forceDiskReload=false})async{final nowMs=DateTime~now()~millise'
'condsSinceEpoch;if(!force&&!forceDiskReload&&cfgProxyNodes~isNotEmpty&&nowMs-_lastSyncDiskMs<4000)return;'),
("if(force)_lastDiskSig='';", '=', "if(forceDiskReload)_lastDiskSig='';"),
('await syncProfileNodesFromDisk(ref,f', '}catch(_){}r',
'await syncProfileNodesFromDisk(ref,force:true,forceDiskReload:true);await requestApplyProfile(ref);'),
('(byR[resolveReg(nm', '\n}\n}\n}\nfor (', "(byR[resolveReg(nm, sv, resolvedNodeIpCache[nm] ?? '')~$1] ??= <String>[])~add(nm);"),
('static void syncSe', 'static Futur',
'static void syncSelectedMapToProfile(Ref ref) {\nif (!simpleTakeover) return;\ntry {\nfinal curProfile = ref~read(currentProfileProvider);\nif'
' (curProfile == null) return;\nMap<String, String>? nextSel;\nvoid setSel(String g, String v) { if ((nextSel ?? curProfile~selectedMap)[g] !'
'= v) { nextSel ??= Map<String, String>~from(curProfile~selectedMap); nextSel![g] = v; } }\nfinal hubStk = stkNs[regCode];\nif (hubStk != nul'
'l && hubStk~isNotEmpty && !isManagedGroup(hubStk)) setSel(hubGroup, hubStk);\nfor (final rc in mRegs) { final rStk = stkNs[rc]; if (rStk !='
" null && rStk~isNotEmpty && !isManagedGroup(rStk)) setSel(regGroup(rc), rStk); }\nfor (final cv in vendors) { if (cv~id~startsWith('custom_"
"')) setSel(custCatGroup(cv~id), custTargetRegGroup(cv)); }\nif (nextSel != null) ref~read(profilesProvider~notifier)~put(curProfile~copyWit"
'h(selectedMap: nextSel!));\n} catch (_) {}\n}\n'),
("RegExp('^${RegExp~", '~hasMatch(p)', "_cachedRx('^${RegExp~escape(st)}([ _~-]~*|\\\\~(exe|app|bin))?\\$')"),
('RegExp(rx~replaceF', '~hasMatch(pt', "_cachedRx(rx~replaceFirst('(?i)', ''), caseSensitive: false)"),
('RegExp(prx~replace', '~hasMatch(ra', "_cachedRx(prx~replaceFirst('(?i)', ''), caseSensitive: false)"),
('RegExp(rx~replaceF', '~hasMatch(pt', "_cachedRx(rx~replaceFirst('(?i)', ''), caseSensitive: false)"),
('RegExp(prx~replace', '~hasMatch(ra', "_cachedRx(prx~replaceFirst('(?i)', ''), caseSensitive: false)"),
]
SG12 = [
("String _dailyWhoamiTried='';", '=', "// v127_zero_loop_guardian\nDateTime? _lastAutoGrpSyncAt; int _idleTickMod=0; String _dailyWhoamiTried='';"),
('Future<void> _boot', '(String owne',
'Future<void> _boot() async {\nawait _B~ensureLoaded();\nref~read(simpleModeProvider~notifier)~setMode(_B~simpleTakeover);\nfor (final v in _B'
'~vendors) { _hlSn~addAll(v~hIps); }\nawait _B~syncProfileNodesFromDisk(ref);\nawait _rcGs();\n_t1 = Timer~periodic(const Duration(seconds: 1)'
', (_) => unawaited(_tf()));\n_t2 = Timer~periodic(const Duration(seconds: 5), (_) => unawaited(_tp(false)));\nfinal enCnt = _B~vendors~where'
'((v) => v~enabled)~length, bCnt = _B~browserEnvs~where((b) => b~enabled)~length, cCnt = _B~companions~where((c) => c~enabled)~length;\n_log'
"(LogCat~core, '${_B~brandName} v${_B~appVersion} 已就绪', '主进程线程与伴生进程树守护已开启 · $enCnt 大厂商 · $bCnt 专享浏览器 · 已保存 $cCnt 项伴生白名单', true);\nunawaited("
'_B~refreshAllSubDiskStats(ref)~then((_) => _emit()));\nunawaited(refreshCatalogApps());\nif (Platform~isAndroid) { unawaited(_B~loadApps(ref'
')~then((v) { _apps = v; _emit(); })); } else { unawaited(scanProcessTreeNow(silentIfNoNew: true)); }\nunawaited(_tf());\n}'),
('Future<void> _rcGs()async{', '=', 'Future<void> _rcGs({bool emitState = true})async{'),
('final(rc,rl)=_B~resolveReg(nm,raw,ip);', '=', 'if(ip~isNotEmpty)_B~resolvedNodeIpCache[nm]=ip;final(rc,rl)=_B~resolveReg(nm,raw,ip);'),
('final gs=_B~readGr', 'var(realNode',
'final nowAuto=DateTime~now(),canAutoApply=_lastAutoGrpSyncAt==null||nowAuto~difference(_lastAutoGrpSyncAt!)~inSeconds>=45;final gs=_B~read'
'Groups(ref);if(gs~isNotEmpty&&_B~simpleTakeover&&!_B~applyingProfile&&canAutoApply&&(!gs~any((g)=>g~name==_B~hubGroup)||!gs~any((g)=>g~nam'
'e==_B~probeGroup))){_lastAutoGrpSyncAt=nowAuto;unawaited(_B~requestApplyProfile(ref,onStatusChanged:_emit));return;}'),
("_node='';_meta=null;_emit();return;}", '=', "_node='';_meta=null;if(emitState)_emit();return;}"),
('if(gs~isNotEmpty&&_B~simpleTakeover&&!_B~applyingProfile&&g', '}for (final ',
'if(gs~isNotEmpty&&_B~simpleTakeover&&!_B~applyingProfile&&canAutoApply&&gMap~containsKey(_B~hubGroup)&&by~keys~any((c)=>!gMap~containsKey('
'_B~regGroup(c)))){_lastAutoGrpSyncAt=nowAuto;unawaited(_B~requestApplyProfile(ref,onStatusChanged:_emit));}'),
('return (node: n, i', '\nif (_B~simp',
'return (node: n, ip: m~ip, raw: m~raw, s24: m~s24, ms: _delayOf(n), sel: n == targetHub, sticky: n == stk);\n}(),\n];\nif (emitState) _emit()'
';'),
('await _B~syncProfileNodesFromDisk(ref, force: force);', '=', 'await _B~syncProfileNodesFromDisk(ref, force: force, forceDiskReload: force);'),
]
SGC12 = [
('if(ipStr~isNotEmpt', 'if(cc~length', 'if(ipStr~isNotEmpty){_B~resolvedNodeIpCache[n]=ipStr;final cc=_B~lookupIpSync(ipStr);'),
('Future<void> _tf()', 'final cLogs=',
'// v127_nonblocking_tick\nFuture<void> _tf() async { if (_b1) return; final appVis = _B~isAppVisible(ref), runningNow = _B~isRunning(ref); '
'if (!appVis && !runningNow) return; _b1 = true; try { if (appVis) _memMB = (ProcessInfo~currentRss / (1024 * 1024))~round()~clamp(16, 4096'
'); if (!Platform~isAndroid && !Platform~isIOS && (runningNow || appVis)) { final nowScan = DateTime~now(), intMs = runningNow ? 6000 : 120'
'00; if (_ltScn == null || nowScan~difference(_ltScn!)~inMilliseconds >= intMs) unawaited(scanProcessTreeNow(silentIfNoNew: true)); }'),
('await _rcGs();fina', '_runSec++;if',
'if (runningNow || _idleTickMod % 3 == 0 || _regs~isEmpty) await _rcGs(emitState: false); final pkgMap = _B~readPkgNames(ref); if (!_B~isRu'
'nning(ref)) { final wasActive = _runSec > 0 || _upR != 0 || _dnR != 0 || _la != null; _cu~clear(); _stlSn~clear(); _swSks~clear(); _la = n'
'ull; _runSec = 0; _upR = _dnR = _vR = _fR = _dR = 0; _idleTickMod++; if (wasActive || _procsL~isEmpty || _idleTickMod % 4 == 1) { _sdApp(p'
'kgMap); _rfIdl(pkgMap); if (appVis || wasActive) _emit(); } return; } _idleTickMod = 0;'),
('_procsL=list;_emit', 'Future<void>', '_procsL=list;if(appVis)_emit();}catch(_){}finally{_b1=false;}}'),
]
SW12 = [
("import 'dart:ui' show FontFeature, ImageFilter;", '=',
"// v127_skia_smooth_ui\nimport 'dart:ui' show BlurStyle, FontFeature, ImageFilter, MaskFilter;"),
('typedef _FB = FlClashBridge;', '=',
'typedef _FB = FlClashBridge;\nfinal bool _kDesktop = Platform~isWindows || Platform~isLinux || Platform~isMacOS;\nfinal bool _kSkiaThrottle '
'= Platform~isWindows || Platform~isLinux;'),
('final simple = ref', '\nfinal topOf',
'final simple = ref~watch(simpleModeProvider), appVis = _FB~watchAppVisible(ref), cs = context~colorScheme, mqSize = MediaQuery~sizeOf(cont'
'ext);\nif (mqSize~isEmpty) return ColoredBox(color: SurfaceLevel~page~colorOf(cs));\nfinal width = mqSize~width;'),
('Offstage(offstage:', '\nif (!simple',
'if (!simple) Positioned~fill(child: originalChild),\nif (simple) Positioned~fill(child: TickerMode(enabled: appVis, child: const SimpleWork'
'benchView())),'),
('final phase = _orbitCtrl~value;', '=',
'final rawP = _orbitCtrl~value, qSteps = (widget~busy || widget~running) ? 320~0 : 160~0, phase = _kSkiaThrottle ? (rawP * qSteps)~floorToD'
'ouble() / qSteps : rawP;'),
('const steps = 96;', '=', 'const steps = 64;'),
('final glowAlpha = ', '\nfinal idleS',
'final glowAlpha = busy ? 0~38 : (0~10 + 0~30 * morph);\ncanvas~drawCircle(Offset(cx, cy + 3~0), coreR * 0~94, Paint()~~color = glowCol~with'
'Values(alpha: glowAlpha)~~maskFilter = const MaskFilter~blur(BlurStyle~normal, 9~0));'),
('duration: const Duration(milliseconds: 22', '\nfinal List<', 'duration: const Duration(milliseconds: 2200),\n);'),
('_dispTo = widget~speedBps~toDouble();\n}', '=', '_dispTo = widget~speedBps~toDouble();\nif (widget~running) _waveCtrl~repeat();\n}'),
('super~didUpdateWidget(oldWidget);\nf', '\nif (widget~',
'super~didUpdateWidget(oldWidget);\nif (widget~running && !_waveCtrl~isAnimating) { _waveCtrl~repeat(); } else if (!widget~running && _waveC'
'trl~isAnimating) { _waveCtrl~stop(); }\nfinal now = DateTime~now()~millisecondsSinceEpoch;'),
('return Expanded(\nc', '\ndecoration:', 'return Expanded(\nchild: RepaintBoundary(\nchild: DecoratedBox('),
('Positioned(\nleft: ', '\ncolor: acce',
'Positioned(\nleft: 1, right: 1, bottom: 1, height: 53,\nchild: ClipRRect(\nborderRadius: const BorderRadius~vertical(bottom: Radius~circular('
'21)),\nchild: RepaintBoundary(\nchild: AnimatedBuilder(\nanimation: _waveCtrl,\nbuilder: (ctx, _) {\nfinal rawP = _waveCtrl~value, phase = _kSk'
'iaThrottle ? (rawP * 88~0)~floorToDouble() / 88~0 : rawP;\nfinal subRaw = ((DateTime~now()~millisecondsSinceEpoch - _lastPushMs) / 1000~0)~'
'clamp(0~0, 1~0);\nfinal subFrac = _kSkiaThrottle ? (subRaw * 36~0)~floorToDouble() / 36~0 : subRaw;\nreturn CustomPaint(\npainter: _SmoothWav'
'ePainter(\nsamples: _buf,\nsubFrac: subFrac,\nphase: phase,'),
('liveSpeed: widget~', '\nPadding(\npa', 'liveSpeed: widget~speedBps~toDouble(),\n),\n);\n},\n),\n),\n),\n),'),
('AnimatedBuilder(\nanimation: _waveCtrl,\nbuilder: (ctx, c', 'Text(\nlabel,', 'GlyphIcon(glyph, size: 12~5, color: accent),\n'),
('bool shouldRepaint(covariant _S', '\n}\nclass _Sl',
'bool shouldRepaint(covariant _SmoothWavePainter old) => old~running != running || old~liveSpeed != liveSpeed || old~phase != phase || old~'
'subFrac != subFrac || old~color != color;'),
('final trackBg = dk', '\ndecoration:',
'final trackBg = _kDesktop ? (dk ? const Color(0xF2151C2B) : const Color(0xF7F8FAFC)) : (dk ? const Color(0xD9161D2B) : const Color(0xE8F8F'
'AFC));\nfinal rimCol = cs~onSurface~withValues(alpha: dk ? 0~13 : 0~09);\nWidget wrapDock(Widget w) => _kDesktop ? RepaintBoundary(child: w)'
' : RepaintBoundary(child: ClipRRect(borderRadius: BorderRadius~circular(24), child: BackdropFilter(filter: ImageFilter~blur(sigmaX: 20, si'
'gmaY: 20), child: w)));\nfinal dockBody = wrapDock(\nDecoratedBox('),
('},\n),\n),\n),\n),\n),\n);\nif (isDesktop) {', '=', '},\n),\n),\n),\n),\n);\nif (isDesktop) {'),
('unawaited(ref~read', '      _blPol', ''),
('child: ClipRSuperellipse(\nborderRadius: BorderRadius~circular(2', '\n20,\nborder:',
'child: (() { Widget w(Widget x) => _kDesktop ? x : ClipRRect(borderRadius: BorderRadius~circular(20), child: BackdropFilter(filter: ImageF'
'ilter~blur(sigmaX: 18, sigmaY: 18), child: x)); return w(DecoratedBox(\ndecoration: _rBox(\ndk ? const Color(0xF2181F2E) : const Color(0xF7F'
'FFFFF),'),
('),\n),\n),\n),\n),\n),\n),\n),\n),\n)', '\nfinal cs = ', '),\n),\n)); })(),\n),\n),\n),\n),\n);\n}\n@override\nWidget build(BuildContext context) {'),
('final rtTraffic = ', 'final kbOpen', ''),
('tunOn,\nrtTraffic,\nisDesktop,', '=', 'tunOn,\nisDesktop,'),
('Expanded(\nchild: A', '\nchild: Cons', 'Expanded(\nchild: RepaintBoundary(\nchild: Align(\nalignment: Alignment~topCenter,'),
('builder: (ctx, t, child) {\nreturn Opacity(', '=', 'builder: (ctx, t, child) {\nif (t >= 0~999) return child!;\nreturn Opacity('),
('child: pageBody,\n),\n),\n),\n),\n),\n],\n);', '=', 'child: pageBody,\n),\n),\n),\n),\n),\n),\n],\n);'),
]
SWC12 = [
('return ClipRSupere', '\n22,\nborder:',
'// v127_skia_smooth_cards\nWidget wrapB(Widget x) => _kDesktop ? x : ClipRRect(borderRadius: BorderRadius~circular(22), child: BackdropFilt'
'er(filter: ImageFilter~blur(sigmaX: 18, sigmaY: 18), child: x));\nreturn wrapB(DecoratedBox(\ndecoration: _rBox(\ndk ? const Color(0xF2181F2E'
') : const Color(0xF7FFFFFF),'),
('size: 30,\n),\n],\n),', '\nBuildContex', 'size: 30,\n),\n],\n),\n)));\n}\nWidget _buildOverviewPage('),
('Widget _buildOverv', 'Widget subBe',
'Widget _buildOverviewPage(BuildContext c, GuardianState st, List<SubRichItem> richSubs, bool run, bool sysPx, bool tunOn, bool isDesktop) '
'{\nif (isDesktop) {\nreturn Row(crossAxisAlignment: CrossAxisAlignment~start, spacing: 14, children: <Widget>[\nExpanded(child: RepaintBounda'
'ry(child: ConstrainedBox(constraints: const BoxConstraints(minHeight: 400), child: _statusCard(c, st, richSubs, run, sysPx, tunOn)))),\nExp'
'anded(child: RepaintBoundary(child: ConstrainedBox(constraints: const BoxConstraints(minHeight: 400), child: _fallbackAndWhoamiCard(c, st,'
' richSubs)))),\n]);\n}\nreturn Column(crossAxisAlignment: CrossAxisAlignment~stretch, spacing: 14, children: <Widget>[\nRepaintBoundary(child:'
' _statusCard(c, st, richSubs, run, sysPx, tunOn)),\nRepaintBoundary(child: _fallbackAndWhoamiCard(c, st, richSubs)),\n]);\n}\nWidget _statusCa'
'rd(BuildContext c, GuardianState st, List<SubRichItem> richSubs, bool run, bool sysPx, bool tunOn) {\nfinal ntf = ref~read(guardianProvider'
"~notifier), dk = _isDk(c);\nfinal probeStr = !run ? '未连接' : (st~ms < 0 ? '超时' : (st~ms == 0 ? '待测速' : '${st~ms} ms'));\nfinal probeCol = !ru"
'n ? _cN : (st~ms < 0 ? _cR : (st~ms == 0 ? _cW : (st~ms < 260 ? _cP : _cW)));\nfinal meta = st~meta;\nfinal curIp = (meta != null && meta~ip'
"~isNotEmpty) ? meta~ip : ((meta != null && meta~raw~isNotEmpty) ? meta~raw : (st~node~isEmpty ? '待选节点' : st~node));\nfinal enabledSubs = st"
'~mergeSubs ? <SubRichItem>[for (final s in richSubs) if (!st~disabledSubs~contains(s~id)) s] : <SubRichItem>[if (richSubs~isNotEmpty) rich'
'Subs~where((s) => s~selected)~firstOrNull ?? richSubs~first];\nfinal prefSubId = !st~fbDir ? _FB~activePrefSubIdOf(st~reg) : 0;\nfinal prefS'
"ubLbl = prefSubId > 0 ? (richSubs~where((s) => s~id == prefSubId)~firstOrNull?~label ?? _FB~activePrefSubLabelOf(st~reg)) : '';\n"),
('if (hasQuota)\nClip', '\nchild: Deco', 'if (hasQuota)\nClipRRect(\nborderRadius: BorderRadius~circular(99),'),
('return ClipRSupere', '\ndecoration:', 'return DecoratedBox('),
('Row(\nspacing: 10,\nchildren: <Widget>[\n_', 'Column(\ncros',
'Consumer(builder: (tCtx, tRef, _) {\nfinal rtTraffic = _FB~watchRealtimeTraffic(tRef);\nfinal effUpSpeed = rtTraffic~upSpeed > 0 || rtTraffi'
'c~upHist~isNotEmpty ? (rtTraffic~upSpeed > 0 ? rtTraffic~upSpeed : st~upR) : st~upR;\nfinal effDnSpeed = rtTraffic~downSpeed > 0 || rtTraff'
'ic~downHist~isNotEmpty ? (rtTraffic~downSpeed > 0 ? rtTraffic~downSpeed : st~dnR) : st~dnR;\nfinal effUpTotal = rtTraffic~upTotal > 0 ? rtT'
'raffic~upTotal : st~pxB;\nfinal effDnTotal = rtTraffic~downTotal > 0 ? rtTraffic~downTotal : st~drB;\nreturn Row(spacing: 10, children: <Wid'
'get>[\n_LiveTrafficCard(isUpload: true, speedBps: effUpSpeed, totalBytes: effUpTotal, history: rtTraffic~upHist, revision: rtTraffic~revisi'
'on, running: run),\n_LiveTrafficCard(isUpload: false, speedBps: effDnSpeed, totalBytes: effDnTotal, history: rtTraffic~downHist, revision: '
'rtTraffic~revision, running: run),\n]);\n}),\n'),
('activeColor: _cN,\nstacked: true,\nheight: 58,\n),\n),\n],', '\nBuildContex',
'activeColor: _cN,\nstacked: true,\nheight: 58,\n),\n),\n],\n),\n],\n),\n),\n);\n}\nWidget _fallbackAndWhoamiCard('),
]
_u = lambda x: x .replace('~', '.')
_s = lambda s, h, t, v: (lambda i: s[:i] + v + (s[i + len(h):] if t == '=' else s[s .index(t, i + len(h)):]))(s .index(h))
_r = lambda s, x: _s(s, _u(x[0]), _u(x[1]), _u(x[2]))
def _p(d, f, m, ps): p = d / (f + _u('~dart')); s = p .read_text('utf-8'); p .write_text(functools .reduce(_r, ps, s), 'utf-8') if _u(m) not in s else 0
ALL12 = (FB12, SG12, SGC12, SW12, SWC12)
def _ck(): assert hashlib .sha256(repr(ALL12) .encode('utf-8')) .hexdigest()[:12] == '39268d826bfb'
def _a1(od): _p(od, 'flclash_bridge', 'v127_win_zero_stall_bridge', FB12); _p(od, 'smart_guardian', 'v127_zero_loop_guardian', SG12)
def _a2(od): _p(od, 'smart_guardian_core', 'v127_nonblocking_tick', SGC12); _p(od, 'simple_workbench', 'v127_skia_smooth_ui', SW12)
def apply_v127(od): _ck(); _a1(od); _a2(od); _p(od, 'simple_workbench_cards', 'v127_skia_smooth_cards', SWC12)
