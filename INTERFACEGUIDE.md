<p align="left">
    <img width="110" src="https://github.com/MilesCoMEdia/PiCam/blob/a43414c283be9498c1f7eb952dc2a7d07228a778/CONNECTLGOICON.png" alt="PiCamConnect Logo">
</p> 

## PiCam Connect Design & Copy Guidelines

### 1. Voice & Tone

Clean, direct, user-focused—modeled on Apple’s style:

* **Use**: “Frame your shot. Tap to capture.”
* **Not**: “You should go ahead and tap here to take a photo.”
* Use **sentence case** for labels/alerts (e.g., “Save image”), per Apple HIG **Typography & Writing**.
* Address the user as **“you”**: “You can adjust brightness.” Avoid passive voice.

> [!NOTE]
> Keep tone polished and aspirational, yet simple—see Apple HIG **Writing** in **bold**: [developer.apple.com][1].

---

### 2. Copywriting Examples

| Element         | ✅ Apple‑style                 | ❌ Avoid                                                                       |
| --------------- | ----------------------------- | ----------------------------------------------------------------------------- |
| **Button**      | “Connect to Device”           | “Click here to connect your PiCam”                                            |
| **Alert**       | “Connection lost. Reconnect?” | “Oops! You've lost connection. Please reconnect.”                             |
| **Instruction** | “Place camera within frame.”  | “You should place the camera so it fits inside the frame before you proceed.” |
| **Error**       | “Failed to save image.”       | “Image saving failed due to an unknown error.”                                |

* Buttons: **3–5 words max**.
* Alerts: **start with action** (“Reconnect?” not “You must reconnect”).
* Avoid jargon like “BLE” or “payload” unless contextually clear.

---

### 3. Typography

> [!IMPORTANT]
> Use **San Francisco** (Apple system font) per Apple HIG **Typography**. [developer.apple.com][2], [msc-kobol-public-prod.apple.com][3]

| Context              | Font Variant    | Size (pt) | Weight       |
| -------------------- | --------------- | --------- | ------------ |
| Navigation titles    | SF Display      | 20–28     | Semibold     |
| Section headers      | SF Display      | 17–22     | Medium       |
| Body / labels        | SF Text         | 15        | Regular      |
| Button labels        | SF Text/Display | 17        | Semibold     |
| Secondary info       | SF Text         | 13        | Regular      |
| Footnotes / captions | SF Text         | 11 (min)  | Thin/Regular |

> [!CAUTION]
> Do **not** go below 11 pt body text—minimum for readability. [median.co][4]

> [!NOTE]
> Use **Dynamic Type** (Body, Headline, Title) so text scales with system accessibility settings. [codershigh.github.io][5], [msc-kobol-public-prod.apple.com][3]

* Avoid manual kerning; use SF’s optical tracking. [developer.apple.com][2]

---

### 4. Layout & Spacing

* Prioritize **white space, hierarchy, and minimal clutter**. [encyclopedia.design][6], [docs.developer.apple.com][7]
* Standard margins: **16 pt** (iPhone), **20 pt** (iPad).
* Spacing between elements: at least **8 pt**.
* Touch targets: at least **44×44 pt**.
* Equal spacing enhances harmony.
* Prefer to left align content for compatibility with iOS 26.

> [!CAUTION]
>  Don’t overcrowd screens—if too dense, **split into steps/screens**.

> [!NOTE]
> For layout systems and spacing recommendations, see Apple HIG **Layout & Organization**: [docs.developer.apple.com][7], [developer.apple.com][8]

---

### 5. Icons (SF Symbols)

* Use **SF Symbols** for native consistency. [developer.apple.com][9], [app.uxcel.com][10]
* Sizes: typically **17×17 pt** (body), **20×20 pt** (titles/toolbars).
* Use single-color glyphs; rely on system tint.
* Don’t recolor or alter shapes that conflict with system usage.

> [!NOTE]
>  SF Symbols align with San Francisco type and accessibility settings. [developer.apple.com][9], [developer.apple.com][11]

---

### 6. Color & Contrast

* Use a **neutral palette**: white, light gray, dark gray, and **system blue** accents.
* Ensure text contrast ratio ≥ 4.5:1 per WCAG and Apple HIG. ([encyclopedia.design][6], [docs.developer.apple.com][12])
* Use system colors (`systemBlue`, `label`, `secondaryLabel`) to support light/dark mode.

> [!CAUTION]
>  Avoid low-contrast text like light gray on white—these fail accessibility and appear weak.

---

### 7. Logo & App Icon

* App icon should be:

  * Simple and meaningful (camera/lens motif).
  * Flat, without gradients or shadows.
  * Centered and legible at **60×60 pt** icon size.
* Provide all required sizes:

  * App Store: **1024×1024 px**
  * iPhone: **180×180 pt**
  * iPad: **167×167 pt**

> [!NOTE]
> Follow Apple HIG **App Icon** guidance: [developer.apple.com][13], [devimages-cdn.apple.com][14]

---

### 8. What *Not* to Include

> [!TIP]
> Never include emojis in UI copy or labels, as this can lead to un-necessary distractions that may shift focus away from the main content.
* No unnecessary explanations—keep copy minimal.
* Avoid technical jargon ("API", "WS", "payload").
* Skip marketing fluff like “ultimate experience” unless clearly justified.

---

### 9. Privacy

