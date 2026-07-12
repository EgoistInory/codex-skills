---
name: realistic-human-image-qa
description: Use this skill whenever the user asks for realistic human image generation, reference-guided generation, image-to-image/image2 work, photoreal portraits, full-body photos, fashion/editorial people shots, pose-heavy人物生图, reference-image prompt extraction, multi-reference prompt merging, batch multi-image prompt output, or complete copy-paste image prompts with quality and physical-reality checks. Always apply this skill for 写实真人, 真人写真, 参考图生图, 参考生成图片, 图生图, 参考图生图提示词, 真人图片提示词获取, 真人写实生图, 真人写实提示词, 真人写实规则, 真人穿搭, 真人图片反推, 真人图片用途说明, 真人生图创作意图说明, 真人图误判风险, 非露骨表达, 合规时装摄影, 服装展示, 写实人物穿搭, 情绪写真, 泪目感写真, 小红书穿搭图, 反推参考图, image2写实融合, 摄影参数置信度, 成片观感反推, 生图效果评估测试, 手机自拍, 对镜自拍, 手持手机遮脸, 手机机型识别, 关键商品道具强约束, iPhone Pro Max, 多图输出硬性规则, 多图分镜清单, Image 1, Image 2, Image 3, 单次多图输出, 多参考图提示词整合, 多张参考图一次输出多张图片, 真人cos, cosplay, cos生图工作流, 拆解图上身图, 影子预告图, 同套造型连续组图, 角色服装一致性, 人物摆姿势, 人物插入背景, 局部重绘, 手指修复, 二郎腿, 全身照, 半身照, 泳装写真, 海边写真, 完整提示词直接复制, 只输出最终提示词, 不要中间过程, 最终输出要求, GPT网页手机端生图工作流, 面容妆容细节, 发丝层次, 人物肌理, 摄影后期, 滤镜调色, 服装自然, or physical-reality prompt checks.
---

# Realistic Human Image QA Prompting

Use this skill for both prompt extraction and actual reference-guided image generation. Turn the user's request and references into a generation-ready prompt package that actively checks anatomy, pose, contact, clothing, camera logic, and scene physics. The goal is not just to add a long negative prompt; the goal is to help the image model generate a physically plausible person in a physically plausible scene.

## Core workflow

1. Identify the human subject count, framing, pose, clothing, camera angle, and environment.
2. Add positive physical constraints before adding negative keywords. Positive constraints usually work better than only saying what to avoid.
3. Add targeted negative keywords for the risky body regions in the requested pose.
4. Keep negatives specific. Avoid huge generic negative blocks that may suppress normal hands, fabric folds, or body shape.
5. If the user provides a source image, preserve its real-world geometry: viewpoint, floor plane, horizon, light direction, object scale, occlusion order, and contact shadows.
6. When extracting from realistic person references, include face shape, jawline, eyes, gaze, brows, nose bridge, lips, lip color, blush, eye makeup, skin pores, hair layers, hair direction, fabric material, garment fit, pose force, light direction, focal-length feel, composition, depth of field, exposure, color temperature, film/phone feel, filter, color grading, grain, sharpening, and de-AI constraints.
7. If the user provides multiple reference images, first decide whether they want prompt extraction, one merged prompt, or image generation. If the user asks `分别生成 N 条 Final Copy Prompt`, `每张图一条`, `按图分别提取`, or `中间过程和细则都不要`, output one clean copyable text block: start with `【多图输出硬性规则｜最高优先级】`, then add `【语境声明】` only when useful, optional `【统一人物锚点】`, `【统一服装与造型】`, and `【统一场景与摄影风格】` when they improve consistency, then `【Final Copy Prompt 1】` through `【Final Copy Prompt N】`, `【质量约束】`, `【Shared Negative Prompt】`, and `【最终输出要求】`. Do not show `Shared Style Anchor`, `Reference Card`, `Merged Prompt Ingredients`, `Shared Style Enhancer`, `Optional Model Notes`, or one merged prompt unless explicitly requested.
8. Do not leave the user with only categorized fragments. Every useful subject, face/makeup, hair, pose, wardrobe, scene, light, camera, post-production, quality, and negative constraint must be folded into the relevant `Final Copy Prompt`.
9. For batch multi-image output, put shared English negatives once near the end in `【Shared Negative Prompt】`, then add `【最终输出要求】`. Do not repeat identical negatives inside every `Final Copy Prompt N` block.
10. If uploaded image content is unavailable, unsupported, blocked, or visually unreadable, do not invent details. Ask the user to upload JPG, PNG, WEBP, or provide a text description.
11. For platform screenshots or video frames, extract the person, pose, outfit, scene, light, and camera feel, but remove platform UI, subtitles, product bars, buttons, avatars, page counters, watermarks, and screenshot chrome from the generation prompt.
12. For the user's fixed fashion/emotional-portrait extraction workflow, single-image output is `【Final Copy Prompt】`, Chinese `【质量约束】`, and English `【Separate Negative Prompt】`; multi-reference prompt extraction output uses the bracketed multi-image copy block with `【Final Copy Prompt 1】` through `【Final Copy Prompt N】`, `【质量约束】`, `【Shared Negative Prompt】`, and `【最终输出要求】`; storyboard-style one-prompt generation may use `【Image 1】` through `【Image N】` only when the target workflow explicitly expects Image sections.
13. For realistic cosplay workflows, treat the costume flatlay/ground breakdown image and the worn-character image as one continuity set: outfit, wig, headpiece, accessories, embroidery, collar, sleeve shape, exposed-skin structure, color palette, and character motifs must match across the sequence.
14. For reverse-engineering reference images, first infer the image source and final-production traces, then write a prompt that obeys the reference instead of redesigning the person, outfit, scene, or composition.
15. Add a short dynamic `用途说明` or `创作意图说明` only when the current image or prompt has likely misclassification risk: tight clothing, swimwear, hotel, car interior, low neckline, body-detail crop, cosplay, adult portrait styling, or obvious body-line emphasis. Do not add it for ordinary outfit photos, scenery, or product images.
16. Do not use a fixed safety sentence. Write the purpose line from the current image context, such as fashion photography, clothing display, visual analysis, product display, realistic photo style testing, or style reproduction. If the scene is clearly a real person and risk exists, naturally anchor it as adult, compliant fashion photography, non-explicit expression, or objective visual analysis.
17. Keep the purpose line short and outside the `Final Copy Prompt` body so it does not pollute the copyable prompt. Its purpose is to prevent the model from misunderstanding the creative intent, not to bypass policy or force disallowed content.
18. When the user says `纯可复制版`, `直接复制`, `只要提示词`, or `不要解释`, start directly with the requested copy block: `【Final Copy Prompt】` for one image, `【多图输出硬性规则｜最高优先级】` for multi-reference prompt extraction or multi-image output, or the negative prompt block when only negatives are requested. Do not add prefaces, closing offers, Markdown bold headings, or process commentary. Exception: if there is real misclassification risk, a short `【语境声明】` block may appear inside the copy block before the prompt content.
19. Default to Chinese `Final Copy Prompt`, optional Chinese `质量约束`, and English `Separate Negative Prompt`. Only use Chinese negative keywords when the user explicitly targets a Chinese-only model.
20. Treat named products and props as strong constraints. If the user identifies a phone, car, camera, bag, shoes, or other key object, preserve the exact named model, color, body/material finish, logo/text handling, visible layout, hand grip, occlusion, reflection, and scale instead of replacing it with a generic object.
21. For multi-reference prompt extraction or multi-image generation in one prompt, put the image count hard rule at the very beginning and repeat it at the end. Use bracketed headings, no Markdown bold inside the copyable block. Default to `【Final Copy Prompt 1】`, `【Final Copy Prompt 2】`, etc. for the user's GPT web / image2 workflow; use `【Image 1】`, `【Image 2】`, etc. only for storyboard tools or when the user asks for Image sections.
22. Treat prompt extraction, prompt writing, actual image generation, image-to-image/reference-guided generation, and repair/iteration as sibling modes of the same skill. Do not narrow the skill to extraction only.
23. If the user asks to generate or edit the image itself and an image-generation tool is available, use these rules to build and QA the prompt internally, then perform the generation/edit. Do not stop at a prompt-only answer unless the user asks for the prompt text.
24. For both single-image and multi-image prompt delivery, place all model-facing sections inside one `text` code block so the user can copy once. Do not put `【语境声明】`, shared anchors, individual `Final Copy Prompt` sections, quality constraints, and negative prompts into separate code blocks.

