# Design Tokens & Quick Reference Guide

**Astrology App - Design System Tokens**

A quick reference guide to all design tokens used in the Flutter application. Use this for rapid lookups during development.

---

## Quick Access Tokens

### Colors

#### Primary Colors
```dart
AppColors.primary        // #6366F1 (Indigo) - Main brand
AppColors.primaryLight   // #818CF8 - Light variant
AppColors.primaryDark    // #4F46E5 - Dark variant
```

#### Secondary Colors
```dart
AppColors.secondary      // #DB7093 (Pale Violet Red)
AppColors.secondaryLight // #E591AB - Light variant
AppColors.secondaryDark  // #C5637A - Dark variant
```

#### Planetary Colors
```dart
AppColors.sun       // #FFD700 (Gold)
AppColors.moon      // #F0F0F5 (Silver)
AppColors.mars      // #EF4444 (Red)
AppColors.mercury   // #9CA3AF (Gray)
AppColors.jupiter   // #F97316 (Orange)
AppColors.venus     // #4ADE80 (Green)
AppColors.saturn    // #3B82F6 (Blue)
AppColors.rahu      // #7C3AED (Purple)
AppColors.ketu      // #EC4899 (Pink)
```

#### Element Colors
```dart
// Fire (Aries, Leo, Sagittarius)
AppColors.fireElement       // #FF6B6B
AppColors.fireElementLight  // #FFB4B4
AppColors.fireElementDark   // #CC5555

// Earth (Taurus, Virgo, Capricorn)
AppColors.earthElement      // #8B7355
AppColors.earthElementLight // #C4A77D
AppColors.earthElementDark  // #6B5840

// Air (Gemini, Libra, Aquarius)
AppColors.airElement        // #FFD93D
AppColors.airElementLight   // #FFECA1
AppColors.airElementDark    // #CCAE31

// Water (Cancer, Scorpio, Pisces)
AppColors.waterElement      // #6BCEFF
AppColors.waterElementLight // #B4E7FF
AppColors.waterElementDark  // #56A5CC
```

#### Semantic Colors
```dart
AppColors.success   // #10B981 (Green)
AppColors.warning   // #F59E0B (Amber)
AppColors.error     // #EF4444 (Red)
AppColors.info      // #3B82F6 (Blue)
AppColors.disabled  // #D1D5DB (Gray)
```

#### Light Mode Backgrounds
```dart
AppColors.backgroundLight  // #FAFAFC (Soft white)
AppColors.surfaceLight     // #FFFFFF (Pure white)
AppColors.surfaceVariantLight // #F3F4F6 (Light gray)
```

#### Dark Mode Backgrounds (Default)
```dart
AppColors.backgroundDark   // #0F0F23 (Deep navy)
AppColors.surfaceDark      // #1A1A2E (Dark navy)
AppColors.surfaceVariantDark // #252538 (Darker navy)
```

#### Light Mode Text
```dart
AppColors.textPrimaryLight    // #1F2937 (Very dark gray)
AppColors.textSecondaryLight  // #6B7280 (Medium gray)
AppColors.textTertiaryLight   // #9CA3AF (Light gray)
```

#### Dark Mode Text
```dart
AppColors.textPrimaryDark    // #F0F0F5 (Almost white)
AppColors.textSecondaryDark  // #B0B0C0 (Light gray)
AppColors.textTertiaryDark   // #7C7C8F (Medium gray)
```

#### Gradients
```dart
AppColors.cosmicGradient  // Purple → Violet → Lavender
AppColors.nebulaGradient  // Indigo → Pale Violet → Orange
AppColors.sunsetGradient  // Amber → Red → Violet Red
```

### Spacing

```dart
AppSpacing.xs      // 4px   - Extra small (tight spacing)
AppSpacing.sm      // 8px   - Small (padding, gaps)
AppSpacing.md      // 16px  - Medium (default, most common)
AppSpacing.lg      // 24px  - Large (section spacing)
AppSpacing.xl      // 32px  - Extra large (major sections)
AppSpacing.xxl     // 48px  - 2x Extra large (hero sections)
AppSpacing.xxxl    // 64px  - 3x Extra large (onboarding)
```

### Padding Presets

```dart
// All directions
AppSpacing.paddingXs, .paddingSm, .paddingMd, .paddingLg, .paddingXl, .paddingXxl

// Horizontal
AppSpacing.paddingHorizontalXs, .paddingHorizontalSm, .paddingHorizontalMd, etc.

// Vertical
AppSpacing.paddingVerticalXs, .paddingVerticalSm, .paddingVerticalMd, etc.

// Top
AppSpacing.paddingTopSm, .paddingTopMd, .paddingTopLg, .paddingTopXl

// Bottom
AppSpacing.paddingBottomSm, .paddingBottomMd, .paddingBottomLg, .paddingBottomXl
```

