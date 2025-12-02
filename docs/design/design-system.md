# Design System - Astrology App

## Design Philosophy

### Theme: "Cosmic Mysticism Meets Modern Minimalism"

**Core Concept:** Create a spiritual, trustworthy, and enchanting experience that feels both ancient and cutting-edge. The app should transport users to a cosmic realm while maintaining clarity and usability.

**Design Pillars:**
1. **Mystical Yet Approachable** - Spiritual without being intimidating
2. **Clarity First** - Despite cosmic theme, information must be crystal clear
3. **Depth & Dimension** - Use gradients, shadows, and layers for cosmic depth
4. **Smooth & Magical** - Every interaction feels intentional and enchanting
5. **Trust & Credibility** - Professional design that inspires confidence

---

## Color System

### Primary Color Palette: "Cosmic Purple"

Based on extensive research of successful astrology apps (Co-Star, Sanctuary, The Pattern), purple/indigo themes dominate as they represent:
- Spirituality and mysticism
- Intuition and the subconscious
- Cosmic energy and the universe
- Pisces symbolism (mystical water sign)

#### Main Colors:

**Primary - Deep Space Purple**
```
Light Mode:
- Primary 900: #1F1B79 (Lucky Point) - Main brand color
- Primary 700: #492C9B (Daisy Bush) - Interactive elements
- Primary 500: #7F4BAF (Studio) - Highlights
- Primary 300: #A680DB (Lavender) - Accents
- Primary 100: #E4B3FF (Mauve) - Subtle backgrounds

Dark Mode (Recommended Default):
- Primary 900: #0D0B2E (Deeper space)
- Primary 700: #1F1B79 (Lucky Point)
- Primary 500: #492C9B (Daisy Bush)
- Primary 300: #7F4BAF (Studio)
- Primary 100: #A680DB (Lavender)
```

**Secondary - Cosmic Accent Colors**
```
Moonlight Silver: #C4C4D9 - For text, icons
Stardust Gold: #FFD700 - Special highlights, premium features
Nebula Pink: #E91E63 - Love/relationships sections
Mars Red: #D32F2F - Warnings, important alerts
Jupiter Blue: #1976D2 - Career/success indicators
Venus Green: #4CAF50 - Health, growth, success states
```

**Neutral Grays (Dark Theme)**
```
Surface Colors:
- Background: #0A0A14 (Deep space black)
- Surface: #1A1A2E (Card backgrounds)
- Surface Elevated: #252541 (Elevated cards)
- Border: #3A3A58 (Dividers, borders)

Text Colors:
- Primary Text: #FFFFFF (Pure white)
- Secondary Text: #B0B0C8 (Muted lavender-gray)
- Disabled Text: #6A6A88 (Very muted)
- Hint Text: #4A4A68 (Subtle hints)
```

**Neutral Grays (Light Theme - Optional)**
```
Surface Colors:
- Background: #F5F5FA (Soft lavender white)
- Surface: #FFFFFF (Pure white)
- Surface Elevated: #FAFAFE (Slightly tinted)
- Border: #E0E0EA (Light borders)

Text Colors:
- Primary Text: #1A1A2E (Dark blue-black)
- Secondary Text: #5A5A78 (Medium gray)
- Disabled Text: #9A9AAF (Light gray)
- Hint Text: #BABABF (Very light gray)
```

### Semantic Colors

**Status & Feedback**
```
Success: #4CAF50 (Venus Green)
Warning: #FFC107 (Amber)
Error: #F44336 (Red-orange)
Info: #2196F3 (Blue)
```

**Zodiac Element Colors**
```
Fire Signs (Aries, Leo, Sagittarius): #FF6B6B (Warm red-orange)
Earth Signs (Taurus, Virgo, Capricorn): #8D6E63 (Rich brown)
Air Signs (Gemini, Libra, Aquarius): #64B5F6 (Sky blue)
Water Signs (Cancer, Scorpio, Pisces): #4DB6AC (Teal)
```

---

## Typography

### Font Families

**Primary Font: Poppins** (Modern, clean, geometric)
- Use for: Headlines, buttons, navigation
- Weights: 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)
- Why: Modern, readable, supports multiple languages, friendly yet professional

