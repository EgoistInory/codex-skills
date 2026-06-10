---
name: realistic-human-image-qa
description: Use this skill whenever the user asks for realistic human image generation, photoreal portraits, full-body photos, fashion/editorial people shots, pose-heavy人物生图, reference-image prompt extraction, multi-reference prompt merging, batch multi-image prompt output, or wants complete copy-paste image prompts with positive prompts, negative prompts, quality constraints, and physical-reality checks. Always apply this skill for 写实真人, 真人写真, 人物摆姿势, 参考图生图提示词, 多参考图提示词整合, 多张参考图一次输出多张图片, 完整提示词直接复制, 只输出最终提示词, 不要中间过程, GPT网页手机端生图工作流, 面容妆容细节, 发丝层次, 人物肌理, 摄影后期, 滤镜调色, 手指修复, 二郎腿, 全身照, 半身照, 泳装写真, 海边写真, 服装自然, or physical-reality prompt checks.
---

# Realistic Human Image QA Prompting

Use this skill to turn a user request for realistic human image generation into a prompt package that actively checks anatomy, pose, contact, clothing, camera logic, and scene physics. The goal is not just to add a long negative prompt; the goal is to make the image model understand a physically plausible person in a physically plausible scene.

## Core workflow

1. Identify the human subject count, framing, pose, clothing, camera angle, and environment.
2. Add positive physical constraints before adding negative keywords. Positive constraints usually work better than only saying what to avoid.
3. Add targeted negative keywords for the risky body regions in the requested pose.
4. Keep negatives specific. Avoid huge generic negative blocks that may suppress normal hands, fabric folds, or body shape.
5. If the user provides a source image, preserve its real-world geometry: viewpoint, floor plane, horizon, light direction, object scale, occlusion order, and contact shadows.
6. When extracting from realistic person references, include face shape, jawline, eyes, gaze, brows, nose bridge, lips, lip color, blush, eye makeup, skin pores, hair layers, hair direction, fabric material, garment fit, pose force, light direction, focal-length feel, composition, depth of field, exposure, color temperature, film/phone feel, filter, color grading, grain, sharpening, and de-AI constraints.
7. If the user provides multiple reference images, extract a compact `Reference Card` for each image only when the user asks for cards or parallel extraction. If the user asks to "提取提示词", "分别生成 Final Copy Prompt", or "不要中间过程", default to final-only output: `Final Copy Prompt 1..N`, one shared `Separate Negative Prompt`, then `Batch Generation Note`.
8. Do not leave the user with only categorized fragments. Every useful subject, face/makeup, hair, pose, wardrobe, scene, light, camera, post-production, quality, and negative constraint must be folded into the relevant `Final Copy Prompt`.
9. For batch multi-image output, put shared English negatives once at the end in `Separate Negative Prompt`, then add `Batch Generation Note`. Do not repeat identical negatives after every prompt.
10. If uploaded image content is unavailable, unsupported, blocked, or visually unreadable, do not invent details. Ask the user to upload JPG, PNG, WEBP, or provide a text description.
11. For platform screenshots or video frames, extract the person, pose, outfit, scene, light, and camera feel, but remove platform UI, subtitles, product bars, buttons, avatars, page counters, watermarks, and screenshot chrome from the generation prompt.

## Output format

When the user asks for a prompt, return this structure:

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

For multiple reference images, return:

```text
Shared Style Anchor:
[consistent subject, wardrobe, environment, color, camera, texture, mood]

Reference 1:
- Role in final image: [style / pose / wardrobe / background / composition / mood]
- Positive traits to reuse: [subject, pose, clothing, scene, light, camera, texture]
- Risk points to prevent: [hands, joints, clothing, horizon, water, background, artifacts]
- Reusable phrase: [one concise phrase that can be merged into the final prompt]

Reference 2:
...

Merged Prompt Ingredients:
- Subject and identity-safe visible traits: [...]
- Wardrobe and props: [...]
- Pose and composition: [...]
- Scene and camera: [...]
- Quality and realism constraints: [...]
- Negative constraints: [...]

Shared Style Enhancer:
[short reusable style tail, folded into every Final Copy Prompt rather than left as a separate copy block]

Optional Model Notes:
[aspect ratio, Midjourney-style flags if supported, reference/pose/depth guidance; omit in batch mode unless essential]

Final Copy Prompt 1:
```text
[one complete Chinese prompt for image 1]
```

Final Copy Prompt 2:
```text
[one complete Chinese prompt for image 2]
```

...

Separate Negative Prompt:
[one shared English comma-separated negative prompt if the images share the same risk profile]

Per-Image Negative Additions:
[only include when a specific prompt has unique risks such as holding objects, mirror selfies, crossed legs, shallow water, over-shoulder pose, or complex skirts]

Batch Generation Note:
[Chinese instruction to generate the same number of independent images as the Final Copy Prompts]
```

