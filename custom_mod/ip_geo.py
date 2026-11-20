import pathlib, re
from ip_geo_db import GEO_CLS, BRG_P1
from ip_geo_core import BRG_P2, DET_NAME, PARSE_DISK
NEW_RC = r"""Future<void> _rcGs()async{await _B.syncProfileNodesFromDisk(ref);for(final(nm,sv)in _B.cfgProxyNodes){final prev=_ec[nm],a=InternetAddress.tryParse(sv),ip=(prev?.ip.isNotEmpty??false)?prev!.ip:(a?.address??''),raw=(prev?.raw.isNotEmpty??false)?prev!.raw:sv,s24=prev?.s24??((a!=null&&a.type==InternetAddressType.IPv4&&a.rawAddress.length==4)?'${a.rawAddress[0]}.${a.rawAddress[1]}.${a.rawAddress[2]}.0/24':null),s16=prev?.s16??((a!=null&&a.type==InternetAddressType.IPv4&&a.rawAddress.length==4)?'${a.rawAddress[0]}.${a.rawAddress[1]}.0.0/16':null);final(rc,rl)=_B.resolveReg(nm,raw,ip);_ec[nm]=(ip:ip,s24:s24,s16:s16,rc:rc,rl:rl,raw:raw);}final gs=_B.readGroups(ref);if(gs.isNotEmpty&&_B.simpleTakeover&&!_B.applyingProfile&&!gs.any((g)=>g.name==_B.hubGroup)){unawaited(_B.requestApplyProfile(ref,onStatusChanged:_emit));return;}var(realNodes,gMap,hubLeaf)=gs.isNotEmpty?_exTp(gs):(const<String>[],<String,BridgeGroup>{},'');if(_B.cfgProxyNodes.isNotEmpty){final rSet=realNodes.toSet(),gSet=gMap.keys.toSet();realNodes=<String>[...realNodes,for(final p in _B.cfgProxyNodes)if(!gSet.contains(p.$1)&&rSet.add(p.$1))p.$1];if(hubLeaf.isEmpty&&realNodes.isNotEmpty)hubLeaf=(_B.stkNs[_B.regCode]!=null&&realNodes.contains(_B.stkNs[_B.regCode]))?_B.stkNs[_B.regCode]!:realNodes.first;}}"""
NEW_PM = r"""EndpointMeta _pm(String n){final c=_ec[n];final(rc,rl)=_B.resolveReg(n,c?.raw??'',c?.ip??'');if(c!=null)return(ip:c.ip,s24:c.s24,s16:c.s16,rc:rc,rl:rl,raw:c.raw);return(ip:'',s24:null,s16:null,rc:rc,rl:rl,raw:'');}Future<EndpointMeta> _rm(String n,[bool force=false])async{await _B.ensureGeoIpLoaded();final pv=_ec[n],now=DateTime.now();if(!force&&pv!=null&&pv.ip.isNotEmpty&&_B.lookupIpSync(pv.ip).isNotEmpty){final(rc,rl)=_B.resolveReg(n,pv.raw,pv.ip);return _ec[n]=(ip:pv.ip,s24:pv.s24,s16:pv.s16,rc:rc,rl:rl,raw:pv.raw);}if(!force&&_er[n]!=null&&now.isBefore(_er[n]!))return _pm(n);var srv=await _B.queryServer(ref,n);if(srv.isEmpty)srv=pv?.raw??'';"""
NEW_BG = r"""Future<void> _bg(List<String> prioNs,List<String> allNs)async{if(_br)return;_br=true;try{await _B.ensureGeoIpLoaded();final now=DateTime.now();bool need(String n)=>(_ec[n]?.ip.isEmpty??true)&&(_er[n]==null||!now.isBefore(_er[n]!));final p=prioNs.where(need).toList(),q=<String>[...p,...allNs.where((n)=>!p.contains(n)&&need(n))];for(var i=0;i<q.length;i+=16){await _resB(q.skip(i).take(16).toList());}final unknownIps=<String>{for(final n in allNs)if((_ec[n]?.ip.isNotEmpty??false)&&_B.lookupIpSync(_ec[n]!.ip).isEmpty)_ec[n]!.ip};if(unknownIps.isNotEmpty){await _B.scanGeoDatBatch(unknownIps);final still=<String>[for(final ip in unknownIps)if(_B.lookupIpSync(ip).isEmpty)ip];if(still.isNotEmpty)await _B.fetchOnlineGeoBatch(still);for(final n in allNs){final c=_ec[n];if(c!=null&&c.ip.isNotEmpty&&c.raw.isNotEmpty){final cc=_B.lookupIpSync(c.ip);if(cc.length==2&&cc!='CN')_B.ipGeoCache['srv:${c.raw.toLowerCase()}']=cc;}}await _B.savePrefs();}if(q.isNotEmpty||unknownIps.isNotEmpty)await _rcGs();if(_B.isRunning(ref)){final transitNs=<String>[for(final n in allNs)if(!_B.nodeExitCache.containsKey(n)&&(() {final ip=_ec[n]?.ip??'',cc=ip.isNotEmpty?_B.lookupIpSync(ip):'';return cc.isEmpty||cc=='CN'||cc=='ANYCAST'||_pm(n).rc=='OTHER';}()))n];if(transitNs.isNotEmpty&&await _B.probeTransitNodesExitIp(ref,transitNs))await _rcGs();}}catch(_){}finally{_br=false;}}"""
def apply(od: pathlib.Path) -> None:
    fb_p, sg_p, sgc_p = od / 'flclash_bridge.dart', od / 'smart_guardian.dart', od / 'smart_guardian_core.dart'
  fb, sg, sgc = fb_p.read_text('utf-8'), sg_p.read_text('utf-8'), sgc_p.read_text('utf-8')
    fb = fb.replace("import 'dart:convert';", "import 'dart:convert';import 'dart:typed_data';", 1)
    fb, c0 = re.subn(r"(class\s+FlClashBridge\s*\{)", lambda m: GEO_CLS + "\n" + m.group(1) + "\n" + BRG_P1 + BRG_P2, fb, count=1)
    fb = fb.replace("'philippines', '菲律宾'", "'philippines', 'philippine', '菲律宾', '菲律賓', '馬尼拉', '宿霧', '克拉克', '马卡蒂', '帕赛', '达沃', '港菲', '新菲', '台菲', 'clark', 'makati', 'pasay', 'davao', 'flb'").replace("'马来西亚', '马来'", "'马来西亚', '馬來西亞', '吉隆坡', '檳城', '港马', '新马', '马来'")
    fb, ci = re.subn(r"iKws\s*=\s*<String>\[[^\]]+\];", "iKws = <String>['剩余流量','距离下次','套餐到期','过期时间','有效期','流量重置','官网地址','最新网址','traffic:','expire:'];", fb, count=1)
    fb, cp = re.subn(r"static void _parseTxt\(String raw,.*?cfgRegs\.\.clear\(\)\.\.addAll\(<String>\[for\(final p in out\)detReg\(p\.\$1,p\.\$2\)\.\$1\]\);\}\}catch\(_\)\{\}\}", lambda m: PARSE_DISK, fb, count=1, flags=re.S)
    fb, cd = re.subn(r"static \(String,String\) detReg\(String n,String srv\)\{.*?return'🌐 \$rc';\}", lambda m: DET_NAME, fb, count=1, flags=re.S)
    assert (c0, ci, cp, cd) == (1, 1, 1, 1), (c0, ci, cp, cd)
    for a, b in [
        ("for (final lan in const <String>['127.0.0.0/8'", "ad('DOMAIN,checkip.amazonaws.com,$probeGroup');ad('DOMAIN,ipv4.icanhazip.com,$probeGroup');for (final lan in const <String>['127.0.0.0/8'"),
        ("(byR[detReg(nm, sv).$1] ??= <String>[]).add(nm);", "(byR[resolveReg(nm, sv, '').$1] ??= <String>[]).add(nm);"),
        ("if(byR.isNotEmpty){cfgRegs..clear()..addAll(byR.keys);}", "if(byR.isNotEmpty){cfgRegs.addAll(byR.keys);}"),
        ("cfg['proxy-groups'] = <Map<String, dynamic>>[buildHubGroup(),", "Map<String, dynamic> buildProbeGroup(){final m=<String,dynamic>{'name':probeGroup,'type':'select','proxies':uIn.isNotEmpty?dedup(<String>[...uIn,'DIRECT']):<String>['DIRECT']};if(provKeys.isNotEmpty){m['use']=provKeys;m['exclude-filter']=infoExcludeRx;}return m;}cfg['proxy-groups'] = <Map<String, dynamic>>[buildHubGroup(),buildProbeGroup(),"),
        ("if (extraCust.isNotEmpty) {vendors = <VendorSpec>[vendors.first,...extraCust,...vendors.skip(1)];}}return;}}", "if (extraCust.isNotEmpty) {vendors = <VendorSpec>[vendors.first,...extraCust,...vendors.skip(1)];}}if(m['ipGeoCache'] is Map){for(final ge in (m['ipGeoCache'] as Map).entries){if('${ge.key}'.isNotEmpty&&'${ge.value}'.isNotEmpty)ipGeoCache['${ge.key}']='${ge.value}';}}if(m['nodeExitCache'] is Map){for(final ne in (m['nodeExitCache'] as Map).entries){if('${ne.key}'.isNotEmpty&&'${ne.value}'.isNotEmpty)nodeExitCache['${ne.key}']='${ne.value}';}}return;}}"),
        ("finally {if (!c.isCompleted) c.complete();}", "finally {await ensureGeoIpLoaded();if (!c.isCompleted) c.complete();}"),
        ("'vendors': vJson,}),);", "'vendors': vJson,'ipGeoCache':<String,String>{for(final e in ipGeoCache.entries.take(1500))e.key:e.value},'nodeExitCache':<String,String>{for(final e in nodeExitCache.entries.take(600))e.key:e.value},}),);"),
    ]:
        assert a in fb, a[:60]
        fb = fb.replace(a, b, 1)
    sg, s1 = re.subn(r"Future<void> _rcGs\(\)async\{await _B\.syncProfileNodesFromDisk\(ref\);.*?realNodes\.first;\}", lambda m: NEW_RC, sg, count=1, flags=re.S)
    assert s1 == 1 and "_B.cfgRegs..clear()..addAll(by.keys);" in sg
    sg = sg.replace("_B.cfgRegs..clear()..addAll(by.keys);", "_B.cfgRegs.addAll(by.keys);", 1)
    sgc, g1 = re.subn(r"EndpointMeta _pm\(String n\)\{final c=_ec\[n\];.*?final\(rc,rl\)=_B\.detReg\(n,srv\);", lambda m: NEW_PM, sgc, count=1, flags=re.S)
    sgc, g2 = re.subn(r"Future<void> _bg\(List<String> prioNs,List<String> allNs\)async\{.*?finally\{_br=false;\}\}", lambda m: NEW_BG, sgc, count=1, flags=re.S)
    assert (g1, g2) == (1, 1), (g1, g2)
    for a, b in [
        ("if(srv.isEmpty){_er[n]=now.add(const Duration(seconds:4));return _ec[n]=(ip:'',s24:null,s16:null,rc:rc,rl:rl,raw:'');}",
         "if(srv.isEmpty){_er[n]=now.add(const Duration(seconds:4));final(rc0,rl0)=_B.resolveReg(n,'','');return _ec[n]=(ip:'',s24:null,s16:null,rc:rc0,rl:rl0,raw:'');}"),
        ("if(a==null)_er[n]=now.add(const Duration(seconds:8));\nreturn _ec[n]=(ip:a?.address??'',s24:s24,s16:s16,rc:rc,rl:rl,raw:srv,);",
         "if(a==null)_er[n]=now.add(const Duration(seconds:8));final ipStr=a?.address??'';if(ipStr.isNotEmpty){final cc=_B.lookupIpSync(ipStr);if(cc.length==2&&cc!='CN'&&srv.trim().isNotEmpty)_B.ipGeoCache['srv:${srv.trim().toLowerCase()}']=cc;}final(rc,rl)=_B.resolveReg(n,srv,ipStr);return _ec[n]=(ip:ipStr,s24:s24,s16:s16,rc:rc,rl:rl,raw:srv,);"),
        ("ch!=_B.hubGroup", "ch!=_B.hubGroup&&ch!=_B.probeGroup"),
    ]:
        assert a in sgc, a[:60]
        sgc = sgc.replace(a, b, 1)
    fb_p.write_text(fb, 'utf-8'); sg_p.write_text(sg, 'utf-8'); sgc_p.write_text(sgc, 'utf-8')