**Secondary Font: Inter** (Highly legible body text)
- Use for: Body text, descriptions, long-form content
- Weights: 400 (Regular), 500 (Medium), 600 (SemiBold)
- Why: Excellent readability, optimized for screens

**Accent Font: Cinzel** (Elegant, mystical)
- Use for: Special headers, zodiac sign names, mystical elements
- Weights: 400 (Regular), 600 (SemiBold), 700 (Bold)
- Why: Adds elegance and ancient mysticism without being hard to read

### Type Scale

```dart
// Font sizes in logical pixels
class AppTextStyles {
  // Headlines
  static const h1 = 32.0; // Page titles
  static const h2 = 28.0; // Section headers
  static const h3 = 24.0; // Sub-sections
  static const h4 = 20.0; // Card titles
  static const h5 = 18.0; // Small headers
  
  // Body
  static const bodyLarge = 16.0; // Main body text
  static const bodyMedium = 14.0; // Secondary text
  static const bodySmall = 12.0; // Captions, hints
  
  // Special
  static const button = 16.0; // Button text
  static const caption = 12.0; // Tiny text
  static const overline = 10.0; // Labels, tags
}

// Line heights (multipliers)
class AppLineHeights {
  static const tight = 1.2; // Headlines
  static const normal = 1.5; // Body text
  static const relaxed = 1.8; // Long-form reading
}

// Letter spacing
class AppLetterSpacing {
  static const tight = -0.5;
  static const normal = 0.0;
  static const wide = 0.5;
  static const wider = 1.0;
}
```

### Text Styles Implementation

```dart
class AppTextStyles {
  // Headlines (Poppins)
  static const h1 = TextStyle(
    fontFamily: 'Poppins',
    fontSize: 32,
    fontWeight: FontWeight.w700,
    height: 1.2,
    letterSpacing: -0.5,
  );
  
  static const h2Mystical = TextStyle(
    fontFamily: 'Cinzel',
    fontSize: 28,
    fontWeight: FontWeight.w600,
    height: 1.3,
    letterSpacing: 1.0,
  );
  
  // Body (Inter)
  static const bodyLarge = TextStyle(
    fontFamily: 'Inter',
    fontSize: 16,
    fontWeight: FontWeight.w400,
    height: 1.5,
    letterSpacing: 0.0,
  );
  
  static const bodyMedium = TextStyle(
    fontFamily: 'Inter',
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.5,
    letterSpacing: 0.0,
  );
  
  // Special
  static const zodiacLabel = TextStyle(
    fontFamily: 'Cinzel',
    fontSize: 14,
    fontWeight: FontWeight.w600,
    height: 1.3,
    letterSpacing: 1.5,
    textTransform: TextTransform.uppercase,
  );
}
```

---

## Spacing System

### Base Unit: 8px (Logical Pixels)

**Spacing Scale:**
```dart
class AppSpacing {
  static const xxs = 2.0;   // Micro spacing
  static const xs = 4.0;    // Extra small
  static const sm = 8.0;    // Small
  static const md = 16.0;   // Medium (base)
  static const lg = 24.0;   // Large
  static const xl = 32.0;   // Extra large
  static const xxl = 48.0;  // Double extra large
  static const xxxl = 64.0; // Triple extra large
}
```

**Usage Guidelines:**
- **xxs (2px):** Icon padding, tight spacing
- **xs (4px):** Badge spacing, chip padding
- **sm (8px):** Button padding, list item spacing
- **md (16px):** Card padding, general spacing (most common)
- **lg (24px):** Section spacing, large card padding
- **xl (32px):** Screen padding, major sections
- **xxl (48px):** Between major components
- **xxxl (64px):** Hero sections, onboarding

---

## Border Radius

### Radius Scale

```dart
class AppRadius {
  static const none = 0.0;
  static const sm = 8.0;    // Small elements
  static const md = 12.0;   // Cards, buttons
  static const lg = 16.0;   // Large cards
  static const xl = 24.0;   // Modal, bottom sheets
  static const full = 9999.0; // Circular elements
}
```

**Design Pattern:** Use larger radius (12-16px) to create soft, cosmic feel

---

## Shadows & Elevation

### Shadow System (Dark Theme)

