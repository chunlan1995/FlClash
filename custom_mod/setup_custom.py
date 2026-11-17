#!/usr/bin/env python3
"""FlClash Custom Build Wiring: generates bridge, copies custom UI/guardian, patches HomePage, signs Android APK."""
import pathlib
import re
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
MOD = pathlib.Path(__file__).resolve().parent


def read_tree(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        return ''
    if p.is_file():
        return p.read_text(encoding='utf-8', errors='ignore')
    return '\n'.join(f.read_text(encoding='utf-8', errors='ignore') for f in sorted(p.rglob('*.dart')))


BRIDGE_TMPL = """// ignore_for_file: require_trailing_commas, lines_longer_than_80_chars, dead_null_aware_expression, invalid_null_aware_operator
import 'dart:async';
import 'package:fl_clash/core/core.dart';
import 'package:fl_clash/database/database.dart';
import 'package:fl_clash/enum/enum.dart';
import 'package:fl_clash/models/models.dart';
import 'package:fl_clash/providers/providers.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

typedef BridgeProfile = ({String label, bool selected, VoidCallback onSelect});
typedef BridgeGroup = ({String name, bool isSelector, String now, List<String> all});
typedef BridgeConn = ({String id, int up, int down, String proc, int? uid, String target, String net, List<String> chains});
typedef BridgeLog = ({String level, String payload, String time});

class FlClashBridge {
  static const String probeUrl = 'https://www.gstatic.com/generate_204';

  static bool isRunning(Ref ref) => __READ_RUN__;

  static bool watchRunning(WidgetRef ref) => __WATCH_RUN__;

  static Future<void> toggleRunning(WidgetRef ref, BuildContext context, bool enable) async {
    final _ = context;
    await ref.read(setupActionProvider.notifier).setRunning(enable);
  }

  static List<BridgeProfile> watchProfiles(WidgetRef ref) {
    try {
      final list = ref.watch(profilesProvider);
      final notifier = ref.read(profilesProvider.notifier);
      __WATCH_CUR__
      return [
        for (final raw in list)
          () {
            final p = notifier.labeled(raw);
            final lbl = __PROF_LBL__;
            return (
              label: lbl.isNotEmpty ? lbl : '订阅 #${p.id}',
              selected: p.id == curId,
              onSelect: () {
                __SEL_PROF__
              },
            );
          }(),
      ];
    } catch (_) {
      return const [];
    }
  }

  static List<BridgeGroup> _groups(Iterable<Group> list) => [
    for (final g in list)
      (
        name: g.name,
        isSelector: g.type == __SEL_ENUM__,
        now: g.now ?? '',
        all: [for (final p in g.all) p.name],
      ),
  ];

  static List<BridgeGroup> readGroups(Ref ref) {
    try {
      return _groups(ref.read(groupsProvider));
    } catch (_) {
      return const [];
    }
  }

  static List<BridgeGroup> watchGroups(WidgetRef ref) {
    try {
      return _groups(ref.watch(groupsProvider));
    } catch (_) {
      return const [];
    }
  }

  static Future<void> selectNode(Ref ref, {required String groupName, required String proxyName}) async {
    await ref.read(proxiesActionProvider.notifier).changeProxy(
      groupName: groupName,
      proxyName: proxyName,
    );
  }

  static Future<String> queryServer(Ref ref, String name) async {
    try {
      final d = await __CORE__.getProxyDefinition(name);
      return '${d?['server'] ?? ''}'.trim();
    } catch (_) {
      return '';
    }
  }

  static Future<int> testDelayMs(Ref ref, String name, {int timeoutMs = 1000}) async {
    try {
      final r = await __CORE__
          .testDelay(TestDelayParams(proxyName: name, testUrl: probeUrl, timeout: timeoutMs))
          .timeout(Duration(milliseconds: timeoutMs + 150));
      return r.value ?? -1;
    } catch (_) {
      return -1;
    }
  }

  static Map<String, String> readPkgNames(Ref ref) {
    try {
      final pkgs = ref.read(packagesProvider);
      return {
        for (final pkg in pkgs) ...{
          __PKG_MAP__
        },
      };
    } catch (_) {
      return const {};
    }
  }

  static Future<List<BridgeConn>> fetchConns(Ref ref) async {
    try {
      final list = await __CORE__.getConnections();
      return [
        for (final c in list)
          (
            id: c.id,
            up: c.upload,
            down: c.download,
            proc: c.metadata.process,
            uid: __UID__,
            target: (c.metadata.host.isNotEmpty ? c.metadata.host : c.metadata.destinationIP).isNotEmpty
                ? '${c.metadata.host.isNotEmpty ? c.metadata.host : c.metadata.destinationIP}:${c.metadata.destinationPort}'
                : '',
            net: c.metadata.network,
            chains: c.chains,
          ),
      ];
    } catch (_) {
      return const [];
    }
  }

  static Future<void> closeConn(Ref ref, String id) async {
    try {
      await __CORE__.closeConnection(id);
    } catch (_) {}
  }

  static List<BridgeLog> readLogs(Ref ref) {
    try {
      final l = __LOGS_LIST__;
      final s = l.length > 25 ? l.length - 25 : 0;
      return [
        for (final i in l.sublist(s))
          (level: i.logLevel.name, payload: i.payload, time: '${i.dateTime}'),
      ];
    } catch (_) {
      return const [];
    }
  }
}
"""


def detect_core_expr(prov: str, views: str, core_files: str) -> str:
    all_src = prov + '\n' + views
    mc = re.search(r'(ref\.read\(\w+Provider\)|\b\w*coreController\b)\s*\.\s*(?:testDelay|getConnections|getProxyDefinition)\b', all_src)
    if mc:
        return mc.group(1)
    if 'coreHandlerProvider' in prov:
        return 'ref.read(coreHandlerProvider)'
    if 'coreController' in all_src or 'coreController' in core_files:
        return 'coreController'
    mp = re.search(r'\b(\w*core\w*Provider)\b', read_tree('lib/providers/core.dart') + '\n' + read_tree('lib/providers/generated'))
    if mp:
        return f'ref.read({mp.group(1)})'
    return 'coreController'


def detect_profile_wiring(prov: str, views: str) -> tuple[str, str]:
    all_src = prov + '\n' + views
    if 'currentProfileIdProvider' not in prov:
        return 'const int? curId = null;', ''
    watch_cur = 'final curId = ref.watch(currentProfileIdProvider);'
    if re.search(r'currentProfileIdProvider\.notifier\s*\)\s*\.value\s*=', all_src):
        return watch_cur, 'ref.read(currentProfileIdProvider.notifier).value = p.id;'
    if re.search(r'currentProfileIdProvider\.notifier\s*\)\s*\.update\s*\(\s*\(', all_src):
        return watch_cur, 'ref.read(currentProfileIdProvider.notifier).update((_) => p.id);'
    m_fn = re.search(r'class\s+CurrentProfileId\b[\s\S]{0,600}\bvoid\s+(\w+)\s*\(\s*int\??\s+\w+\s*\)', prov)
    if m_fn:
        return watch_cur, f'ref.read(currentProfileIdProvider.notifier).{m_fn.group(1)}(p.id);'
    if 'set value(' in prov:
        return watch_cur, 'ref.read(currentProfileIdProvider.notifier).value = p.id;'
    return watch_cur, ''


def main() -> None:
    prov = read_tree('lib/providers')
    views = read_tree('lib/views')
    models = read_tree('lib/models') + '\n' + read_tree('lib/database')
    enums = read_tree('lib/enum')
    core_files = read_tree('lib/core')

    read_run = 'ref.read(isStartProvider)' if 'isStartProvider' in prov else 'ref.read(runTimeProvider) != null'
    watch_run = 'ref.watch(isStartProvider)' if 'isStartProvider' in prov else 'ref.watch(runTimeProvider) != null'
    core_expr = detect_core_expr(prov, views, core_files)
    watch_cur, sel_prof = detect_profile_wiring(prov, views)
    prof_lbl = 'p.realLabel' if ('get realLabel' in models or '.realLabel' in views) else "(p.label ?? '').trim()"
    sel_enum = 'GroupType.Selector' if 'Selector' in enums else 'GroupType.selector'

    m_meta = re.search(r'class\s+Metadata\b[\s\S]{0,1500}', models)
    has_uid = bool(re.search(r'\buid\b', m_meta.group(0) if m_meta else models))
    uid_expr = "int.tryParse('${c.metadata.uid}')" if has_uid else 'null'

    m_pkg = re.search(r'class\s+Package\b[\s\S]{0,1200}', models)
    ptxt = m_pkg.group(0) if m_pkg else ''
    if 'packageName' in ptxt and 'label' in ptxt:
        pkg_map = "pkg.packageName: '${pkg.label} (${pkg.packageName})',"
        if 'uid' in ptxt:
            pkg_map += " 'uid:${pkg.uid}': '${pkg.label} (${pkg.packageName})',"
    else:
        pkg_map = ''

    m_fl = re.search(r'class\s+FixedList\b[\s\S]{0,800}', models + '\n' + read_tree('lib/common'))
    fl_txt = m_fl.group(0) if m_fl else 'list'
    logs_list = 'ref.read(logsProvider).list' if re.search(r'\blist\b', fl_txt) else 'ref.read(logsProvider).toList()'

    bridge = (
        BRIDGE_TMPL
        .replace('__READ_RUN__', read_run)
        .replace('__WATCH_RUN__', watch_run)
        .replace('__CORE__', core_expr)
        .replace('__WATCH_CUR__', watch_cur)
        .replace('__SEL_PROF__', sel_prof)
        .replace('__PROF_LBL__', prof_lbl)
        .replace('__SEL_ENUM__', sel_enum)
        .replace('__UID__', uid_expr)
        .replace('__PKG_MAP__', pkg_map)
        .replace('__LOGS_LIST__', logs_list)
    )

    out_dir = ROOT / 'lib/custom'
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'flclash_bridge.dart').write_text(bridge, encoding='utf-8')
    shutil.copyfile(MOD / 'smart_guardian.dart', out_dir / 'smart_guardian.dart')
    shutil.copyfile(MOD / 'simple_workbench.dart', out_dir / 'simple_workbench.dart')

    hp = ROOT / 'lib/pages/home.dart'
    hsrc = hp.read_text(encoding='utf-8')
    if 'SimpleModeHost(' not in hsrc:
        hsrc = hsrc.replace(
            "import 'package:prism_ui/prism_ui.dart';",
            "import 'package:fl_clash/custom/simple_workbench.dart';\nimport 'package:prism_ui/prism_ui.dart';",
            1,
        ).replace(
            '  @override\n  Widget build(BuildContext context, WidgetRef ref) {',
            '  @override\n  Widget build(BuildContext context, WidgetRef ref) {\n'
            '    return SimpleModeHost(originalChild: _buildOriginalHome(context, ref));\n  }\n\n'
            '  Widget _buildOriginalHome(BuildContext context, WidgetRef ref) {',
            1,
        )
        assert 'SimpleModeHost(' in hsrc, 'HomePage patch target not matched'
        hp.write_text(hsrc, encoding='utf-8')

    ad = ROOT / 'android'
    ks = ad / 'app/keystore.jks'
    lp = ad / 'local.properties'
    kt = shutil.which('keytool')
    if ad.exists() and kt and not ks.exists():
        subprocess.run(
            [
                kt, '-genkeypair', '-v', '-keystore', str(ks),
                '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
                '-alias', 'flclash', '-storepass', 'flclash123', '-keypass', 'flclash123',
                '-dname', 'CN=FlClashCustom, OU=Dev, O=Custom, L=City, S=State, C=CN',
            ],
            check=True,
        )
        with lp.open('a', encoding='utf-8') as f:
            f.write('\nkeyAlias=flclash\nstorePassword=flclash123\nkeyPassword=flclash123\n')

    print(f'Custom FlClash wired: run={read_run}, core={core_expr}, profile={prof_lbl}')


if __name__ == '__main__':
    main()
