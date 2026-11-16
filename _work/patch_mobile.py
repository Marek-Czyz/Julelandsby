import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def sub(a, b, cnt=1):
    global s
    assert s.count(a) >= 1, a[:70]
    s = s.replace(a, b) if cnt == 0 else s.replace(a, b, cnt)

# ------------------------------------------------------------------ head: viewport, iOS meta, device detection
sub('<meta name="viewport" content="width=device-width, initial-scale=1">',
'''<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Julelandsby">
<meta name="theme-color" content="#1d232b">
<script>
// Device detection -> classes on <html>: is-mobile (phone / narrow screen), is-ios, landscape.
// Override with ?device=mobile or ?device=desktop
(function () {
  const forced = new URLSearchParams(location.search).get('device');
  const ua = navigator.userAgent;
  const ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const phoneUA = /iPhone|iPod|Android.+Mobile|Windows Phone/.test(ua);
  function apply() {
    const coarse = matchMedia('(pointer: coarse)').matches;
    const small = Math.min(innerWidth, innerHeight) < 600;
    const mobile = forced ? forced === 'mobile' : (phoneUA || (coarse && small) || innerWidth < 760);
    const c = document.documentElement.classList;
    c.toggle('is-mobile', mobile); c.toggle('is-ios', ios); c.toggle('landscape', innerWidth > innerHeight);
  }
  apply(); addEventListener('resize', apply); addEventListener('orientationchange', apply);
  window.__isMobile = () => document.documentElement.classList.contains('is-mobile');
})();
</script>''')

# ------------------------------------------------------------------ CSS for mobile
sub("  .lbl.big { font-size:13px; }\n</style>",
'''  .lbl.big { font-size:13px; }
  #mbar { display:none; }

  /* ---------------- phone layout: full-screen 3D + bottom sheet ---------------- */
  html.is-mobile, html.is-mobile body { position:fixed; inset:0; overscroll-behavior:none; -webkit-text-size-adjust:100%; }
  html.is-mobile body { font-size:15px; -webkit-tap-highlight-color:transparent; }
  html.is-mobile #app { display:block; height:100%; }
  html.is-mobile #view { position:fixed; left:0; right:0; top:0; bottom:calc(64px + env(safe-area-inset-bottom)); }
  html.is-mobile #side { position:fixed; left:0; right:0; bottom:0; width:auto; min-width:0; z-index:10;
    height:calc(64px + env(safe-area-inset-bottom)); max-height:none; padding:0 14px calc(14px + env(safe-area-inset-bottom));
    border-right:none; border-top:1px solid #3a4553; border-radius:14px 14px 0 0; box-shadow:0 -4px 18px rgba(0,0,0,.45);
    overflow:hidden; transition:height .25s ease; -webkit-overflow-scrolling:touch; }
  html.is-mobile #side.open { height:78%; overflow-y:auto; }
  html.is-mobile.landscape #side.open { height:88%; }
  html.is-mobile #mbar { display:flex; align-items:center; gap:10px; position:sticky; top:0; z-index:2; background:var(--panel);
    height:64px; margin:0 -14px 8px; padding:6px 10px 0; }
  html.is-mobile #mbar::before { content:''; position:absolute; top:5px; left:50%; width:38px; height:4px; margin-left:-19px; border-radius:2px; background:#55606d; }
  html.is-mobile #mbar button { min-width:48px; height:44px; font-size:18px; padding:0; }
  html.is-mobile #mTitle { flex:1; text-align:center; font-weight:700; font-size:15px; line-height:1.2; cursor:pointer; user-select:none; }
  html.is-mobile #mTitle small { display:block; font-weight:400; font-size:11px; color:var(--muted); }
  html.is-mobile #nav, html.is-mobile #stepTitle { display:none; }
  html.is-mobile h1 { font-size:17px; }
  html.is-mobile .steps button { padding:11px 0; font-size:16px; }
  html.is-mobile button, html.is-mobile select { min-height:40px; font-size:15px; }
  html.is-mobile label.chk { min-height:36px; padding-right:8px; }
  html.is-mobile label.chk input { width:20px; height:20px; }
  html.is-mobile #hint { top:auto; bottom:8px; right:8px; font-size:11px; }
  html.is-mobile #compass { top:calc(8px + env(safe-area-inset-top)); left:8px; font-size:11px; padding:3px 6px; }
  html.is-mobile .lbl { font-size:9.5px; padding:1px 4px; }
  html.is-mobile .lbl.big { font-size:10.5px; }
  html.is-mobile .lbl.dim { font-size:11px; }
  html.is-mobile td, html.is-mobile th { font-size:12.5px; padding:5px 4px; }
</style>''')

# ------------------------------------------------------------------ mobile bar markup + hint
sub('''  <div id="side">
    <h1 id="title">''', '''  <div id="side">
    <div id="mbar"><button id="mPrev" aria-label="Previous step">◀</button>
      <div id="mTitle" role="button"><span id="mStep">Step</span><small id="mHint">tap for details</small></div>
      <button id="mNext" aria-label="Next step">▶</button></div>
    <h1 id="title">''')

# ------------------------------------------------------------------ renderer performance on phones
sub("renderer.setPixelRatio(Math.min(devicePixelRatio, 2));",
    "const MOBILE_START = window.__isMobile();\nrenderer.setPixelRatio(Math.min(devicePixelRatio, MOBILE_START ? 2 : 2));")
