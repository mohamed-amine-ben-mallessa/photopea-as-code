---
name: photopea-as-code
description: >
  Design images programmatically with Photopea (free browser Photoshop) via its MCP
  server. Use when the user wants to create or edit an image/banner/social-post/poster,
  work with PSD files and layers, apply gradients/filters/text/shapes, generate mockups,
  or batch-process images — without Photoshop and without an API key. Keywords: photopea,
  design as code, image generation, banner, social post, PSD, layers, mockup, photoshop
  alternative, export png, programmatic design.
license: MIT
---

# Photopea as Code

Drive the **photopea MCP** (~34 tools, free browser Photoshop) to design images in code.
A browser window opens on the first tool call — that's Photopea, expected.

## Exact tool args (verified — don't guess)
- `photopea_create_document`: `width`,`height` (req), `fillColor` (hex bg), `name`.
- `photopea_add_layer`: `name`. (Create a layer BEFORE applying a gradient to it.)
- `photopea_add_gradient`: `target` (existing layer name), `type:"linear"`,
  `colors:["#hex","#hex"]` (≥2), `angle`.
- `photopea_add_text`: **`content`** (NOT "text"), `x`,`y` (req), `size`, `color`,
  `bold`, `italic`, `font`, `letterSpacing`, `alignment`.
- `photopea_add_shape`: `type` ("rectangle"/"ellipse"), `bounds:{x,y,width,height}`
  (use **x/y**, not left/top), `fillColor`, `strokeColor`, `strokeWidth`.
- `photopea_export_image`: **`outputPath`** + `format` (png/jpg/webp/psd/svg);
  `quality` 1-100 (JPG only).
- `photopea_run_script`: raw Photopea JS — **must end with `app.echoToOE(...)`**.

## A working recipe (1080×1080 post)
```
create_document(1080,1080, fillColor="#16182e")
add_layer("bg"); add_gradient(target="bg", type="linear", colors=["#16182e","#283276"], angle=120)
add_shape(rectangle, bounds={x:90,y:150,width:120,height:12}, fillColor="#f5d76e")   # accent bar
add_text(content="HEADLINE", x:88, y:320, size:84, color="#ffffff", bold=true)
add_shape(rectangle, bounds={x:90,y:740,width:380,height:92}, fillColor="#f5d76e")   # CTA button
add_text(content="Call to action", x:120, y:770, size:38, color="#16182e", bold=true)
export_image(outputPath="post.png", format="png")
```

## Power: run_script
For anything the typed tools don't cover, use `photopea_run_script`. Full
Photoshop-compatible JS model. Examples:
- Resize canvas: `app.activeDocument.resizeCanvas(1200,1200); app.echoToOE("ok");`
- Edit a smart object (mockups): `executeAction(stringIDToTypeID("placedLayerEditContents"))`.
- Read info: `app.echoToOE(JSON.stringify({w:app.activeDocument.width}))`.

## Reference
- `docs/SCRIPTING.md` — full JS API, smart-object mockups, export formats, Live Messaging.
- `docs/LEARN-REFERENCE.md` — all 45 Photopea features (menu path + script) condensed.

## Design tips
- Warm, on-brand palettes; one accent color; a type ramp (eyebrow → hero → subtitle).
- Match canvas to platform: IG square 1080×1080, story 1080×1920, OG/banner 1200×630.
- Keep text inside safe margins; big hero type can overflow — size down if it clips.