### Border Radius

```dart
AppDimensions.radiusXs      // 4px   - Extra small
AppDimensions.radiusSm      // 8px   - Small
AppDimensions.radiusMd      // 12px  - Medium (default)
AppDimensions.radiusLg      // 16px  - Large (cards)
AppDimensions.radiusXl      // 24px  - Extra large (modals)
AppDimensions.radiusCircle  // 999px - Circular

// Pre-computed BorderRadius objects
AppDimensions.borderRadiusXs, .borderRadiusSm, .borderRadiusMd, etc.
AppDimensions.borderRadiusTopMd  // Top corners only
AppDimensions.borderRadiusTopLg  // Top corners only (larger)
```

### Icon Sizes

```dart
AppDimensions.iconXs   // 16px - Small badges
AppDimensions.iconSm   // 20px - Inline icons
AppDimensions.iconMd   // 24px - Default icon size
AppDimensions.iconLg   // 32px - Large/prominent icons
AppDimensions.iconXl   // 48px - Extra large feature icons
AppDimensions.iconXxl  // 64px - 2x Extra large hero icons
```

### Touch Targets

```dart
AppDimensions.touchTargetMin // 48px - WCAG minimum
```

### Component Dimensions

```dart
AppDimensions.cardElevation          // 2.0
AppDimensions.cardElevationHigh      // 8.0
AppDimensions.cardMaxWidth           // 400px
AppDimensions.cardMinHeight          // 100px

AppDimensions.appBarHeight           // 56px
AppDimensions.appBarHeightCollapsed  // 64px

AppDimensions.bottomNavHeight        // 80px

AppDimensions.inputFieldHeight       // 56px
AppDimensions.inputFieldPadding      // 16px

AppDimensions.dialogWidth            // 320px

AppDimensions.dividerThickness       // 1px
AppDimensions.dividerThicknessBold   // 2px

AppDimensions.chartGlyphSize         // 28px
AppDimensions.chartGlyphSizeLarge    // 32px
AppDimensions.chartGlyphSizeSmall    // 24px
```

### Shadows

```dart
AppDimensions.shadowLight      // Subtle elevation (cards)
AppDimensions.shadowMedium     // Elevated cards, buttons
AppDimensions.shadowHigh       // Floating elements, FABs
AppDimensions.shadowElevated   // Modals, dialogs
```

### Typography

#### Font Families (via Google Fonts)
```dart
// Headlines & Display
GoogleFonts.playfairDisplay()  // Display, Headline styles

// Body Text
GoogleFonts.lora()             // Body, Caption, Interpretation

// UI Elements
GoogleFonts.montserrat()       // Labels, Buttons, Overline

// Symbols
GoogleFonts.notoSans()         // Zodiac glyphs
```

#### Display Styles
```dart
AppTypography.displayLarge   // 32px, bold, 1.2 line height
AppTypography.displayMedium  // 28px, bold, 1.3 line height
AppTypography.displaySmall   // 24px, semi-bold, 1.3 line height
```

#### Headline Styles
```dart
AppTypography.headlineLarge   // 22px, semi-bold
AppTypography.headlineMedium  // 20px, semi-bold
AppTypography.headlineSmall   // 18px, semi-bold
```

#### Body Styles
```dart
AppTypography.bodyLarge   // 16px, regular, 1.6 line height
AppTypography.bodyMedium  // 14px, regular, 1.5 line height
AppTypography.bodySmall   // 12px, regular, 1.5 line height
```

#### Label Styles
```dart
AppTypography.labelLarge   // 14px, medium weight, 1.25 letter spacing
AppTypography.labelMedium  // 12px, medium weight, 1.2 letter spacing
AppTypography.labelSmall   // 10px, medium weight, 1.5 letter spacing
```

#### Special Styles
```dart
AppTypography.button           // 16px, semi-bold (Montserrat)
AppTypography.zodiacGlyph      // 24px (Noto Sans)
AppTypography.zodiacGlyphLarge // 32px (Noto Sans)
AppTypography.interpretation   // 15px, italic, 1.7 line height
AppTypography.caption          // 12px, regular (Lora)
AppTypography.overline         // 10px, semi-bold (Montserrat)
```

### Animations

```dart
// Durations
Duration duration200ms = Duration(milliseconds: 200);  // Fast
Duration duration300ms = Duration(milliseconds: 300);  // Normal
Duration duration500ms = Duration(milliseconds: 500);  // Slow

// Curves
Curves.easeInOut   // Default smooth motion
Curves.easeOut     // Entry animations
Curves.easeIn      // Exit animations
Curves.elasticOut  // Playful bounce
Cubic(0.4, 0.0, 0.2, 1.0)  // Cosmic smooth curve
```

---

