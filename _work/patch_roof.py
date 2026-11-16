import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()

def sub(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b)

# ---------------------------------------------------------------- LED cable code
a0 = s.index("// --- LED cable per house (method from Ladsby_connection)")
a1 = s.index("// ===========================================================================\n// Side panel")
new = r'''// --- LED cable per house (method from Ladsby_connection + LED_Roof photos):
//     driver -> round cables bundled in the garland along the front -> under the plate to the back edge ->
//     up over the back edge -> on the foam (under vatt) -> in just under the back wall -> 20 cm slack loop on the floor ->
//     inline plug  <->  short round pigtail from the end of the LED strip under the ridge beam (roof rests loose).
const ROOF_DY = 18, SLACK = 20, PIG = 10, BUNDLE_R = 0.7;
function ledPaths(h, i, roofLift, conn) {
  const D = village.D, wx = X => X - BOARD_L/2, fTop = village.foamTop, drv = village.driver, n = HOUSES.length;
  const gz = D/2 + 7, ang = i / n * Math.PI * 2;
  const oy = Math.sin(ang) * BUNDLE_R, oz = Math.cos(ang) * BUNDLE_R;       // round bundle cross-section
  const toW = (v, dy = 0) => v.clone().applyAxisAngle(V(0,1,0), h.rot).add(V(wx(h.x), h.padY + dy, h.z));
  const S = toW(V(0, h.stripY, h.stripEnd), roofLift*ROOF_DY);              // strip end (in the roof)
  const Cr = S.clone().add(V(0, -PIG, 0));                                    // pigtail socket
  const zb = h.z - h.fz/2;                                                    // back wall (stage side)
  const ex = clamp(S.x - wx(0), h.x - h.fx/2 + 3, h.x + h.fx/2 - 3);          // entry x (board coords)
  const E1 = V(wx(ex), h.padY + 0.35, zb + 1.2);
  const cc = V(wx(ex) + 3.2, h.padY + 0.35, zb + 4.6), r = SLACK / (2*Math.PI);
  const coil = [];
  for (let k = 0; k <= 24; k++) { const a = Math.PI + k/24 * Math.PI*2; coil.push(V(cc.x + Math.cos(a)*r, cc.y + k*0.012, cc.z + Math.sin(a)*r*0.95)); }
  const rest = V(wx(ex) + 7.5, h.padY + 0.6, zb + 5);                         // plug lying on the floor before connecting
  const plug = rest.clone().lerp(Cr.clone().add(V(0, -1.4, 0)), conn);
  const house = [
    V(wx(drv.x) + 7, FLOOR + 2.5, drv.z - 1 + oz), V(wx(-8), FLOOR + 4 + oy, gz + oz), V(wx(h.x) + 3, FLOOR + 4 + oy, gz + oz),
    V(wx(ex), FLOOR + 0.5, D/2 + 1), V(wx(ex), FLOOR + 0.5, -D/2 - 0.7),                     // under the plate (30 mm gap)
    V(wx(ex), fTop(ex, -D/2 + 0.5) + 0.3, -D/2 - 0.7), V(wx(ex), fTop(ex, -D/2 + 0.5) + 0.3, -D/2 + 0.5),
    V(wx(ex), fTop(ex, zb - 1.5) + 0.3, zb - 1.5), E1,                                         // just under the wall
    ...coil,                                                                                   // 20 cm slack
    plug.clone(),
  ];
  return { house, pig:[S, Cr], plug, sock:Cr, E1 };
}
function connector(pos, mat, len) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, len, 14), mat); m.position.copy(pos); return m;
}
let plugLabel = null, pigLabel = null;
function buildLedCables(roofLift = 0, conn = 1) {
  for (const c of [...G.wiringLED.children]) if (c.isMesh) { c.geometry.dispose(); G.wiringLED.remove(c); }
  const D = village.D, wx = X => X - BOARD_L/2, fTop = village.foamTop, gz = D/2 + 7;
  const firstLen = !HOUSES[0].ch;
  HOUSES.forEach((h, i) => {
    const P = ledPaths(h, i, roofLift, conn);
    G.wiringLED.add(cable(P.house, M.ledCab));
    G.wiringLED.add(cable(P.pig, M.ledCab));
    G.wiringLED.add(connector(P.sock.clone().add(V(0, -0.6, 0)), M.dev, 1.4));     // socket on the roof pigtail
    G.wiringLED.add(connector(P.plug.clone().add(V(0, 0.2, 0)), M.dev, 1.6));      // plug on the house cable
    if (firstLen) {
      const F = ledPaths(h, i, 0, 1);
      lengths.push({ name:`${h.label} (pos. ${i+1}) incl. 20 cm slack`, ch:i+1, len:polyLen(F.house), col:COL.led });
      h.ch = i + 1;
    }
  });
  // cable ties around the round bundle
  const xEnd = wx(Math.max(...HOUSES.map(h => h.x)));
  for (let x = wx(-8); x < xEnd; x += 25) {
    const t = new THREE.Mesh(new THREE.TorusGeometry(BUNDLE_R + 0.45, 0.12, 6, 16), M.white);
    t.position.set(x, FLOOR + 4, gz); t.rotation.y = Math.PI/2; G.wiringLED.add(t);
  }
  if (firstLen) {
    const h0 = HOUSES[1], P2 = ledPaths(HOUSES[2], 2, 0, 1);
    addLabel(G.wiringLED, 'Round LED cables, bundled with ties', V(wx(-8), FLOOR + 6.5, gz), [4], 'led');
    addLabel(G.wiringLED, 'Cable runs under the plate from front to back', V(wx(h0.x + 2), FLOOR + 1, 0), [4], 'led');
    addLabel(G.wiringLED, 'Up over the back edge (under vatt)', V(wx(HOUSES[3].x), fTop(HOUSES[3].x, -D/2) + 1, -D/2 - 1), [4,5], 'led');
    addLabel(G.wiringLED, 'In just under the back wall + 20 cm slack loop', P2.E1.clone().add(V(0, 1.5, 3)), [5], 'led');
    addLabel(G.wiringLED, 'Plug on house cable', V(0, 0, 0), [5,6], 'led'); plugLabel = labels[labels.length-1];
    addLabel(G.wiringLED, 'Pigtail from LED strip end (roof)', V(0, 0, 0), [5,6], 'led'); pigLabel = labels[labels.length-1];
  }
  const P1 = ledPaths(HOUSES[1], 1, roofLift, conn);
  if (plugLabel) plugLabel.position.copy(P1.plug).add(V(0, conn > 0.99 ? -3 : 1, 0));
  if (pigLabel) pigLabel.position.copy(P1.sock).add(V(0, 3, 0));
}

'''
s = s[:a0] + new + s[a1:]

