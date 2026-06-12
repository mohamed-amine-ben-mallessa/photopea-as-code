# Photopea scripting reference (for `photopea_run_script`)

The Photopea MCP's typed tools are built on top of Photopea's **Photoshop-compatible
JS scripting API**. For anything the typed tools don't cover, use
`photopea_run_script({script})` — raw JS. **The script MUST end with `app.echoToOE(result)`**
to return a value to the agent (the MCP waits for it).

Sources: photopea.com/learn/* , /api/live , /api/plugins , /tuts/* .

## Core object model
- `app` — the application. `app.documents`, `app.activeDocument`, `app.fonts`,
  `app.open(url, as, asSmart)`.
- `app.activeDocument` (a Document) — `.width`, `.height`, `.layers`, `.activeLayer`,
  `.selection`, `.name` (rw), `.source` (rw, an ID). Methods: `resizeImage(w,h)`,
  `resizeCanvas(w,h,anchor)`, `rotateCanvas(deg)`, `flatten()`, `mergeVisibleLayers()`,
  `save()`, `close()`, `clearHistory()` (frees RAM between batch iterations),
  `saveToOE(format)`.
- Layers: `doc.artLayers.add()`, `doc.layerSets.add()` (folders), `layer.duplicate()`,
  `layer.remove()`, `layer.merge()`, `layer.translate(x,y)`, `layer.rotate(deg)`,
  `layer.resize(wPct,hPct,anchor)`. Props (settable): `.name`, `.visible`,
  `.opacity` (0-100), `.fillOpacity`, `.blendMode` (BlendMode.MULTIPLY/SCREEN/OVERLAY/…).
- Selection (`doc.selection`): `selectAll()`, `deselect()`, `select(bounds,type)`,
  `fill(color)`, `stroke(color,w)`, `expand(n)`, `contract(n)`, `feather(r)`, `invert()`,
  `translate(x,y)`, `store(channel)`, `load(channel)`. `type` ∈ SelectionType.REPLACE/
  EXTEND/DIMINISH/INTERSECT.
- Color: `var c=new SolidColor(); c.rgb.hexValue="283276";`
- Adjustments (on an ArtLayer): `adjustBrightnessContrast(b,c)`, `adjustLevels(...)`,
  `posterize(n)`, `invert()`, `desaturate()`.
- Filters: `applyGaussianBlur(r)`, `applyMotionBlur(angle,r)`, `applyAddNoise(amt,dist,mono)`,
  `applySharpen()`, `applyUnSharpMask(amt,r,thr)`. (Can't filter text/pattern — rasterize first.)

## Export (the only real "save")
`app.activeDocument.saveToOE(format)` renders + returns bytes. Formats:
`"png"`, `"jpg:0.8"`, `"webp:0.6"`, `"psd:true"`, `"svg:true,false,…"`, `"gif"`.
(Via the MCP, prefer the typed `photopea_export_image` tool: `outputPath` + `format`
∈ png/jpg/webp/psd/svg, `quality` 1-100 for JPG only.)

## Return data to the agent
`app.echoToOE(JSON.stringify(obj))` — send a string/JSON back. Every action the MCP
runs ends with `app.echoToOE('ok')`. Your custom scripts must do the same.

## 🎯 Smart Objects = the mockup engine
A Smart Object (SO) wraps layers into an internal PSD "source". Transform/scale an SO
non-destructively; **change the source once → every placement updates**. That's mockups.

**Edit a Smart Object's contents by script** (verified, from /tuts/edit-smart-objects-with-a-script):
```javascript
// open the SO's internal source as a document:
var l = app.activeDocument.layers.getByName("arrow");   // the smart-object layer
app.activeDocument.activeLayer = l;
executeAction(stringIDToTypeID("placedLayerEditContents"));
// ...now the active document IS the SO source. Edit it (replace image, change text)...
app.activeDocument.save();   // propagates back to ALL instances of this SO
app.activeDocument.close();  // return to the mockup doc
```
Convert a layer to a Smart Object by script:
```javascript
var l = app.activeDocument.layers.getByName("ground");
app.activeDocument.activeLayer = l;
executeAction(stringIDToTypeID("newPlacedLayer"));
```
`executeAction(nameID, descriptor)` runs a low-level action; `stringIDToTypeID("…")`
turns an action name into its ID. This is the Photoshop "Action Manager" model.

### Replacing the SO image with a new design
Two ways:
1. Enter the SO (`placedLayerEditContents`), then inside the source:
   `app.open(newImageURL, null, false)` / paste / `selection.fill`, resize to fit,
   `save()`, `close()`.
2. `app.open(designURL, "smart"==true)` pastes a new image into the *current* doc as a
   fresh SO placed over the placeholder area (simpler for some templates).

### Bulk loop (one mockup per design)
```javascript
// pseudocode the agent runs per image, looping outside via the MCP:
// 1. open the mockup PSD (photopea_open_file)
// 2. enter SO -> replace contents with design_i -> save() -> close()
// 3. saveToOE("png")  (or photopea_export_image)  -> one finished mockup
// 4. clearHistory()  (free RAM)  -> next design
```
For a **no-code** batch, the native route is **Image > Variables**: assign a
*pixel-content* variable to the placeholder layer, load a **CSV** (column = variable
name, cell = source image filename) in **Data Sets**, then **Export as** → a ZIP with
one render per CSV row. (UI feature; use it when there are many designs.)

## Live Messaging API (how the MCP talks to the browser)
Outer page ↔ Photopea iframe via `postMessage`:
```javascript
window.addEventListener("message", e => { /* e.data = "done" | ArrayBuffer | echo string */ });
var wnd = document.getElementById("pp").contentWindow;
wnd.postMessage('app.activeDocument.saveToOE("png");', "*");   // send a script string
// Photopea replies: (ArrayBuffer bytes if saveToOE) then the literal "done"
```
- Send a **String** = a script to run. Send an **ArrayBuffer** = a file to load (PSD/PNG/font/brush).
- Photopea sends `"done"` on init and after **every** message it finishes.
- This is exactly the request/response loop the MCP uses under the hood.

## Headless launch config (embed Photopea with files + a startup script)
Load `photopea.com#` + `encodeURIComponent(JSON)`:
```json
{
  "files": ["https://site/mockup.psd", "data:image/png;base64,iVBOR..."],
  "resources": ["https://site/brushes/Nature.ABR"],
  "server": { "version": 1, "url": "https://site/save.php", "formats": ["psd:true","png","jpg:0.8"] },
  "script": "app.activeDocument.rotateCanvas(90); app.echoToOE('done');"
}
```