## Reference-guided generation and repair mode

When the user supplies one or more references for actual generation, use the same fidelity and physical-reality rules as prompt extraction, but treat the prompt package as an internal generation plan unless the user also requests the text.

- Preserve the visible subject, face, makeup, hair, outfit, pose, scene, camera position, light, post-production feel, and named products according to the requested degree of similarity.
- Apply positive anatomy, contact, fabric, scene-integration, and camera constraints before generation.
- For hand repair, crossed legs, shallow water, background insertion, or complex occlusion, use the pose-specific and repair guidance later in this skill; recommend or use masking, reference pose, OpenPose, Depth, ControlNet, or inpainting when the target workflow supports them.
- If the user requests several generated images, keep shared identity/style anchors and per-image differences separate. Respect the actual image tool's output limits; use separate generation calls when one call cannot return the requested count.
- After generation, inspect the result when the tool or workflow exposes it. Check identity drift, anatomy, hands, clothing structure, contact shadows, reflections, perspective, and reference fidelity before claiming success.

## Template decision: fused single-image, independent multi-image

The user's latest settled workflow is a fusion solution:

- Single reference image: use one fused fashion/portrait template. It combines face, makeup, skin texture, hair, outfit, pose, scene, photography, post-production, and physical-reality constraints into one Chinese `Final Copy Prompt`.
- Emotional portrait: do not treat it as a separate competing template. If the reference has tearful, vulnerable, cool, cinematic, or emotional qualities, add an emotional enhancement module inside the single-image template.
- Multiple reference images: do not use the single-image fusion template to average all images into one prompt unless the user explicitly wants one merged image. Default to a single clean copyable block with `【多图输出硬性规则｜最高优先级】`, optional consistency anchors, `【Final Copy Prompt 1】` through `【Final Copy Prompt N】`, `【质量约束】`, `【Shared Negative Prompt】`, and `【最终输出要求】`.
- Multi-image generation from one prompt: treat the hard-count block as an output-control layer, not as a replacement for the single-image fusion, reverse-engineering, dynamic purpose, photography-confidence, product/prop, or negative-prompt rules. Start with a hard rule that the model must output N independent images, then use optional shared anchors and per-image `Final Copy Prompt N` sections; repeat the count rule at the end.

Tradeoffs and final choice:

- A concise single-image template is stable and easy to copy, but can miss face, makeup, texture, and post-production details.
- A very detailed extraction template improves realism and reference fidelity, but becomes too scattered if pasted as analysis fragments.
- A multi-image merge template is useful for one composite image, but is wrong for batch extraction because it mixes people, outfits, poses, scenes, and composition across references.
- Final rule: single images use the fused bracketed template; multi-reference prompt extraction uses a hard-rule-first copy block with separate `Final Copy Prompt N` sections and no visible cards; one-prompt multi-image generation uses the same count-first control pattern with shared anchors, shared negatives, and a final repeated count rule.

## Multi-reference final-only extraction mode

Use this mode when the user uploads several references and asks to extract prompts, especially with wording like `分别生成7条Final Copy Prompt`, `中间过程和细则都不要`, `按每张图分别输出`, or `只要最终可复制提示词`.

Rules:

- Output one complete Chinese `Final Copy Prompt` per reference image, numbered in the same order as the images: `【Final Copy Prompt 1】`, `【Final Copy Prompt 2】`, etc.
- Each prompt must stand alone. Fold the relevant face, makeup, skin texture, hair, wardrobe, pose, scene, camera, post-production, quality, and physical-reality constraints into that prompt.
- Do not output `Shared Style Anchor`, `Reference Card`, `Merged Prompt Ingredients`, `Shared Style Enhancer`, `Optional Model Notes`, or a single merged `Final Copy Prompt` unless the user explicitly asks for analysis, cards, or one merged image.
- Start with `【多图输出硬性规则｜最高优先级】` and repeat the count rule at `【最终输出要求】`.
- Add `【语境声明】` only when it helps avoid misclassification or clarify legitimate use. Add `【统一人物锚点】`, `【统一服装与造型】`, and `【统一场景与摄影风格】` only when the references share the same person, outfit/styling, scene, or finished-image mood.
- Keep shared negative keywords in one English `【Shared Negative Prompt】` at the end. Add brief per-image negative additions only when a specific image has a unique risk.
- Put all copyable output inside a plain text block when answering in ChatGPT web. Use bracketed headings and no Markdown bold inside that block.

Default extraction format:

```text
【多图输出硬性规则｜最高优先级】
本次任务必须输出 N 张独立图片，不是 1 张。
下方内容是 N 张图片的独立提示词清单，不是一张图的综合描述。
请严格按照【Final Copy Prompt 1】到【Final Copy Prompt N】分别生成。
每个 Final Copy Prompt 对应 1 张完整成图。
禁止宫格、拼图、分屏、上下拼接、左右拼接、海报排版、合成一张。
禁止只输出 1 张。

【语境声明】
[only when useful]

【统一人物锚点】
[only when the references need the same subject identity]

【统一服装与造型】
[only when outfit, makeup, hair, accessories, or props should stay consistent]

【统一场景与摄影风格】
[only when the references share a scene system or finished-image mood]

【Final Copy Prompt 1】
[one complete Chinese prompt for reference image 1]

【Final Copy Prompt 2】
[one complete Chinese prompt for reference image 2]

...

【质量约束】
[shared Chinese realism, anatomy, clothing, prop, contact, light, perspective, and UI-removal constraints]

【Shared Negative Prompt】
[one shared English negative keyword block]

【最终输出要求】
最终必须返回 N 张独立图片，1 个 Final Copy Prompt 对应 1 张。不得缺失，不得合并，不得拼接，不得宫格，不得分屏，不得把多张内容融合成一张图。
```