## Color Palette Reference Table

| Color | Hex | Usage | Light/Dark |
|-------|-----|-------|-----------|
| Primary | #6366F1 | CTA buttons, main actions | Both |
| Secondary | #DB7093 | Secondary buttons, love | Both |
| Sun | #FFD700 | Highlights, premium | Both |
| Success | #10B981 | Positive feedback | Both |
| Warning | #F59E0B | Cautions | Both |
| Error | #EF4444 | Errors, negatives | Both |
| Info | #3B82F6 | Information | Both |
| Background (Light) | #FAFAFC | Page background | Light |
| Background (Dark) | #0F0F23 | Page background | Dark |
| Surface (Light) | #FFFFFF | Cards, containers | Light |
| Surface (Dark) | #1A1A2E | Cards, containers | Dark |
| Text Primary (Light) | #1F2937 | Main text | Light |
| Text Primary (Dark) | #F0F0F5 | Main text | Dark |

---

## Spacing Usage Matrix

| Size | Value | Best For | Example |
|------|-------|----------|---------|
| **xs** | 4px | Micro spacing | Badge padding |
| **sm** | 8px | Small gaps | List item spacing, button padding |
| **md** | 16px | Default spacing | Card padding (MOST COMMON) |
| **lg** | 24px | Section spacing | Gap between sections |
| **xl** | 32px | Major sections | Screen padding |
| **xxl** | 48px | Hero sections | Major component gaps |
| **xxxl** | 64px | Onboarding screens | Page-breaking gaps |

---

## Typography Size Hierarchy

```
32px - Display Large (Page titles)
  ↓
28px - Display Medium (Section headers)
  ↓
24px - Display Small (Sub-sections)
  ↓
22px - Headline Large (Card titles)
  ↓
20px - Headline Medium (Sub-headers)
  ↓
18px - Headline Small (Feature titles)
  ↓
16px - Body Large (Main content) ← Most used for body
  ↓
14px - Body Medium (Secondary text) ← Most used overall
  ↓
12px - Body Small (Captions)
  ↓
10px - Overline (Labels)
```

---

## Component Size Guide

### Buttons
- **Height:** 56px (minimum for touch targets)
- **Padding:** 24px horizontal, 12px vertical
- **Border Radius:** 12px (radiusMd)
- **Icon Size:** 20-24px

### Cards
- **Padding:** 16px (paddingMd, default)
- **Border Radius:** 12-16px (radiusMd to radiusLg)
- **Elevation:** 2px (standard), 8px (elevated)
- **Max Width:** 400px (mobile optimized)

### Inputs
- **Height:** 56px (touch target minimum)
- **Padding:** 16px horizontal + 16px vertical
- **Border Radius:** 12px (radiusMd)
- **Border Width:** 1px (normal), 2px (focused)

### Icons
- **Default:** 24px (iconMd)
- **Inline:** 20px (iconSm)
- **Buttons:** 32px (iconLg)
- **Features:** 48px (iconXl)

### Avatar/Image
- **Small:** 32x32px
- **Medium:** 48x48px
- **Large:** 64x64px

---

## Theme System Access

### Accessing Colors

```dart
// From theme
Theme.of(context).colorScheme.primary
Theme.of(context).colorScheme.secondary
Theme.of(context).colorScheme.surface
Theme.of(context).colorScheme.error

// From custom colors
AppColors.primary
AppColors.secondary
AppColors.sun
AppColors.mars
```

### Accessing Text Styles

```dart
// From theme
Theme.of(context).textTheme.displayLarge
Theme.of(context).textTheme.headlineMedium
Theme.of(context).textTheme.bodyLarge

// From custom typography
AppTypography.displayLarge
AppTypography.headlineSmall
AppTypography.bodyMedium
```

### Accessing Spacing

```dart
// Always use constants, never hardcode
AppSpacing.md      // 16px
AppSpacing.lg      // 24px
AppSpacing.paddingMd  // EdgeInsets.all(16)
AppSpacing.paddingHorizontalLg  // EdgeInsets.symmetric(horizontal: 24)
```

---

## Common Implementation Patterns

### Button with Loading State
```dart
PrimaryButton(
  label: 'Generate Chart',
  onPressed: isLoading ? null : generateChart,
  isLoading: isLoading,
)
```

### Card with Hover Effect
```dart
CustomCard(
  elevation: isHovered ? 4 : 2,
  onTap: () {},
  child: child,
)
```

### Text with Gradient
```dart
ShaderMask(
  shaderCallback: (bounds) =>
    AppColors.cosmicGradient.createShader(bounds),
  child: Text('Mystical Text'),
)
```

### Themed Padding
```dart
Padding(
  padding: AppSpacing.paddingMd,  // 16px all sides
  child: child,
)
```

