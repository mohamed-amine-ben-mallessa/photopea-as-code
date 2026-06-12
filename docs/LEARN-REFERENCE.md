# Photopea — complete /learn reference (all 45 pages)

Menu paths + JS scripting API for every Photopea feature, condensed for an agent driving
Photopea via the **photopea MCP** (`photopea_run_script` runs raw JS; end every script with
`app.echoToOE(...)`). The public /learn pages confirm menu paths; the scripting names follow
Photopea's Photoshop-compatible model. For export use `app.activeDocument.saveToOE(fmt)` or
the typed `photopea_export_image` tool. Deep scripting + smart-object mockups:
see [PHOTOPEA-SCRIPTING.md](PHOTOPEA-SCRIPTING.md).

---

## Basics

### Workspace
Toolbar (left) · Sidebar panels (right, `Window > …`) · Working Area (doc tabs) · Top Menu.
**X** swap FG/BG, **D** reset b/w. JS: `app.documents`, `app.activeDocument` (switch:
`app.activeDocument = app.documents[i]`), `app.foregroundColor` (SolidColor).

### Navigation
Pan **Space**+drag; zoom **Ctrl+Space**/Alt+wheel; **Ctrl+0** fit, **Ctrl+1** 100%.
`Ctrl+R` rulers. History: `Ctrl+Z`, `Shift+Ctrl+Z` fwd, `Alt+Ctrl+Z` back. View is UI-only.

### Image / Canvas size
`Image > Image Size` (resample+DPI) vs `Image > Canvas Size` (frame only). JS:
`doc.resizeImage(w,h,res,ResampleMethod.BICUBIC)`, `doc.resizeCanvas(w,h,AnchorPosition.MIDDLECENTER)`,
`doc.rotateCanvas(deg)`. Sizes are `UnitValue(800,"px")`. Pass only W/H to keep DPI.

### Color spaces / modes
`Image > Mode > {RGB,CMYK,Grayscale,Lab,Bitmap,Indexed; 8/16/32 bits}`. JS: `doc.mode`
(DocumentMode.*), `doc.changeMode(ChangeMode.RGB|CMYK|GRAYSCALE|LAB|…)`,
`doc.bitsPerChannel = BitsPerChannelType.EIGHT|SIXTEEN|THIRTYTWO`. /learn/color-spaces is
conceptual (CIELAB/XYZ, ICC profiles) — no UI there.

### Guides, grid & snapping
`View > Show > {Guides,Grid,Pixel Grid}`, `View > Extras`, `View > Snap`, `View > Snap To >`.
Snap ≈5px. JS: `doc.guides.add(Direction.HORIZONTAL|VERTICAL, position)`; `guide.coordinate`,
`guide.direction`. Guides per-doc; grid global (Edit > Preferences).

### Storages / File I/O
Local, Google Drive, Dropbox, OneDrive, Peadrive. `File > Open` / `Open More > Storage`,
`File > Save` (Ctrl+S → origin), `File > Export As` (PNG/JPG/SVG/PDF). JS: `app.open(url)`,
`doc.saveToOE("png"|"jpg:0.8"|"psd")`, `app.echoToOE(text)`.

---

## Layers

### Layers (basics)
New/delete/duplicate (`Ctrl+J`). JS: `doc.artLayers.add()`, `doc.layerSets.add()` (groups),
`layer.duplicate()`, `layer.remove()`, `layer.merge()`, `doc.mergeVisibleLayers()`,
`doc.flatten()`. Props: `.name`, `.visible`, `.opacity`(0-100), `.fillOpacity`,
`.blendMode`(BlendMode.NORMAL|MULTIPLY|SCREEN|OVERLAY|…). Active: `doc.activeLayer`.

### Other layer types
Raster vs generated (Text, Smart Object, Fill, Adjustment) + Groups + Clipping.
`Layer > New Fill Layer > {Solid|Gradient|Pattern}`, `Layer > New Adjustment Layer > …`,
`Layer > Rasterize`, `Layer > Clipping Mask` (`Alt+Ctrl+G`). Type via `layer.kind`
(LayerKind.NORMAL|TEXT|SMARTOBJECT|SOLIDFILL|GRADIENTFILL|PATTERNFILL|adjustments).
Pixel tools need a direct raster — rasterize first.

### Layer manipulation
Move tool; arrows nudge 1px / Shift 10px; Ctrl = temp Move; align buttons; auto-select.
JS: `layer.translate(dx,dy)`, `layer.move(ref, ElementPlacement.PLACEBEFORE/PLACEAFTER)`,
`.resize(wPct,hPct,anchor)`, `.rotate(deg,anchor)`.