```dart
class AppShadows {
  // Subtle glow effect for dark theme
  static const glow1 = BoxShadow(
    color: Color(0x1A7F4BAF), // 10% Primary 500
    blurRadius: 8,
    offset: Offset(0, 2),
  );
  
  static const glow2 = BoxShadow(
    color: Color(0x267F4BAF), // 15% Primary 500
    blurRadius: 16,
    offset: Offset(0, 4),
  );
  
  static const glow3 = BoxShadow(
    color: Color(0x337F4BAF), // 20% Primary 500
    blurRadius: 24,
    offset: Offset(0, 8),
  );
  
  // Cosmic purple glow
  static const cosmicGlow = [
    BoxShadow(
      color: Color(0x447F4BAF),
      blurRadius: 20,
      spreadRadius: 2,
    ),
  ];
}
```

**Elevation Levels:**
1. **Level 0:** Flat on background (no shadow)
2. **Level 1:** Cards (glow1)
3. **Level 2:** Raised buttons, active cards (glow2)
4. **Level 3:** Floating action buttons, dialogs (glow3)
5. **Special:** Mystical elements (cosmicGlow)

---

## Iconography

### Icon Style: "Cosmic Line Art"

**Guidelines:**
- Use outlined icons as default (not filled)
- 24x24dp standard size
- 2px stroke width for consistency
- Round line caps and joins
- Can add subtle gradients for special icons

**Icon Library:** Material Icons + Custom Cosmic Icons

**Custom Icon Categories:**
1. **Zodiac Symbols** - 12 sign glyphs
2. **Planetary Symbols** - Sun, Moon, planets
3. **Elements** - Fire, Earth, Air, Water
4. **Cosmic Elements** - Stars, constellations, phases
5. **Mystical** - Crystals, tarot cards, chakras

**Icon Colors:**
```dart
// Standard icons
Icon(
  Icons.home,
  color: AppColors.secondaryText,
  size: 24,
)

// Active/Selected icons
Icon(
  Icons.home,
  color: AppColors.primary500,
  size: 24,
)

// With gradient (special icons)
ShaderMask(
  shaderCallback: (bounds) => LinearGradient(
    colors: [AppColors.primary500, AppColors.nebulaPink],
  ).createShader(bounds),
  child: Icon(Icons.star, size: 24),
)
```

---

## Components

### Buttons

#### Primary Button
```dart
ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: AppColors.primary700,
    foregroundColor: Colors.white,
    elevation: 0,
    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
    shadowColor: AppColors.primary500.withOpacity(0.3),
  ),
  onPressed: () {},
  child: Text('Primary Action'),
)
```

#### Secondary Button (Outlined)
```dart
OutlinedButton(
  style: OutlinedButton.styleFrom(
    foregroundColor: AppColors.primary500,
    side: BorderSide(color: AppColors.primary500, width: 1.5),
    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
  onPressed: () {},
  child: Text('Secondary Action'),
)
```

#### Text Button
```dart
TextButton(
  style: TextButton.styleFrom(
    foregroundColor: AppColors.primary500,
    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
  ),
  onPressed: () {},
  child: Text('Text Action'),
)
```

### Cards

#### Standard Card
```dart
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: AppColors.surface,
    borderRadius: BorderRadius.circular(16),
    boxShadow: AppShadows.glow1,
    border: Border.all(
      color: AppColors.border.withOpacity(0.1),
      width: 1,
    ),
  ),
  child: child,
)
```

#### Elevated Card (Hover/Active)
```dart
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: AppColors.surfaceElevated,
    borderRadius: BorderRadius.circular(16),
    boxShadow: AppShadows.glow2,
    border: Border.all(
      color: AppColors.primary500.withOpacity(0.3),
      width: 1,
    ),
  ),
  child: child,
)
```

### Input Fields

```dart
TextField(
  decoration: InputDecoration(
    filled: true,
    fillColor: AppColors.surface,
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: AppColors.border),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: AppColors.border),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: AppColors.primary500, width: 2),
    ),
    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
  ),
)
```

---

## Visual Effects

### Gradients

**Primary Cosmic Gradient**
```dart
LinearGradient(
  begin: Alignment.topLeft,
  end: Alignment.bottomRight,
  colors: [
    Color(0xFF1F1B79), // Primary 900
    Color(0xFF492C9B), // Primary 700
    Color(0xFF7F4BAF), // Primary 500
  ],
)
```