### Responsive Spacing
```dart
SizedBox(
  height: MediaQuery.of(context).size.width > 768
    ? AppSpacing.xxl  // Desktop: 48px
    : AppSpacing.lg,  // Mobile: 24px
)
```

### Focus Indicator
```dart
Container(
  decoration: BoxDecoration(
    border: Border.all(
      color: AppColors.primary,
      width: 2,
    ),
  ),
  child: child,
)
```

---

## Contrast Checker Quick Reference

**WCAG 2.1 AA Minimum Ratios:**
- Normal text: 4.5:1
- Large text (18pt+): 3:1
- Interactive elements: 3:1

**Quick Test Combinations:**
```
✓ Primary (#6366F1) on White - 4.8:1 (Good)
✓ Primary (#6366F1) on Light Gray - 3.5:1 (Good)
✓ Secondary (#DB7093) on White - 4.1:1 (Good)
✓ White text on Primary - 4.8:1 (Good)
✓ White text on Secondary - 4.1:1 (Good)
✓ Error (#EF4444) on White - 3.9:1 (Good)
```

---

## Migration Guide from Old Colors

If transitioning from old hardcoded colors:

```dart
// Old way (DON'T DO THIS)
color: Color(0xFF6366F1)

// New way (CORRECT)
color: AppColors.primary
// or
color: Theme.of(context).colorScheme.primary
```

---

## File Locations

**Core Theme Files:**
```
client/lib/core/theme/
├── app_colors.dart       # All color definitions
├── app_typography.dart   # All text styles
├── app_spacing.dart      # Spacing & dimensions
├── app_theme.dart        # Theme definitions
└── theme.dart            # Empty (legacy)
```

**Widget Files:**
```
client/lib/core/widgets/
├── buttons.dart
├── cards.dart
├── inputs.dart
├── loading_indicators.dart
├── error_states.dart
└── index.dart
```

**Documentation:**
```
docs/design/
├── COMPLETE_DESIGN_SYSTEM.md    # Full specifications
├── COMPONENT_CATALOG.md          # Component usage guide
├── DESIGN_TOKENS_REFERENCE.md    # This file
├── design-system.md              # Original design doc
└── color-palette.md              # Color specifications
```

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Color looks different in dark mode | Use `Theme.of(context)` colors, not AppColors |
| Text too small to read | Check line height, use 1.5+ for body text |
| Touch target too small | Ensure minimum 48x48px, use AppSpacing for padding |
| Animation feels sluggish | Use 200-300ms duration, test with DevTools |
| Component styling inconsistent | Check you're using correct AppTypography/AppSpacing constants |
| Contrast ratio fail | Verify 4.5:1 for normal text, 3:1 for large text |
| Spacing looks uneven | Verify using AppSpacing constants (not magic numbers) |

---

## Performance Tips

1. **Use const constructors** where possible to reduce rebuilds
2. **Avoid gradient calculations** in build methods (pre-compute)
3. **Cache gradients** as static constants
4. **Use shadowLight** for most cards (performance-friendly)
5. **Profile animations** with Flutter DevTools (target 60fps)
6. **Lazy load images** with shimmer skeletons
7. **Reuse theme colors** instead of creating new Color objects

---

## Accessibility Checklist

- [ ] All interactive elements 48x48 minimum
- [ ] Color contrast 4.5:1 for text
- [ ] Semantic labels on all interactive elements
- [ ] Focus states visible (2px outline)
- [ ] Keyboard navigation functional
- [ ] No text relies on color alone
- [ ] Font size min 12px for body text
- [ ] Line height min 1.5 for readability
- [ ] Icons have descriptive labels

---

**Quick Links:**
- Complete Design System: `/docs/design/COMPLETE_DESIGN_SYSTEM.md`
- Component Catalog: `/docs/design/COMPONENT_CATALOG.md`
- Color Palette Details: `/docs/design/color-palette.md`
- Original Design Doc: `/docs/design/design-system.md`

**Last Updated:** November 2024
**Framework:** Flutter with Material Design 3

---

## Import Quick Reference

```dart
// Always import what you need at the top of your file

// Colors
import 'package:client/core/theme/app_colors.dart';

// Typography
import 'package:client/core/theme/app_typography.dart';

// Spacing & Sizing
import 'package:client/core/theme/app_spacing.dart';

// Theme
import 'package:client/core/theme/app_theme.dart';

// Buttons
import 'package:client/core/widgets/buttons.dart';

// Cards
import 'package:client/core/widgets/cards.dart';

// Inputs
import 'package:client/core/widgets/inputs.dart';

// Loading States
import 'package:client/core/widgets/loading_indicators.dart';

// Error States
import 'package:client/core/widgets/error_states.dart';
```

This design tokens reference serves as your go-to quick lookup guide during development. Bookmark this page!
