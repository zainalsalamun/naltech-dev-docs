# Fitaru Design System

Dokumen ini berisi arahan visual dan komponen dasar untuk MVP Fitaru.

## Brand Foundation

**Nama:** Fitaru

**Tagline:** Diet santai, progres tetap jalan.

**Positioning:** Aplikasi diet santai untuk mencatat makan, olahraga, dan progres tubuh harian secara realistis.

## Design Principles

- Ringan dipakai setiap hari
- Ramah untuk pemula
- Tidak menghakimi
- Fokus pada progres kecil
- Bersih, modern, dan mudah dipindai
- Terasa sehat tanpa menjadi terlalu klinis
- Terasa aktif tanpa menjadi terlalu agresif seperti aplikasi gym

## Visual Personality

Fitaru harus terasa:

- Fresh
- Calm
- Supportive
- Practical
- Optimistic
- Local-friendly

Fitaru tidak boleh terasa:

- Mengintimidasi
- Terlalu medis
- Terlalu macho
- Terlalu mewah
- Terlalu ramai
- Seperti aplikasi diet ekstrem

## Color Palette

### Primary

**Fitaru Teal**

- Hex: `#1BAE8C`
- Use: primary button, active state, main icon, progress highlight

**Deep Teal**

- Hex: `#0E6F60`
- Use: headline emphasis, selected state, high contrast primary text on light background

### Accent

**Soft Coral**

- Hex: `#FF8A65`
- Use: secondary highlight, friendly CTA accent, small illustration accent

**Warm Amber**

- Hex: `#F6B44B`
- Use: gentle warning, streak, weekly insight, small badge

### Background

**App White**

- Hex: `#FFFFFF`
- Use: main background

**Soft Mint**

- Hex: `#EFFAF6`
- Use: soft section background, success surface, onboarding background

**Warm Off White**

- Hex: `#FAFAF7`
- Use: alternative app background, empty state surface

### Text

**Charcoal**

- Hex: `#1F2A2A`
- Use: primary text

**Slate Gray**

- Hex: `#5C6B6B`
- Use: secondary text

**Muted Gray**

- Hex: `#9AA7A7`
- Use: placeholder, disabled state

### Border and Surface

**Border Soft**

- Hex: `#DDE7E4`
- Use: input border, card border, divider

**Surface Light**

- Hex: `#F4F8F7`
- Use: card background, inactive segmented control

### Semantic

**Success**

- Hex: `#2EAD68`
- Use: success toast, completed habit

**Warning**

- Hex: `#F2A93B`
- Use: gentle reminder, caution state

**Error**

- Hex: `#E05A47`
- Use: validation error only

## Color Usage Ratio

Recommended visual balance:

- 60% white or off-white background
- 20% soft mint or light surfaces
- 10% teal primary elements
- 5% coral accent
- 5% semantic colors and illustration details

Avoid making the whole app only teal. Teal should guide attention, not dominate every surface.

## Typography

### Recommended Font

**Plus Jakarta Sans**

Reason:

- Clean and modern
- Friendly without looking childish
- Works well for Indonesian copy
- Suitable for mobile UI

Fallback:

- Inter
- Manrope
- System sans-serif

### Type Scale

**Display / Onboarding Title**

- Size: 28
- Weight: 700
- Line height: 36

**Page Title**

- Size: 24
- Weight: 700
- Line height: 32

**Section Title**

- Size: 18
- Weight: 700
- Line height: 26

**Card Title**

- Size: 16
- Weight: 700
- Line height: 24

**Body**

- Size: 15
- Weight: 400
- Line height: 22

**Body Small**

- Size: 13
- Weight: 400
- Line height: 20

**Caption**

- Size: 12
- Weight: 500
- Line height: 16

**Button**

- Size: 15
- Weight: 700
- Line height: 20

Typography rules:

- Do not use negative letter spacing.
- Keep text easy to scan.
- Use bold for emphasis sparingly.
- Avoid all caps except very small labels when necessary.