**Nebula Gradient** (Special backgrounds)
```dart
RadialGradient(
  center: Alignment.topRight,
  radius: 1.5,
  colors: [
    Color(0xFF7F4BAF).withOpacity(0.3),
    Color(0xFF492C9B).withOpacity(0.1),
    Colors.transparent,
  ],
)
```

**Shimmer Effect** (Loading states)
```dart
LinearGradient(
  colors: [
    AppColors.surface,
    AppColors.surfaceElevated,
    AppColors.surface,
  ],
  stops: [0.0, 0.5, 1.0],
)
```

### Backdrop Blur

For modals, bottom sheets:
```dart
BackdropFilter(
  filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
  child: Container(
    color: Colors.black.withOpacity(0.5),
    child: child,
  ),
)
```

---

## Animation Guidelines

### Duration Standards
```dart
class AppDurations {
  static const fast = Duration(milliseconds: 200);
  static const normal = Duration(milliseconds: 300);
  static const slow = Duration(milliseconds: 500);
}
```

### Curves
```dart
class AppCurves {
  static const easeInOut = Curves.easeInOut;
  static const easeOut = Curves.easeOut;
  static const bounce = Curves.elasticOut;
  static const cosmic = Cubic(0.4, 0.0, 0.2, 1.0); // Custom smooth curve
}
```

### Common Animations
- **Page Transitions:** Fade + slide (300ms, easeInOut)
- **Card Reveal:** Scale from 0.9 to 1.0 (200ms, easeOut)
- **Button Press:** Scale to 0.95 (100ms, easeOut)
- **Shimmer:** Continuous slide animation (1500ms, linear)
- **Glow Pulse:** Opacity 0.5-1.0 (2000ms, easeInOut, repeat)

---

## Accessibility Standards

### Minimum Requirements:

1. **Color Contrast:**
   - Text: 4.5:1 (WCAG AA)
   - Large text (18pt+): 3:1
   - Interactive elements: 3:1

2. **Touch Targets:**
   - Minimum: 44x44 logical pixels
   - Recommended: 48x48 logical pixels

3. **Text Scaling:**
   - Support system text size (1.0x to 2.0x)
   - Test at 1.5x scaling minimum

4. **Semantic Labels:**
   - All interactive elements must have labels
   - Use Semantics widget appropriately

5. **Focus Indicators:**
   - Visible focus states for keyboard navigation
   - 2px outline in primary color

---

## Design Tokens (Summary)

```dart
class AppTheme {
  // Colors
  static const primary = Color(0xFF7F4BAF);
  static const background = Color(0xFF0A0A14);
  static const surface = Color(0xFF1A1A2E);
  
  // Typography
  static const fontFamily = 'Inter';
  static const headlineFont = 'Poppins';
  static const mysticalFont = 'Cinzel';
  
  // Spacing
  static const spacingUnit = 8.0;
  
  // Radius
  static const radiusMd = 12.0;
  static const radiusLg = 16.0;
  
  // Elevation
  static const elevationCard = 2.0;
  static const elevationDialog = 8.0;
}
```

---

## Best Practices

✅ **DO:**
- Use dark theme as default (cosmic aesthetic)
- Apply generous spacing for breathable layouts
- Use purple gradients for mystical elements
- Include subtle animations for magic feel
- Maintain high contrast for readability
- Test in both light and dark conditions

❌ **DON'T:**
- Overuse bright neon colors
- Create cluttered interfaces
- Use too many fonts (max 3 families)
- Ignore accessibility guidelines
- Apply excessive animations
- Use harsh shadows on dark backgrounds

---

**Design Review Checklist:**
- [ ] Uses approved color palette
- [ ] Typography follows scale
- [ ] Spacing uses 8px grid
- [ ] Border radius is consistent
- [ ] Meets accessibility standards
- [ ] Animations are smooth (60fps)
- [ ] Works in light AND dark mode
- [ ] Touch targets are 44px minimum
- [ ] Text has sufficient contrast
- [ ] Design feels "cosmic" yet clear

---

This design system creates a modern, mystical astrology experience that builds trust while maintaining usability. Every design decision should reference this document for consistency.