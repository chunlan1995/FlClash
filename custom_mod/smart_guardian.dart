// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, unawaited_futures, curly_braces_in_flow_control_structures
import 'dart:async'; import 'dart:io'; import 'package:flutter_riverpod/flutter_riverpod.dart'; import 'flclash_bridge.dart';
enum MatchTier { s24('同/24网段'), s16('同/16网段'), region('同国家/区域'), global('全局低延迟'); const MatchTier(this.label); final String label; }
enum LogCat { failover('无缝转接'), conn('进程连接'), warn('延迟预警'), core('系统核心'); const LogCat(this.label); final String label; }
typedef EndpointMeta = ({String ip, String? s24, String? s16, String regCode, String regLabel, String raw});
typedef ProcStat = ({String name, int upRate, int downRate, int sumUp, int sumDown, int conns, String exit});
typedef LogItem = ({int id, DateTime time, LogCat cat, String title, String detail, bool hot});
typedef SwitchRec = ({DateTime time, String from, String to, int ms, MatchTier tier, String detail, int reset}); class GuardianState {
const GuardianState({this.autoSwitch = true, this.limitMs = 1000, this.probing = false, this.group = '', this.node = '', this.delayMs = 0, this.meta, this.sumUp = 0, this.sumDown = 0, this.upRate = 0, this.downRate = 0, this.procs = const [], this.switches = const [], this.logs = const []});
final bool autoSwitch, probing; final int limitMs, delayMs, sumUp, sumDown, upRate, downRate; final String group, node; final EndpointMeta? meta;
final List<ProcStat> procs; final List<SwitchRec> switches; final List<LogItem> logs; int get sumTotal => sumUp + sumDown;
GuardianState copy({bool? autoSwitch, int? limitMs, bool? probing, String? group, String? node, int? delayMs, EndpointMeta? meta, int? sumUp, int? sumDown, int? upRate, int? downRate, List<ProcStat>? procs, List<SwitchRec>? switches, List<LogItem>? logs}) =>
GuardianState(autoSwitch: autoSwitch ?? this.autoSwitch, limitMs: limitMs ?? this.limitMs, probing: probing ?? this.probing, group: group ?? this.group, node: node ?? this.node, delayMs: delayMs ?? this.delayMs, meta: meta ?? this.meta, sumUp: sumUp ?? this.sumUp, sumDown: sumDown ?? this.sumDown, upRate: upRate ?? this.upRate, downRate: downRate ?? this.downRate, procs: procs ?? this.procs, switches: switches ?? this.switches, logs: logs ?? this.logs);
} String fmtBytes(int b) { if (b <= 0) return '0 B'; const u = ['B', 'KB', 'MB', 'GB', 'TB']; var v = b.toDouble(); var i = 0;
while (v >= 1024 && i < 4) { v /= 1024; i++; } return '${v.toStringAsFixed(i == 0 ? 0 : (v >= 100 ? 1 : 2))} ${u[i]}'; }
String fmtRate(int bps) => '${fmtBytes(bps)}/s';
String fmtTime(DateTime d) => '${d.hour.toString().padLeft(2, '0')}:${d.minute.toString().padLeft(2, '0')}:${d.second.toString().padLeft(2, '0')}';
final simpleModeProvider = NotifierProvider<SimpleModeNotifier, bool>(SimpleModeNotifier.new);
class SimpleModeNotifier extends Notifier<bool> { @override bool build() => true; void setMode(bool v) => state = v; }
final guardianProvider = NotifierProvider<GuardianNotifier, GuardianState>(GuardianNotifier.new); class GuardianNotifier extends Notifier<GuardianState> {
Timer? _t1, _t2; DateTime? _lastAt, _lastSwAt; bool _b1 = false, _b2 = false; int _seq = 1; String _logSig = ''; final Map<String, EndpointMeta> _epCache = {};
final Map<String, (int, int)> _cursors = {}; final Set<String> _seenIds = {}; final Map<String, ProcStat> _procs = {}; final Map<String, DateTime> _cool = {};
static const _pseudo = {'DIRECT', 'REJECT', 'REJECT-DROP', 'PASS', 'COMPATIBLE'}; static const _regs = <(String, String, List<String>)>[
('HK', '香港HK', ['🇭🇰', 'hong kong', 'hongkong', '香港', 'hk']), ('TW', '台湾TW', ['🇹🇼', 'taiwan', 'taipei', '台湾', '台北', 'tw']),
('SG', '新加坡SG', ['🇸🇬', 'singapore', '新加坡', '狮城', 'sg']), ('JP', '日本JP', ['🇯🇵', 'japan', 'tokyo', 'osaka', '日本', '东京', '大阪', 'jp']),
('KR', '韩国KR', ['🇰🇷', 'korea', 'seoul', '韩国', '首尔', 'kr']), ('US', '美国US', ['🇺🇸', 'america', 'los angeles', 'san jose', 'seattle', '美国', '洛杉矶', '圣何塞', '西雅图', '硅谷', '纽约', 'us']),
('GB', '英国UK', ['🇬🇧', 'london', 'britain', '英国', '伦敦', 'uk', 'gb']), ('DE', '德国DE', ['🇩🇪', 'germany', 'frankfurt', '德国', '法兰克福', 'de']),
('FR', '法国FR', ['🇫🇷', 'france', 'paris', '法国', 'fr']), ('NL', '荷兰NL', ['🇳🇱', 'netherlands', '荷兰', 'nl']),
('CA', '加拿大CA', ['🇨🇦', 'canada', '加拿大', 'ca']), ('AU', '澳洲AU', ['🇦🇺', 'australia', '澳大利亚', '悉尼', 'au']),
('RU', '俄罗斯RU', ['🇷🇺', 'russia', '俄罗斯', 'ru']), ('IN', '印度IN', ['🇮🇳', 'india', '印度', 'in']),
('MY', '大马MY', ['🇲🇾', 'malaysia', '马来西亚', 'my']), ('TH', '泰国TH', ['🇹🇭', 'thailand', '泰国', 'th']), ]; @override GuardianState build() {
ref.onDispose(() { _t1?.cancel(); _t2?.cancel(); }); Future<void>.microtask(() { _t1 = Timer.periodic(const Duration(seconds: 1), (_) => unawaited(_tickFast()));
_t2 = Timer.periodic(const Duration(seconds: 4), (_) => unawaited(_tickProbe(false)));
_addLog(LogCat.core, '极简智控守护已启动', '严格阈值 1000ms · 同/24→/16网段→同区域无缝转接 · 当次运行进程流量统计', true); }); return const GuardianState(); }
void setAuto(bool v) { state = state.copy(autoSwitch: v); _addLog(LogCat.core, v ? '已开启超时自动无缝转接' : '已暂停超时自动无缝转接', '阈值: ${state.limitMs}ms'); }
void setLimit(int ms) { state = state.copy(limitMs: ms); _addLog(LogCat.core, '超时阈值已设为 ${ms}ms', '探测 >= ${ms}ms 或无响应立即触发同段/同区无缝转接'); }
void resetTraffic() { _procs.clear(); state = state.copy(sumUp: 0, sumDown: 0, upRate: 0, downRate: 0, procs: const []); _addLog(LogCat.core, '已清零当次运行累计流量', '进程上下行统计已重新开始'); }
void clearLogs() => state = state.copy(logs: const []); Future<void> manualCheck() => _tickProbe(true); Future<void> pickNode(String grp, String node) async {
await FlClashBridge.selectNode(ref, groupName: grp, proxyName: node); final m = await _resolveMeta(node);
final d = await FlClashBridge.testDelayMs(ref, node, timeoutMs: state.limitMs); state = state.copy(group: grp, node: node, delayMs: d, meta: m);
_addLog(LogCat.core, '手动切换节点: $node', '策略组: $grp · 延迟: ${d > 0 ? "${d}ms" : "超时/待测"} · ${m.ip.isNotEmpty ? m.ip : m.regLabel}'); }
void _addLog(LogCat cat, String title, String detail, [bool hot = false]) {
final l = [(id: _seq++, time: DateTime.now(), cat: cat, title: title, detail: detail, hot: hot), ...state.logs]; if (l.length > 220) l.removeRange(220, l.length);
state = state.copy(logs: l); } (String, String) _detectReg(String name, String srv) { final s = '${name.toLowerCase()} ${srv.toLowerCase()}';
for (final (c, lbl, toks) in _regs) { for (final t in toks) {
if (t.length <= 2 ? RegExp('(^|[^a-z0-9])${RegExp.escape(t)}([^a-z0-9]|\$)').hasMatch(s) : s.contains(t)) return (c, lbl); } } return ('OTHER', '其他区域'); }
Future<EndpointMeta> _resolveMeta(String name) async { final prev = _epCache[name]; if (prev != null && (prev.ip.isNotEmpty || prev.raw.isEmpty)) return prev;
final srv = await FlClashBridge.queryServer(ref, name); final (rc, rl) = _detectReg(name, srv);
if (srv.isEmpty) return _epCache[name] = (ip: '', s24: null, s16: null, regCode: rc, regLabel: rl, raw: ''); InternetAddress? addr = InternetAddress.tryParse(srv);
if (addr == null) { try { final r = await InternetAddress.lookup(srv).timeout(const Duration(milliseconds: 1200));
if (r.isNotEmpty) addr = r.firstWhere((a) => a.type == InternetAddressType.IPv4, orElse: () => r.first); } catch (_) {} } String? s24, s16;
if (addr != null && addr.type == InternetAddressType.IPv4 && addr.rawAddress.length == 4) {
final b = addr.rawAddress; s24 = '${b[0]}.${b[1]}.${b[2]}.0/24'; s16 = '${b[0]}.${b[1]}.0.0/16'; }
return _epCache[name] = (ip: addr?.address ?? '', s24: s24, s16: s16, regCode: rc, regLabel: rl, raw: srv); } (BridgeGroup?, String) _leafOf(List<BridgeGroup> gs) {
if (gs.isEmpty) return (null, ''); final m = {for (final g in gs) g.name: g};
var sel = gs.firstWhere((g) => g.isSelector && g.all.isNotEmpty, orElse: () => gs.first); var leaf = sel.now; for (var i = 0; i < 6 && m.containsKey(leaf); i++) {
final sub = m[leaf]!; if (sub.isSelector && sub.all.isNotEmpty) sel = sub; if (sub.now.isEmpty || sub.now == leaf) break; leaf = sub.now; } return (sel, leaf); }
Future<void> _tickFast() async { if (_b1) return; _b1 = true; try { final cLogs = FlClashBridge.readLogs(ref); if (cLogs.isNotEmpty) {
final last = cLogs.last; final sig = '${last.time}|${last.payload}'; if (sig != _logSig) { _logSig = sig; final low = last.payload.toLowerCase();
if (low.contains('i/o timeout') || low.contains('deadline exceeded') || (low.contains('dial') && low.contains('timeout'))) {
_addLog(LogCat.warn, '捕获底层连接超时', last.payload, true); if (state.autoSwitch && FlClashBridge.isRunning(ref)) unawaited(_tickProbe(false, true)); } } }
final gs = FlClashBridge.readGroups(ref); final (sel, leaf) = _leafOf(gs);
if (sel != null && leaf.isNotEmpty && leaf != state.node) state = state.copy(group: sel.name, node: leaf, meta: await _resolveMeta(leaf));
if (!FlClashBridge.isRunning(ref)) { _cursors.clear(); _lastAt = null; if (state.upRate != 0 || state.downRate != 0) {
state = state.copy(upRate: 0, downRate: 0, procs: [for (final p in _procs.values) (name: p.name, upRate: 0, downRate: 0, sumUp: p.sumUp, sumDown: p.sumDown, conns: 0, exit: p.exit)]);
} return; } final now = DateTime.now(); final dt = _lastAt == null ? 1000 : now.difference(_lastAt!).inMilliseconds.clamp(250, 5000); _lastAt = now;
final conns = await FlClashBridge.fetchConns(ref); final pkgMap = FlClashBridge.readPkgNames(ref);
final live = <String>{}; final dUpMap = <String, int>{}, dDownMap = <String, int>{}, cntMap = <String, int>{}; var gUp = 0, gDown = 0; for (final c in conns) {
live.add(c.id); final prev = _cursors[c.id]; final du = prev == null ? c.up : (c.up >= prev.$1 ? c.up - prev.$1 : 0);
final dd = prev == null ? c.down : (c.down >= prev.$2 ? c.down - prev.$2 : 0); _cursors[c.id] = (c.up, c.down); final raw = c.proc.trim().replaceAll('\\', '/');
final pName = raw.isNotEmpty ? (pkgMap[raw] ?? raw.split('/').last) : ((c.uid != null && c.uid! > 0) ? (pkgMap['uid:${c.uid}'] ?? 'App (UID:${c.uid})') : '系统/未知进程');
final ex = c.chains.isNotEmpty ? c.chains.first : leaf; if (!_seenIds.contains(c.id) && c.target.isNotEmpty) {
_seenIds.add(c.id); if (_seenIds.length > 1200) _seenIds.remove(_seenIds.first);
_addLog(LogCat.conn, '$pName → ${c.target}', '${c.net.toUpperCase()} · 出口: ${ex.isEmpty ? "DIRECT" : ex}'); }
cntMap[pName] = (cntMap[pName] ?? 0) + 1; dUpMap[pName] = (dUpMap[pName] ?? 0) + du; dDownMap[pName] = (dDownMap[pName] ?? 0) + dd; gUp += du; gDown += dd;
final old = _procs[pName];
_procs[pName] = (name: pName, upRate: 0, downRate: 0, sumUp: (old?.sumUp ?? 0) + du, sumDown: (old?.sumDown ?? 0) + dd, conns: cntMap[pName]!, exit: ex.isNotEmpty ? ex : (old?.exit ?? ''));
} _cursors.removeWhere((k, _) => !live.contains(k)); final k = 1000.0 / dt; final list = <ProcStat>[]; for (final e in _procs.entries) {
final item = (name: e.key, upRate: ((dUpMap[e.key] ?? 0) * k).round(), downRate: ((dDownMap[e.key] ?? 0) * k).round(), sumUp: e.value.sumUp, sumDown: e.value.sumDown, conns: cntMap[e.key] ?? 0, exit: e.value.exit);
_procs[e.key] = item; list.add(item); }
list.sort((a, b) => (a.upRate + a.downRate > 0 || b.upRate + b.downRate > 0) ? (b.upRate + b.downRate).compareTo(a.upRate + a.downRate) : (b.sumUp + b.sumDown).compareTo(a.sumUp + a.sumDown));
state = state.copy(sumUp: state.sumUp + gUp, sumDown: state.sumDown + gDown, upRate: (gUp * k).round(), downRate: (gDown * k).round(), procs: list);
} catch (_) {} finally { _b1 = false; } } Future<void> _tickProbe(bool manual, [bool fromLog = false]) async {
if (_b2 || (!manual && (!FlClashBridge.isRunning(ref) || !state.autoSwitch))) return;
if (!manual && _lastSwAt != null && DateTime.now().difference(_lastSwAt!).inSeconds < 4) return; _b2 = true; state = state.copy(probing: true); try {
final gs = FlClashBridge.readGroups(ref); final (sel, leaf) = _leafOf(gs); if (sel == null || leaf.isEmpty || _pseudo.contains(leaf.toUpperCase())) return;
final cur = await _resolveMeta(leaf); final lim = state.limitMs; var d = await FlClashBridge.testDelayMs(ref, leaf, timeoutMs: lim);
if (!manual && d >= lim) { await Future<void>.delayed(const Duration(milliseconds: 200)); d = await FlClashBridge.testDelayMs(ref, leaf, timeoutMs: lim); }
state = state.copy(group: sel.name, node: leaf, delayMs: d, meta: cur);
if (d > 0 && d < lim) { if (manual) _addLog(LogCat.core, '测速健康: $leaf (${d}ms < ${lim}ms)', '${cur.ip} ${cur.regLabel}'.trim()); return; }
final why = d <= 0 ? (fromLog ? '拨号超时 & 探测无响应' : '探测超时 (> ${lim}ms)') : '延迟 ${d}ms >= ${lim}ms'; _cool[leaf] = DateTime.now().add(const Duration(seconds: 35));
_addLog(LogCat.warn, '触发超时无缝转接: $leaf', '$why · 正在匹配同网段(${cur.s24 ?? cur.regLabel})可用节点', true);
final gSet = {for (final g in gs) g.name}; final now = DateTime.now();
final pool = sel.all.where((n) => n != leaf && !_pseudo.contains(n.toUpperCase()) && !gSet.contains(n) && (_cool[n] == null || !_cool[n]!.isAfter(now))).toList();
if (pool.isEmpty) return; final metas = <String, EndpointMeta>{}; for (var i = 0; i < pool.length; i += 8) { final chunk = pool.skip(i).take(8).toList();
final res = await Future.wait(chunk.map(_resolveMeta)); for (var j = 0; j < chunk.length; j++) metas[chunk[j]] = res[j]; }
int rnk(EndpointMeta m) => (cur.s24 != null && m.s24 == cur.s24) ? 0 : (cur.s16 != null && m.s16 == cur.s16) ? 1 : (cur.regCode != 'OTHER' && m.regCode == cur.regCode) ? 2 : 3;
pool.sort((a, b) => rnk(metas[a]!).compareTo(rnk(metas[b]!)));
final probed = await Future.wait(pool.take(18).map((n) async => (n, await FlClashBridge.testDelayMs(ref, n, timeoutMs: lim))));
final ok = <(String, int, MatchTier, String)>[]; for (final (n, ms) in probed) { if (ms <= 0 || ms >= lim) continue; final m = metas[n]!;
if (cur.s24 != null && m.s24 == cur.s24) ok.add((n, ms, MatchTier.s24, m.s24!));
else if (cur.s16 != null && m.s16 == cur.s16) ok.add((n, ms, MatchTier.s16, m.s16!));
else if (cur.regCode != 'OTHER' && m.regCode == cur.regCode) ok.add((n, ms, MatchTier.region, m.regLabel)); else ok.add((n, ms, MatchTier.global, m.regLabel)); }
if (ok.isEmpty) { _addLog(LogCat.warn, '未找到 < ${lim}ms 的达标节点', '稍后自动重试', true); return; }
ok.sort((a, b) => a.$3.index != b.$3.index ? a.$3.index.compareTo(b.$3.index) : a.$2.compareTo(b.$2)); final (best, bestMs, tier, det) = ok.first;
await FlClashBridge.selectNode(ref, groupName: sel.name, proxyName: best); var resetCnt = 0;
for (final c in await FlClashBridge.fetchConns(ref)) { if (c.chains.contains(leaf)) { await FlClashBridge.closeConn(ref, c.id); resetCnt++; } }
_lastSwAt = DateTime.now(); final sw = (time: _lastSwAt!, from: leaf, to: best, ms: bestMs, tier: tier, detail: det, reset: resetCnt);
state = state.copy(group: sel.name, node: best, delayMs: bestMs, meta: metas[best], switches: [sw, ...state.switches.take(25)]);
_addLog(LogCat.failover, '无缝转接成功: $leaf → $best (${bestMs}ms)', '匹配: ${tier.label} [$det] · 原因: $why · 已迁移重置 $resetCnt 条连接', true);
} finally { _b2 = false; state = state.copy(probing: false); } } }