For ChatGPT image generation, each `Final Copy Prompt` must be fluent Chinese by default. Do not append a long English tag list to the Chinese prompt body. Translate quality, realism, anatomy, fabric, contact, light, and perspective constraints into natural Chinese. Put English keyword-style negatives such as `bad anatomy`, `extra fingers`, `watermark`, `text`, `logo`, `collage`, `grid`, `split-screen`, and `screenshot UI` only in `Separate Negative Prompt` for models that support a negative field.

When the user asks for prompt extraction and does not explicitly request the analysis process, output only the final usable blocks: `Final Copy Prompt`, optional numbered `Final Copy Prompt 1..N`, `Separate Negative Prompt`, optional `Per-Image Negative Additions`, and optional `Batch Generation Note`. Keep `Reference Card`, `Merged Prompt Ingredients`, and reasoning internal unless the user asks to see them.

Do not copy sensitive identity claims from reference images. Describe visible, non-sensitive visual traits and make the subject an adult when swimwear, lingerie, or sensual styling appears.

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
   - Batch multi-image output: return one `Final Copy Prompt` per reference image, numbered `Final Copy Prompt 1`, `Final Copy Prompt 2`, etc.
4. Deduplicate negative prompts. If the images share the same failure risks, output one shared `Separate Negative Prompt` at the end instead of repeating it after each prompt.
5. Add per-image negative additions only when a specific image has a unique risk, such as holding objects, mirror selfies, crossed legs, shallow water, back-side over-shoulder poses, complex skirts, reflective surfaces, or strong occlusion.
6. Put `Batch Generation Note` after the final negative prompt block, not inside each prompt. It must be the last output block in batch mode and ask the model to generate the same number of independent images as the number of `Final Copy Prompt` blocks.

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

Use this final copy format:

```text
Final Copy Prompt 1:
生成一张[目标画面]，融合这些参考图方向：[共同风格、主体、场景]。保留[必须保留的细节]。画面采用[姿势、构图、镜头、光线]。保持写实成人真人质感：[人体结构、手部、服装受力、身体或脚底接触、阴影、透视、背景或水面/地面/家具关系]。避免[中文化后的主要失败点]。[中文画质和风格增强语句]。

Final Copy Prompt 2:
生成一张[第二张参考图对应的目标画面]，保留[第二张图的独有姿势、穿搭、构图或场景]，同时延续共同风格锚点。保持写实成人真人质感和真实物理逻辑。避免[第二张图的中文化主要失败点]。

Separate Negative Prompt:
bad anatomy, extra fingers, missing fingers, extra limbs, bad legs, floating feet, distorted clothing, wrong perspective, no contact shadow, AI artifacts, subtitle, caption text, social media UI, platform UI, product bar, app buttons, watermark, text, logo, collage, grid, split-screen, screenshot UI

Batch Generation Note:
请一次性生成与 Final Copy Prompt 数量对应的独立图片；例如有 2 条提示词就生成 2 张独立图片。不要宫格，不要拼图，不要多图合成在一张图里，不要保留平台截图界面、按钮、文字或水印。
```

Use this language split by default:

- `Final Copy Prompt`: all Chinese, polished and directly readable as one photography instruction for GPT image generation.
- `Separate Negative Prompt`: English keyword list for Midjourney, SDXL, Civitai, LoRA, or any model with a negative prompt field.
- `Batch Generation Note`: Chinese batch-output instruction, only when there are two or more `Final Copy Prompt` blocks.
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
low quality, low resolution, blurry anatomy, blurry face, face collapse, motion-smudged fingers, warped edges, uneven linework, melted details, duplicated contours, jagged silhouette, over-smoothed skin, plastic skin, mannequin look, uncanny realism, AI artifacts, overexposed, oversaturated, oily lighting, over-sharpened, heavy noise, watermark, text, logo, subtitle, caption text, social media watermark, social media UI, platform UI, product bar, app buttons, username, avatar, page indicator, screenshot border, collage, grid, split-screen, screenshot UI, platform UI, buttons
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
cutout look, pasted-on subject, mismatched perspective, mismatched lighting, no contact shadow, wrong scale, incorrect occlusion, subject clipping through background objects, background warped around subject
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

If any answer is missing and the image depends on it, add a short constraint to the prompt rather than asking the user unless the missing detail changes the creative direction.