## Multi-image hard output control

Use this module when the user wants one prompt to produce several independent images in the same generation task. This does not replace the single-image fusion template or reverse-reference rules; it only changes the priority and wording of multi-image count control.

Rules:

- Put `【多图输出硬性规则｜最高优先级】` before any subject, outfit, scene, or style description.
- State the exact count: `本次任务必须输出 N 张独立图片，不是 1 张`.
- State that the following content is an independent prompt list, not a single merged description.
- Use `【Final Copy Prompt 1】`, `【Final Copy Prompt 2】`, `【Final Copy Prompt 3】` headings by default. Use `Image 1..N` only when the user or target tool explicitly asks for Image storyboard labels.
- Separate shared anchors from per-image differences: shared person, makeup, outfit, scene system, photography style, and negative prompt go in unified blocks; each `Final Copy Prompt N` contains the full prompt for that image.
- End with `【最终输出要求】` and repeat that the output must contain N independent images, one Final Copy Prompt per completed picture, with no missing images, collage, grid, split screen, stitching, poster layout, or merged canvas.
- If the target product only supports one image per call, say that text prompts can improve intent clarity but cannot bypass product output limits; the stable workflow is to split the `Final Copy Prompt N` blocks into separate calls or use a model/API with batch `n` support.
- If a model keeps returning only one image, do not keep lengthening a single fused prompt. Split the `Final Copy Prompt N` blocks into separate calls, or use an API/model setting that explicitly supports multiple images.

Default multi-image structure:

```text
【多图输出硬性规则｜最高优先级】
本次任务必须输出 N 张独立图片，不是 1 张。
下方内容是 N 张图片的独立提示词清单，不是一张图的综合描述。
请严格按照【Final Copy Prompt 1】、【Final Copy Prompt 2】、【Final Copy Prompt 3】分别生成。
每个 Final Copy Prompt 对应 1 张完整成图。
禁止宫格、拼图、分屏、上下拼接、左右拼接、海报排版、合成一张。
禁止只输出 1 张。

【可选语境声明】
[only when misclassification risk exists; omit otherwise]

【统一人物锚点】
[shared adult subject, face, makeup, skin texture, hair, body proportion, accessories, temperament]

【统一服装与造型】
[shared clothing structure, material, color, fit, seams, shoes, bag, jewelry, product props, fabric tension]

【统一场景与摄影风格】
[shared space, light direction, color, camera feel, focal-length feel, post-production texture]

【Final Copy Prompt 1】
[aspect ratio/crop, camera angle, pose, expression, hand action, prop relation, scene detail, what to preserve from reference 1]

【Final Copy Prompt 2】
[only the second image's camera angle, pose, expression, hand action, prop relation, crop, and composition changes]

【Final Copy Prompt 3】
[only the third image's independent differences while preserving shared anchors]

【质量约束】
[Chinese realism, anatomy, hand/foot, clothing, material, contact, light, perspective, scene integration, prop fidelity]

【Shared Negative Prompt】
[shared English negative keywords]

【最终输出要求】
最终必须返回 N 张独立图片，1 个 Final Copy Prompt 对应 1 张。不得缺失，不得合并，不得拼接，不得宫格，不得分屏，不得把多张内容融合成一张图。
```

## Reference reverse-engineering and image2 fusion

Use this module when the user asks to `反推参考图`, recover a prompt from a finished image, run image-to-image/image2, or test whether a generated prompt can reproduce the final reference-image look.

Core rule: the prompt must obey the reference image. Do not redesign the person, outfit, pose, scene, or composition. Strengthen realism, face specificity, skin texture, clothing material, human-environment integration, camera/final-image feel, and removal of UI/watermark/screenshot artifacts.

First classify the likely source before writing the prompt:

- phone original photo, phone front-camera selfie, phone rear 1x/2x/3x portrait
- Xiaohongshu/social screenshot, video frame, livestream frame, compressed repost
- e-commerce model photo, studio portrait, post-produced editorial photo
- car-interior shoot, night mixed-light scene, AI derivative or heavily edited image

Photography parameters use confidence tiers:

- High confidence: if EXIF, model watermark, user-provided device info, obvious lens compression, or studio lighting is visible, write concrete or near-concrete device/lens/exposure traits such as phone/camera tendency, focal length, aperture, shutter, ISO, white balance, exposure, composition, light, and color grade.
- Medium confidence: for social images, selfies, platform-compressed photos, and lightly retouched portraits, write visual equivalents such as `接近手机 1x 视角`, `疑似手机人像模式`, `类似 50mm 人像视角`, or `视觉上相当于中焦人像压缩感`.
- Low confidence: for screenshots, strong beauty filters, heavy compression, AI derivative images, liquified/retouched photos, and heavily recolored images, do not invent exact devices or parameters. Only describe camera position, perspective, depth of field, light, color, crop, platform compression, and final-image texture.

Extract final-production traces explicitly when visible: platform compression, video-frame softness, light beauty filter, skin smoothing, sharpening, denoise, color grading, local brightening, skin-tone unification, liquify traces, edge smearing, screenshot crop, time/battery/progress bars, captions, UI chrome, and black borders.

For phone selfies, mirror selfies, and hand-held-phone face-covering references, treat the phone as a primary prop:

- If the model, color, and lens layout are visually clear or supplied by the user, write the exact device and exterior finish, such as `iPhone 17 Pro Max 星宇橙色机型，机身本体为星宇橙色外观，不是橙色手机壳`.
- If only the family or visual tendency is clear, write a confidence-limited phrase such as `疑似 iPhone Pro Max 系列手机，暖橙金属机身外观，注意表现为手机本体颜色，不要生成橙色保护壳`.
- Describe rear camera module shape, lens count and placement, metal frame, body color, case/no-case distinction, logo/text suppression, reflections, finger grip, phone-face occlusion, and scale relative to the hand.
- Do not downgrade a named device to `orange phone case`, `generic smartphone`, or a random model. User-specified product identity overrides weak visual uncertainty unless it conflicts with the visible reference.

Field priority for reverse prompts:

- Face: face shape, eye shape, eye distance, nose bridge/nose tip, lip shape, brow shape, hairline, flyaways, makeup, skin texture, slight asymmetry. Avoid generic phrases like only `漂亮`, `精致`, `白皙`, or `大眼睛`.
- Outfit: structure, material, thickness, elasticity, fit, folds, seams, edges, socks/shoes, bag, jewelry, accessories, and garment tension.
- Pose: center of gravity, shoulders/neck, wrists, fingers, waist/hips, knees, ankles, shoe-sole contact, seated contact, body twist, and occlusion.
- Scene integration: light direction, contact shadows, environmental reflection, subject edge transition, spatial perspective, floor/wall/furniture/car interior/plants/glass material relationships.
- Photography facts: focal-length feel, shooting distance, light ratio, color temperature, exposure, depth of field, composition, sharpness, post-production traces, and final realistic photo texture. Do not rely on vague `cinematic`, `premium`, or `atmospheric` labels without concrete visual facts.