### Free Transform
`Ctrl+T`; `Edit > Transform > {Scale,Rotate,Skew,Distort,Perspective,Warp,Flip}`. Top bar:
X,Y,W,H,Angle,Skew + 3×3 origin. Shift=ratio, Alt=center, Ctrl=free corners, Enter commit.
JS: `layer.resize/rotate/translate` with `AnchorPosition.*`.

### Masks
Raster + Vector + Clipping (max 1 raster + 1 vector per layer). `Layer > Raster Mask > Add`,
`Layer > Vector Mask > Add`. Properties: Density, Feather (render-time). Click layer-vs-mask
thumbnail to choose paint target. Chain icon links mask to content.

### Layer Styles
Drop/Inner Shadow, Stroke, Color/Gradient Overlay, Bevel&Emboss, Outer/Inner Glow.
Double-click layer / right-click > Blending Options. JS: `layer.applyStyle(style)`; granular
params are edited via the layer's style JSON, not per-property setters.

### Channels
`Window > Channels`. Component (R,G,B) + alpha + extra alpha/spot channels. Bottom bar:
load-as-selection, save-selection, new, delete. JS: `doc.channels`, `doc.activeChannels`,
`doc.channels.add()`, `channel.kind` (ChannelType.COMPONENT|MASKEDAREA|SELECTEDAREA|SPOTCOLOR).

### Layer Comps
`Window > Layer Comps` — snapshot per-layer Visibility/Position/Appearance. New/Update/Delete/
Apply. No built-in per-comp export (apply then export manually).

### Smart Objects → see PHOTOPEA-SCRIPTING.md
`executeAction(stringIDToTypeID("placedLayerEditContents"))` enters the source; edit; `save()`
propagates to all instances; `close()`. `"newPlacedLayer"` converts a layer to a SO. The
mockup engine.

---

## Selections

### Selections (concept)
One per doc, 0-100% per pixel. `Select > Inverse|Modify(Expand/Contract/Feather)|Deselect(Ctrl+D)
|Transform`. Quick Mask **Q**. JS `doc.selection`: `selectAll()`, `deselect()`,
`select(bounds,type,feather,antiAlias)`, `fill(color,mode,opacity)`, `stroke(...)`, `expand`,
`contract`, `feather`, `invert`, `translate`, `store(channel)`/`load(channel)`. Type =
SelectionType.REPLACE|EXTEND|DIMINISH|INTERSECT.

### Creating / Advanced selecting
Rect/Ellipse, Lasso/Polygonal/Magnetic, Magic Wand (Tolerance+Contiguous), Quick Selection,
`Select > Color Range` (soft). Ctrl+click layer thumb = load alpha. JS: `selection.grow(tol,contig)`,
`selectBorder(px)`, `selection.bounds`.

### Refine Edge / Select & Mask
`Select > Refine Edge`. Trimap: White keep / Black remove / Grey uncertain. Output: New Layer
(best, keeps color), Raster Mask, or Selection. No JS API — use masks/channels.

### Moving selected data
`Edit`: Cut/Copy/Copy Merged(Shift+Ctrl+C)/Paste/Fill/Stroke. JS: `selection.cut()`, `.copy([merged])`,
`.clear()`, `.fill(color,mode,opacity)`, `.stroke(...)`.

---

## Text

### Text
Point / Paragraph / On-a-curve. **T** tool. Editing LOCKS the layer — Esc/checkmark to exit
(agent gotcha). JS: text `ArtLayer` has `.textItem` with **`totalTextStyle`** (JSON of all
style params: font,size,color,leading,tracking,justify) and **`transform`** (affine matrix).
Read/modify/reassign `totalTextStyle` to restyle. Set `layer.kind=LayerKind.TEXT`,
`layer.textItem.contents="…"`.

### Text Style
`Window > Character` / `Window > Paragraph`. Char: font,size,color,kerning,tracking,leading.
Para: alignment/justify, direction, margins. Import TTF/OTF via `File > Open`. All map into
`totalTextStyle`.

---

## Vector graphics

### Vector graphics / structure
Paths (Paths panel, Work Path) · Vector Masks · Shape Layers (fill + vector mask).
`Window > Paths`; Ctrl+click path = selection. Hierarchy Shape→Paths→Knots (Anchor + 2 Handles);
open/closed paths; smooth(circle)/corner(square) knots. Per-path boolean: Union/Subtract/
Intersect/Exclude. Fill/Stroke: None/Color/Gradient/Pattern; stroke position Inside/Center/Outside.

