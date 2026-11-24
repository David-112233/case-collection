"""Build eval_rules.json for case-228 from the table below.

    python cases/case-228-T3/rules_drafts/manual_v1/build_rules.py

Edit the tables here and re-run; do not hand-edit eval_rules.json.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
INPUT = CASE / "input.json"

FR, LC, MC = "functional_requirements", "layout_constraints", "motion_constraints"
DEFAULT = "默认外观（页面加载完成、未点击）的稳定状态。"
GLOW = "点击中央圆形按钮一次、进入发光模式后的稳定状态（等待任何切换过渡结束）。"
FRAME = ("机身自身方向：有接口的一端为底端，另一端为顶端；面向正面、顶端朝上时的左右即机身的左右。"
         "按 input，机身左侧长边是画面中能看到厚度的那条长边。")

# (req_id, dimension, type, description, target, [evidence...])
# evidence: (quote, field, check, kind, decider, viewports, extra)
REQS = [
    ("SR-01", "static", "region", "页面整体：组成、背景色、无滚动条", "page", [
        ("页面只展示一台立体的音乐播放器模型及其投影", FR,
         "默认外观下，页面可见内容只有一台立体的音乐播放器及其投影；没有标题、说明文字、按钮、导航或其他装饰区块，也没有第二台播放器。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("页面背景为纯色珊瑚红", LC,
         "播放器和投影以外的页面背景为单一纯色的珊瑚红（偏橙的粉红色系）；采样页面四角与四边中点颜色一致。渐变、图案、纹理不满足；红、橙、粉之外明显不同的色相（如灰、蓝、黄）不满足。不指定色号。",
         "computed_color", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("页面不出现滚动条", LC,
         "两个视口下页面都不出现滚动条且不能滚动：window.innerWidth − documentElement.clientWidth 与 window.innerHeight − documentElement.clientHeight 均为 0，滚动尝试后 scrollX、scrollY 仍为 0。",
         "dom_interaction", "program", ["desktop", "wide"], {"state": DEFAULT}),
    ]),
    ("SR-02", "static", "relation", "播放器在视口中的位置与缩放", "player↔viewport", [
        ("播放器位于视口正中", LC,
         "播放器（机身可见像素的外接框，不含投影）中心与视口中心大致重合，水平、竖直方向都只有小幅偏差；明显偏向某一侧或贴边的不满足。两个视口分别测量，任一视口明显偏离即不满足。",
         "geometry", "program+judge", ["desktop", "wide"], {"state": DEFAULT}),
        ("整体尺寸随视口宽度等比缩放", LC,
         "比较 1280 与 1920 两个宽度下机身外接框宽度与视口宽度之比：两者大致相等（播放器随视口宽度同比例变大）；宽视口下播放器像素尺寸不变或明显不成比例的不满足。程序给比值，边界交 Judge。",
         "geometry", "program+judge", ["desktop", "wide"], {"state": DEFAULT}),
    ]),
    ("SR-03", "static", "region", "播放器的摆放、视角与朝向", "player.view", [
        ("机身平放，从斜上方俯视", LC,
         "机身像平放在桌面上，从斜上方俯视：能看到一个大的正面（在画面中呈倾斜的四边形），同时能看到机身侧边的厚度。纯正面平视图（看不到厚度）、机身竖立或侧立的不满足。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("带透视", LC,
         "机身呈现透视效果：离观者近的部分略大、远的部分略小，例如同一面上本应平行的长边在画面中不完全平行、底端一侧略宽。完全平行投影（等轴测、远近同大）的不满足。透视程度不设数值，可辨即可。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("机身正面（有屏幕的一面）向上", LC,
         "屏幕所在的面是机身朝上、面向观者的大面；屏幕不在侧边、端面或背面。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("机身长轴从左上斜向右下", LC,
         "机身长轴在画面中斜向放置，一端在左上、另一端在右下；长轴水平、竖直或从右上斜向左下的不满足。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("底端在右下方", LC,
         "有充电口和耳机孔的底端位于长轴的右下端，顶端在左上端；两端颠倒的不满足。长轴方向错误由上一条负责，本条只看底端是否为画面中偏右下的那一端。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("SR-04", "static", "element", "机身形状与配色", "body", [
        ("一个扁平的长方体机身", FR,
         "播放器机身是一个扁平的长方体：厚度明显小于长和宽，正面为长方形轮廓；圆柱、明显不规则或没有厚度的平面图形不满足。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("四角为圆角", FR,
         "机身正面轮廓的四个角都是圆角，不是尖角；能看到的侧边在转角处随之弯过。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("侧边有可见的厚度", FR,
         "画面中能看到机身侧边形成的一条有宽度的面（厚度），与正面明暗或颜色可区分；只有正面一个平面、看不出厚度的不满足。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("机身为明黄色", LC,
         "机身（正面与可见侧边、端面）整体为明亮的黄色；暗黄、土黄、橙色、白色或其他色系的不满足。不指定色号。",
         "computed_color", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("正面最亮，底端端面稍暗，左侧长边更暗", LC,
         "机身三个可见面的明暗依次为：正面最亮，底端端面稍暗，左侧长边最暗。" + FRAME + "三个面同亮、顺序颠倒、或看不到其中某个面的不满足。程序采样三面亮度，边界交 Judge。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("圆角处的颜色在相邻两面之间逐级过渡", LC,
         "可见的圆角侧面（如左侧长边与底端端面之间的转角）颜色介于相邻两个面之间，呈逐级或平滑的过渡；转角处与某一面同色后突然跳变到另一面颜色、或出现与两面都不相近的颜色的不满足。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("SR-05", "static", "element", "屏幕", "screen", [
        ("黑色圆角矩形屏幕", FR,
         "机身正面上有一块屏幕，形状为圆角矩形（在倾斜视角下为相应的圆角四边形）。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("屏幕为纯黑色", LC,
         "屏幕为均匀的纯黑色，没有图案、文字、渐变或明显偏灰、偏蓝。",
         "computed_color", "program+judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("SR-06", "static", "element", "环形按钮、中央按钮与四个图标", "wheel", [
        ("环形按钮", FR,
         "机身正面上有一个环形按钮：圆环形的面，与屏幕分开。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("滚轮为白色", LC,
         "环形按钮的环面为白色。",
         "computed_color", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("环形中央有一个圆形按钮", FR,
         "环形按钮中央有一个圆形按钮，与圆环同心，和环面颜色可区分。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("上方为文字“MENU”", FR,
         "环面上方有文字“MENU”（大写，文字可为 DOM 文本、SVG 或图形，按可见字形判）。“上方”按机身自身方向，即靠顶端（屏幕）一侧。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": DEFAULT, "member": "icon.menu"}),
        ("右侧为快进图标", FR,
         "环面右侧有一个快进图标（向右的双三角，可带竖线）。“右侧”按机身自身方向：面向正面、顶端朝上时的右侧。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT, "member": "icon.forward"}),
        ("左侧为快退图标", FR,
         "环面左侧有一个快退图标（向左的双三角，可带竖线）。“左侧”按机身自身方向。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT, "member": "icon.backward"}),
        ("下方为播放/暂停图标", FR,
         "环面下方（靠底端一侧）有一个播放/暂停图标（三角形与两条竖线的组合）。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT, "member": "icon.playpause"}),
        ("四个图标为半透明黑色", LC,
         "四个图标都为半透明的黑色：呈黑色或深灰，略透出下面的白色环面；彩色或白色的不满足。程序读颜色与透明度，边界交 Judge。",
         "computed_color", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("环面上有四个黑色小图标", FR,
         "四个图标都是小图标，完整落在环面上，不压到中央按钮，也不超出圆环外缘。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("SR-07", "static", "relation", "屏幕与环形按钮在正面上的位置关系", "screen↔wheel↔front", [
        ("屏幕和环形按钮都左右居中", LC,
         "屏幕在机身正面上左右居中：屏幕两侧到机身左右长边的距离大致相等（按机身自身方向）。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": DEFAULT, "member": "screen"}),
        ("屏幕和环形按钮都左右居中", LC,
         "环形按钮在机身正面上左右居中：圆环两侧到机身左右长边的距离大致相等（按机身自身方向）。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": DEFAULT, "member": "wheel"}),
        ("环形直径略小于屏幕宽度", LC,
         "环形按钮的外径略小于屏幕的宽度（沿机身左右方向比较）：比屏幕窄，但只窄一点；大于等于屏幕宽度、或不到屏幕宽度一半的不满足。",
         "geometry", "program+judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("SR-08", "static", "element", "底端端面的充电口与耳机孔", "ports", [
        ("黑色宽充电口", FR,
         "机身底端端面上有一个黑色、横向较宽（宽明显大于高）的充电口。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT, "member": "port.charge"}),
        ("圆形耳机孔", FR,
         "机身底端端面上有一个圆形耳机孔。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT, "member": "port.jack"}),
        ("底端端面上并排的黑色宽充电口和圆形耳机孔", FR,
         "充电口和耳机孔在底端端面上沿端面长度方向并排，彼此分开、不重叠。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("充电口和耳机孔在底端端面中部", LC,
         "充电口和耳机孔作为一组位于底端端面的中部（沿端面长度方向大致居中），不偏到某一角。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("SR-09", "static", "element", "投影", "shadow", [
        ("机身左侧的一块投影", FR,
         "有一块投影从机身左侧长边一侧露出（在画面中位于机身的左下方一侧），像机身落在背景上的影子；没有投影、或投影只在其他方向露出的不满足。" + FRAME,
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
        ("投影为半透明黑色", LC,
         "投影为半透明的黑色：比背景暗，仍能透出背景的珊瑚红色调；不透明的纯黑、彩色或比背景亮的不满足。",
         "computed_color", "program+judge", ["desktop"], {"state": DEFAULT}),
        ("投影为半透明黑色的圆角矩形", LC,
         "投影形状为圆角矩形（在倾斜视角下为相应的圆角四边形），边缘清楚可辨；圆形、椭圆或无形的模糊光晕不满足。",
         "screenshot_visual", "judge", ["desktop"], {"state": DEFAULT}),
    ]),
    ("DR-01", "dynamic", "interaction", "点击切换发光模式、保持与恢复", "toggle", [
        ("点击中央圆形按钮可以切换显示模式", FR,
         "在默认外观下点击中央圆形按钮一次：页面切换到另一种显示模式（发光模式），整体外观明显改变。点击后没有任何变化的不满足。",
         "dom_interaction", "program+judge", ["desktop"], {"state": "默认外观 → 点击中央圆形按钮一次"}),
        ("点击滚轮后页面进入发光模式并保持该状态", MC,
         "进入发光模式后不再操作，等待 3 秒：页面仍保持发光模式，不自动回到默认外观。",
         "dom_interaction", "program+judge", ["desktop"], {"state": GLOW}),
        ("再次点击滚轮回到默认外观", MC,
         "在发光模式下再次点击中央圆形按钮：页面回到默认外观，与点击前的截图一致（背景、机身配色、投影等恢复）。按字面判：第一次点击本身没有切换时页面仍是默认外观，本条 PASS，不与 DR-01.C1 重复扣分。",
         "dom_interaction", "program+judge", ["desktop"], {"state": "发光模式 → 再次点击中央圆形按钮"}),
    ]),
    ("DR-02", "dynamic", "state_appearance", "发光模式的外观", "glow", [
        ("页面背景变为黑色", MC,
         "发光模式下页面背景变为黑色（采样页面四角与四边中点）。",
         "computed_color", "program", ["desktop"], {"state": GLOW}),
        ("机身正面变为浅灰蓝色", MC,
         "发光模式下机身正面变为浅灰蓝色：浅、略带蓝的灰色；仍为黄色、纯白、深蓝或其他色系的不满足。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": GLOW}),
        ("侧边和端面变为白色", MC,
         "发光模式下机身可见的侧边和端面变为白色（或接近白色）。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": GLOW}),
        ("机身轮廓带蓝色外发光", MC,
         "发光模式下机身外轮廓周围有一圈蓝色的外发光，从轮廓向外渐弱；没有发光或发光不是蓝色的不满足。",
         "screenshot_visual", "judge", ["desktop"], {"state": GLOW}),
        ("充电接口和耳机孔变为蓝色", MC,
         "发光模式下充电口和耳机孔都呈蓝色。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": GLOW}),
        ("中央圆形按钮变为浅蓝色", MC,
         "发光模式下中央圆形按钮变为浅蓝色。",
         "screenshot_visual", "program+judge", ["desktop"], {"state": GLOW}),
    ]),
    ("DR-03", "dynamic", "absence", "两种模式下画面静止", "page.motion", [
        ("两种模式下画面都是静止的，没有持续或循环播放的动画", MC,
         "默认外观与发光模式各自稳定后，不操作页面，间隔约 1 秒连续截图 3 张：画面完全相同，document.getAnimations() 中没有无限循环的动画。点击切换时的一次性过渡不计。任一模式出现持续或循环动画即不满足。",
         "dom_interaction", "program", ["desktop"], {"state": "默认外观稳定后；发光模式稳定后"}),
    ]),
]

DEPENDENCIES = [
    ("SR-04.C1", ["SR-03.*", "SR-04.C2", "SR-04.C3", "SR-04.C5", "SR-04.C6", "SR-07.*", "SR-09.C1"], "确认画面中没有可辨认的机身时，视角、朝向、形状与相对位置条件无法成立。"),
    ("SR-05.C1", ["SR-05.C2", "SR-03.C3", "SR-07.C1", "SR-07.C3"], "确认没有屏幕时，只阻断涉及屏幕的条件。"),
    ("SR-06.C1", ["SR-06.C2", "SR-06.C4", "SR-06.C5", "SR-06.C6", "SR-06.C7", "SR-06.C9", "SR-07.C2", "SR-07.C3"], "确认没有环形按钮时，环面上的图标和环的位置条件无法成立。"),
    ("SR-06.C3", ["DR-01.*", "DR-02.*", "DR-03.C1"], "确认没有中央圆形按钮时，无从按 input 触发切换；DR-03 只阻断发光模式那一半采样，默认外观仍照常检查。"),
    ("SR-08.C1", ["SR-08.C3", "SR-08.C4", "DR-02.C5"], "确认没有充电口时，只阻断涉及充电口的条件。"),
    ("SR-08.C2", ["SR-08.C3", "SR-08.C4", "DR-02.C5"], "确认没有耳机孔时，只阻断涉及耳机孔的条件。"),
    ("SR-09.C1", ["SR-09.C2", "SR-09.C3"], "确认没有投影时，投影的颜色与形状无法判定。"),
    ("DR-01.C1", ["DR-01.C2", "DR-02.*"], "确认点击中央圆形按钮不能进入发光模式时，发光模式的保持与外观无法观察。DR-01.C3 按字面判，不在此列。"),
]


def main() -> None:
    inp = json.loads(INPUT.read_text(encoding="utf-8"))
    static, dynamic, owner = [], [], []
    n = {"static": 0, "dynamic": 0}
    kinds = {}
    for rid, dim, typ, desc, target, evs in REQS:
        req = {"id": rid, "dimension": dim, "type": typ, "description": desc, "target": target,
               "source_fields": sorted({e[1] for e in evs}), "mandatory_evidence": []}
        for i, (quote, field, check, kind, decider, vps, extra) in enumerate(evs, 1):
            text = inp[field]
            assert "".join(quote.split()) in "".join(text.split()), (rid, i, quote)
            ev = {"id": f"C{i}", "mandatory": True, "source": "input", "source_fields": [field], "source_quote": quote,
                  "target": extra.get("member", target), "applies_when": extra["state"], "check": check,
                  "kind": kind, "decider": decider, "viewport": vps[0] if len(vps) == 1 else "both",
                  "required_objects": [extra.get("member", target)], "sample_viewports": vps}
            if len(vps) > 1:
                ev["viewport_scoring"] = "one_evidence_multiple_observations"
            if "member" in extra:
                ev["member"] = extra["member"]
            req["mandatory_evidence"].append(ev)
            owner.append({"evidence_id": f"{rid}.C{i}", "target": ev["target"], "viewport": ev["viewport"]})
            n[dim] += 1
            kinds[decider] = kinds.get(decider, 0) + 1
        (static if dim == "static" else dynamic).append(req)

    rules = {
        "schema_version": "semantic-eval-rules/3.0",
        "case_id": "case-228",
        "tier": "T3",
        "rule_status": "DRAFT_PENDING_USER_REVIEW",
        "revision": "manual_v1",
        "input_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "input_source": {"path": "input.json", "note": "用户 2026-11-24 审核修改后的版本（提交 945c78f）。"},
        "output_contract_ref": "scripts/eval_rules_generation/preparation/output_contract_v2.json",
        "scoring_policy_ref": "scripts/eval_rules_generation/preparation/evaluation_policy_v2.json#/scoring_policy",
        "source_policy": {
            "requirements": "input.json only; no DEC-037 common-sense condition added; business_background supplies context only.",
            "gt": "ground_truth.html = source.html minus CodePen boilerplate, the four infinite keyframe animations (fixed at the from frame) and the 0.6s transitions. GT only for binding/self-test, never a requirement source. Source details not in input (hold switch, screen/wheel position along the long axis, default centre-button colour, glow-mode shadow and halo, the glow-mode screen/wheel depth artefact) are not tested.",
            "model_outputs": "No model output exists or was read when drafting these rules.",
        },
        "render_baseline": {
            "status": "NOT_FROZEN",
            "states": ["default", "glow"],
            "viewports": {"desktop": [1280, 800], "wide": [1920, 1080]},
            "note": "主采证视口 1280×800；1920×1080 只用于“随视口宽度等比缩放”“视口正中”“无滚动条”。播放器尺寸按视口宽度缩放，手机宽度下机身只有约 40px，细节不可判，所以不设手机视口；待用户确认。",
            "resources": "JS 与外部资源按输出契约 v2 允许；评测网络导致脚本或图标加载失败记 UNRESOLVED，不判模型 FAIL。",
        },
        "frame_policy": {
            "body_frame": FRAME,
            "single_owner": "长轴方向只由 SR-03.C4 负责，底端位置只由 SR-03.C5 负责；图标、居中、投影等方位按模型实际呈现的机身自身方向换算，不因朝向错误重复扣分。",
        },
        "member_policy": {
            "icons": "MENU、快进、快退、播放/暂停四个图标为并列成员，存在与方位各一条；颜色、大小是 input 一句话统一规定的性质，各一条。",
            "centering": "“屏幕和环形按钮都左右居中”分屏幕、环形两个成员各一条。",
            "ports": "充电口、耳机孔各一条存在条件；并排、在中部是二者整组性质，各一条。",
        },
        "granularity_policy": {
            "same_fact": "同一事实只放一条：屏幕“黑色”（FR）与“纯黑色”（LC）合为 SR-05.C2；图标“黑色”（FR）与“半透明黑色”（LC）合为 SR-06.C8；投影“半透明黑色”只在 SR-09.C2。",
            "split": "一句话里的独立事实分开：机身扁平长方体、圆角、厚度各一条；视角、透视、正面向上、长轴方向、底端位置各一条；投影颜色与形状各一条。",
            "trigger_wording": "input 中触发写作“点击中央圆形按钮”（BB、FR）与“点击滚轮”（MC）；中央按钮位于滚轮中央，按中央按钮驱动可同时满足两种说法，见 review.md 待确认 1。",
            "scoring_merge": "沿用 case-213/217/221/227 的并列失败合并约定：同一检查模板在并列成员上、由同一处实现造成的失败合为一组，只判一档；流水线逐条分留档。",
        },
        "measure_policy": {
            "program_first": "背景与面颜色采样、外接框几何、滚动、动画列表由程序判；程序不确定时交 Judge，不判 FAIL。",
            "judge": "视角、透视、形状、厚度、圆角过渡、方位、发光是定性视觉条件，交 Judge；条件正文写出最低判定标准。",
            "qualitative_words": "“大致”“略小于”“明显”不设数值阈值；程序只给测量值，边界由 Judge 判断。颜色只按色名判色系，不给色号。",
        },
        "quality_gate": [
            {"id": "G1", "description": "HTML forms a valid evaluable DOM; parser/environment failure alone is not model fatal failure.", "source": "project_output_contract"},
            {"id": "G2", "description": "JS is allowed by the shared v2 policy; no blanket script/event-attribute violation.", "source": "project_output_contract"},
            {"id": "G3", "description": "External fonts, font stylesheets, images and ordinary links are allowed; resource availability is checked separately.", "source": "project_output_contract"},
            {"id": "G4", "description": "One complete HTML; page CSS embedded in head/style or style attributes; required JS embedded.", "source": "project_output_contract"},
            {"id": "G5", "description": "input.forbidden is empty; no case-specific prohibition is invented.", "source": "input.forbidden"},
        ],
        "static_requirements": static,
        "dynamic_requirements": dynamic,
        "dimension_policy": {"D1": 0.5, "D2": 0.5, "reason": "input 含 motion_constraints（点击切换发光模式），按 DEC-038 两维各占 50%。"},
        "dependency_policy": {
            "version": "model-dependency-fail/1.0",
            "rule": "已确认模型缺失前置对象或行为、实际阻断下游条件时，上下游都判 FAIL、各自判档（DEC-029）；定位、网络或采证失败记 UNRESOLVED；不受阻的成员与条件继续检查。",
            "prerequisites": [{"upstream": u, "downstream": d, "when": w} for u, d, w in DEPENDENCIES],
        },
        "attribution_policy": {
            "direct_duplicates": "同一事实只扣一次：FR 与 LC 重复描述的颜色合为一条；门禁与 Evidence 不重复。",
            "shared_quotes": {
                "SR-07.C1 / SR-07.C2": "“屏幕和环形按钮都左右居中”分属屏幕、环形两个成员。",
                "SR-09.C2 / SR-09.C3": "“半透明黑色的圆角矩形”拆为颜色与形状两个事实。",
                "SR-08.C3 / SR-08.C1-C2": "存在由 C1、C2 判；C3 只判二者并排。",
                "SR-06.C9 / SR-06.C8": "“黑色小图标”中的颜色归 C8，C9 只判大小与落在环面上。",
                "SR-04.C* / DR-02.C2-C3": "默认黄色在 D1；发光模式的正面、侧边颜色在 D2，是不同状态。",
                "DR-01.C1 / DR-02.*": "C1 只判点击后发生了模式切换；各项发光外观分别由 DR-02 判。",
            },
            "owner_index": owner,
        },
        "scoring": {"note": "Routing IDs only; formula and deductions come exclusively from the shared scoring policy.",
                    "gates": {"fatal": {"gate_ids": ["G1"]}, "ordinary": {"gate_ids": ["G2", "G3", "G4", "G5"]}}},
        "multi_viewport_verdict_policy": {"coverage": ["desktop", "wide"], "PASS": "适用视口均通过。", "FAIL": "任一适用视口确认失败即 FAIL，只判一档、扣一次。", "UNRESOLVED": "无确认 FAIL 且有视口未判定。"},
        "draft_review": {"reviewer": "Claude implementer self-review (duet)", "independent_review": False,
                         "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                         "checked": ["source quotes are literal substrings of input", "member split and same-fact ownership", "GT satisfies every condition by visual comparison with the 2026-11-24 renders (no program self-check script run)"],
                         "not_performed": ["target registry / binding", "program GT self-check", "Judge run", "release freeze", "API calls", "model scoring", "user acceptance"]},
        "evidence_count": {"static": n["static"], "dynamic": n["dynamic"], "total": n["static"] + n["dynamic"], "by_decider": kinds},
    }
    (HERE / "eval_rules.json").write_text(json.dumps(rules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(rules["evidence_count"], ensure_ascii=False))


if __name__ == "__main__":
    main()
