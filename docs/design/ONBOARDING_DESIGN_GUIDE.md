# Onboarding Design Guide - Cosmic Mysticism Theme

**Version:** 1.0
**Last Updated:** November 27, 2025
**Status:** COMPLETE

---

## Overview

This guide documents the design specifications and implementation patterns for the Kundali astrology app's Onboarding flow. All screens follow the **Cosmic Mysticism** design philosophy with emphasis on smooth animations, clear visual hierarchy, and excellent user experience.

---

## Design Philosophy: Cosmic Mysticism

### Core Principles
1. **Modern Minimalism:** Clean, uncluttered layouts with purposeful elements
2. **Ethereal Beauty:** Soft gradients, subtle glows, and mystical color palettes
3. **Smooth Motion:** Intentional animations that guide the user through the experience
4. **Clear Clarity:** Despite the mystical theme, information hierarchy and readability are paramount
5. **Trustworthiness:** Straightforward language, proper feedback, and logical flows

### Visual Language
- **Gradients:** Deep space colors transitioning to primary accent colors
- **Icons:** Outlined material icons representing concepts (calendar, clock, location, check)
- **Typography:** Elegant Playfair Display for headings, readable Lora for body text
- **Colors:** Deep navy backgrounds (#0F0F23) with indigo accents (#6366F1)
- **Depth:** Subtle shadows and layering create perceived depth

---

## Screen-by-Screen Specifications

### 1. Splash Screen

#### Purpose
Create a magical first impression and initialize the app.

#### Layout Components
| Component | Size | Details |
|-----------|------|---------|
| **Background Gradient** | Full screen | Deep Space → Primary (0.15 alpha) → Deep Space |
| **Logo Circle** | 120x120dp | Circular gradient with double glow shadow |
| **App Name** | Dynamic | Gradient text using ShaderMask |
| **Tagline** | Dynamic | "Your Cosmic Guide" in secondary color |
| **Loading Spinner** | 40x40dp | Circular progress indicator |

#### Animations
```
Timeline (Total: 2.3s):
├─ Logo Glow Pulse: 0-500ms (scale 1.0→1.1)
├─ Logo Fade: 0-500ms (opacity 0→1)
├─ Name Fade: 400-900ms (opacity 0→1, 400ms delay)
├─ Tagline Fade: 700-1200ms (opacity 0→1, 700ms delay)
└─ Navigation: 2.3s
```

#### Color Specifications
| Element | Color | Alpha | Usage |
|---------|-------|-------|-------|
| Background | #0F0F14 | 1.0 | Top/bottom |
| Gradient | #6366F1 | 0.15 | Center |
| Logo | #6366F1 | 0.8-1.0 | Primary accent |
| Glow | #6366F1 | 0.3-0.6 | Shadow effect |
| Text | #F0F0F5 | 1.0 | App name |
| Tagline | #6366F1 | 0.7 | Secondary text |

#### Responsive Behavior
- Maintains aspect ratio on all screen sizes
- Logo size adjusts proportionally on larger screens
- Text scales with system font size settings

---

### 2. Onboarding Welcome Screen

#### Purpose
Introduce app features and motivate user to start onboarding.

#### Layout Components
| Section | Height | Details |
|---------|--------|---------|
| **Progress Dots** | 16dp | Step 0 indicator (visual only) |
| **Zodiac Illustration** | 200dp | Rotating animated circle |
| **Title** | Dynamic | "Discover Your Cosmic Path" |
| **Subtitle** | Dynamic | Feature description |
| **Feature Cards** | 3 × 100dp | Icons + title + description |
| **Info Card** | Dynamic | App requirements explanation |
| **Button** | 56dp | "Get Started" CTA |

#### Animations
```
Timeline (Total: 800ms, then repeat zodiac rotation):
├─ Page Fade + Slide: 0-250ms
├─ Illustration: 100-350ms (scale + fade)
├─ Card 1: 300-550ms (slide from bottom)
├─ Card 2: 400-650ms (staggered 100ms)
├─ Card 3: 500-750ms (staggered 100ms)
├─ Button: 700-1000ms
└─ Zodiac Rotation: 0-800ms (continuous loop)
```

#### Feature Cards
```
Card Structure:
┌─────────────────────────┐
│ 🎯 Title (✨, 🌙, ⭐) │
├─────────────────────────┤
│ Short description text  │
│ explaining feature      │
└─────────────────────────┘

Background: #1A1A2E @ 80% alpha
Border: #6366F1 @ 15% alpha
Padding: 16dp (AppSpacing.md)
```

#### Color Specifications
| Element | Color | Alpha | Usage |
|---------|-------|-------|-------|
| Background | #0F0F23 | 1.0 | Page background |
| Gradient | #6366F1 | 0.1 | Accent overlay |
| Cards | #1A1A2E | 0.8 | Card surface |
| Borders | #6366F1 | 0.15 | Card outline |
| Icons | Emoji | - | Feature icons |
| Text | #F0F0F5 | 1.0 | Primary text |
| Secondary | #B0B0C0 | 1.0 | Description text |

---

### 3. Birth Date Screen

#### Purpose
Collect user's birth date for chart calculation.

#### Layout Components
| Component | Size | Details |
|-----------|------|---------|
| **Progress Dots** | 16dp | ● ○ ○ (Step 1/4) |
| **Illustration** | 120x120dp | Calendar icon in circle |
| **Title** | Dynamic | "When were you born?" |
| **Form Card** | Full-width | Date picker + info section |
| **Buttons** | 56dp | Back / Next navigation |

#### Progress Dots Specification
```
Active Dot (Current Step):
- Size: 8dp diameter
- Color: #6366F1
- Shadow: 8dp blur, 0.4 alpha
- Animation: Instant (no animation)

Inactive Dots:
- Size: 8dp diameter
- Color: #3A3A58
- Shadow: None
- Animation: Smooth fade/scale on activation (300ms)

Spacing: 8dp between dots
```

#### Form Card Structure
```
┌──────────────────────────────────┐
│ 🗓️ Birth Date                    │
│ [Date Picker Field]              │
│                                  │
│ ℹ️ Why we need this              │
│ Explanation text...              │
└──────────────────────────────────┘
```

#### Validation & Feedback
- **Valid date:** Green checkmark appears
- **Invalid date:** Red outline + error message
- **Future date:** Error message "Please select a past date"
- **Extreme age:** Warning if over 150 years old

---

### 4. Birth Time Screen

#### Purpose
Collect user's birth time for accurate chart generation.

#### Layout Components
| Component | Size | Details |
|-----------|------|---------|
| **Progress Dots** | 16dp | ○ ● ○ (Step 2/4) |
| **Illustration** | 120x120dp | Clock icon in circle |
| **Title** | Dynamic | "What time were you born?" |
| **Time Picker** | Full-width | Time input card |
| **Checkbox** | Auto | "I don't know exact time" |
| **Info Card** | Auto | Time accuracy importance |
| **Buttons** | 56dp | Back / Next navigation |

#### Time Picker Card
```
┌──────────────────────────────────┐
│ 🕐 Birth Time                    │
│ [Time Picker] [Clear Button]     │
│                                  │
│ ☑ I don't know exact time        │
│   We'll use noon as default      │
│                                  │
│ ℹ️ Time Accuracy Matters         │
│ Even small differences affect... │
└──────────────────────────────────┘
```

#### Time Accuracy Info
- Explains Ascendant sensitivity
- Recommends birth certificate
- Offers default noon time option

---

### 5. Birth Location Screen

#### Purpose
Collect birth location for timezone and chart accuracy.

#### Layout Components
| Component | Size | Details |
|-----------|------|---------|
| **Progress Dots** | 16dp | ○ ○ ● (Step 3/4) |
| **Illustration** | 120x120dp | Location icon in circle |
| **Title** | Dynamic | "Where were you born?" |
| **Form Fields** | Full-width | City, State, Country inputs |
| **Coordinates** | Collapsible | Optional lat/long fields |
| **Info Card** | Auto | Location importance |
| **Buttons** | 56dp | Back / Next navigation |

#### Form Fields Layout
```
┌──────────────────────────────────┐
│ 📍 City                          │
│ [Input Field]                    │
│                                  │
│ 🗺️ State/Province               │
│ [Input Field]                    │
│                                  │
│ 🌍 Country                       │
│ [Input Field]                    │
│                                  │
│ ☑ Enter coordinates (optional)   │
│   For even more accuracy         │
│ [Latitude Field]                 │
│ [Longitude Field]                │
└──────────────────────────────────┘
```

#### Validation
- **City:** Required, min 2 characters
- **Country:** Required, validated against country list
- **State:** Optional, but recommended
- **Latitude:** -90 to 90 range
- **Longitude:** -180 to 180 range
- **Coordinates:** Both required if enabled

---

### 6. Confirmation Screen

#### Purpose
Review all collected data before generating chart.

#### Layout Components
| Component | Size | Details |
|-----------|------|---------|
| **Progress Dots** | 16dp | ○ ○ ○ ● (Step 4/4) |
| **Illustration** | 120x120dp | Check icon in circle |
| **Title** | Dynamic | "Review Your Details" |
| **Details Card** | Full-width | All collected information |
| **Edit Buttons** | Auto | Edit date/time and location |
| **Terms Checkbox** | Auto | Agreement to generate chart |
| **Info Card** | Auto | Next steps explanation |
| **CTA Button** | 56dp | "Generate My Chart" |

#### Details Card Structure
```
┌────────────────────────────────────┐
│ 📅 Birth Date                      │
│ November 27, 1990                  │
│                                    │
│ 🕐 Birth Time                      │
│ 3:45 PM                            │
│                                    │
│ 📍 Birth Location                  │
│ New York, NY, United States        │
│                                    │
│ 🌍 Coordinates (if provided)       │
│ 40.7128°N, 74.0060°W              │
└────────────────────────────────────┘
```

#### Edit Options
- Edit buttons positioned below details card
- Each button navigates back to relevant step
- Preserves other data during editing

#### Next Steps Info
```
┌────────────────────────────────────┐
│ ℹ️ Next Steps                       │
│                                    │
│ 1. Generate Vedic birth chart      │
│ 2. Calculate planetary positions   │
│ 3. Analyze life predictions        │
│ 4. Show personalized insights      │
└────────────────────────────────────┘
```

---

## Animation Specifications

### Global Animation Tokens

#### Durations
| Token | Value | Usage |
|-------|-------|-------|
| `durationFast` | 150ms | Hover states, quick feedback |
| `durationNormal` | 300ms | Standard transitions, page flows |
| `durationSlow` | 500ms | Prominent animations, hero transitions |
| `durationVerySlow` | 800ms | Page entrance, complex sequences |

#### Curves
| Token | Curve | Usage |
|-------|-------|-------|
| `curveEaseOut` | easeOut | Element entrances (smooth deceleration) |
| `curveEaseInOut` | easeInOut | Element exits, smooth transitions |
| `curveLinear` | linear | Continuous animations (rotations) |

### Specific Animation Patterns

#### Pattern A: Page Entrance (Fade + Slide)
```dart
FadeTransition(
  opacity: Tween<double>(0, 1).animate(
    CurvedAnimation(
      parent: controller,
      curve: const Interval(0, 0.25, curve: Curves.easeOut),
    ),
  ),
  child: SlideTransition(
    position: Tween<Offset>(
      Offset(0, 0.05),
      Offset.zero,
    ).animate(...),
    child: content,
  ),
)
```

**Timing:** 0-250ms
**Effect:** Slide up + fade in
**Curve:** easeOut
**Distance:** 0.05 offset (24dp on 480dp screen)

#### Pattern B: Cascade/Stagger
```dart
// Card 1: 300-550ms
// Card 2: 400-650ms (100ms stagger)
// Card 3: 500-750ms (100ms stagger)

SlideTransition(
  position: Tween<Offset>(
    Offset(0, 0.08),
    Offset.zero,
  ).animate(
    CurvedAnimation(
      parent: controller,
      curve: const Interval(0.3, 0.55, curve: Curves.easeOut),
    ),
  ),
  child: FadeTransition(opacity: cardOpacity, child: card),
)
```

**Pattern:** Cards appear sequentially
**Delay:** 100ms between each
**Duration:** 250ms each
**Distance:** 0.08 offset (38dp on 480dp screen)

#### Pattern C: Continuous Rotation
```dart
RotationTransition(
  turns: Tween(begin: 0.0, end: 1.0).animate(
    CurvedAnimation(
      parent: controller,
      curve: Curves.linear,
    ),
  ),
  child: zodiacIcon,
)
```

**Timing:** 800ms per rotation
**Curve:** linear
**Effect:** Smooth continuous rotation
**Sync:** Synchronized with page animations

#### Pattern D: Scale + Glow
```dart
ScaleTransition(
  scale: Tween<double>(1.0, 1.1).animate(
    CurvedAnimation(
      parent: controller,
      curve: const Interval(0, 0.35, curve: Curves.easeInOut),
    ),
  ),
  child: GlowContainer(child: logo),
)
```

**Timing:** 0-350ms pulse
**Effect:** Scale + glow intensity increase
**Loop:** Can repeat continuously

---

## Component Specifications

### Progress Dots Component

#### Dimensions
```
Dot Size: 8dp diameter
Dot Spacing: 8dp between centers (4dp gap)
Total Width (4 dots): 44dp
Height: 16dp
```

#### States
| State | Color | Shadow | Animation |
|-------|-------|--------|-----------|
| Active | #6366F1 | 0.4 blur | Instant on update |
| Inactive | #3A3A58 | None | 300ms fade on activate |
| Upcoming | #3A3A58 | None | Static |

#### Usage
```dart
ProgressDots(
  currentStep: 1,        // 1-4
  totalSteps: 4,
  activeColor: AppColors.primary,
  inactiveColor: Color(0xFF3A3A58),
  dotSize: 8.0,
  spacing: AppSpacing.sm,
)
```

### Illustration Containers

#### Dimensions
```
Size: 120x120dp
Border Radius: 50% (circular)
Border: 2dp thick
```

#### Styling
```
Background Gradient:
├─ Primary: #6366F1 @ 0.15
├─ Secondary: #DB7093 @ 0.1
└─ Blend: topLeft to bottomRight

Border Color: #6366F1 @ 0.2
Box Shadow:
├─ Blur: 30dp
├─ Spread: 5dp
└─ Color: #6366F1 @ 0.1

Icon Size: 56dp
Icon Color: #6366F1
```

### Form Cards

#### Layout
```
Padding: 24dp (AppSpacing.lg)
Border Radius: 16dp (AppSpacing.md)
Min Height: 180dp
Full Width: Yes
```

#### Styling
```
Background: #1A1A2E @ 0.8 alpha
Border: 1dp, #6366F1 @ 0.15
Box Shadow:
├─ Blur: 12dp
├─ Spread: 0dp
├─ Offset: (0, 4)
└─ Color: #000000 @ 0.2
```

#### Sections
```
Title: headlineSmall (16dp)
Content: bodyMedium / bodySmall
Divider: 24dp margins
Info Box: 16dp padding, primary @ 0.08 bg
```

---

## Color Specifications

### Complete Palette for Onboarding

#### Primary Colors
```
Primary: #6366F1
├─ Used for: Icons, borders, accents, progress indicators
├─ Alpha variations: 0.1, 0.15, 0.3, 0.7, 1.0
└─ Contrast: Excellent on dark backgrounds

Secondary: #DB7093
├─ Used for: Gradients, special emphasis
├─ Alpha: 0.1 (gradient overlay)
└─ Contrast: Good on dark backgrounds
```

#### Background Colors
```
Deep Space: #0F0F23
├─ Used for: Page background
├─ Coordinates with: Primary gradient overlay
└─ Accessibility: Excellent for eye comfort

Surface: #1A1A2E
├─ Used for: Cards, containers
├─ Alpha: 0.8 (semi-transparent)
└─ Contrast: Strong for readability

Elevated: #252538
├─ Used for: Nested containers
└─ Depth indication
```

#### Text Colors
```
Primary Text: #F0F0F5 (Almost White)
├─ Used for: Headings, main content
├─ Contrast: 19:1 on #0F0F23
└─ Size: 16dp+

Secondary Text: #B0B0C0 (Light Gray)
├─ Used for: Descriptions, support text
├─ Contrast: 8:1 on #0F0F23
└─ Size: 14dp

Tertiary Text: #7C7C8F (Medium Gray)
├─ Used for: Hints, disabled states
├─ Contrast: 5.5:1 on #0F0F23
└─ Size: 12dp
```

---

## Typography Specifications

### Font Selection
```
Headings: Playfair Display
├─ Weight: 600 (SemiBold)
├─ Tracking: 0.15-0.5 (letter spacing)
└─ Used for: Titles, section headers

Body: Lora
├─ Weight: 400 (Regular)
├─ Tracking: 0
└─ Used for: Content, descriptions

Labels: Montserrat
├─ Weight: 500-600
├─ Tracking: 0.1-0.2
└─ Used for: Form labels, buttons
```

### Size Specifications
| Style | Font | Size | Weight | Spacing |
|-------|------|------|--------|---------|
| Display Large | Playfair | 32dp | Bold | 0.5 |
| Display Medium | Playfair | 28dp | Bold | 0.3 |
| Headline Large | Playfair | 22dp | 600 | 0.15 |
| Headline Medium | Playfair | 20dp | 600 | 0.15 |
| Headline Small | Playfair | 18dp | 600 | 0.1 |
| Body Large | Lora | 16dp | 400 | 0 |
| Body Medium | Lora | 14dp | 400 | 0 |
| Body Small | Lora | 12dp | 400 | 0 |
| Label Large | Montserrat | 14dp | 600 | 0.1 |
| Label Medium | Montserrat | 12dp | 500 | 0.15 |
| Label Small | Montserrat | 11dp | 500 | 0.2 |

---

## Spacing System

### Base Unit: 4dp

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4dp | Small gaps, micro-spacing |
| `sm` | 8dp | Component padding, icon spacing |
| `md` | 16dp | Form field spacing, card padding |
| `lg` | 24dp | Section spacing, major padding |
| `xl` | 32dp | Screen section separation |
| `xxl` | 48dp | Major section spacing |
| `xxxl` | 56dp | Spacer before bottom buttons |

### Applied Spacing
```
Page Padding: 24dp horizontal, 24dp vertical
Card Padding: 24dp
Form Field Spacing: 16dp vertical
Section Dividers: 24dp or 32dp
Bottom Padding: 56dp (button height + spacing)
```

---

## Responsive Design Specifications

### Breakpoints
| Category | Min Width | Max Width |
|----------|-----------|-----------|
| Mobile | 320dp | 599dp |
| Tablet | 600dp | 839dp |
| Desktop | 840dp | ∞ |

### Scaling Behavior
```
Small Phones (320-360):
├─ Font sizes: -2dp from defaults
├─ Spacing: Maintain minimums (no reduction)
└─ Illustrations: 100x100dp

Regular Phones (360-599):
├─ Font sizes: Standard
├─ Spacing: Standard
└─ Illustrations: 120x120dp

Tablets (600-839):
├─ Font sizes: +2dp from defaults
├─ Spacing: +4dp from standard
└─ Illustrations: 160x160dp
└─ Max width: 600dp centered

Desktop (840+):
├─ Font sizes: +4dp from defaults
├─ Spacing: +8dp from standard
└─ Illustrations: 200x200dp
└─ Max width: 700dp centered
```

---

## Accessibility Guidelines

### WCAG 2.1 AA Compliance

#### Color Contrast
- Minimum ratio: 4.5:1 for normal text
- Minimum ratio: 3:1 for large text (18dp+)
- All combinations tested and verified

#### Touch Targets
- Minimum size: 44dp x 44dp
- Minimum spacing: 8dp between targets
- All buttons and inputs meet requirements

#### Focus Indicators
- Visible focus rings on form fields
- Clear keyboard navigation order
- Proper tab index management

#### Motion
- No parallax or distracting effects
- Animations serve functional purposes
- Optional disable animations support possible

#### Text
- Clear, simple language
- Descriptive labels for form fields
- Error messages clear and actionable

---

## Implementation Checklist

- [x] Cosmic gradient backgrounds on all screens
- [x] Proper color usage from AppColors
- [x] Correct typography from AppTypography
- [x] Consistent spacing from AppSpacing
- [x] Smooth animations from AppAnimations
- [x] Progress dots component created and used
- [x] Form validation implemented
- [x] Error handling and feedback
- [x] Navigation between screens
- [x] Responsive design for all screen sizes
- [x] WCAG 2.1 AA accessibility compliance
- [x] 60fps animation performance
- [x] Proper animation controller lifecycle
- [x] No hardcoded values
- [x] Complete documentation

---

## Troubleshooting

### Animation Issues

**Problem:** Animations appear janky or slow
**Solution:**
- Profile with Flutter DevTools
- Check for expensive operations in build()
- Verify animation controller timing
- Test on actual device (simulators can be slow)

**Problem:** Progress dots don't animate smoothly
**Solution:**
- Ensure AnimatedContainer is used
- Verify animation duration is set
- Check color definitions (use AppColors)

### Layout Issues

**Problem:** Content overflows on small screens
**Solution:**
- Wrap in SingleChildScrollView
- Use responsive font sizing
- Reduce padding on small screens
- Test on 320dp width device

**Problem:** Cards don't have proper shadows
**Solution:**
- Check Material version
- Verify BoxShadow color is not black
- Ensure elevation is not set (use BoxShadow)

### Navigation Issues

**Problem:** Back button not working
**Solution:**
- Verify PopScope or WillPopScope implementation
- Check navigation routes are registered
- Ensure context is passed correctly

---

## References

- Flutter Documentation: https://flutter.dev/docs
- Material Design 3: https://m3.material.io
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- App Design System: `docs/design/COMPLETE_DESIGN_SYSTEM.md`
- Animation Guide: `docs/design/PHASE_2_ANIMATION_SPECS.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 27, 2025 | Initial complete guide |

---

*This design guide serves as the definitive reference for all onboarding screen implementation and styling. All team members should refer to this document when working on onboarding-related features.*