## Plugins API (sidebar web panels)
A plugin is just a website declared in the environment config; it gets a sidebar button
and talks to Photopea via the same Live Messaging (`window.parent.postMessage(...)`).
```json
{ "environment": { "plugins": [
  { "name": "Photo Store", "url": "https://example.com/store", "icon": "===https://example.com/i.png" } ] } }
```
Install via **Window > Plugins > Add Plugin**. Icon: black on transparent, prepend `===`
to the icon URL for theme adaptation.

## Useful tutorials (photopea.com/tuts/<slug>)
- `edit-smart-objects-with-a-script` — the SO scripting above (mockups).
- `bulk-generate-mockups-from-a-psd` — the UI mockup batch.
- `batch-convert-images-online-no-upload` — batch format conversion.
- `generate-nft-combinations-online` — combinatorial layer export (NFT/variant sheets).
- `change-text-in-image-online` — swap text layers programmatically.
- `add-watermark-to-photo`, `remove-background-from-photo`, `prepare-graphics-for-printing`,
  `set-a-specific-width-height-and-dpi-of-an-image`, `convert-jpg-to-pdf-online`,
  `make-grid-collages-from-images`, `stitch-images-together-online`,
  `focus-stack-images-online`, `vectorize-raster-images`, `convert-images-into-a-mp4-video-online`.
- Conversions to layered PSD: `convert-pdf-to-layered-psd`, `convert-figma-to-psd`,
  `convert-sketch-to-psd`, `convert-xd-file-to-psd`, `convert-eps-to-layered-psd`,
  `convert-affinity-afphoto-to-psd-online`.

## Templates
photopea.com/templates/ = a gallery of ready-made PSD templates ("Hot / New / Top"),
publishable by users (`/tuts/publish-your-psd-templates-in-photopea`). Open one, swap its
smart object / text, export. Good starting point for mockups, social posts, print.

---

## Recipes verified in practice

### Use a CUSTOM FONT (the part the docs gloss over)
Photopea (web) does **not** read your OS-installed fonts. To use a custom OTF/TTF/WOFF2
in code, load it with `photopea_load_font` — and the URL trick that actually works is a
**`data:` URI**, not a local `file:///` path (the browser sandbox blocks `file://`).

```python
import base64
with open("MyFont.otf", "rb") as f:
    font_uri = "data:font/otf;base64," + base64.b64encode(f.read()).decode()
pp.call("photopea_load_font", {"url": font_uri})
# then find the exact name Photopea registered it under:
names = pp.call("photopea_list_fonts", {})        # JSON list of PostScript names
# now pass it to text:
pp.call("photopea_add_text", {"content": "TITLE", "x": 90, "y": 400,
                              "size": 134, "color": "#191210", "font": "MyFont-Regular"})
```
- ✅ `data:` URI works. ❌ `file:///C:/...` times out (sandbox).
- A `.otf` ~50 KB encodes fine inline. The font is available to `add_text`/`edit_text`
  for the rest of the session.

### Make ink "soak into" a paper/texture background (multiply)
Open a texture as the background, add your text, then set the **text layer's blend mode
to MULTIPLY** so the ink follows the paper's wrinkles/grain — an authentic printed look.

```python
pp.call("photopea_open_file", {"source": "/abs/kraft.png"})       # texture as bg
pp.call("photopea_add_text", {"content": "PHOTOPEA", "x": 90, "y": 400,
                              "size": 134, "color": "#191210", "font": "MyFont-Regular"})
pp.run_script('app.activeDocument.activeLayer.blendMode = BlendMode.MULTIPLY; app.echoToOE("ok");')
```
- `run_script` targets `app.activeDocument.activeLayer` — i.e. the layer you JUST added,
  so call it right after each `add_text`.
- ⚠️ **Multiply darkens.** Use **dark ink colors** (near-black, deep red, forest green).
  Light colors (cream, pale ocre, white) become **invisible** under multiply on a dark
  texture — keep those at `NORMAL` blend (skip the multiply for light text), or don't use
  light colors on dark paper at all.
- Other useful `BlendMode` values: `SCREEN` (lightens — for light ink on dark), `OVERLAY`,
  `LINEARBURN` (stronger ink), `NORMAL` (reset).

### Make many color variants of one layout
Loop over a palette list; per variant: open the texture, add text in the variant's colors
(+ multiply), export, then `app.activeDocument.close()` to reset for the next one. Same
idea powers `social-post-factory`'s themeable posts.
```