### Creating / manipulating shapes
Top-bar **Mode**: Shape (new layer) / Path (add to current) / Pixels (rasterize now). Tools:
Pen, Free Pen, Rect/Ellipse/Line, Custom Shape (.CSH), Parametric (Polygon/Star/Spiral).
Path Select (whole) vs Direct Select (knots). Double-click anchor toggles smooth/corner.
Right-click text > **Convert to Shape** = glyphs to paths. Export SVG/PDF keeps vector.

### Vectorize bitmap
`Image > Vectorize Bitmap` — params: number of colors, noise reduction. Replaces raster with
vector layers → SVG/PDF. (Also `app.showWindow("vbitmap")`.)

---

## Tools

### Brush tools
Brush/Pencil/Eraser/Clone/Healing/Blur/Sharpen/Smudge/Dodge/Burn. Constrained to selection.
Circular (Size+Hardness) or Pattern brush. `Window > Brush`: Spacing ≤25%, dynamics, scatter.
Import .ABR via `File > Open`; `Edit > Define New > Brush`.

### Basic / Advanced / Smart tools
Basic: Move, Marquee, Lasso, Crop, Eyedropper, Brush, Eraser, Fill, Text, Shapes, Hand, Zoom.
Advanced: Clone Stamp, Healing, Gradient, Blur/Sharpen/Smudge, Dodge/Burn. Smart: Magic Cut
(`app.showWindow("magiccut")`, bg removal), Object/Quick selection, Magic Wand.

---

## Filters (mostly UI; few JS methods)

### Adjustments & Filters
Adjustments (color): Brightness/Contrast, Levels(Ctrl+L), Curves(Ctrl+M), Hue/Sat(Ctrl+U),
Color Balance, Posterize, Invert, Desaturate. Destructive `Image > Adjustments`; non-destructive
`Layer > New Adjustment Layer`. JS on ArtLayer: `adjustBrightnessContrast(b,c)`, `posterize(n)`,
`invert()`, `desaturate()`. Filters: `applyGaussianBlur(r)`, `applyMotionBlur(angle,r)`,
`applyAddNoise(...)`, `applySharpen()`, `applyUnSharpMask(...)`. Can't filter text/pattern (rasterize).

### Vanishing Point
`Filter > Vanishing Point` — define perspective planes (Ctrl+drag for adjacent), Stamp/Brush/
Marquee/Transform in perspective, Ctrl+V pastes into a plane. Breaks on cropped photos. UI-only.

### Blur Gallery
`Filter > Blur Gallery`: Field/Iris/Tilt-Shift/Path/Spin blur, combinable. UI-only (simple
Gaussian/Motion live under `Filter > Blur`).

---

## Output & automation

### Artboards
"Docs inside a doc" — top-level folders with a viewport. Create via New Document checkbox /
Artboard tool / import (Sketch/XD/Figma auto-detect; PDF page → artboard). **Export As > PNG/JPG
with "As Artboards"** → ZIP, one file per artboard; PDF → one page per artboard. (Key for
multi-format batch.)

### Animations
Layer-name based: name starting `_a_` = a frame (100ms default); non-prefixed layers show in
every frame. Delay: append `,ms` → `_a_dog,500`. Parallel: folders + `Layer > Animation > Merge`.
Export GIF/APNG/WEBP via `File > Export As` (auto-detects `_a_`). No timeline/MP4 here.

### Slices
Slice tool (drag) + Slice Select. Auto-slices fill gaps. `View > Slices`. `Export As > PNG/JPG/GIF`
→ ZIP of one image per slice + an HTML file.

### Automate (Actions / Scripts / Variables)
- **Actions** (`Window > Actions`): record/replay steps; load/save .ATN. Single-doc playback.
- **Scripts** (`File > Script`): raw JS, the real automation surface (`app.*`, see scripting doc).
- **Variables** (`Image > Variables`): pixel/text/visibility variables + **CSV Data Sets** →
  **Export as** ZIP, one render per row. The no-code batch/mockup engine.

---

## Key takeaways for the agent
1. **`photopea_run_script`** unlocks the full Photoshop-compatible JS model — use it for
   anything the typed MCP tools lack. Always end with `app.echoToOE(...)`.
2. **Mockups/variants:** smart-object scripting (`placedLayerEditContents`) OR `Image > Variables`+CSV.
3. **Multi-file export:** Artboards "As Artboards", or Slices → ZIP.
4. **Text:** drive via the `totalTextStyle` JSON blob + `transform` matrix.
5. **Animations:** the `_a_` layer-name convention → GIF/WEBP.
6. UI-only (no JS): Refine Edge, Vanishing Point, Blur Gallery, Vectorize — drive via menu/Live API.
```
