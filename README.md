# Julelandsby

Christmas village (julelandsby) for the advent concert – 4 villages, each on a 2400 × 600 mm OSB plate with isofoam terrain, 6 model houses and 4 street lights.

**Live 3D model:** https://julelandsby.web.app (works on desktop and iPhone)

## Contents

| Path | What |
|---|---|
| `City_Layout_3D/landsby_lights.html` | Interactive 3D model (three.js): layout of Landsby 1–4, step-by-step assembly, LED / street-light wiring, DMX channels, cable lengths. Single self-contained file (loads three.js from CDN). |
| `hosting/` | Firebase Hosting setup (project `julelandsby`). `public/index.html` is the published copy of the model. |
| `City_layout/` | Source drawings: scene design PDF, house drawings (House_1–6), connection drawing, LED roof photos, photos. |
| `Assembly/`, `*.pdf`, `Description.txt` | House assembly instructions (EN/NO) and their source images. |
| `_work/` | Scripts used to build the assembly-instruction PDFs. |

## Update the website

```
copy City_Layout_3D\landsby_lights.html hosting\public\index.html
cd hosting
firebase deploy --only hosting
```

URL options for the model: `?v=1..4` (landsby), `?step=1..7`, `?device=mobile|desktop`.