Single-image reverse prompt format:

```text
【Final Copy Prompt】
生图效果评估测试：生成一张[aspect/framing]写实真人照片，不保留任何平台界面、按钮、头像、字幕、时间、电量栏、水印、黑边和截图边框。画面以参考图最终成片观感为准，不重新设计人物、服装、场景和构图，只强化写实质感、人物与环境融合、皮肤肌理、衣物材质和摄影成片细节。[then write subject, face, hair, outfit, pose, scene integration, photography-confidence details, and quality constraints in Chinese]

【质量约束】
[Chinese quality constraints for realism, anatomy, material, contact, light, perspective, post-production, and named product/prop fidelity]

【Separate Negative Prompt】
[English targeted negatives]
```

Multi-image reverse prompt format: if the user asks to extract prompts from several reference images, use the count-first `【Final Copy Prompt 1】`, `【Final Copy Prompt 2】`, etc. format by default. Use `Image 1..N` only when the user or target tool explicitly asks for Image sections.

Self-improving rule: if the current rules are not enough for a special reference type, add a short `本次规则补充：...` outside the final copy block. If the user asks for a pure copyable output, keep the rule supplement outside the prompt body so it does not pollute what they copy into the image model.

## Cos consecutive workflow

Use this module when the user asks for a cos workflow, `拆解图 -> 上身图`, character cosplay prompts, or a continuous Xiaohongshu/Douyin-style cos content sequence.

Default structure:

```text
[角色名] Cos 组图统一设定
[one Chinese paragraph defining the character, adult coser, wig, makeup, costume, accessories, scene style, and the rule that every later image must match the first outfit breakdown image]

【Final Copy Prompt 1（[角色名]·地面服装拆解 / 影子预告图）】
[one complete Chinese prompt for an independent outfit flatlay or ground breakdown image, with sunlight, real floor, luggage/props if useful, and a cast human shadow teaser]

【Final Copy Prompt 2（[角色名]·对应人物上身图）】
[one complete Chinese prompt for the same adult coser wearing the exact same outfit, wig, headpiece, earrings/accessories, embroidery, collar, sleeve shape, color, and exposed-skin structure]

【Final Copy Prompt 3（可选：怼脸 / 自拍 / 动作 / 全身补充成片）】
[one complete Chinese prompt for a same-outfit closeup, selfie, action shot, or full-body continuation]

[角色名] 组 Negative Prompt
[English negative prompt]

统一约束补充
后续每条提示词都只生成 1 张独立完整图片，不要把多张内容合成在一张图里；不要拼图，不要宫格，不要分屏，不要海报排版。若为连续组图，每一张都应是独立成片，但前后在人物、服装、发型、配饰和场景叙事上保持一致性，确保是同一套造型的连续内容。
```

Cos continuity requirements:

- The first image is an outfit breakdown or shadow teaser, not a collage: costume pieces should be laid out clearly on a real floor, with natural sunlight, contact shadows, readable fabric texture, and optional suitcase/room props for lived-in preparation context.
- The second image must be the corresponding worn look. Explicitly say it uses the exact same costume from image 1, not a similar outfit.
- Optional third image keeps the same person, wig, headpiece, accessories, costume, makeup direction, and visual story; it may change crop, action, angle, or distance.
- For named game/anime characters, preserve recognizable cosplay elements as costume/prop details while keeping the image photorealistic adult cosplay, not cartoon rendering.
- Avoid cheap studio cosplay, rough convention snapshot, random fashion approximation, inconsistent wig, missing headpiece, missing tassels/earrings, wrong embroidery, simplified costume, and platform UI.

## Output format

When the user asks for a prompt package rather than direct image generation, return this structure:

```text
Prompt:
[natural-language prompt with subject, pose, anatomy, clothing, environment, light, camera, realism]

Physical Reality Checks:
- [short checklist items tailored to the scene]

Negative Prompt:
[comma-separated targeted negative keywords]

Optional Model Notes:
[only include if useful: aspect ratio, inpainting/masking advice, ControlNet/OpenPose/depth/reference-image guidance]
```

If the user asks for only negative keywords, provide `Negative Prompt` plus a short `Use with` note explaining which pose or body region it targets.

For reference-image prompt extraction in the user's current Chinese GPT workflow, prefer this final-only format over the generic `Prompt / Physical Reality Checks` structure:

```text
【Final Copy Prompt】
[one complete Chinese prompt, directly copyable, no intermediate analysis]

【质量约束】
[Chinese quality constraints when useful]

【Separate Negative Prompt】
[one English negative keyword block]
```

If the reference is a fashion, lifestyle, or emotional portrait of a woman, clearly make the subject a young adult woman or young adult Asian woman when visually appropriate. Do not infer minor age. Preserve the reference's face, makeup, skin texture, hair, outfit, pose, scene, composition, light, and post-production feel as a single fluent Chinese prompt.

For multiple reference images, return cards only if the user asks to see the extraction process or is intentionally running a parallel card workflow. If the user asks to extract prompts or output N final prompts, use the multi-reference final-only extraction mode above with bracketed `Final Copy Prompt N` headings. If the user asks one prompt/task to generate N images, skip visible cards and return the hard-rule multi-image generation structure:

```text
【多图输出硬性规则｜最高优先级】
本次任务必须输出 N 张独立图片，不是 1 张。
下方内容是 N 张图片的独立分镜清单，不是一张图的综合描述。
请严格按照【Final Copy Prompt 1】、【Final Copy Prompt 2】、【Final Copy Prompt 3】分别生成。
每个 Final Copy Prompt 对应 1 张完整成图。
禁止宫格、拼图、分屏、拼接、海报排版、合成一张。
禁止只输出 1 张。

【统一人物锚点】
[consistent subject, face, hair, makeup, body proportion, temperament]

【统一服装与造型】
[consistent wardrobe, materials, shoes, bag, accessories, product props]

【统一场景与摄影风格】
[consistent environment, light, camera feel, color, texture, mood]

【Final Copy Prompt 1】
[image 1-specific crop, pose, action, angle, expression, hand/prop relation, reference details]

【Final Copy Prompt 2】
[image 2-specific crop, pose, action, angle, expression, hand/prop relation, reference details]

【质量约束】
[Chinese realism, anatomy, material, contact, light, perspective, and integration constraints]

【Shared Negative Prompt】
[one shared English negative keyword block, plus per-image additions only when needed]

【最终输出要求】
最终必须返回 N 张独立图片，1 个 Final Copy Prompt 对应 1 张。不得缺失，不得合并，不得拼接，不得宫格，不得分屏，不得把多张内容融合成一张图。
```