sub("sun.shadow.mapSize.set(4096, 4096);", "sun.shadow.mapSize.set(MOBILE_START ? 2048 : 4096, MOBILE_START ? 2048 : 4096);")
sub("const n = 900, cone = new THREE.ConeGeometry(0.9, 5, 5)", "const n = MOBILE_START ? 450 : 900, cone = new THREE.ConeGeometry(0.9, 5, 5)")
sub("const bloom = new UnrealBloomPass(new THREE.Vector2(512, 512), 0, 0.4, 0.75); composer.addPass(bloom);",
    "const bloom = new UnrealBloomPass(new THREE.Vector2(512, 512), 0, 0.4, 0.75); composer.addPass(bloom);\n"
    "const useComposer = !MOBILE_START;                       // phones: render directly (no bloom) – faster, less battery\n"
    "function renderFrame() { if (useComposer) composer.render(); else renderer.render(scene, camera); }")
sub("  controls.update(); composer.render(); labelRenderer.render(scene, camera);",
    "  controls.update(); renderFrame(); labelRenderer.render(scene, camera);")

# ------------------------------------------------------------------ camera framing for narrow / portrait screens
sub("function goCam(name) { const c = CAMS[name]; camAnim = { p0:camera.position.clone(), t0:controls.target.clone(), p1:V(...c.p), t1:V(...c.t), k:0 }; }",
'''// presets are framed for a ~4:3 view; on narrow (portrait) screens move the camera back so the 240 cm board fits
function camPose(name) {
  const c = CAMS[name], t = V(...c.t), p = V(...c.p);
  const f = clamp(1.3 / camera.aspect, 1, 2.8);
  return { p: t.clone().add(p.sub(t).multiplyScalar(f)), t };
}
function goCam(name) { const c = camPose(name); camAnim = { p0:camera.position.clone(), t0:controls.target.clone(), p1:c.p, t1:c.t, k:0 }; }
let lastCam = 'persp';''')
sub("document.querySelectorAll('[data-cam]').forEach(b => b.onclick = () => goCam(b.dataset.cam));",
    "document.querySelectorAll('[data-cam]').forEach(b => b.onclick = () => { goCam(b.dataset.cam); closeSheet(); });")
sub("  camera.position.set(...CAMS.persp.p); controls.target.set(...CAMS.persp.t);",
    "  { const c = camPose('persp'); camera.position.copy(c.p); controls.target.copy(c.t); }")

# ------------------------------------------------------------------ resize via ResizeObserver (sheet / rotation)
sub("addEventListener('resize', resize); resize();",
    "addEventListener('resize', resize); new ResizeObserver(resize).observe(view); resize();")

# ------------------------------------------------------------------ sheet behaviour + step title in the bar
sub("const cb = id => document.getElementById(id);",
'''const cb = id => document.getElementById(id);
const sideEl = document.getElementById('side');
function closeSheet() { if (window.__isMobile()) { sideEl.classList.remove('open'); sideEl.scrollTop = 0; updHint(); } }
function updHint() { cb('mHint').textContent = sideEl.classList.contains('open') ? 'tap to close' : 'tap for details'; }
cb('mTitle').onclick = () => { sideEl.classList.toggle('open'); if (!sideEl.classList.contains('open')) sideEl.scrollTop = 0; updHint(); };
cb('mPrev').onclick = () => cb('prev').click();
cb('mNext').onclick = () => cb('next').click();
function setHint() {
  cb('hint').textContent = window.__isMobile() ? '1 finger: rotate · 2 fingers: zoom / pan'
                                               : 'Left-drag: rotate · Right-drag: pan · Wheel: zoom';
}
setHint(); addEventListener('resize', setHint);''')
sub("STEPS.forEach((s, i) => { const b = document.createElement('button'); b.textContent = i+1; b.onclick = () => setStep(i); stepsEl.appendChild(b); });",
    "STEPS.forEach((s, i) => { const b = document.createElement('button'); b.textContent = i+1; b.onclick = () => { setStep(i); closeSheet(); }; stepsEl.appendChild(b); });")
sub("  cb('stepTitle').textContent = s.t;\n", "  cb('stepTitle').textContent = s.t; cb('mStep').textContent = s.t;\n")
sub("  cb('stepTitle').textContent = 'Complete landsby';", "  cb('stepTitle').textContent = 'Complete landsby'; cb('mStep').textContent = 'Complete landsby'; closeSheet();")

# ------------------------------------------------------------------ saving on iPhone: share sheet if available
sub("cb('btnGlb').onclick = () => {", '''async function saveBlob(blob, name) {
  const file = new File([blob], name, { type:blob.type });
  if (window.__isMobile() && navigator.canShare && navigator.canShare({ files:[file] })) {
    try { await navigator.share({ files:[file], title:name }); return; } catch (e) { if (e.name === 'AbortError') return; }
  }
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
cb('btnGlb').onclick = () => {''')
sub('''    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([res], { type:'model/gltf-binary' }));
    a.download = `${village.name.replace(/\\s/g, '_')}.glb`; a.click();''',
    '''    saveBlob(new Blob([res], { type:'model/gltf-binary' }), `${village.name.replace(/\\s/g, '_')}.glb`);''')
sub("cb('btnPng').onclick = () => { composer.render(); const a = document.createElement('a'); a.href = renderer.domElement.toDataURL('image/png'); a.download = `${village.name.replace(/\\s/g,'_')}_step${step+1}.png`; a.click(); };",
    "cb('btnPng').onclick = () => { renderFrame(); renderer.domElement.toBlob(b => saveBlob(b, `${village.name.replace(/\\s/g,'_')}_step${step+1}.png`), 'image/png'); };")

open(p, 'w', encoding='utf-8').write(s)
print('ok')