# ---------------------------------------------------------------- house / misc
sub("  Object.assign(h, { group:house, body, roof, light, Hr, stripY:Hr - 1.9 });",
"""  // strip end used for the pigtail: the end nearest the back (stage side) of the board
  const zEnd = [sl/2, -sl/2].sort((a, b) => { const wa = V(0,0,a).applyAxisAngle(V(0,1,0), h.rot), wb = V(0,0,b).applyAxisAngle(V(0,1,0), h.rot);
    return (wa.z - wb.z) || (wa.x - wb.x); })[0];
  Object.assign(h, { group:house, body, roof, light, Hr, stripY:Hr - 1.9, stripEnd:zEnd });
  addLabel(roof, 'Roof rests loose on the walls (not fastened)', V(0, t.Ht + 1, 0), h.idx === 1 ? [6] : [], 'big');""")
sub("  strip:  new THREE.MeshStandardMaterial({ color:0xf2f2f2, roughness:0.5 }),",
    "  strip:  new THREE.MeshStandardMaterial({ color:0x151515, roughness:0.5 }),\n  white:  new THREE.MeshStandardMaterial({ color:0xf2f2f2, roughness:0.6 }),")
sub("addLabel(house, h.label, V(0, t.Ht + 4, 0), [5,6], 'big');", "addLabel(house, h.label, V(0, t.Ht + 4, 0), [5,6,7], 'big');")
sub("addLabel(g, `Street light ${l.i+1}`, V(0, H + 3, 0), [3,6], 'sl');", "addLabel(g, `Street light ${l.i+1}`, V(0, H + 3, 0), [3,7], 'sl');")
sub("V(wx(150), FLOOR + 10, gz), [6]);", "V(wx(150), FLOOR + 10, gz), [7]);")
sub("'8-channel LED driver (Deca LED)', V(wx(drv.x), FLOOR + 7, drv.z), [4,6], 'big');", "'8-channel LED driver (Deca LED)', V(wx(drv.x), FLOOR + 7, drv.z), [4,7], 'big');")
sub("'DMX control', V(wx(dmx.x), FLOOR + 6, dmx.z), [4,6], 'big');", "'DMX control', V(wx(dmx.x), FLOOR + 6, dmx.z), [4,7], 'big');")
sub("  buildLedCables(0);\n", "  buildLedCables(0, 1);\n")
sub("grid-template-columns:repeat(6,1fr)", "grid-template-columns:repeat(7,1fr)")
sub('<input type="checkbox" id="cbExplode"> Lift houses & roofs', '<input type="checkbox" id="cbExplode"> Lift roofs')
sub("each junction box sits on a house pad, so it is reachable when that house is lifted off.".capitalize(),
    "Each junction box sits on a house pad, so it is reachable when that house is lifted off.")