For ChatGPT image generation, each `Final Copy Prompt` must be fluent Chinese by default. Do not append a long English tag list to the Chinese prompt body. Translate quality, realism, anatomy, fabric, contact, light, and perspective constraints into natural Chinese. Put English keyword-style negatives such as `bad anatomy`, `extra fingers`, `watermark`, `text`, `logo`, `collage`, `grid`, `split-screen`, and `screenshot UI` only in `Separate Negative Prompt` for models that support a negative field.

When the user asks for prompt extraction and does not explicitly request the analysis process, output only the final usable blocks. Single-image tasks use `【Final Copy Prompt】`, `【质量约束】`, and `【Separate Negative Prompt】`. Multi-reference prompt extraction tasks use the count-first bracketed block with `【Final Copy Prompt 1】` through `【Final Copy Prompt N】`, `【质量约束】`, `【Shared Negative Prompt】`, and `【最终输出要求】`. Keep `Reference Card`, `Merged Prompt Ingredients`, and reasoning internal unless the user asks to see them.

For Chinese multi-reference extraction or one-prompt multi-image generation where the user wants several independent images, use the latest hard-rule headings by default:

```text
【多图输出硬性规则｜最高优先级】
本次任务必须输出 N 张独立图片，不是 1 张。
下方内容是 N 张图片的独立分镜清单，不是一张图的综合描述。
请严格按照【Final Copy Prompt 1】、【Final Copy Prompt 2】、【Final Copy Prompt 3】分别生成。
每个 Final Copy Prompt 对应 1 张完整成图。
禁止宫格、拼图、分屏、拼接、海报排版、合成一张。
禁止只输出 1 张。

【统一人物锚点】
[shared person, face, makeup, hair, body proportion, temperament]

【统一服装与造型】
[shared outfit, fabric, shoes, bag, accessories, product props]

【统一场景与摄影风格】
[shared scene, light, camera feel, color, post-production texture]

【Final Copy Prompt 1】
[image 1-specific crop, pose, camera angle, action, expression, props, reference details]

【Final Copy Prompt 2】
[image 2-specific crop, pose, camera angle, action, expression, props, reference details]

【质量约束】
[shared Chinese quality constraints]

【Shared Negative Prompt】
[shared English negative keywords]

【最终输出要求】
最终必须返回 N 张独立图片，1 个 Final Copy Prompt 对应 1 张。不得缺失，不得合并，不得拼接，不得宫格，不得分屏，不得把多张内容融合成一张图。
```

Use `Image 1..N` and `Batch Generation Note` labels only when the user asks for that exact format or when a non-Chinese model/tooling workflow expects those labels.

Do not copy sensitive identity claims from reference images. Describe visible, non-sensitive visual traits and make the subject an adult when swimwear, lingerie, or sensual styling appears.

## Dynamic purpose statement

Use a dynamic purpose statement only when it reduces likely model
misclassification. It is optional, short, and context-specific.

Add it for risky but legitimate visual contexts:

- tight or body-line-focused fashion
- swimwear, lingerie-like styling, low neckline, or exposed shoulders/back
- hotel, bedroom, bathroom mirror, car interior, or other easily misunderstood
  scenes
- partial body crops, close body-detail framing, or pose-heavy references
- cosplay, adult portrait, editorial fashion, or commercial garment display

Do not add it for ordinary outfits, scenery, product-only images, or clear
non-risky reference extraction.

Write it as one brief Chinese line before the prompt blocks:

```text
用途说明：用于服装展示与写实摄影效果测试，重点呈现穿搭、材质、姿态和光影，保持客观、专业、非露骨表达。
```

Vary the wording for the actual image. Do not paste this exact line by default.
The statement should classify the task into a legitimate context such as
fashion photography, clothing display, visual analysis, product display,
realistic photography testing, or style reproduction. It should not claim to
override safety rules.

## Positive constraints to include

### Whole body anatomy

Use positive wording like:

- anatomically correct adult human body
- natural body proportions
- symmetrical shoulders and hips unless pose requires rotation
- consistent limb thickness from joint to joint
- smooth natural muscle and skin transitions
- visible joints placed correctly at shoulders, elbows, wrists, hips, knees, and ankles
- one continuous spine line, balanced posture, stable center of gravity
- limbs connected to the torso in physically possible positions

For full-body prompts, add:

- both feet placed on the same floor plane unless one foot is intentionally lifted
- correct contact shadows under feet or body
- knees, ankles, and toes aligned with the pose
- no hidden extra limb behind clothing or furniture

### Hands and fingers

Hands need explicit positive structure, especially when holding objects, touching face, crossing arms, or resting on legs.

Use:

- each visible hand has five fingers and one thumb
- natural finger spacing
- fingers bend only at real knuckles
- fingernails aligned with fingertips
- wrist connected cleanly to forearm
- hands follow the same perspective scale as the face and body
- no fingers fused into objects, hair, face, or clothing

For hands near the face:

- fingertips gently touch the cheek without merging into skin
- clear separation between fingers and face
- natural contact shadow where hand touches skin

For hands holding objects:

- fingers wrap around the object with visible grip logic
- object occludes fingers in the correct order
- thumb opposes the fingers naturally

### Crossed legs and seated poses

Crossed-leg and seated poses often fail because the model loses depth order. Add clear geometry.

Use:

- seated pose with pelvis resting naturally on the chair
- one thigh crosses over the other with clear front/back depth
- visible knee joint of the front leg
- lower leg continues naturally from knee to ankle
- calves and ankles do not merge
- fabric compresses slightly at the crossed knee
- chair, seat, and body have correct contact shadows

For legs:

- two legs only
- thighs, knees, calves, ankles, and feet remain distinct
- consistent leg thickness
- no duplicated calves or floating feet
- clear occlusion order where one leg crosses the other

### Clothing and fabric physics

Clothing should obey body shape, gravity, seams, and contact points.

Use:

- clothing follows the underlying body form without melting into skin
- fabric drapes under gravity
- natural folds at elbows, waist, hips, knees, and contact points
- seams and buttons remain aligned with body perspective
- sleeves connect cleanly at shoulders and wrists
- hemline follows the body and pose
- no impossible transparent overlaps unless requested

For tight clothing:

- fabric stretches smoothly over the body
- no random bulges, dents, or uneven limb thickness

For loose clothing:

- folds hang downward consistently
- fabric separates from skin at open edges
- wrinkles respond to sitting, bending, or arm movement

### Background, lighting, and camera logic

For inserted backgrounds or reference environments, emphasize:

- subject matches the background perspective and horizon line
- feet and furniture align to the same floor plane
- body scale matches nearby objects
- light direction matches the environment
- shadow softness and direction match the scene
- correct occlusion between subject, furniture, walls, and props
- reflections only appear where reflective surfaces exist
- lens perspective is consistent across face, torso, limbs, and background

For indoor scenes:

- stable floor contact, wall verticals, furniture scale, realistic room depth

For outdoor scenes:

