"""슬라이드 애니메이션 (OOXML <p:timing>) 생성.

python-pptx 에는 애니메이션 API 가 없어서 XML 을 직접 쓴다.
steps 의 각 항목 = 클릭 한 번(또는 자동)에 함께 나타나는 도형 id 목록.

    set_timing(slide, steps=[[id1], [id2, id3]], video=(movie_id, dur_ms))
"""
from lxml import etree
from pptx.oxml.ns import qn

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"


class _Ids:
    def __init__(self):
        self.n = 0

    def __call__(self):
        self.n += 1
        return self.n


def _fade_in(ids, spid, node_type):
    """나타나기 + 페이드 (PowerPoint 기본 '페이드' 나타내기 효과, presetID=10)."""
    return f"""
<p:par><p:cTn id="{ids()}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{node_type}">
  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
  <p:childTnLst>
    <p:set><p:cBhvr><p:cTn id="{ids()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
    </p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
    <p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{ids()}" dur="500"/>
      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
  </p:childTnLst></p:cTn></p:par>"""


def _play_video(ids, spid, dur_ms):
    """슬라이드가 열리면 영상 자동 재생 (presetClass=mediacall)."""
    return f"""
<p:par><p:cTn id="{ids()}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect">
  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
  <p:childTnLst>
    <p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{ids()}" dur="{dur_ms}" fill="hold"/>
      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>
  </p:childTnLst></p:cTn></p:par>"""


def _group(ids, inner, auto, main_seq_id):
    """클릭 한 번(또는 자동 시작) 단위."""
    start = (f'<p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="{main_seq_id}"/></p:cond>'
             if auto else '<p:cond delay="indefinite"/>')
    return f"""
<p:par><p:cTn id="{ids()}" fill="hold"><p:stCondLst>{start}</p:stCondLst><p:childTnLst>
  <p:par><p:cTn id="{ids()}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
    {inner}
  </p:childTnLst></p:cTn></p:par>
</p:childTnLst></p:cTn></p:par>"""


def set_timing(slide, steps=(), video=None):
    """steps: [[spid, ...], ...] 클릭마다 페이드인. video: (spid, 길이 ms) 슬라이드 시작 시 자동 재생."""
    steps = [s for s in steps if s]
    if not steps and not video:
        return
    ids = _Ids()
    root_id = ids()
    seq_id = ids()
    groups = []
    if video:
        groups.append(_group(ids, _play_video(ids, video[0], video[1]), auto=True, main_seq_id=seq_id))
    for step in steps:
        inner = "".join(_fade_in(ids, spid, "clickEffect" if k == 0 else "withEffect")
                        for k, spid in enumerate(step))
        groups.append(_group(ids, inner, auto=False, main_seq_id=seq_id))
    media = ""
    if video:
        media = f"""
<p:video><p:cMediaNode vol="80000"><p:cTn id="{ids()}" fill="hold" display="0">
  <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>
  <p:tgtEl><p:spTgt spid="{video[0]}"/></p:tgtEl></p:cMediaNode></p:video>"""
    xml = f"""
<p:timing xmlns:p="{P_NS}"><p:tnLst><p:par>
<p:cTn id="{root_id}" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
  <p:seq concurrent="1" nextAc="seek"><p:cTn id="{seq_id}" dur="indefinite" nodeType="mainSeq"><p:childTnLst>
    {"".join(groups)}
  </p:childTnLst></p:cTn>
  <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
  <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
  </p:seq>
  {media}
</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>"""
    sld = slide._element
    old = sld.find(qn("p:timing"))
    if old is not None:
        sld.remove(old)
    new = etree.fromstring(xml)
    # <p:timing> 은 <p:clrMapOvr> 다음, <p:extLst> 앞에 와야 한다
    ext = sld.find(qn("p:extLst"))
    if ext is not None:
        ext.addprevious(new)
    else:
        sld.append(new)