# ---------------------------------------------------------------- steps
a0 = s.index("  { t:'4 ")
a1 = s.index("];\nlet step = 0")
s = s[:a0] + '''  { t:'4 · LED cables to the houses', cam:'under', xray:true, show:['base','foam','wiringSL','wiringLED','lamps','devices'],
    txt:['One round cable (purple in the model) per house from the 8-channel Deca LED driver at the left end.', 'The cables run as a round bundle along the front of the board.', 'At each house the cable turns in under the plate (30 mm gap), runs to the back edge and comes up over the back edge of the foam.'] },
  { t:'5 · Vatt, houses & cable slack', cam:'back', xray:true, asm:0, show:['base','foam','vatt','wiringSL','wiringLED','houses','lamps','devices'],
    txt:['Lay the vatt (cotton snow) over the foam – it hides all cables on top of the foam.', 'Put every house on its pad. The cable goes in just under the back wall.', 'Leave about 20 cm of extra cable inside the house, with the plug on the end.', 'Each roof has the LED strip under the ridge (top) beam, with a short pigtail + socket at one end.'] },
  { t:'6 · Connect roof LED & put roofs on', cam:'house', xray:true, asm:'anim', show:['base','foam','vatt','wiringSL','wiringLED','houses','lamps','devices'],
    txt:['When all houses are in place: hold the roof just above its house.', 'Using the 20 cm slack, pull the plug up and connect it to the roof pigtail.', 'Lower the roof onto the walls – it just rests there (not fastened); the slack folds back into the house.'] },
  { t:'7 · Garland, DMX & power on', cam:'persp', lights:true, show:['base','foam','vatt','wiringSL','wiringLED','houses','lamps','garland','devices','decor'],
    txt:['Lay the garland along the front – the cable bundle runs hidden inside it to the driver.', 'Connect DMX control → driver. Ch 1–6 = houses, Ch 7 = street lights, Ch 8 = spare.'] },
''' + s[a1:]
sub("  if (s.lift) { lift = 1; liftTarget = 0; slowLift = true; } else { liftTarget = cb('cbExplode').checked ? 1 : 0; slowLift = false; }",
"""  cb('cbExplode').checked = false; extraTarget = 0;
  if (s.asm === 0) { asm = asmTarget = 0; }
  else if (s.asm === 'anim') { asm = 0; asmTarget = 1; }
  else { asm = asmTarget = 1; }""")
sub("cb('cbExplode').onchange = e => { liftTarget = e.target.checked ? 1 : 0; slowLift = false; };",
    "cb('cbExplode').onchange = e => { extraTarget = e.target.checked ? 1 : 0; };")

# ---------------------------------------------------------------- animation loop
a0 = s.index("let lift = 0, liftTarget = 0")
a1 = s.index("  if (camAnim) {")
s = s[:a0] + '''// assembly state: asm 0 = roofs held above, plug apart; 0..0.4 plug goes up and connects; 0.5..1 roof lowered
let asm = 1, asmTarget = 1, extra = 0, extraTarget = 0, lastKey = '';
function animate() {
  requestAnimationFrame(animate);
  asm += Math.sign(asmTarget - asm) * Math.min(0.004, Math.abs(asmTarget - asm));
  extra += Math.sign(extraTarget - extra) * Math.min(0.04, Math.abs(extraTarget - extra));
  const conn = smooth(asm / 0.4), roofLift = Math.max(1 - smooth((asm - 0.5) / 0.5), smooth(extra));
  const key = conn.toFixed(4) + '/' + roofLift.toFixed(4);
  if (key !== lastKey) {
    HOUSES.forEach(h => { h.group.position.y = h.padY; h.roof.position.y = roofLift * ROOF_DY; });
    buildLedCables(roofLift, conn); lastKey = key;
  }
''' + s[a1:]
sub("const CAMS = {\n", "const CAMS = {\n  house: { p:[-40, 95, -150],  t:[-50, 22, -12] },\n")
sub("setStep(Math.max(0, Math.min(5, (parseInt(q.get('step')) || 1) - 1)));",
    "setStep(Math.max(0, Math.min(STEPS.length-1, (parseInt(q.get('step')) || 1) - 1)));")
sub("  if (q.has('lift')) { cb('cbExplode').checked = q.get('lift') === '1'; liftTarget = +cb('cbExplode').checked; }",
    "  if (q.has('asm')) { asm = asmTarget = parseFloat(q.get('asm')); }")
sub("  if (q.has('instant')) { lift = liftTarget; if (camAnim) camAnim.k = 0.999; }",
    "  if (q.has('instant')) { if (!q.has('asm')) asm = asmTarget; if (camAnim) camAnim.k = 0.999; }")
sub("// URL options: ?v=1&step=4&cam=under&xray=1&lights=1&lift=1&all=1&instant=1",
    "// URL options: ?v=1&step=4&cam=under&xray=1&lights=1&asm=0.3&all=1&instant=1")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