- natural sun direction, ground contact, atmospheric perspective, realistic wind effect on hair and fabric

### Swimwear, beach, and shallow-water scenes

When the scene includes beaches, pools, shallow water, or swimwear, add both aesthetic and physics constraints:

- adult model, editorial or lifestyle framing, non-explicit pose
- horizon line stays level unless a Dutch angle is requested
- waterline matches the body pose, such as ankle-deep, knee-deep, seated in shallow water, or kneeling in shallow water
- waves wrap around legs or knees without cutting through them
- wet skin and fabric highlights follow the light direction
- swimwear straps, knots, seams, and side ties remain attached and symmetrical in perspective
- fabric is not painted onto skin, does not clip through the torso, and does not create extra body contours
- hair, hat edges, ribbons, and loose fabric respond to the same wind direction

Use prompt language like:

```text
realistic summer beach portrait, shallow ocean water, level horizon, soft natural sunlight, clean blue-and-white color palette, natural skin texture, subtle film grain, subject sharply focused, background softly blurred, realistic water contact around legs, swimwear straps and side ties aligned with body perspective
```

For swimwear or revealing clothing, avoid sexualized wording. Use "adult model", "editorial fashion", "vacation portrait", "natural pose", and "tasteful composition".

### Reference-image prompt decomposition

When extracting prompts from reference images, decompose each image into reusable fields:

- Subject: age category as adult, apparent styling, expression, body orientation, overall temperament.
- Face and makeup: face shape, jawline, forehead proportion, eye shape, gaze direction, brow shape, nose bridge, lip shape, lip color, blush position, eye-makeup intensity, under-eye/aegyo-sal detail, highlight placement, visible pores, skin translucency, natural skin texture.
- Hair: hairstyle, layers, strand direction, hair color, bangs, flyaways, hair accessories, wind or gravity direction.
- Wardrobe: garment type, color, pattern, straps, seams, buttons, lace, denim, satin, knit, leather, accessories, hat, jewelry, shoes, fabric material, fit, drape, garment tension, contact wrinkles.
- Pose and force: standing, side lean, front-facing, kneeling, seated, back-side over-shoulder, hand/object contact, body weight support, limb force direction, floor/chair/prop contact, occlusion order.
- Environment: beach, water depth, room, furniture, floor plane, horizon, foreground/background objects, platform screenshot context only if it affects the crop or framing.
- Light, camera, and composition: light direction, softness, focal-length feel, camera height, crop, framing, composition, depth of field, exposure, color temperature, subject sharpness.
- Texture, mood, and post-production: real skin texture, fabric texture, film grain, phone snapshot feel, vlog/video-frame feel, filter, color grading, bloom, softness, sharpening, editorial/photobook/lifestyle mood.
- Failure prevention: anatomy, hands, face collapse, hair merging, garment structure, floor/water/furniture contact, horizon, water/background deformation, platform UI, subtitle, product bar, watermark/text/logo.

For the user's fashion/emotional-portrait extraction workflow, make sure the final Chinese prompt covers:

- Face: face shape, jawline, facial proportions, eye shape, brow shape, nose bridge, lip shape, expression, temperament.
- Makeup: base makeup, eye makeup, eyelashes, aegyo-sal/under-eye detail, blush, lip color, skin glow.
- Human texture: realistic skin texture, pores, slight imperfections, natural skin color, no over-smoothing.
- Hair: color, length, bangs, curl, volume, flyaways, strand flow, accessories.
- Outfit: top, bottom, dress/skirt, shoes, socks, bag, accessories, material, fit, cut, folds, contact and layering.
- Pose/action: standing, sitting, side body, looking back, chin resting on hand, touching hair, selfie, walking, leaning, hand movement, leg movement.
- Scene: indoor/outdoor space, furniture, windows, walls, floor, plants, props, lived-in details.
- Photography: composition, camera angle, depth of field, light direction, color temperature, exposure, tone, filter, post-production texture, real phone-shot or Xiaohongshu outfit-photo feel.

If the reference carries emotional, tearful, vulnerable, cool, or cinematic feeling, add the emotional portrait enhancement inside the same `Final Copy Prompt`: watery eyes, slightly red outer corners, damp eyelashes, slightly red nose tip, gently pressed lips, restrained emotion, low-saturation tone, soft focus, film grain, shallow depth of field, foreground blur, cinematic light.

### Unsupported or unreadable references

If the image is unsupported, unavailable, or too unclear to inspect, do not fill in imagined face, outfit, pose, or scene details. Reply briefly that the reference cannot be extracted reliably and ask for a JPG, PNG, WEBP, or a short visual description. If only part of the image is readable, extract only visible details and mark the missing detail as unspecified.

### Platform screenshot and video-frame cleanup

For 小红书, 抖音, TikTok, Instagram, video screenshots, livestream frames, product pages, or phone screenshots, preserve the useful photographic content but strip app UI from the final prompt. Do not ask the model to recreate subtitles, usernames, avatars, product bars, buttons, page indicators, screenshot borders, watermarks, logos, or interface text. Add these risks to the English negative prompt when relevant:

```text
subtitle, caption text, social media UI, platform UI, product bar, app buttons, username, avatar, page indicator, screenshot border, watermark, text, logo
```

For a set of references, preserve consistent style anchors and vary only pose/framing details. A useful shared style tail is:

```text
高清写实摄影质感，真实皮肤纹理，柔和自然光，浅景深，轻微胶片颗粒，构图干净，主体清晰锐利，背景自然虚化，光影细腻，具有高级人像摄影质感，画面中不要出现水印、文字或 logo。
```

## Multi-reference integration workflow

Use this workflow when the user uploads several reference photos or says they want to run several GPT conversations in parallel and combine the results.

1. In each reference-image conversation, ask GPT to output only a `Reference Card` when the user is intentionally running a parallel extraction workflow. For ordinary "提取提示词" requests, skip visible cards and return final copy blocks directly.
2. Each `Reference Card` must identify the image's role in the final prompt: style, subject, pose, wardrobe, background, camera, lighting, or failure-prevention.
3. Decide the output mode:
   - Single final image: merge cards by separating shared anchors from conflicting details, then return one `Final Copy Prompt`.
   - Multi-reference prompt extraction: return the count-first copyable block with `【Final Copy Prompt 1】`, `【Final Copy Prompt 2】`, etc., no visible cards or merge analysis, plus `【质量约束】`, one shared English `【Shared Negative Prompt】`, and `【最终输出要求】`.
   - One-prompt multi-image generation: use the multi-image hard output control structure with `【多图输出硬性规则｜最高优先级】`, optional shared anchors, per-image `Final Copy Prompt N` sections by default, one shared negative prompt, and a final repeated output requirement.
4. Deduplicate negative prompts. If the images share the same failure risks, output one shared `Separate Negative Prompt` at the end instead of repeating it after each prompt.
5. Add per-image negative additions only when a specific image has a unique risk, such as holding objects, mirror selfies, crossed legs, shallow water, back-side over-shoulder poses, complex skirts, reflective surfaces, or strong occlusion.
6. Put the count hard rule before all multi-reference extraction or multi-image output content and repeat it after the final negative prompt block. This is an output-control layer; it does not replace per-image prompt detail.

