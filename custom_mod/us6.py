import base64, json, zlib # end
import us1, us2, us3, us4, us5 # end
def _rs(s, a, b, v): # end
    i = s .index(a) # end
    j = s .index(b, i) # end
    return s[:i] + v + s[j:] # end
def apply_v118(od): # end
    raw = us1 .P1 + us2 .P2 .replace('4l/9a1Dw1o', '4l/8a1Dw1o') + us3 .P3 + us4 .P4 .replace('TtNtNtNSkno', 'TtNtNSkno') + us5 .P5 # end
    d = json .loads(zlib .decompress(base64 .b64decode(raw)) .decode('utf-8')) # end
    pfb = od / ('flclash_bridge' + '.' + 'dart') # end
    fb = pfb .read_text('utf-8') # end
    if 'SubRichItem' not in fb: # end
        fb = fb .replace(d['fb_imp_old'], d['fb_imp_new'], 1) # end
        fb = fb .replace('typedef BridgeProfile =', d['fb_types'] + 'typedef BridgeProfile =', 1) # end
        fb = fb .replace('class FlClashBridge {', 'class FlClashBridge {\n' + d['fb_body'], 1) # end
        fb = fb .replace(d['a_snc'], d['a_snc_new'], 1) # end
        pfb .write_text(fb, 'utf-8') # end
    psg = od / ('smart_guardian' + '.' + 'dart') # end
    sg = psg .read_text('utf-8') # end
    if 'syncAndApplyNow' not in sg: # end
        sg = sg .replace('极简智控已就绪', '已就绪') # end
        sg = sg .replace('Future<void> togRun(', d['sg_extra'] + 'Future<void> togRun(', 1) # end
        psg .write_text(sg, 'utf-8') # end
    psw = od / ('simple_workbench' + '.' + 'dart') # end
    sw = psw .read_text('utf-8') # end
    if 'wb_sub_modal' not in sw: # end
        sw = sw .replace('final _pkSearchFocus=FocusNode();', d['sw_fields'], 1) # end
        sw = sw .replace(d['a_init'], d['a_init'] + d['sw_init'], 1) # end
        sw = _rs(sw, 'for(final c in<TextEditingController>[_cSearchCtrl', d['a_disp'], d['sw_dispose']) # end
        sw = _rs(sw, 'Future<void>_toggleRun(bool run)async{', 'bool _isDk(BuildContext c)=>', d['sw_helpers']) # end
        sw = _rs(sw, 'Widget _inp(', 'String _menuRegLbl(', d['sw_inp']) # end
        sw = _rs(sw, 'Widget _hdr(BuildContext c,GuardianState st,', '@override Widget build(BuildContext context){', d['sw_hdr']) # end
        sw = _rs(sw, "const titles=<String>['智控'", '}catch(err){', d['sw_build']) # end
        sw = sw .replace("Text('重新加载 BlueClash')", "Text('重新加载')") # end
        psw .write_text(sw, 'utf-8') # end
    pswc = od / ('simple_workbench_cards' + '.' + 'dart') # end
    swc = pswc .read_text('utf-8') # end
    if '_buildSubsPage(' not in swc: # end
        swc = _rs(swc, 'Widget _buildOverviewPage(', 'Widget _fallbackAndWhoamiCard(', d['swc_subs']) # end
        pswc .write_text(swc, 'utf-8') # end