People expect apps to protect their privacy. You must disclose your privacy practices and any data collected in the App Store listing, and minimize data collection. ([developer.apple.com][1])
###  Key Principles

1. **Transparency**

   * Clearly disclose *what* personal data you collect and *why*.
   * Only request **required permissions** when they are essential for functionality.

2. **Permission Prompts**

   * Trigger only *when needed*, not at launch.
   * Provide **pre‑permission context** explaining why access is needed (e.g. camera, location).

3. **Minimal Data Collection & Use**

   * Collect only the data necessary for core features.
   * Avoid gathering sensitive data in the background.

4. **Data Handling & Retention**

   * Use secure transport (HTTPS) and encrypt data at rest.
   * Store data only as long as needed; provide user ability to delete.

5. **Privacy in App Store**

   * Supply accurate **Privacy Nutrition Labels** (iOS 14+).
   * Ensure labels reflect types of data: *tracking*, *linked*, or *not linked*.

---
> [!NOTE]
> Refer to Apple HIG - Privacy for more information **[https://developer.apple.com/design/human-interface-guidelines/privacy/](https://developer.apple.com/design/human-interface-guidelines/privacy/)** ([developer.apple.com][1])

### 📋 Summary Table

| Guideline                    | Description                                                               |
| ---------------------------- | ------------------------------------------------------------------------- |
| **Transparency**             | Clearly state what is collected and why                                   |
| **Permission Timing**        | Request only when necessary, with context prior to prompt                 |
| **Minimize Data Use**        | Restrict collection to data essential for app functionality               |
| **Secure & Limit Retention** | Encrypt in transit/storage; keep data only as long as users need it       |
| **App Store Labels**         | Include accurate Privacy Nutrition Labels—tracking, linked, unlinked data |

> [!TIP]
> Do **not** collect data just to boost analytics—this can lead to **App Store rejection**.

> [!IMPORTANT]
> Always include **purpose strings** in your `Info.plist` (e.g. `NSCameraUsageDescription`), as required by Apple at permission prompts.

___ 

### 10. Reference to Apple HIG

Use the following notes throughout the guide for context:

> [!TIP]
> See Apple HIG – **Writing**: **[https://developer.apple.com/design/human-interface-guidelines/writing/](https://developer.apple.com/design/human-interface-guidelines/writing/)**

> [!TIP]
> See Apple HIG – **Typography**: **[https://developer.apple.com/design/human-interface-guidelines/typography/](https://developer.apple.com/design/human-interface-guidelines/typography/)**

> [!TIP]
> See Apple HIG – **Layout & Organization**: **[https://developer.apple.com/design/human-interface-guidelines/layout-and-organization/](https://developer.apple.com/design/human-interface-guidelines/layout-and-organization/)**

> [!TIP]
> See Apple HIG – **SF Symbols** and icons: **[https://developer.apple.com/design/human-interface-guidelines/sf-symbols/](https://developer.apple.com/design/human-interface-guidelines/sf-symbols/)**

---


[1]: https://developer.apple.com/design/human-interface-guidelines/writing?utm_source=chatgpt.com "Writing | Apple Developer Documentation"
[2]: https://developer.apple.com/design/human-interface-guidelines/typography?utm_source=chatgpt.com "Typography | Apple Developer Documentation"
[3]: https://msc-kobol-public-prod.apple.com/design/Human-Interface-Guidelines/typography?utm_source=chatgpt.com "Typography | Apple Developer Documentation"
[4]: https://median.co/blog/apples-ui-dos-and-donts-typography?utm_source=chatgpt.com "What are Apple’s guidelines on typography for iOS apps?"
[5]: https://codershigh.github.io/guidelines/ios/human-interface-guidelines/visual-design/typography/index.html?utm_source=chatgpt.com "Typography - Visual Design - iOS Human Interface Guidelines - GitHub Pages"
[6]: https://encyclopedia.design/2025/02/03/the-essence-of-apple-design-a-deep-dive-into-human-centered-innovation/?utm_source=chatgpt.com "The Impact of Apple Human Interface Guidelines on UX"
[7]: https://docs.developer.apple.com/design/Human-Interface-Guidelines/layout?utm_source=chatgpt.com "Layout | Apple Developer Documentation"
[8]: https://developer.apple.com/design/human-interface-guidelines/layout-and-organization?utm_source=chatgpt.com "Human Interface Guidelines - Apple Developer"
[9]: https://developer.apple.com/design/human-interface-guidelines/sf-symbols?utm_source=chatgpt.com "SF Symbols | Apple Developer Documentation"
[10]: https://app.uxcel.com/courses/apple-hig/icons-symbols-guidelines-647?utm_source=chatgpt.com "Icons & Symbols Guidelines Lesson | Uxcel"
[11]: https://developer.apple.com/sf-symbols/?utm_source=chatgpt.com "SF Symbols - Apple Developer"
[12]: https://docs.developer.apple.com/design/human-interface-guidelines/inclusion?utm_source=chatgpt.com "Inclusion - Apple Developer Documentation"
[13]: https://developer.apple.com/design/human-interface-guidelines/icons?utm_source=chatgpt.com "Icons | Apple Developer Documentation"
[14]: https://devimages-cdn.apple.com/wwdc-services/images/C03E6E6D-A32A-41D0-9E50-C3C6059820AA/guides-76105412-ED4C-4D9D-AAA5-E039F7FE142B/WWDC24-Design.pdf?utm_source=chatgpt.com "Design Highlights - Apple Inc."