Use this `Reference Card` schema for each parallel extraction:

```text
Reference Card:
- Role in final image:
- Subject and visible styling:
- Wardrobe, props, and accessories:
- Pose, contact, and body geometry:
- Scene, lighting, camera, and texture:
- Must-preserve details:
- Failure risks:
- Reusable phrase:
```

Use this final copy format for multi-reference prompt extraction and one-prompt multi-image generation by default.

```text
【多图输出硬性规则｜最高优先级】
本次任务必须输出 2 张独立图片，不是 1 张。
下方内容是 2 张图片的独立分镜清单，不是一张图的综合描述。
请严格按照【Final Copy Prompt 1】、【Final Copy Prompt 2】分别生成。
每个 Final Copy Prompt 对应 1 张完整成图。
禁止宫格、拼图、分屏、拼接、海报排版、合成一张。
禁止只输出 1 张。

【统一人物锚点】
[shared subject, face, hair, makeup, body proportion, temperament]

【统一服装与造型】
[shared outfit, fabric, shoes, bag, accessories, product props]

【统一场景与摄影风格】
[shared scene, light, camera, color, post-production texture]

【Final Copy Prompt 1】
[first image crop, pose, camera angle, expression, hand/prop relation, scene details, reference-specific details]

【Final Copy Prompt 2】
[second image crop, pose, camera angle, expression, hand/prop relation, scene details, reference-specific details]

【质量约束】
[shared Chinese realism, anatomy, clothing, prop, contact, light, perspective, and UI-removal constraints]

【Shared Negative Prompt】
bad anatomy, extra fingers, missing fingers, extra limbs, bad legs, floating feet, distorted clothing, wrong perspective, no contact shadow, AI artifacts, subtitle, caption text, social media UI, platform UI, product bar, app buttons, watermark, text, logo, collage, grid, split-screen, screenshot UI

【最终输出要求】
最终必须返回 2 张独立图片，1 个 Final Copy Prompt 对应 1 张。不得缺失，不得合并，不得拼接，不得宫格，不得分屏，不得把多张内容融合成一张图。
```

Use this language split by default:

- `Final Copy Prompt`: all Chinese, polished and directly readable as one photography instruction for GPT image generation.
- `Separate Negative Prompt`: English keyword list for Midjourney, SDXL, Civitai, LoRA, or any model with a negative prompt field.
- `Batch Generation Note`: legacy label only when a tool expects it; otherwise use the hard-rule first/final structure for multi-image generation.
- `Optional Model Notes`: may keep technical terms such as `35mm`, `4K`, `HDR`, `OpenPose`, `Depth`, `ControlNet`, `--ar`, and `--style raw` when they are model controls, not prose style tags.

## Targeted negative prompt blocks

Use only the blocks that match the scene. Combine them into one comma-separated negative prompt.

### General realistic human negatives

```text
bad anatomy, anatomically impossible body, deformed body, distorted body proportions, inconsistent limb thickness, asymmetrical limbs, broken joints, misplaced joints, dislocated shoulders, twisted torso, warped spine, floating limbs, extra limbs, missing limbs, duplicated body parts, fused body parts, melted skin, unnatural skin folds, lumpy body, uneven silhouette
```

### Hands and fingers

```text
bad hands, deformed hands, malformed hands, extra fingers, missing fingers, fused fingers, webbed fingers, duplicated fingers, broken fingers, twisted fingers, overlapping fingers, fingers merging into skin, fingers merging into objects, wrong number of fingers, unnatural knuckles, misplaced thumb, extra thumb, missing thumb, distorted fingernails, claw hands, oversized hands, tiny hands, disconnected wrist
```

### Arms and shoulders

```text
extra arms, missing arms, fused arms, broken arms, twisted forearms, unnatural elbow bend, dislocated elbow, dislocated shoulder, uneven arm length, arms merging with torso, hands emerging from sleeves incorrectly, sleeve fused to skin
```

### Legs, crossed legs, and seated pose

```text
bad legs, extra legs, missing legs, duplicated legs, fused legs, crossed legs merging, unclear leg occlusion, broken knees, twisted knees, misplaced knee joint, disconnected ankle, duplicated calves, missing feet, floating feet, feet not touching ground, impossible seated pose, pelvis floating above chair, legs melting into chair, unnatural thigh overlap, uneven leg thickness
```

### Feet

```text
bad feet, deformed feet, extra toes, missing toes, twisted ankles, backwards feet, feet fused with shoes, shoes fused with floor, floating shoes, mismatched shoe perspective
```

### Clothing

```text
bad clothing, melted clothing, clothing fused to skin, impossible fabric, broken seams, misaligned buttons, warped collar, sleeves merging with arms, duplicated sleeves, missing sleeve openings, fabric floating without support, unnatural folds, random bulges, uneven waistline, distorted hemline, clothing clipping through body, clothing clipping through chair
```

### Swimwear and tight garments

```text
swimwear structure errors, broken bikini straps, duplicated straps, missing straps, misaligned side ties, straps floating off body, straps fused to skin, swimsuit clipping through body, swimsuit painted on skin, wrong garment tension, uneven garment edges, distorted waistline, fabric creating extra body contours, oversexualized pose, vulgar pose
```

### Face, hair, and accessories

```text
asymmetrical face, distorted face, misplaced eyes, extra teeth, melted lips, hair fused with face, hair fused with fingers, earrings fused to skin, glasses fused to face, accessories floating, accessories merging with clothing
```

### Phones and named product props

```text
wrong phone model, orange phone case, generic smartphone, incorrect camera layout, wrong lens placement, deformed phone, melted phone edges, fake phone case, inaccurate iPhone body color, wrong product color, wrong product model, generic product, distorted logo, readable logo text, distorted reflection, bad hand grip, fingers fused with phone, phone fused with face
```

### Cosplay continuity and costume accuracy

```text
wrong character design, inaccurate cosplay costume, inconsistent outfit, inconsistent wig, inconsistent headpiece, missing accessories, missing hat, missing tassels, missing earrings, inaccurate embroidery, wrong costume pattern, simplified costume, low detail fabric, messy costume details, costume fused to skin, wig fused with face, headpiece floating, accessories floating, cheap studio cosplay, rough convention snapshot, cartoon rendering, chibi style, comic style
```

### Environment insertion and physical logic

```text
wrong perspective, inconsistent perspective, mismatched horizon line, incorrect scale, subject too large for background, subject too small for background, floating subject, no contact shadow, inconsistent shadows, wrong light direction, mismatched lighting, inconsistent reflections, impossible occlusion, body clipping through furniture, feet clipping through floor, props merging with body, background warping around subject
```

### Beach, water, and horizon