## Spacing

Base spacing unit: `4px`

Recommended spacing:

- `4px`: tiny gap
- `8px`: compact gap
- `12px`: field inner gap
- `16px`: default component gap
- `20px`: section spacing
- `24px`: page padding
- `32px`: large section spacing
- `40px`: onboarding spacing

Mobile page padding:

- Horizontal: `20px`
- Top: depends on safe area
- Bottom: must account for bottom navigation

## Corner Radius

Use rounded corners, but keep them controlled.

- Small controls: `8px`
- Inputs: `12px`
- Buttons: `14px`
- Cards: `16px`
- Bottom sheet: `24px` top corners
- Circular icon button: fully round

Cards should feel soft but not overly bubbly.

## Shadows

Use shadows lightly.

Default card shadow:

- Color: `#12302A`
- Opacity: 8%
- Blur: 16
- Y: 6

Use shadows only for:

- Floating action button
- Bottom sheet
- Important card elevation

Prefer borders and surface contrast for normal cards.

## Icon Style

Recommended icon style:

- Rounded line icons
- Stroke width: 2
- Simple and clear

Icon direction:

- Meal: bowl, fork, plate
- Exercise: activity, dumbbell, shoe, walking
- Water: droplet, cup
- Weight: scale
- Progress: line chart
- Tips: lightbulb or book
- Profile: user

Use icons inside quick actions and bottom navigation.

## Illustration Style

Illustration direction:

- Simple flat illustration
- Soft human shapes
- Food, water, walking, progress chart themes
- Limited color palette using teal, mint, coral, amber
- Avoid overly muscular fitness visuals
- Avoid medical/hospital feeling

Illustrations should feel like everyday healthy living, not transformation pressure.

## Components

## Button

### Primary Button

Use for the main action on a screen.

Style:

- Background: `#1BAE8C`
- Text: white
- Height: `52px`
- Radius: `14px`
- Font: 15 / 700

Examples:

- Mulai Sekarang
- Simpan
- Buat Target
- Mulai Pakai Fitaru

### Secondary Button

Use for alternative actions.

Style:

- Background: `#EFFAF6`
- Text: `#0E6F60`
- Border: optional `#DDE7E4`
- Height: `52px`
- Radius: `14px`

Examples:

- Lewati dulu
- Ubah target
- Tambah foto

### Text Button

Use for low-priority actions.

Style:

- Text: `#0E6F60`
- No background
- Font: 15 / 700

Examples:

- Masuk
- Lewati
- Lihat semua

## Input Field

Style:

- Height: `52px`
- Background: white
- Border: `#DDE7E4`
- Radius: `12px`
- Text: `#1F2A2A`
- Placeholder: `#9AA7A7`
- Padding horizontal: `16px`

States:

- Default: border soft
- Focus: teal border
- Error: error border with short helper text
- Disabled: surface light background

## Card

Use cards for individual summaries or repeated items.

Style:

- Background: white or `#F4F8F7`
- Border: `#DDE7E4`
- Radius: `16px`
- Padding: `16px`

Card types:

- Consistency score card
- Daily summary card
- Food log item
- Exercise log item
- Weekly review metric
- Tips article preview

Avoid putting cards inside other cards.

## Quick Action

Use on dashboard for fast input.

Items:

- Makan
- Olahraga
- Berat
- Air

Style:

- Icon top
- Label bottom
- Surface: `#EFFAF6`
- Active/pressed: teal background with white icon/text
- Radius: `16px`
- Minimum height: `76px`

## Segmented Control

Use for choices like meal time, progress tabs, or intensity.

Examples:

- Sarapan / Siang / Malam / Snack / Minuman
- Ringan / Sedang / Berat
- Berat / Makan / Olahraga / Konsistensi

Style:

- Container background: `#F4F8F7`
- Selected background: white
- Selected text: `#0E6F60`
- Unselected text: `#5C6B6B`
- Radius: `12px`

## Stepper

Use for numeric values:

- Usia
- Berat badan
- Air minum
- Durasi olahraga
- Olahraga per minggu

Style:

- Minus icon button
- Value in center
- Plus icon button
- Button size: `40px`
- Radius: circular

## Progress Bar

Use for:

- Skor konsistensi
- Air minum
- Setup profile step

Style:

- Track: `#DDE7E4`
- Fill: `#1BAE8C`
- Height: `8px`
- Radius: full

## Toast / Success Message

Use after successful actions.

Style:

- Background: `#1F2A2A`
- Text: white
- Radius: `14px`
- Padding: `12px 16px`

Copy examples:

- Tercatat. Makan enak tetap bisa jalan bareng progres.
- Mantap. Gerak sedikit tetap berarti.
- Berat tercatat. Fokus ke tren, bukan satu angka hari ini.

## Bottom Navigation

Items:

- Home
- Catat
- Progress
- Tips
- Profil

Style:

- Background: white
- Border top: `#DDE7E4`
- Active icon/text: `#1BAE8C`
- Inactive icon/text: `#9AA7A7`
- Height: `72px` plus safe area

Catat can be slightly emphasized as the central action, but should not disrupt the layout.

## Empty State

Use when no data has been recorded.

Tone:

- Friendly
- Encouraging
- Actionable

Examples:

Makan:

> Belum ada makanan tercatat hari ini. Mulai dari satu catatan kecil dulu.

Olahraga:

> Belum olahraga hari ini. Jalan 10 menit juga sudah progres.

Berat:

> Belum ada data berat. Catat sesekali untuk lihat trennya.

## Copywriting Guidelines

Tone:

- Santai
- Supportive
- Tidak menghakimi
- Realistis
- Pendek dan jelas

Use:

- "tercatat"
- "progres"
- "pelan-pelan"
- "tetap jalan"
- "lebih sadar"
- "kebiasaan kecil"

Avoid:

- "gagal"
- "buruk"
- "cheat"
- "tidak disiplin"
- "kalori berlebihan"
- "target gagal"

## Core Copy Examples

Dashboard:

- Hari ini sudah 2 dari 4 kebiasaan tercatat. Progres tetap jalan.
- Makan enak tetap boleh, yang penting tercatat.

Meal log:

- Tercatat. Makan enak tetap bisa jalan bareng progres.

Exercise log:

- Mantap. Gerak sedikit tetap berarti.

Weight log:

- Berat tercatat. Fokus ke tren, bukan satu angka hari ini.

Weekly review:

- Minggu ini kamu lebih konsisten di olahraga. Untuk minggu depan, coba rapikan snack malam pelan-pelan.

## Accessibility

Minimum recommendations:

- Text contrast must stay readable on all backgrounds.
- Touch target minimum: `44px`.
- Do not communicate status with color only.
- Use clear labels for icon buttons.
- Error messages must explain what user needs to fix.
- Support dynamic text where possible.

## MVP Screen Style Direction

### Splash

- White or soft mint background
- Centered logo
- Tagline underneath

### Onboarding

- Large illustration
- One title
- One short paragraph
- Simple pagination dots
- Primary CTA at bottom

### Home

- Friendly greeting at top
- Consistency score card
- Quick actions
- Daily summary
- Supportive message

### Catat Makan

- Segmented meal time
- Simple input form
- Porsi selector
- Optional calorie
- Optional photo

### Progress

- Clean chart area
- Weekly metrics
- Insight message

### Profil

- Personal summary
- Target section
- Settings list

## Implementation Notes

For mobile development:

- Keep components reusable.
- Define colors as tokens.
- Define typography as tokens.
- Use consistent spacing tokens.
- Keep form input flows short.
- Make calorie input optional by default.
- Keep dashboard useful even with partial data.

## Next Step

After this design system, the next recommended step is creating a simple high-fidelity UI mockup for the main screens:

1. Splash
2. Onboarding
3. Home dashboard
4. Catat makan
5. Progress
