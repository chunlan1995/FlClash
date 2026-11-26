import hashlib
FB13 = [
("import 'package:fl_clash/p", "\nimport 'package:fl_clash/w",
"// v128_pure_core_bridge\nimport 'package:archive/archive_io~dart';\nimport 'package:fl_clash/pages/scan~dart';\nimport 'package:fl_clash/p"
"roviders/providers~dart';\nimport 'package:flutter/services~dart';\nimport 'package:path/path~dart' as pkg_path;"),
('static void openSu', 'static Futur',
"static Future<({bool ok, String msg, int nodes})> importSubFromUrl(Ref ref, {required String url, String label = '', String ageKey = ''}"
') async {\nfinal lines = <String>[for (final ln in const LineSplitter()~convert(url~trim())) if (ln~trim()~isNotEmpty) ln~trim()];\nif (li'
"nes~isEmpty) return (ok: false, msg: '请输入有效的订阅链接或节点分享链接', nodes: 0);\ntry {\nfinal core = ref~read(coreHandlerProvider), pAct = ref~read(p"
'rofilesActionProvider~notifier);\nfinal shareLinks = <String>[for (final l in lines) if (l~isShareLink) l];\nfinal urlLinks = <String>[for'
' (final l in lines) if (!l~isShareLink) l];\nvar addedCnt = 0, lastId = 0;\nif (shareLinks~isNotEmpty) {\nfinal decoded = await core~decode'
'ShareLinks(shareLinks);\nfinal taken = <String>{~~~reservedCustomProxyNames};\nfinal proxies = <Map<String, dynamic>>[];\nfor (final defs i'
"n decoded) {\nfor (final def in defs) {\nfinal nm = freeProxyName(linkProxyName(def), taken);\nproxies~add(<String, dynamic>{~~~def, 'name'"
": nm});\n}\n}\nif (proxies~isEmpty) return (ok: false, msg: '未能解析出有效分享节点', nodes: 0);\nfinal firstNm = '${proxies~first['name']}';\nfinal eff"
"Lbl = label~trim()~isNotEmpty ? label~trim() : (proxies~length == 1 ? firstNm : '$firstNm 等 ${proxies~length} 节点');\nfinal cfgYaml = awai"
"t encodeYamlTask(<String, dynamic>{'proxies': proxies});\nfinal saved = await Profile~normal(label: effLbl)~saveFile(Uint8List~fromList(u"
'tf8~encode(cfgYaml)), validate: (path, _) => core~validateConfig(path));\npAct~putProfile(saved);\nlastId = saved~id;\naddedCnt++;\n}\nfor (v'
"ar idx = 0; idx < urlLinks~length; idx++) {\nfinal u = urlLinks[idx];\nif (!u~startsWith('http://') && !u~startsWith('https://')) return ("
"ok: false, msg: '链接格式无效：$u', nodes: 0);\nfinal effLbl = label~trim()~isNotEmpty ? (urlLinks~length > 1 ? '${label~trim()} #${idx + 1}' : "
'label~trim()) : null;\nfinal baseP = Profile~normal(label: effLbl, url: u)~copyWith(ageSecretKey: ageKey~trim());\nfinal dl = await baseP~'
'update(validate: (path, key) => core~validateProfile(path, key));\npAct~putProfile(dl);\nlastId = dl~id;\naddedCnt++;\n}\nif (addedCnt <= 0) '
"return (ok: false, msg: '未导入任何订阅', nodes: 0);\nawait refreshAllSubDiskStats(ref, force: true);\nawait syncProfileNodesFromDisk(ref, force:"
' true, forceDiskReload: true);\nawait requestApplyProfile(ref);\nfinal nCnt = lastId > 0 ? (subDiskStats[lastId]?~nodes ?? subNodeCounts[l'
"astId] ?? cfgProxyNodes~length) : cfgProxyNodes~length;\nshowBannerMsg('订阅导入成功 · 新增 $addedCnt 项 ($nCnt 节点)', kind: 'success');\nreturn (ok"
": true, msg: '已成功导入 $addedCnt 项订阅（$nCnt 节点）', nodes: nCnt);\n} catch (e) {\nreturn (ok: false, msg: '导入失败：$e', nodes: 0);\n}\n}\nstatic Futur"
'e<({bool ok, String msg})> importSubFromLocalFile(Ref ref) async {\ntry {\nfinal pf = await picker~pickerFile();\nif (pf == null) return (o'
"k: false, msg: '');\nfinal bytes = await pf~readBytes();\nif (bytes~isEmpty) return (ok: false, msg: '所选文件为空');\nfinal rawLbl = pf~name~rep"
"laceAll(RegExp(r'\\~(ya?ml|txt|conf)$', caseSensitive: false), '')~trim();\nfinal saved = await Profile~normal(label: rawLbl~isNotEmpty ? "
'rawLbl : pf~name)~saveFile(bytes, validate: (path, key) => ref~read(coreHandlerProvider)~validateProfile(path, key));\nref~read(profilesA'
'ctionProvider~notifier)~putProfile(saved);\nawait refreshAllSubDiskStats(ref, force: true);\nawait syncProfileNodesFromDisk(ref, force: tr'
'ue, forceDiskReload: true);\nawait requestApplyProfile(ref);\nfinal nCnt = subDiskStats[saved~id]?~nodes ?? subNodeCounts[saved~id] ?? 0;\n'
"final msg = '已导入本地配置「${saved~realLabel}」（$nCnt 节点）';\nshowBannerMsg(msg, kind: 'success');\nreturn (ok: true, msg: msg);\n} catch (e) {\nsho"
"wBannerMsg('本地文件导入失败：$e', kind: 'error');\nreturn (ok: false, msg: '本地文件导入失败：$e');\n}\n}\nstatic Future<({bool ok, String msg})> importSubFr"
'omQr(BuildContext c, Ref ref, {bool fromGallery = false}) async {\ntry {\nString? qrUrl;\nif (!fromGallery && (Platform~isAndroid || Platfo'
'rm~isIOS)) {\nqrUrl = await BaseNavigator~push<String>(c, const ScanPage());\n} else {\nqrUrl = await picker~pickerConfigQRCode();\n}\nif (qr'
"Url == null || qrUrl~trim()~isEmpty) return (ok: false, msg: '');\nfinal res = await importSubFromUrl(ref, url: qrUrl~trim());\nif (!res~o"
"k && res~msg~isNotEmpty) showBannerMsg(res~msg, kind: 'error');\nreturn (ok: res~ok, msg: res~msg);\n} catch (e) {\nshowBannerMsg('二维码识别失败："
"$e', kind: 'error');\nreturn (ok: false, msg: '二维码识别失败：$e');\n}\n}\nstatic Future<({bool ok, String msg})> exportFullBackupZip(Ref ref) asyn"
"c {\ntry {\nawait savePrefs();\nawait syncBlacklistKernelFile();\nfinal h = await appPath~homeDirPath;\nfinal tmpRoot = Directory('${await ap"
"pPath~tempPath}/bc_bak_${DateTime~now()~millisecondsSinceEpoch}');\nawait tmpRoot~create(recursive: true);\ntry {\nfinal savedOk = await re"
"f~read(backupActionProvider~notifier)~backup((archPath) async {\nfinal stageDir = Directory('${tmpRoot~path}/stage');\nawait stageDir~crea"
'te(recursive: true);\nfinal inp = InputFileStream(archPath);\ntry {\nfinal arch = ZipDecoder()~decodeStream(inp);\nfor (final af in arch~fil'
'es) {\nif (!af~isFile) continue;\nfinal outP = pkg_path~normalize(pkg_path~joinAll(<String>[stageDir~path, ~~~pkg_path~posix~split(af~name'
"~replaceAll('\\\\', '/'))]));\nif (!pkg_path~isWithin(stageDir~path, outP)) continue;\nawait Directory(pkg_path~dirname(outP))~create(recurs"
'ive: true);\nfinal outS = OutputFileStream(outP);\ntry { af~writeContent(outS); } finally { await outS~close(); }\n}\n} finally {\nawait inp~'
"close();\n}\nfinal extDir = Directory('${stageDir~path}/blueclash_ext');\nawait extDir~create(recursive: true);\nfor (final rel in const <St"
"ring>['custom_minimal_v2~json', 'blueclash_blacklist~json', 'profiles/blueclash_whoami_exits~json']) {\nfinal srcF = File('$h/$rel');\nif "
"(await srcF~exists()) await srcF~copy('${extDir~path}/${rel~replaceAll('/', '__')}');\n}\nfinal mergedZip = '${tmpRoot~path}/merged_backup"
"~zip';\nfinal enc = ZipFileEncoder()~~create(mergedZip);\ntry {\nfor (final ent in stageDir~listSync(recursive: true, followLinks: false)) "
'{\nif (ent is! File) continue;\nfinal relP = pkg_path~posix~joinAll(pkg_path~split(pkg_path~relative(ent~path, from: stageDir~path)));\nawa'
"it enc~addFile(ent, relP);\n}\n} finally {\nawait enc~close();\n}\nfinal d = DateTime~now();\nfinal ts = '${d~year}${d~month~toString()~padLef"
't(2, "0")}${d~day~toString()~padLeft(2, "0")}-${d~hour~toString()~padLeft(2, "0")}${d~minute~toString()~padLeft(2, "0")}\';\nfinal uri = a'
"wait picker~saveFileWithPath('BlueClash-Backup-$ts~zip', mergedZip);\nreturn uri != null;\n});\nif (!savedOk) return (ok: false, msg: '');\n"
"const m = '完整备份已导出（含全部订阅、分流规则、浏览器与黑名单）';\nshowBannerMsg(m, kind: 'success');\nreturn (ok: true, msg: m);\n} finally {\ntry { if (await tmpRo"
"ot~exists()) await tmpRoot~delete(recursive: true); } catch (_) {}\n}\n} catch (e) {\nshowBannerMsg('导出备份失败：$e', kind: 'error');\nreturn (ok"
": false, msg: '导出备份失败：$e');\n}\n}\nstatic Future<({bool ok, String msg})> restoreFullBackupZip(Ref ref) async {\ntry {\nfinal pf = await pick"
"er~pickerFile();\nif (pf == null) return (ok: false, msg: '');\nfinal bytes = await pf~readBytes();\nif (bytes~isEmpty) return (ok: false, "
"msg: '备份文件为空');\nfinal h = await appPath~homeDirPath;\nfinal tmpRoot = Directory('${await appPath~tempPath}/bc_rst_${DateTime~now()~millis"
"econdsSinceEpoch}');\nawait tmpRoot~create(recursive: true);\ntry {\nfinal zipPath = '${tmpRoot~path}/input~zip', stageDir = Directory('${t"
"mpRoot~path}/unz');\nawait File(zipPath)~writeAsBytes(bytes, flush: true);\nawait stageDir~create(recursive: true);\nvar hasCoreBackup = fa"
'lse, hasBcExt = false;\nfinal inp = InputFileStream(zipPath);\ntry {\nfinal arch = ZipDecoder()~decodeStream(inp);\nfor (final af in arch~fi'
"les) {\nif (!af~isFile) continue;\nfinal norm = af~name~replaceAll('\\\\', '/');\nif (norm == 'config~json') hasCoreBackup = true;\nif (norm~s"
"tartsWith('blueclash_ext/')) hasBcExt = true;\nfinal outP = pkg_path~normalize(pkg_path~joinAll(<String>[stageDir~path, ~~~pkg_path~posix"
'~split(norm)]));\nif (!pkg_path~isWithin(stageDir~path, outP)) continue;\nawait Directory(pkg_path~dirname(outP))~create(recursive: true);'
'\nfinal outS = OutputFileStream(outP);\ntry { af~writeContent(outS); } finally { await outS~close(); }\n}\n} finally {\nawait inp~close();\n}\n'
"if (!hasCoreBackup && !hasBcExt) return (ok: false, msg: '无效的备份包（未检测到配置数据）');\nif (hasCoreBackup) {\nawait ref~read(backupActionProvider~n"
"otifier)~restore(RestoreOption~all, (dlPath) async {\nawait File(zipPath)~copy(dlPath);\nreturn dlPath;\n});\n}\nfinal extDir = Directory('${"
"stageDir~path}/blueclash_ext');\nif (await extDir~exists()) {\nconst mapBack = <String, String>{\n'custom_minimal_v2~json': 'custom_minimal"
"_v2~json',\n'blueclash_blacklist~json': 'blueclash_blacklist~json',\n'profiles__blueclash_whoami_exits~json': 'profiles/blueclash_whoami_e"
"xits~json',\n};\nfor (final entry in mapBack~entries) {\nfinal sf = File('${extDir~path}/${entry~key}');\nif (await sf~exists()) {\nfinal df "
"= File('$h/${entry~value}');\nawait df~parent~create(recursive: true);\nawait sf~copy(df~path);\n}\n}\n}\n_loadCompleter = null;\n_lastDiskSig "
"= '';\nawait ensureLoaded();\nawait syncBlacklistKernelFile();\nawait refreshAllSubDiskStats(ref, force: true);\nawait syncProfileNodesFromD"
"isk(ref, force: true, forceDiskReload: true);\nawait requestApplyProfile(ref);\nconst m = '备份恢复完成，全部订阅、分流与黑名单规则已热生效';\nshowBannerMsg(m, kin"
"d: 'success');\nreturn (ok: true, msg: m);\n} finally {\ntry { if (await tmpRoot~exists()) await tmpRoot~delete(recursive: true); } catch ("
"_) {}\n}\n} catch (e) {\nshowBannerMsg('恢复备份失败：$e', kind: 'error');\nreturn (ok: false, msg: '恢复备份失败：$e');\n}\n}\nstatic ({bool autoLaunch, boo"
'l silentLaunch, bool autoRun, bool minimizeOnExit, bool showTrayTitle, bool notifStop}) watchSysSettings(WidgetRef ref) =>\nref~watch(app'
'SettingProvider~select((x) => (autoLaunch: x~autoLaunch, silentLaunch: x~silentLaunch, autoRun: x~autoRun, minimizeOnExit: x~minimizeOnE'
'xit, showTrayTitle: x~showTrayTitle, notifStop: x~showNotificationStopAction)));\nstatic void updateSysSetting(WidgetRef ref, {bool? auto'
'Launch, bool? silentLaunch, bool? autoRun, bool? minimizeOnExit, bool? showTrayTitle, bool? notifStop}) {\nref~read(appSettingProvider~no'
'tifier)~update((s) => s~copyWith(autoLaunch: autoLaunch ?? s~autoLaunch, silentLaunch: silentLaunch ?? s~silentLaunch, autoRun: autoRun '
'?? s~autoRun, minimizeOnExit: minimizeOnExit ?? s~minimizeOnExit, showTrayTitle: showTrayTitle ?? s~showTrayTitle, showNotificationStopA'
'ction: notifStop ?? s~showNotificationStopAction));\n}\nstatic ({ThemeMode mode, bool pureBlack}) watchThemeCfg(WidgetRef ref) =>\nref~watc'
'h(themeSettingProvider~select((s) => (mode: s~themeMode, pureBlack: s~pureBlack)));\nstatic void updateThemeCfg(WidgetRef ref, {ThemeMode'
'? mode, bool? pureBlack}) {\nref~read(themeSettingProvider~notifier)~update((s) => s~copyWith(themeMode: mode ?? s~themeMode, pureBlack: '
'pureBlack ?? s~pureBlack));\n}\nstatic const List<(HotAction, String, String)> kBlueClashHotActions = <(HotAction, String, String)>[\n(HotA'
"ction~view, '显示 / 隐藏主窗口', '随时呼出或隐藏桌面主界面'),\n(HotAction~start, '启动 / 停止代理', '一键切换核心代理运行状态'),\n(HotAction~mode, '切换分流 / 全局直连', '在代理分流与全局直连间切"
"换'),\n(HotAction~proxy, '开关系统代理', '切换操作系统全局系统代理'),\n(HotAction~tun, '开关 TUN 模式', '切换虚拟网卡接管模式'),\n(HotAction~delayTest, '一键节点测速', '对当前出口执行即时"
"延迟测速'),\n(HotAction~updateProfiles, '同步全部订阅', '后台静默更新全部远程订阅'),\n];\nstatic List<({HotAction action, String title, String subtitle, Set<Keyb"
'oardModifier> modifiers, int? key, List<String> caps, String? err})> watchHotKeyRows(WidgetRef ref) {\nfinal list = ref~watch(hotKeyActio'
'nsProvider), fails = ref~watch(hotKeyFailuresProvider), labels = ShortcutLabels~host();\nreturn <({HotAction action, String title, String'
' subtitle, Set<KeyboardModifier> modifiers, int? key, List<String> caps, String? err})>[\nfor (final (act, ttl, sub) in kBlueClashHotActi'
'ons) () {\nfinal hit = list~where((x) => x~action == act)~firstOrNull ?? HotKeyAction(action: act);\nfinal k = hit~key;\nreturn (action: ac'
't, title: ttl, subtitle: sub, modifiers: hit~modifiers, key: k, caps: k != null ? labels~parts(hit~modifiers, k) : const <String>[], err'
': fails[act]);\n}(),\n];\n}\nstatic void setHotKeyRecMode(WidgetRef ref, bool recording) {\ntry { ref~read(hotKeyRecordingProvider~notifier)~'
'value = recording; } catch (_) {}\n}\nstatic String? checkHotKeyConflictTitle(WidgetRef ref, HotAction selfAct, Set<KeyboardModifier> mods'
', int? key) {\nif (key == null) return null;\nfor (final item in ref~read(hotKeyActionsProvider)) {\nif (item~action != selfAct && item~key'
' == key && keyboardModifierListEquality~equals(item~modifiers, mods)) {\nfinal hit = kBlueClashHotActions~where((x) => x~$1 == item~actio'
'n)~firstOrNull;\nreturn hit?~$2 ?? item~action~name;\n}\n}\nreturn null;\n}\nstatic void saveHotKeyRow(WidgetRef ref, HotAction action, Set<Ke'
'yboardModifier> mods, int? key) {\nfinal ntf = ref~read(hotKeyActionsProvider~notifier), cur = ntf~value;\nfinal isBound = key != null && '
'isValidHotKey(mods, key);\nfinal binding = HotKeyAction(action: action, modifiers: mods, key: key);\nfinal out = <HotKeyAction>[];\nvar pla'
'ced = false;\nfor (final item in cur) {\nif (item~action == action) {\nplaced = true;\nif (isBound) out~add(binding);\n} else if (!(isBound &'
'& item~key == key && keyboardModifierListEquality~equals(item~modifiers, mods))) {\nout~add(item);\n}\n}\nif (isBound && !placed) out~add(bi'
'nding);\nntf~value = out;\n}\nstatic LogLevel watchCoreLogLevel(WidgetRef ref) => ref~watch(patchClashConfigProvider~select((s) => s~logLev'
'el));\nstatic void setCoreLogLevel(WidgetRef ref, LogLevel lv) {\nref~read(patchClashConfigProvider~notifier)~update((s) => s~copyWith(log'
'Level: lv));\n}\nstatic List<BridgeLog> watchCoreLogsFull(WidgetRef ref, {int maxItems = 240}) {\ntry {\nfinal l = ref~watch(logsProvider)~l'
'ist;\nfinal start = l~length > maxItems ? l~length - maxItems : 0;\nfinal sub = l~sublist(start);\nreturn <BridgeLog>[for (var i = sub~leng'
"th - 1; i >= 0; i--) (level: sub[i]~logLevel~name, payload: sub[i]~payload, time: '${sub[i]~dateTime}')];\n} catch (_) {\nreturn const <Br"
'idgeLog>[];\n}\n}\nstatic void clearCoreLogs(WidgetRef ref) {\ntry { ref~read(logsProvider~notifier)~value = FixedList(maxLogsLength); } cat'
'ch (_) {}\n}\nstatic Future<bool> exportCoreLogsFile(WidgetRef ref, List<({DateTime t, LogCat cat, String title, String detail, bool ok})>'
" gLogs) async {\ntry {\nfinal sb = StringBuffer()~~writeln('=== BlueClash v$appVersion Diagnostic Logs ===')~~writeln('Exported: ${DateTim"
"e~now()~toIso8601String()}')~~writeln('\n--- Guardian Events (${gLogs~length}) ---');\nfor (final g in gLogs) { sb~writeln('[${g~t~toIso86"
"01String()}] [${g~cat~name}] ${g~title} | ${g~detail}'); }\nfinal cLogs = ref~read(logsProvider)~list;\nsb~writeln('\n--- Mihomo Core Logs "
"(${cLogs~length}) ---');\nfor (final lg in cLogs) { sb~writeln('[${lg~dateTime}] [${lg~logLevel~name~toUpperCase()}] ${lg~payload}'); }\nf"
'inal d = DateTime~now();\nfinal ts = \'${d~year}${d~month~toString()~padLeft(2, "0")}${d~day~toString()~padLeft(2, "0")}-${d~hour~toString'
'()~padLeft(2, "0")}${d~minute~toString()~padLeft(2, "0")}\';\nfinal uri = await picker~saveFile(\'BlueClash-Logs-$ts~log\', Uint8List~fromLi'
"st(utf8~encode(sb~toString())));\nif (uri != null) showBannerMsg('日志文件已导出', kind: 'success');\nreturn uri != null;\n} catch (e) {\nshowBanne"
"rMsg('导出日志失败：$e', kind: 'error');\nreturn false;\n}\n}\nstatic Future<int> closeAllActiveConns(Ref ref) async {\ntry {\nfinal list = await ref"
'~read(coreHandlerProvider)~getConnections()~timeout(const Duration(milliseconds: 1500));\nawait Future~wait(list~map((c) async {\ntry { aw'
'ait ref~read(coreHandlerProvider)~closeConnection(c~id)~timeout(const Duration(milliseconds: 800)); } catch (_) {}\n}));\nreturn list~leng'
'th;\n} catch (_) {\nreturn 0;\n}\n}\nstatic Future<String> readSubYaml(int id) async {'),
('static Future<void> sw', 'await reques',
'static Future<void> switchUiMode(Ref ref, bool simple, {VoidCallback? onStatusChanged}) async {\nsimpleTakeover = true; _ensureRuleAndPro'
'cessMode(ref); _syncAndroidVpnAccessIfStopped(ref, true);\nawait requestApplyProfile(ref, onStatusChanged: onStatusChanged);}'),
]
SG13 = [
('// v127_zero_loop_guardian', '=', '// v128_pure_guardian\n// v127_zero_loop_guardian'),
('Future<void> syncA', '\nawait _B~re',
'Future<void> reloadAfterRestore() async {\n_hlSn~~clear()~~addAll(<String>[for (final v in _B~vendors) ~~~v~hIps]);\n_ec~clear(); _er~clea'
'r();\nawait _rcGs();\nunawaited(refreshCatalogApps());\n_emit();\n}\nFuture<void> syncAndApplyNow({bool force = true}) async {'),
]
SW13 = [
("import 'package:fl", "\nimport 'package:fl_clash/w",
"// v128_eight_tab_pure_ui\nimport 'package:fl_clash/ui/icons/icons~dart';\nimport 'package:fl_clash/common/common~dart' show ShortcutLabel"
"s, isModifierKey, isValidHotKey, primaryHotKeyModifiers;\nimport 'package:fl_clash/enum/enum~dart' show HotAction, KeyboardModifier, LogL"
'evel;'),
('final bool _kSkiaT', '\nconst _bcIs',
'final bool _kSkiaThrottle = Platform~isWindows || Platform~isLinux;\nList<BoxShadow> _e1Shadows(BuildContext context) => context~colorSch'
'eme~brightness == Brightness~dark\n? const <BoxShadow>[BoxShadow(color: Color(0x38000000), offset: Offset(0, 4), blurRadius: 12), BoxShad'
'ow(color: Color(0x20000000), offset: Offset(0, 1), blurRadius: 3)]\n: const <BoxShadow>[BoxShadow(color: Color(0x100F172A), offset: Offse'
't(0, 4), blurRadius: 12), BoxShadow(color: Color(0x080F172A), offset: Offset(0, 1), blurRadius: 3)];\nList<BoxShadow> _e2Shadows(BuildCon'
'text context) => context~colorScheme~brightness == Brightness~dark\n? const <BoxShadow>[BoxShadow(color: Color(0x52000000), offset: Offse'
't(0, 8), blurRadius: 22), BoxShadow(color: Color(0x2E000000), offset: Offset(0, 2), blurRadius: 6)]\n: const <BoxShadow>[BoxShadow(color:'
' Color(0x180F172A), offset: Offset(0, 8), blurRadius: 22), BoxShadow(color: Color(0x0D0F172A), offset: Offset(0, 2), blurRadius: 6)];'),
('class SimpleModeHo', 'class _Spinn',
'class SimpleModeHost extends ConsumerWidget {\nconst SimpleModeHost({super~key, this~originalChild});\nfinal Widget? originalChild;\n@overr'
'ide\nWidget build(BuildContext context, WidgetRef ref) {\ntry { ref~watch(guardianProvider~select((s) => s~auto)); } catch (_) {}\nfinal ap'
'pVis = _FB~watchAppVisible(ref), cs = context~colorScheme, mqSize = MediaQuery~sizeOf(context);\nif (mqSize~isEmpty) return ColoredBox(co'
'lor: SurfaceLevel~page~colorOf(cs));\nreturn TickerMode(enabled: appVis, child: const SimpleWorkbenchView());\n}\n}'),
('(glyph: AppGlyphs~b', '\nclass _Adap',
"(glyph: AppGlyphs~block, mobileLabel: '黑名单', desktopLabel: '全局黑名单'),\n(glyph: AppGlyphs~settings, mobileLabel: '设置', desktopLabel: '系统设置'"
'),\n];'),
('shadows: DashboardShadows~e2(context),', '=', 'shadows: _e2Shadows(context),'),
('size: isDesktop ? 20~0 : 18~5,', '=', 'size: isDesktop ? 19~5 : 17~5,'),
('constraints: const', '\nchild: dock', 'constraints: const BoxConstraints(maxWidth: 760),'),
('String _blAddErr =', 'void _upd(Vo',
"String _blAddErr = '';\nbool _impOpen = false, _impBusy = false, _delSubBusy = false, _bakBusy = false, _connPaused = false, _hkRecHadOld"
" = false;\nString _impErr = '', _delSubLbl = '', _setSect = 'sys', _connQ = '', _logQ = '', _hkRecTitle = '';\nint _delSubId = 0;\nList<Bri"
'dgeConn> _liveConns = const <BridgeConn>[];\nHotAction? _hkRecAct;\nSet<KeyboardModifier> _hkRecMods = const <KeyboardModifier>{};\nint? _h'
'kRecKey;\nfinal _impUrlCtrl = TextEditingController(), _impUrlFocus = FocusNode();\nfinal _impNameCtrl = TextEditingController(), _impName'
'Focus = FocusNode();\nfinal _impAgeCtrl = TextEditingController(), _impAgeFocus = FocusNode();\nfinal _connSearchCtrl = TextEditingControl'
'ler(), _connSearchFocus = FocusNode();\nfinal _logSearchCtrl = TextEditingController(), _logSearchFocus = FocusNode();\nvoid _openImportMo'
"dal() {\n_impUrlCtrl~clear(); _impNameCtrl~clear(); _impAgeCtrl~clear();\n_upd(() { _impErr = ''; _impBusy = false; _impOpen = true; });\n}"
'\nvoid _askDeleteSub(int id, String lbl) {\nHapticFeedback~lightImpact();\n_upd(() { _delSubId = id; _delSubLbl = lbl; _delSubBusy = false;'
' });\n}\nFuture<void> _refreshConnsSnapshot() async {\nfinal ls = await _FB~fetchConns(_gRef);\nif (!mounted) return;\nfinal sorted = List<Br'
'idgeConn>~from(ls)~~sort((a, b) => (b~up + b~down)~compareTo(a~up + a~down));\n_upd(() => _liveConns = sorted~length > 150 ? sorted~subli'
'st(0, 150) : sorted);\n}\nSet<KeyboardModifier> _heldHkModifiers({PhysicalKeyboardKey? except}) {\nfinal pressed = HardwareKeyboard~instanc'
'e~physicalKeysPressed;\nreturn <KeyboardModifier>{for (final m in KeyboardModifier~values) if (m~physicalKeys~any(pressed~contains) && !m'
'~physicalKeys~contains(except)) m};\n}\nbool _onHkKeyEvent(KeyEvent event) {\nif (_hkRecAct == null) return false;\nfinal pk = event~physica'
'lKey;\nif (isModifierKey(pk)) {\nif (event is KeyDownEvent || (event is KeyUpEvent && _hkRecKey == null)) _upd(() { _hkRecKey = null; _hkR'
'ecMods = _heldHkModifiers(); });\nreturn true;\n}\nif (event is KeyUpEvent) return true;\nfinal mods = _heldHkModifiers(except: pk);\nif (pk '
'== PhysicalKeyboardKey~escape && mods~isEmpty) { _closeHkRecorder(); return true; }\n_upd(() { _hkRecMods = mods; _hkRecKey = pk~usbHidUs'
'age; });\nreturn true;\n}\nvoid _openHkRecorder(HotAction act, String title, Set<KeyboardModifier> initMods, int? initKey) {\nHardwareKeyboa'
'rd~instance~removeHandler(_onHkKeyEvent);\nHardwareKeyboard~instance~addHandler(_onHkKeyEvent);\n_FB~setHotKeyRecMode(ref, true);\n_upd(() '
'{ _hkRecAct = act; _hkRecTitle = title; _hkRecMods = Set<KeyboardModifier>~from(initMods); _hkRecKey = initKey; _hkRecHadOld = initKey !'
'= null; });\n}\nvoid _closeHkRecorder() {\nHardwareKeyboard~instance~removeHandler(_onHkKeyEvent);\n_FB~setHotKeyRecMode(ref, false);\nif (mo'
'unted) _upd(() { _hkRecAct = null; _hkRecKey = null; _hkRecMods = const <KeyboardModifier>{}; });\n}\n@override\nvoid initState() {\nsuper~i'
'nitState();\n_FB~onBottomToast = _showBottomToast;\nWidgetsBinding~instance~addPostFrameCallback((_) {\nif (mounted) {\n_blPollTimer = Timer'
'~periodic(const Duration(milliseconds: 1600), (_) {\nif (!mounted) return;\nif (_bTab == 6 && !_blAddOpen) {\nunawaited(_FB~refreshLiveHost'
"sAndBlStats(_gRef)~then((_) { if (mounted && _bTab == 6) _upd(() {}); }));\n} else if (_bTab == 7 && _setSect == 'conns' && !_connPaused "
'&& _hkRecAct == null) {\nunawaited(_refreshConnsSnapshot());\n}\n});\n}\n});\n}'),
('_blTargetsCtrl,\n_blNoteCtrl,\n]) {', '=',
'_blTargetsCtrl,\n_blNoteCtrl,\n_impUrlCtrl,\n_impNameCtrl,\n_impAgeCtrl,\n_connSearchCtrl,\n_logSearchCtrl,\n]) {\nHardwareKeyboard~instance~rem'
'oveHandler(_onHkKeyEvent);'),
('_blTargetsFocus,\n_blNoteFocus,\n]) {', '=',
'_blTargetsFocus,\n_blNoteFocus,\n_impUrlFocus,\n_impNameFocus,\n_impAgeFocus,\n_connSearchFocus,\n_logSearchFocus,\n]) {'),
('shadows: DashboardShadows~e1(c),', '=', 'shadows: _e1Shadows(c),'),
('void _tapBrandIcon', 'List<VendorS', 'void _tapBrandIcon() {\nHapticFeedback~selectionClick();\nif (_bTab != 0) _selectTab(0);\n}\n'),
('} else if (_bTab == 1', ' else if (_b',
"} else if (_bTab == 1) {\ntrailing = _pBtn(c, '新增订阅', _openImportModal, glyph: AppGlyphs~add, solid: true, activeColor: _cB, height: 36, "
'padding: _ehv(14, 0));\n}'),
('} else if (_bTab == 6', '\nreturn Cons',
"} else if (_bTab == 6) {\ntrailing = _pBtn(c, '新增规则', _openBlAddModal, glyph: AppGlyphs~add, solid: true, activeColor: _cB, height: 36, p"
"adding: _ehv(14, 0));\n} else if (_bTab == 7) {\ntrailing = _pBtn(c, _bakBusy ? '处理中~~~' : '一键备份', _bakBusy ? null : () => unawaited(_doBa"
'ckupExport()), glyph: AppGlyphs~export, solid: true, activeColor: _cB, height: 36, padding: _ehv(14, 0));\n}'),
('shadows: DashboardShadows~e2(c),', '=', 'shadows: _e2Shadows(c),'),
("'全局黑名单',\n];", '=', "'全局黑名单',\n'系统设置',\n];"),
('} else if (_bTab == 6) {\np', '\npageBody = ',
'} else if (_bTab == 6) {\npageBody = _buildBlacklistPage(ctx, st, isDesktop);\n} else if (_bTab == 7) {\npageBody = _buildSettingsPage(ctx,'
' st, run, isDesktop);\n} else {'),
('if (!kbOpen && !_p', '\nPositioned(', 'if (!kbOpen && !_pkOpen && !_subOpen && !_blAddOpen && !_impOpen && _delSubId == 0 && _hkRecAct == null)'),
('isDesktop: dBox~maxWidth >= 796,', '=', 'isDesktop: dBox~maxWidth >= 760,'),
('if (_blAddOpen)\nPo', '\nif (_rcptVi',
"if (_blAddOpen)\nPositioned~fill(key: const ValueKey<String>('wb_bl_modal'), child: _buildBlAddModal(sCtx)),\nif (_impOpen)\nPositioned~fil"
"l(key: const ValueKey<String>('wb_imp_modal'), child: _buildSubImportModal(sCtx)),\nif (_delSubId > 0)\nPositioned~fill(key: const ValueKe"
"y<String>('wb_delsub_modal'), child: _buildSubDelConfirmModal(sCtx)),\nif (_hkRecAct != null)\nPositioned~fill(key: const ValueKey<String>"
"('wb_hk_modal'), child: _buildHkRecorderModal(sCtx)),"),
]
HOME13 = (
"// v128_pure_blueclash_home\nimport 'package:fl_clash/custom/simple_workbench~dart';\nimport 'package:fl_clash/providers/providers~dart';\n"
"import 'package:fl_clash/widgets/widgets~dart';\nimport 'package:flutter/widgets~dart';\nimport 'package:flutter_riverpod/flutter_riverpod"
"~dart';\n\nclass HomePage extends ConsumerWidget {\nconst HomePage({super~key});\n@override\nWidget build(BuildContext context, WidgetRef ref"
') {\nreturn PopGuard(\nonPop: (ctx) async {\nif (Navigator~canPop(ctx)) { Navigator~of(ctx)~pop(); } else { await ref~read(systemActionProv'
'ider~notifier)~handleClose(); }\nreturn false;\n},\nchild: const SimpleModeHost(),\n);\n}\n}')
NAV13 = (
"// v128_stripped_views_nav\nimport 'package:fl_clash/common/app_ports~dart';\nimport 'package:fl_clash/enum/enum~dart';\nimport 'package:fl"
"_clash/models/models~dart';\nimport 'package:fl_clash/ui/icons/app_glyphs~dart';\nimport 'package:flutter/widgets~dart';\n\nclass Navigation"
' implements NavigationPort {\nstatic Navigation? _instance;\n@override\nList<NavigationItem> getItems({bool openLogs = false, bool hasProxi'
'es = false}) => <NavigationItem>[\nNavigationItem(glyph: AppGlyphs~dashboard, label: PageLabel~dashboard, builder: (_) => const SizedBox~'
'shrink()),\n];\nNavigation~_internal();\nfactory Navigation() => _instance ??= Navigation~_internal();\n}\nfinal navigation = Navigation();')
HKO13 = (
'      case HotAction~mode:\n        commonAction~updateMode();\n      case HotAction~start:\n        commonAction~toggleRunning();\n      ca'
'se HotAction~view:\n        unawaited(systemAction~updateVisible());\n      case HotAction~proxy:\n        systemAction~updateSystemProxy()'
';\n      case HotAction~tun:\n        systemAction~updateTun();\n      case HotAction~ruleMode:\n        setupAction~changeMode(Mode~rule);\n'
'      case HotAction~globalMode:\n        setupAction~changeMode(Mode~global);\n      case HotAction~directMode:\n        setupAction~chang'
'eMode(Mode~direct);\n      case HotAction~delayTest:\n        unawaited(\n          ref\n              ~read(proxiesActionProvider~notifier)'
'\n              ~delayTestGroups(ref~read(currentGroupsStateProvider)~value),\n        );\n      case HotAction~updateProfiles:\n        una'
'waited(\n          globalState~safeRun(\n            ref~read(profilesActionProvider~notifier)~updateProfiles,\n          ),\n        );')
HKN13 = (
'      case HotAction~mode:\n        unawaited(ref~read(guardianProvider~notifier)~setFbDir(!FlClashBridge~fbDir));\n      case HotAction~s'
'tart:\n        commonAction~toggleRunning();\n      case HotAction~view:\n        unawaited(systemAction~updateVisible());\n      case HotAc'
'tion~proxy:\n        systemAction~updateSystemProxy();\n      case HotAction~tun:\n        systemAction~updateTun();\n      case HotAction~r'
'uleMode:\n        unawaited(ref~read(guardianProvider~notifier)~setFbDir(false));\n      case HotAction~globalMode:\n        unawaited(ref~'
'read(guardianProvider~notifier)~setFbDir(false));\n      case HotAction~directMode:\n        unawaited(ref~read(guardianProvider~notifier)'
'~setFbDir(true));\n      case HotAction~delayTest:\n        unawaited(ref~read(guardianProvider~notifier)~chkNow());\n      case HotAction~'
'updateProfiles:\n        unawaited(FlClashBridge~syncAllSubsWithReport(ref));')
def ck_a(): assert hashlib .sha256(repr((FB13, SG13, SW13, HOME13, NAV13, HKO13, HKN13)) .encode('utf-8')) .hexdigest()[:12] == 'bf826d96013b'