```text
tilted horizon, warped horizon, fake beach background, distorted waves, water cutting through legs, waterline inconsistent with pose, waves merging with body, legs disappearing into water, incorrect reflection, overexposed water, oversaturated sky, background deformation, coastline warped around subject
```

### Image-quality artifacts

```text
low quality, low resolution, blurry anatomy, blurry face, face collapse, motion-smudged fingers, warped edges, uneven linework, melted details, duplicated contours, jagged silhouette, over-smoothed skin, plastic skin, waxy skin, mannequin look, uncanny realism, generic influencer face, same face syndrome, doll face, excessive beauty filter, AI artifacts, overexposed, oversaturated, harsh HDR, muddy shadows, oily lighting, over-sharpened, heavy noise, platform compression artifacts, jpeg artifacts, watermark, text, logo, subtitle, caption text, social media watermark, social media UI, platform UI, product bar, app buttons, username, avatar, page indicator, screenshot border, time bar, battery icon, progress bar, collage, grid, split-screen, screenshot UI, platform UI, buttons
```

## Pose-specific recipes

### Standing full-body portrait

Add:

```text
full-body realistic photograph, balanced standing posture, shoulders and hips aligned naturally, arms relaxed with clear separation from torso, both legs visible, knees and ankles aligned, feet planted on the same floor plane, realistic contact shadows
```

Negative emphasis:

```text
extra legs, missing legs, uneven limb thickness, floating feet, no contact shadow, disconnected wrist, oversized hands
```

### Seated crossed-leg fashion photo

Add:

```text
realistic seated fashion photograph, pelvis naturally supported by the chair, one leg crossed over the other with clear front/back occlusion, visible knee and ankle structure, fabric compressed at the crossed knee, natural chair contact shadows
```

Negative emphasis:

```text
crossed legs merging, unclear leg occlusion, duplicated calves, broken knees, pelvis floating above chair, legs melting into chair, clothing clipping through chair
```

### Hand near face portrait

Add:

```text
realistic portrait, hand gently touching the face, five fingers visible where not occluded, natural finger spacing, fingers bend at real knuckles, clear separation between fingertips and skin, subtle contact shadow
```

Negative emphasis:

```text
extra fingers, fused fingers, fingers merging into skin, misplaced thumb, unnatural knuckles, claw hands, oversized hands
```

### Holding an object

Add:

```text
hand holding the object with realistic grip, thumb opposing the fingers, object and fingers have correct occlusion order, wrist aligned with forearm, object scale matches the hand
```

Negative emphasis:

```text
fingers merging into objects, object fused to hand, impossible grip, missing thumb, extra fingers, mismatched object scale
```

### Side lean and over-shoulder pose

Add:

```text
realistic side-leaning portrait, torso bends naturally from the waist, neck rotation remains within a natural range, shoulder line follows the turn, one hand gently holds hair or clothing with clear finger separation, subject looks back toward camera, waist and hip thickness stay consistent
```

Negative emphasis:

```text
twisted neck, broken torso, impossible waist bend, shoulder deformation, hair fused with fingers, hand fused with hair, distorted back line, uneven waist thickness
```

### Kneeling in shallow water

Add:

```text
realistic kneeling pose in shallow water, knees supported by the ground beneath the water, water ripples wrap around knees and thighs, pelvis and torso balanced naturally, hands have clear contact with hair or clothing, swimwear follows the seated/kneeling body shape
```

Negative emphasis:

```text
missing knees, broken knees, legs disappearing into water, water cutting through thighs, floating pelvis, arms merging with torso, hand and braid fused together, swimwear clipping through body
```

### Back-side over-shoulder portrait

Add:

```text
realistic back-side over-shoulder pose, back line and shoulder blades remain natural, head turns gently toward camera, neck rotation is plausible, hair falls behind the back with wind direction, hands remain partially visible and anatomically connected
```

Negative emphasis:

```text
broken back, distorted shoulder blades, twisted neck, face unclear, eyes misaligned, hair fused with back, extra arm behind torso, flattened body depth
```

## Reference-image or background insertion guidance

When the user inserts a person into an image/background, add this checklist:

- Match the subject to the reference image camera height and focal length.
- Align the feet, chair, or body contact points to the environment floor plane.
- Match the light direction, color temperature, and shadow softness.
- Preserve correct occlusion order: foreground objects cover the subject only where physically in front.
- Match grain, sharpness, depth of field, and contrast to the background.
- Keep body scale consistent with doors, chairs, tables, cars, stairs, and other known-size objects.

Use this prompt language:

```text
integrated naturally into the scene, matching the background perspective, horizon line, focal length, lighting direction, color temperature, shadow softness, ground contact, object scale, occlusion order, grain, sharpness, and depth of field
```

Negative prompt:

```text
cutout look, pasted-on subject, cutout feeling, mismatched perspective, mismatched lighting, no contact shadow, missing contact shadow, wrong scale, incorrect occlusion, subject clipping through background objects, background warped around subject, inconsistent shadow direction, unnatural reflection, broken depth, fake background, poor integration
```

## Optional model notes

For pose-heavy prompts, recommend structure over only text:

- Use a pose/reference image, OpenPose, depth, or lineart control when available.
- For hand repair, mask only the hand and wrist area, keep denoise moderate, and describe exact finger count and grip/contact.
- For crossed legs, use a depth/reference pose because text-only prompts often lose front/back leg order.
- For shallow-water or kneeling poses, use a depth/reference image because water often hides knees, calves, and foot contact.
- Generate at a resolution and aspect ratio that gives hands and feet enough pixels; tiny hands in a full-body shot are more likely to break.
- If the model repeatedly fails, simplify the pose, generate the body first, then inpaint hands or clothing separately.
- If using Midjourney-style syntax and the target model supports these flags, portrait photos usually work well with `--ar 2:3 --style raw --s 100` or `--ar 3:4 --style raw --s 100`; increase stylization only when anatomy remains stable.

## Quality bar

Before returning a prompt, check whether it answers these:

- How many people are present?
- Which limbs are visible and which are intentionally occluded?
- What is touching what?
- Where are the shadows?
- Which object is in front when body parts overlap?
- How does clothing respond to the pose?
- Does the camera perspective match the background?
- Are face, makeup, hair, skin texture, fabric material, and garment fit described beyond generic beauty words?
- Are the light direction, focal-length feel, crop, exposure, color temperature, filter, color grading, grain, and sharpening/de-AI constraints clear?
- If the source is a screenshot or video frame, have UI, subtitles, buttons, product bars, watermarks, and logos been excluded?
- For cos workflows, do the outfit breakdown and worn-character prompts preserve the same costume, wig, headpiece, accessories, embroidery, collar, sleeve shape, exposed-skin structure, color palette, and character motifs?
- For reverse-reference/image2 workflows, did you classify source type, apply photography-parameter confidence, avoid invented exact camera data, extract post-production/platform traces, keep named products/props accurate, and keep the prompt obedient to the reference rather than redesigning it?

If any answer is missing and the image depends on it, add a short constraint to the prompt rather than asking the user unless the missing detail changes the creative direction.
