# Complete Design System Documentation - Astrology App

**Last Updated:** November 2024
**Framework:** Flutter with Material Design 3
**Design Philosophy:** Cosmic Mysticism Meets Modern Minimalism

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Sizing](#spacing--sizing)
5. [Components](#components)
6. [Animations & Interactions](#animations--interactions)
7. [Accessibility Standards](#accessibility-standards)
8. [Implementation Guidelines](#implementation-guidelines)

---

## Design Philosophy

### Core Theme: "Cosmic Mysticism Meets Modern Minimalism"

The design system creates a spiritual, trustworthy, and enchanting experience that feels both ancient and cutting-edge. The app transports users to a cosmic realm while maintaining absolute clarity and usability.

**Design Pillars:**
1. **Mystical Yet Approachable** - Spiritual without intimidation
2. **Clarity First** - Cosmic theme never compromises information clarity
3. **Depth & Dimension** - Gradients, shadows, and layering create cosmic depth
4. **Smooth & Magical** - Every interaction feels intentional and enchanting
5. **Trust & Credibility** - Professional design that inspires confidence

**Design Values:**
- Use generous spacing for breathable layouts
- Apply purple/indigo gradients for mystical elements
- Include subtle animations for magical feel
- Maintain high contrast for readability
- Support both light and dark modes (dark mode default)
- Keep interfaces clean, never cluttered

---

## Color System

### Color Architecture

The color system uses a Material Design 3 compliant approach with cosmic-inspired palettes.

#### Primary Color Palette: Deep Space Purple

**Primary Colors:**
```
Primary:
- #6366F1 (Indigo) - Main brand color
- Light: #818CF8
- Dark: #4F46E5
Usage: CTA buttons, links, primary actions, highlights
```

**Secondary Colors:**
```
Secondary:
- #DB7093 (Pale Violet Red) - Accent color
- Light: #E591AB
- Dark: #C5637A
Usage: Secondary actions, love/relationships, accents
```

**Tertiary (Sun):**
```
- #FFD700 (Gold) - Special highlights, premium features
Usage: Important indicators, premium badges, special elements
```

### Complete Color Palette

#### Light Mode Colors

**Surfaces:**
- Background: #FAFAFC (Soft white)
- Surface: #FFFFFF (Pure white)
- Surface Variant: #F3F4F6 (Light gray)
- Container: N/A (use Surface)

**Text Colors:**
- Primary: #1F2937 (Very dark gray) - Main text
- Secondary: #6B7280 (Medium gray) - Supporting text
- Tertiary: #9CA3AF (Light gray) - Disabled/hints

**Borders & Dividers:**
- Border: #E0E0EA (Light borders)
- Outline: #BABABF (Subtle outlines)

#### Dark Mode Colors (Default)

**Surfaces:**
- Background: #0F0F23 (Deep navy)
- Surface: #1A1A2E (Dark navy)
- Surface Variant: #252538 (Darker navy)
- Container: #2A2A3E (Elevated surfaces)

**Text Colors:**
- Primary: #F0F0F5 (Almost white)
- Secondary: #B0B0C0 (Light gray)
- Tertiary: #7C7C8F (Medium gray)

**Borders & Dividers:**
- Border: #3A3A58 (Dark borders)
- Outline: #4A4A68 (Subtle outlines)

### Semantic Color Palette

**Planetary Colors** (for zodiac/planetary associations):
```
Sun:       #FFD700 (Gold)
Moon:      #F0F0F5 (Silver)
Mars:      #EF4444 (Red)
Mercury:   #9CA3AF (Gray)
Jupiter:   #F97316 (Orange)
Venus:     #4ADE80 (Green)
Saturn:    #3B82F6 (Blue)
Rahu:      #7C3AED (Purple)
Ketu:      #EC4899 (Pink)
```

**Element Colors** (for zodiac elements):
```
Fire (Aries, Leo, Sagittarius):
- Base: #FF6B6B (Red-orange)
- Light: #FFB4B4
- Dark: #CC5555

Earth (Taurus, Virgo, Capricorn):
- Base: #8B7355 (Brown)
- Light: #C4A77D
- Dark: #6B5840

Air (Gemini, Libra, Aquarius):
- Base: #FFD93D (Yellow)
- Light: #FFECA1
- Dark: #CCAE31

Water (Cancer, Scorpio, Pisces):
- Base: #6BCEFF (Blue)
- Light: #B4E7FF
- Dark: #56A5CC
```

**Status Colors:**
```
Success:  #10B981 (Green)
Warning:  #F59E0B (Amber)
Error:    #EF4444 (Red)
Info:     #3B82F6 (Blue)
Disabled: #D1D5DB (Gray)
```

### Gradient System

**Primary Cosmic Gradient** (mystical brand expression):
```dart
LinearGradient(
  begin: Alignment.topLeft,
  end: Alignment.bottomRight,
  colors: [
    Color(0xFF5B21B6), // Deep purple
    Color(0xFF8B5CF6), // Violet
    Color(0xFFC4B5FD), // Lavender
  ],
)
```

**Nebula Gradient** (special backgrounds, overlays):
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

**Sunset Gradient** (alternative brand expression):
```dart
LinearGradient(
  begin: Alignment.topLeft,
  end: Alignment.bottomRight,
  colors: [
    Color(0xFFFEA700), // Amber
    Color(0xFFFF6B6B), // Red
    Color(0xFFC71585), // Violet red
  ],
)
```

**Nebu la Gradient** (special sections):
```dart
LinearGradient(
  begin: Alignment.topCenter,
  end: Alignment.bottomCenter,
  colors: [
    Color(0xFF6366F1), // Indigo
    Color(0xFFDB7093), // Pale violet red
    Color(0xFFF97316), // Orange
  ],
)
```

### Color Usage Guidelines

**Primary (#6366F1):**
- Call-to-action buttons
- Links and interactive elements
- Focus states and active indicators
- Primary brand expression

**Secondary (#DB7093):**
- Secondary buttons and actions
- Love/relationships sections
- Accent highlights
- Alternative CTAs

**Tertiary/Sun (#FFD700):**
- Premium features
- Important achievements
- Special badges
- Highlight elements

**Semantic Colors:**
- Always use semantic colors for status
- Red for errors/warnings
- Green for success states
- Blue for informational content
- Amber for cautions

**Gradients:**
- Use cosmic gradient for hero sections
- Use nebula gradient for background overlays
- Reserve sunset gradient for special features
- Never apply gradients to text (readability)

### Contrast & Accessibility

All color combinations meet WCAG 2.1 AA standards minimum:
- Text on background: 4.5:1 contrast ratio
- Large text (18pt+): 3:1 contrast ratio
- Interactive elements: 3:1 contrast ratio
- Focus indicators: Clearly visible at 2px width

---

## Typography

### Font Families & Usage

**Primary Font: Playfair Display** (Headlines, brand expression)
- Used for: H1-H5 headings, large displays
- Weights: 400, 600, 700 (Bold)
- Characteristics: Elegant, modern serif, mystical feel
- Letter spacing: 0.1-0.5px for headings

**Body Font: Lora** (Body text, long-form content)
- Used for: Body text, descriptions, interpretations
- Weights: 400, 500, 600
- Characteristics: High readability, elegant serifs, comfortable to read
- Letter spacing: 0.25-0.5px
- Line height: 1.5-1.8 for body text

**UI Font: Montserrat** (Labels, buttons, UI text)
- Used for: Button labels, chips, small labels, UI elements
- Weights: 500, 600
- Characteristics: Modern, geometric, clear hierarchy
- Letter spacing: 1.0-1.5px for labels

**Special Font: Noto Sans** (Zodiac glyphs, symbols)
- Used for: Zodiac symbols, planetary glyphs
- Weights: 400, 600
- Characteristics: Comprehensive unicode support

### Type Scale & Sizes

#### Display Styles (Page Headers)

```
Display Large:
- Font Size: 32px
- Font Weight: Bold (700)
- Font Family: Playfair Display
- Line Height: 1.2 (38px)
- Letter Spacing: 0.5px
- Usage: Main page titles, hero sections

Display Medium:
- Font Size: 28px
- Font Weight: Bold (700)
- Font Family: Playfair Display
- Line Height: 1.3 (36px)
- Letter Spacing: 0.3px
- Usage: Large section headers

Display Small:
- Font Size: 24px
- Font Weight: Semi-bold (600)
- Font Family: Playfair Display
- Line Height: 1.3 (31px)
- Letter Spacing: 0.2px
- Usage: Section headers, prominent titles
```

#### Headline Styles (Section Headers)

```
Headline Large:
- Font Size: 22px
- Font Weight: Semi-bold (600)
- Font Family: Playfair Display
- Line Height: 1.4 (31px)
- Letter Spacing: 0.15px
- Usage: Card titles, major sections

Headline Medium:
- Font Size: 20px
- Font Weight: Semi-bold (600)
- Font Family: Playfair Display
- Line Height: 1.4 (28px)
- Letter Spacing: 0.15px
- Usage: Sub-section headers

Headline Small:
- Font Size: 18px
- Font Weight: Semi-bold (600)
- Font Family: Playfair Display
- Line Height: 1.4 (25px)
- Letter Spacing: 0.1px
- Usage: Feature titles, card headers
```

#### Body Styles (Content Text)

```
Body Large:
- Font Size: 16px
- Font Weight: Regular (400)
- Font Family: Lora
- Line Height: 1.6 (26px)
- Letter Spacing: 0.5px
- Usage: Main body text, long-form content

Body Medium:
- Font Size: 14px
- Font Weight: Regular (400)
- Font Family: Lora
- Line Height: 1.5 (21px)
- Letter Spacing: 0.25px
- Usage: Secondary text, descriptions

Body Small:
- Font Size: 12px
- Font Weight: Regular (400)
- Font Family: Lora
- Line Height: 1.5 (18px)
- Letter Spacing: 0.4px
- Usage: Captions, hints, small text
```

#### Label Styles (UI Labels)

```
Label Large:
- Font Size: 14px
- Font Weight: Medium (500)
- Font Family: Montserrat
- Line Height: 1.3 (18px)
- Letter Spacing: 1.25px
- Usage: Button text, form labels

Label Medium:
- Font Size: 12px
- Font Weight: Medium (500)
- Font Family: Montserrat
- Line Height: 1.3 (16px)
- Letter Spacing: 1.2px
- Usage: Secondary labels, badges

Label Small:
- Font Size: 10px
- Font Weight: Medium (500)
- Font Family: Montserrat
- Line Height: 1.2 (12px)
- Letter Spacing: 1.5px
- Usage: Small labels, overlines
```

#### Special Styles

```
Button Text:
- Font Size: 16px
- Font Weight: Semi-bold (600)
- Font Family: Montserrat
- Line Height: 1.2
- Letter Spacing: 0.5px

Zodiac Glyph:
- Font Size: 24px
- Font Weight: Regular (400)
- Font Family: Noto Sans

Zodiac Glyph Large:
- Font Size: 32px
- Font Weight: Regular (400)
- Font Family: Noto Sans

Interpretation (Mystical):
- Font Size: 15px
- Font Weight: Regular (400)
- Font Family: Lora
- Line Height: 1.7 (26px)
- Letter Spacing: 0.3px
- Font Style: Italic
- Usage: Horoscope readings, interpretations

Overline:
- Font Size: 10px
- Font Weight: Semi-bold (600)
- Font Family: Montserrat
- Line Height: 1.2
- Letter Spacing: 1.5px
- Usage: Category labels, section markers

Caption:
- Font Size: 12px
- Font Weight: Regular (400)
- Font Family: Lora
- Line Height: 1.4 (17px)
- Letter Spacing: 0.4px
- Usage: Metadata, small descriptions
```

### Typography Usage Hierarchy

1. **Display Styles** - Hero sections, page titles
2. **Headline Styles** - Section and card headers
3. **Body Styles** - Primary content and descriptions
4. **Label Styles** - UI labels, buttons, small elements
5. **Special Styles** - Zodiac, interpretations, emphasis

### Typography Best Practices

- Display fonts should not have more than 8 words per line
- Body text should have 50-75 characters per line for optimal readability
- Line height should be 1.5 minimum for body text (1.6-1.8 preferred)
- Never use all-caps for body text (only labels and overlines)
- Maintain consistent letter spacing within each style
- Use font weights strategically: 400 for body, 600+ for emphasis

---

## Spacing & Sizing

### Spacing System: 8-Point Grid

All spacing and sizing follows an 8-point grid system for consistency and mathematical harmony.

#### Spacing Scale

```dart
class AppSpacing {
  static const double xs = 4.0;      // Extra small - tight spacing
  static const double sm = 8.0;      // Small - padding around elements
  static const double md = 16.0;     // Medium - standard padding (most common)
  static const double lg = 24.0;     // Large - section spacing
  static const double xl = 32.0;     // Extra large - major sections
  static const double xxl = 48.0;    // 2x Extra large - hero sections
  static const double xxxl = 64.0;   // 3x Extra large - onboarding
}
```

#### Spacing Usage Guidelines

| Size | Pixels | Common Uses |
|------|--------|------------|
| **xxs** | 2px | Icon padding, microgaps |
| **xs** | 4px | Badge padding, tight spacing |
| **sm** | 8px | Button padding, list items, gaps |
| **md** | 16px | Card padding, general spacing (**most common**) |
| **lg** | 24px | Section spacing, large padding |
| **xl** | 32px | Screen padding, major sections |
| **xxl** | 48px | Between major components |
| **xxxl** | 64px | Hero sections, onboarding |

#### Pre-computed Padding Classes

```dart
// All directions
paddingXs   = 4px all
paddingSm   = 8px all
paddingMd   = 16px all (default card padding)
paddingLg   = 24px all
paddingXl   = 32px all
paddingXxl  = 48px all

// Horizontal padding
paddingHorizontalXs = 4px left/right
paddingHorizontalSm = 8px left/right
paddingHorizontalMd = 16px left/right
paddingHorizontalLg = 24px left/right
paddingHorizontalXl = 32px left/right

// Vertical padding
paddingVerticalXs = 4px top/bottom
paddingVerticalSm = 8px top/bottom
paddingVerticalMd = 16px top/bottom
paddingVerticalLg = 24px top/bottom
paddingVerticalXl = 32px top/bottom

// Directional padding
paddingTopSm    = 8px top
paddingTopMd    = 16px top
paddingTopLg    = 24px top
paddingTopXl    = 32px top
paddingBottomSm = 8px bottom
paddingBottomMd = 16px bottom
paddingBottomLg = 24px bottom
paddingBottomXl = 32px bottom
```

### Sizing System

#### Border Radius

```dart
class AppDimensions {
  static const double radiusXs = 4.0;      // Extra small
  static const double radiusSm = 8.0;      // Small
  static const double radiusMd = 12.0;     // Medium (default)
  static const double radiusLg = 16.0;     // Large (cards)
  static const double radiusXl = 24.0;     // Extra large (modals)
  static const double radiusCircle = 999.0; // Circular
}
```

**Border Radius Usage:**
- Input fields: radiusMd (12px)
- Cards: radiusMd to radiusLg (12-16px)
- Buttons: radiusMd (12px)
- Modals: radiusXl (24px)
- Chips: radiusCircle (fully rounded)
- Bottom sheets: radiusXl top only

#### Icon Sizes

```dart
static const double iconXs = 16.0;    // Extra small - small badges
static const double iconSm = 20.0;    // Small - inline icons
static const double iconMd = 24.0;    // Medium - default icon size
static const double iconLg = 32.0;    // Large - prominent icons
static const double iconXl = 48.0;    // Extra large - feature icons
static const double iconXxl = 64.0;   // 2x Extra large - hero icons
```

**Icon Usage:**
- Inline with text: iconSm (20px)
- List/button icons: iconMd (24px)
- Card feature icons: iconLg (32px)
- Large buttons: iconXl (48px)
- Hero sections: iconXxl (64px)

#### Touch Target Sizes

```dart
static const double touchTargetMin = 48.0; // Minimum touch target
```

**Accessibility Requirements:**
- All interactive elements: minimum 48x48 logical pixels
- Recommended: 56x56 for ease of use
- Buttons: typically 48-56px height
- Icon buttons: 48x48 minimum

#### Component Dimensions

**Cards:**
- Elevation: 2.0 (standard), 8.0 (elevated)
- Max width: 400.0 (mobile optimized)
- Min height: 100.0 (ensure touch targets)

**AppBar:**
- Height: 56.0 (standard)
- Height (collapsed): 64.0 (with search)

**Bottom Navigation:**
- Height: 80.0 (includes padding)

**Input Fields:**
- Height: 56.0 (touch target minimum)
- Padding: 16.0 horizontal, 16.0 vertical

**Dialog:**
- Width: 320.0 (mobile optimized)

### Shadow System

The shadow system creates depth without harshness, fitting the cosmic aesthetic.

```dart
class AppDimensions {
  // Light shadow (cards, subtle elevation)
  static List<BoxShadow> shadowLight = [
    BoxShadow(
      color: Colors.black.withOpacity(0.05),
      blurRadius: 4,
      offset: Offset(0, 2),
    ),
  ];

  // Medium shadow (elevated cards, raised buttons)
  static List<BoxShadow> shadowMedium = [
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 8,
      offset: Offset(0, 4),
    ),
  ];

  // High shadow (floating elements, FABs)
  static List<BoxShadow> shadowHigh = [
    BoxShadow(
      color: Colors.black.withOpacity(0.15),
      blurRadius: 16,
      offset: Offset(0, 8),
    ),
  ];

  // Elevated shadow (modals, dialogs)
  static List<BoxShadow> shadowElevated = [
    BoxShadow(
      color: Colors.black.withOpacity(0.2),
      blurRadius: 24,
      offset: Offset(0, 12),
    ),
  ];
}
```

**Shadow Usage:**
- Level 0: No shadow (flat surfaces)
- Level 1: shadowLight (standard cards)
- Level 2: shadowMedium (active/hovered cards, buttons)
- Level 3: shadowHigh (floating elements, FABs)
- Level 4: shadowElevated (modals, dialogs)

### Spacing Examples

**Card Layout:**
```
padding: 16px (md)
gap between elements: 8-16px (sm-md)
border-radius: 12px (radiusMd)
box-shadow: shadowLight
```

**Button Layout:**
```
horizontal padding: 24px (lg)
vertical padding: 12px (md - 4px)
min height: 48px (touchTargetMin)
border-radius: 12px (radiusMd)
icon padding: 8px (sm)
```

**List Item:**
```
padding: 16px (md)
gap between icon/text: 16px (md)
item spacing: 8px (sm) or 0 with divider
```

**Section Spacing:**
```
section margin: 24px (lg)
section title padding: 16px (md)
content padding: 16px (md)
```

---

## Components

### Button Component Family

All buttons use Material Design 3 specifications with cosmic styling adjustments.

#### Primary Button (Filled)

**Purpose:** Main call-to-action, primary user actions like "Login", "Generate Chart", "Save"

**Visual Properties:**
- Background: Primary color (#6366F1)
- Text: White
- Height: 56px minimum (48px acceptable)
- Padding: 24px horizontal, 12px vertical
- Border Radius: 12px (radiusMd)
- Text Style: Button text (16px, 600 weight, Montserrat)
- Shadow: No shadow (elevation 0) or shadowLight on hover
- Disabled state: Gray background, reduced opacity

**Implementation:**
```dart
ElevatedButton(
  style: ElevatedButton.styleFrom(
    backgroundColor: AppColors.primary,
    foregroundColor: Colors.white,
    padding: EdgeInsets.symmetric(
      horizontal: AppSpacing.lg,
      vertical: 12,
    ),
    minimumSize: Size.fromHeight(AppDimensions.touchTargetMin),
    shape: RoundedRectangleBorder(
      borderRadius: AppDimensions.borderRadiusMd,
    ),
  ),
  onPressed: () {},
  child: Text('Action'),
)
```

**Available States:**
- **Default:** Primary color background, white text
- **Hover:** Slight elevation (shadowLight), subtle scale (0.98)
- **Active/Pressed:** Scale to 0.95
- **Disabled:** Gray background (disabled color), 50% opacity
- **Loading:** Shows centered spinner, disabled interaction

**Usage Patterns:**
- Use one primary button per screen maximum
- Position at bottom or top-right
- Full width on mobile (match container width)
- Icon + label for additional context

#### Secondary Button (Outlined)

**Purpose:** Secondary actions, alternatives to primary like "Cancel", "Learn More"

**Visual Properties:**
- Background: Transparent
- Border: 2px secondary color (#DB7093)
- Text: Secondary color
- Height: 56px minimum
- Padding: 24px horizontal, 10px vertical
- Border Radius: 12px (radiusMd)
- Text Style: Button text (secondary color)

**Implementation:**
```dart
OutlinedButton(
  style: OutlinedButton.styleFrom(
    foregroundColor: AppColors.secondary,
    side: BorderSide(color: AppColors.secondary, width: 2),
    padding: EdgeInsets.symmetric(
      horizontal: AppSpacing.lg,
      vertical: 10,
    ),
    minimumSize: Size.fromHeight(AppDimensions.touchTargetMin),
    shape: RoundedRectangleBorder(
      borderRadius: AppDimensions.borderRadiusMd,
    ),
  ),
  onPressed: () {},
  child: Text('Secondary'),
)
```

**Usage Patterns:**
- Pair with primary button for dual actions
- Cancellation, rejection actions
- Alternative paths through flows

#### Text Button

**Purpose:** Tertiary actions, less important flows like "Skip", "Forgot Password?"

**Visual Properties:**
- Background: Transparent
- Text: Primary color
- Padding: 16px horizontal, 8px vertical (smaller than others)
- No border or shadow
- Text Style: labelLarge in primary color

**Implementation:**
```dart
TextButton(
  style: TextButton.styleFrom(
    foregroundColor: AppColors.primary,
    padding: EdgeInsets.symmetric(
      horizontal: AppSpacing.lg,
      vertical: 8,
    ),
  ),
  onPressed: () {},
  child: Text('Text Action'),
)
```

**Usage Patterns:**
- Secondary navigation
- Less critical actions
- Inline with content

#### Icon Button

**Purpose:** Small action buttons with icons (48x48 minimum)

**Visual Properties:**
- Background: primaryContainer color
- Icon: primary color
- Size: 48x48 (touchTargetMin)
- Shape: Circular (radiusCircle)
- Tooltip: Always include for accessibility

**Implementation:**
```dart
Container(
  width: 48,
  height: 48,
  decoration: BoxDecoration(
    color: Theme.of(context).colorScheme.primaryContainer,
    borderRadius: BorderRadius.circular(24),
  ),
  child: IconButton(
    icon: Icon(Icons.add),
    color: AppColors.primary,
    onPressed: () {},
    tooltip: 'Add new',
  ),
)
```

#### Chip/Filter Button

**Purpose:** Category selection, filter tags, small toggleable buttons

**Visual Properties:**
- Unselected: surfaceVariant background, outline border
- Selected: primary background, white text
- Height: 32px (smaller touch target)
- Padding: 12px horizontal
- Border Radius: radiusCircle (fully rounded)
- Icon: Optional leading icon (16-18px)

**Implementation:**
```dart
FilterChip(
  label: Text('Category'),
  selected: isSelected,
  onSelected: (_) {},
  backgroundColor: Theme.of(context).colorScheme.surfaceVariant,
  selectedColor: AppColors.primary,
  avatar: Icon(Icons.check, size: 16),
)
```

#### Gradient Button (Special)

**Purpose:** Premium features, special actions needing visual emphasis

**Visual Properties:**
- Background: Cosmic gradient or custom gradient
- Text: White
- Height: 56px
- Border Radius: 12px (radiusMd)
- Shadow: shadowLight or shadowMedium

**Implementation:**
```dart
Container(
  decoration: BoxDecoration(
    gradient: AppColors.cosmicGradient,
    borderRadius: BorderRadius.circular(12),
  ),
  child: Material(
    color: Colors.transparent,
    child: InkWell(
      onTap: () {},
      child: Center(
        child: Text('Premium Action'),
      ),
    ),
  ),
)
```

#### Floating Action Button (FAB)

**Purpose:** Primary contextual action in screens

**Visual Properties:**
- Background: Primary color
- Icon: White
- Size: 56x56 (standard), 48x48 (compact)
- Shape: Circular
- Shadow: shadowHigh
- Position: Bottom-right corner, 16px margin

**Implementation:**
```dart
FloatingActionButton(
  backgroundColor: AppColors.primary,
  onPressed: () {},
  tooltip: 'Add',
  child: Icon(Icons.add),
)
```

### Card Component Family

Cards are fundamental containers for content organization.

#### Base Custom Card

**Purpose:** Standard content container with consistent styling

**Visual Properties:**
- Background: Surface color
- Border Radius: 12px (radiusMd)
- Padding: 16px (md) default
- Shadow: shadowLight (elevation 2)
- Border: Optional subtle border

**Implementation:**
```dart
Card(
  elevation: 2,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
  ),
  color: Theme.of(context).colorScheme.surface,
  child: Padding(
    padding: AppSpacing.paddingMd,
    child: child,
  ),
)
```

**Variants:**
- **Flat:** No elevation, no shadow
- **Elevated:** shadowMedium, used on hover/interaction
- **With Border:** Subtle 1px border in outline color

#### Info Card

**Purpose:** Display information with icon and title/description

**Anatomy:**
- Leading icon (32px, primary color)
- Title (headlineSmall)
- Description (bodySmall, max 2 lines)
- Optional trailing chevron (if tappable)
- 16px gap between elements

**Usage:**
- Feature highlights
- Information blocks
- Tappable to navigate

#### Stat Card

**Purpose:** Display metrics, scores, ratings with optional progress

**Anatomy:**
- Label (bodyMedium, top)
- Large value (displaySmall, highlighted color)
- Optional unit (bodyMedium, smaller)
- Optional progress bar (below value)
- Icon optional (trailing or in value)

**Examples:**
- Compatibility score: "92%"
- Strength rating: "Strong"
- Count display: "7 planets"

#### Gradient Card

**Purpose:** Eye-catching feature cards with visual emphasis

**Visual Properties:**
- Background: Cosmic or custom gradient
- Shadow: shadowMedium or shadowHigh
- Padding: 24px (lg)
- Border Radius: 16px (radiusLg)
- Content: Typically centered, white text

**Usage:**
- Premium features
- Special offerings
- Brand messaging
- Hero sections

#### Feature Card

**Purpose:** Showcase features with large icons and titles

**Anatomy:**
- Large icon (48px)
- Title (headlineSmall, centered)
- Optional subtitle (bodySmall, centered)
- Clickable area

**Size:** Usually in grid layout (2-3 columns)

#### List Item Card

**Purpose:** Items in scrollable lists with consistent structure

**Anatomy:**
- Leading element (icon, avatar, 48x48)
- Title (bodyLarge, 600 weight)
- Optional subtitle (bodySmall, secondary color)
- Optional trailing element (icon, badge)
- 16px gaps

**Variations:**
- **Unselected:** Normal appearance
- **Selected:** primaryContainer background (50% opacity)
- **Hover:** Slight elevation (shadowMedium)

#### Empty State Card

**Purpose:** Display when no data available

**Anatomy:**
- Large icon (64px, onSurfaceVariant color with transparency)
- Title (headlineMedium)
- Message (bodyMedium)
- Optional action button

**Usage:**
- Empty lists
- No results
- First-time user experience

#### Highlight Card

**Purpose:** Draw attention to specific information (price, discount, special)

**Anatomy:**
- Title (bodyMedium, upper)
- Large value (displaySmall, accent color)
- Optional label (labelSmall, below value)
- Accent color highlighting

### Input Component Family

Form inputs with consistent styling and behavior.

#### Text Input Field (Custom)

**Purpose:** Standard text input for email, name, search, etc.

**Visual Properties:**
- Height: 56px (touchTargetMin)
- Background: surfaceVariant color
- Border: 1px outline, 2px on focus
- Border Radius: 12px (radiusMd)
- Padding: 16px horizontal, 16px vertical
- Label: Above input (labelLarge)
- Icon support: prefix and suffix icons

**Focus States:**
- Focused: 2px primary color border
- Error: Red border
- Disabled: 50% opacity, gray background

**Implementation:**
```dart
TextFormField(
  decoration: InputDecoration(
    filled: true,
    fillColor: Theme.of(context).colorScheme.surfaceVariant,
    labelText: 'Label',
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(color: AppColors.primary, width: 2),
    ),
    contentPadding: EdgeInsets.symmetric(
      horizontal: AppSpacing.md,
      vertical: AppSpacing.md,
    ),
  ),
)
```

#### Email Input Field

**Specialization:**
- Keyboard type: email
- Prefix icon: Icons.email_outlined
- Built-in validation (regex check)
- Error message: "Invalid email format"

#### Password Input Field

**Specialization:**
- Text obscured by default
- Suffix icon: visibility toggle (eye icon)
- Validation: Minimum 8 characters
- Error message: "Password too short"

#### Phone Number Input Field

**Specialization:**
- Keyboard type: phone
- Input formatting: digits only
- Prefix icon: Icons.phone_outlined
- Placeholder: "+1 (555) 000-0000"

#### Search Input Field

**Specialization:**
- Prefix icon: Icons.search
- Rounded border: radiusCircle (fully rounded, 24px radius)
- Suffix: Clear button (X icon) when text entered
- Placeholder: "Search..."

#### Date Picker Field

**Specialization:**
- Prefix icon: Icons.calendar_today
- Opens date picker on tap
- Format: YYYY-MM-DD
- Validation: Can set min/max dates
- Disabled interaction: Read-only

#### Dropdown/Select Field

**Specialization:**
- Dropdown arrow indicator
- Custom items list
- Validation support
- Hint text option

### Loading States

#### Shimmer Loading

**Purpose:** Skeleton screens while content loads

**Visual:**
- Sliding gradient effect (light to medium to light)
- Duration: 2 seconds (configurable)
- Colors: Adapted to light/dark theme
- Smooth, continuous loop

**Usage:**
- Placeholder for images
- Placeholder for text content
- Content preview while loading

#### Skeleton Loaders

**Variants:**
- **TextSkeleton:** 3 lines (configurable) simulating text paragraphs
- **CardSkeleton:** Image placeholder + text lines
- **SkeletonList:** Full list of skeleton items
- **SkeletonGrid:** Grid layout skeletons

**Properties:**
- Height: Customizable (lineHeight default 16px)
- Width: 100% or partial width for varied line lengths
- Border Radius: 8px (rounded appearance)

#### Loading Indicators

**Circular Progress:**
- Size: 48px (default, customizable)
- Stroke Width: 4px
- Color: Primary color (customizable)
- Optional label below (bodyMedium)

**Minimal Loader:**
- Size: 24px
- Stroke Width: 2px
- Used inline with text or in buttons

**Linear Progress Bar:**
- Height: 4px (customizable)
- Full width
- Foreground: Primary color
- Background: surfaceVariant

**Pulsing Loader:**
- Opacity animation (0.3 to 1.0)
- Duration: 1 second (configurable)
- Applied to any child widget
- Used for emphasis without blocking

### Error States

#### Error Message

**Purpose:** Inline error display (form validation, etc.)

**Visual:**
- Background: Error color with 10% opacity
- Border: 1px error color
- Icon: Error icon (left-aligned)
- Text: Error color
- Height: 40px (compact)
- Padding: 12px horizontal, 8px vertical

#### Error Card

**Purpose:** Larger error display with details and action

**Anatomy:**
- Icon (28px, error color)
- Title (bodyMedium, 600 weight, error color)
- Message (bodyMedium, onErrorContainer color)
- Optional action button (full-width primary button)
- Padding: 24px (lg)
- Border: 1px error color

#### Error State Screen

**Purpose:** Full-screen error display (network error, server error)

**Anatomy:**
- Large icon (64px, error color)
- Title (headlineMedium)
- Message (bodyMedium)
- Primary action button ("Retry", "Continue")
- Optional secondary button ("Cancel")
- Centered layout

**Usage:**
- Network failures
- Server errors
- Permission errors

#### Snackbars

**Error Snackbar:**
- Background: Error color
- Icon: Error outline
- Duration: 4 seconds
- Behavior: Floating (bottom with margin)
- Border Radius: 8px

**Success Snackbar:**
- Background: Success color (#10B981)
- Icon: Check circle outline
- Duration: 3 seconds

**Warning Snackbar:**
- Background: Warning color (#F59E0B)
- Icon: Warning outline
- Duration: 4 seconds

**Info Snackbar:**
- Background: Info color (#3B82F6)
- Icon: Info outline
- Duration: 3 seconds

**Implementation:**
```dart
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(
    content: Row(
      children: [
        Icon(Icons.error, color: Colors.white),
        SizedBox(width: 16),
        Expanded(child: Text('Error message')),
      ],
    ),
    backgroundColor: AppColors.error,
    behavior: SnackBarBehavior.floating,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(8),
    ),
  ),
)
```

#### Dialog Components

**Network Error Dialog:**
- Title: "Network Error"
- Message: Connection error explanation
- Actions: "Retry", "Cancel"

**Session Expired Dialog:**
- Title: "Session Expired"
- Message: Session timeout explanation
- Actions: "Log In"

---

## Animations & Interactions

### Animation Principles

**Duration Standards:**
```dart
class AppDurations {
  static const fast = Duration(milliseconds: 200);    // Micro-interactions
  static const normal = Duration(milliseconds: 300);  // Standard transitions
  static const slow = Duration(milliseconds: 500);    // Complex animations
}
```

**Easing Curves:**
```dart
class AppCurves {
  static const easeInOut = Curves.easeInOut;  // Default, natural motion
  static const easeOut = Curves.easeOut;      // Entering, appear animations
  static const easeIn = Curves.easeIn;        // Exiting, dismiss animations
  static const bounce = Curves.elasticOut;    // Delightful, playful
  static const cosmic = Cubic(0.4, 0.0, 0.2, 1.0); // Smooth, mystical
}
```

**Animation Guidelines:**
- All animations should run at 60fps minimum
- Durations: fast (200ms) for micro-interactions, normal (300ms) for page transitions
- Use easeInOut for most transitions (natural, polished feel)
- Test with Flutter DevTools to ensure performance

### Common Animation Types

#### Page Transitions

**Fade + Slide:**
- Duration: 300ms
- Curve: easeInOut
- Effect: Fade opacity while sliding up 50px
- Used for: Modal dialogs, bottom sheets

**Slide Transition:**
- Duration: 300ms
- Curve: easeOut
- Effect: Slide from right (entrance), to left (exit)
- Used for: Screen navigation

#### Card Reveal Animations

**Scale + Fade:**
- Duration: 200ms
- Curve: easeOut
- Effect: Scale from 0.9 to 1.0 while fading in
- Used for: Card lists, grid items

**Staggered Animation:**
- Delay: Increment by 50ms for each item
- Used for: List items revealing one by one

#### Button Interactions

**Press Animation:**
- Scale: 0.95 on press
- Duration: 100ms
- Curve: easeOut
- Feedback: Immediate visual response

**Hover Animation:**
- Elevation increase (shadowMedium)
- Duration: 200ms
- Curve: easeInOut
- Used for: Desktop/web applications

#### Loading State Animations

**Shimmer:**
- Duration: 2 seconds
- Curve: linear
- Effect: Sliding gradient across placeholder
- Continuous loop

**Pulsing:**
- Duration: 1 second
- Curve: easeInOut
- Effect: Opacity 0.3 to 1.0
- Repeat infinitely

**Rotating:**
- Duration: 2 seconds
- Curve: linear
- Effect: 360-degree rotation
- Used for: Loading spinners, planets

#### Special Animations

**Success Burst:**
- Duration: 500ms
- Curve: elasticOut
- Effect: Scale animation with slight bounce
- Used for: Successful action completion

**Error Shake:**
- Duration: 400ms
- Curve: easeInOut
- Effect: Horizontal translation (-10px, +10px, -10px)
- Used for: Form validation errors

**Zodiac Glyph Rotation:**
- Duration: 3 seconds
- Curve: linear
- Effect: Subtle 360-degree rotation
- Repeat infinitely
- Used for: Loading indicators, emphasis

### Interaction Patterns

#### Touch Feedback

**Press Feedback:**
- Scale to 0.95 on long press
- Color shift (slightly darker or lighter)
- Duration: 150-200ms

**Ripple Effect:**
- Material Design ripple (circular)
- Duration: 400ms
- Color: Primary color with 30% opacity

**Haptic Feedback:**
- Light feedback on interactions
- Use only for critical actions
- Not on every button press

#### Hover States (Web/Desktop)

**Button Hover:**
- Elevation increase
- Slight scale (1.02)
- Duration: 200ms

**Card Hover:**
- Elevation increase
- Slight scale (1.02)
- Optional border color change

#### Focus States (Keyboard Navigation)

**Focus Indicator:**
- 2px outline in primary color
- Should be visible at all times
- Not removed on mouse click

**Focus Ring:**
- Circular or rectangular outline
- Sufficient contrast ratio
- Platform-appropriate styling

---

## Accessibility Standards

### Color Contrast Requirements

All color combinations must meet WCAG 2.1 AA standards:

**Text Contrast:**
- Normal text (< 18px): 4.5:1 minimum
- Large text (18pt+ or 600+ weight): 3:1 minimum

**Interactive Elements:**
- Buttons, links: 3:1 minimum
- Icons: 3:1 minimum for meaningful graphics

**Verification:**
- Test all color combinations using WCAG contrast checker
- Test in both light and dark themes
- Verify with real users (color blindness simulation)

### Touch Targets

**Minimum Size:** 48x48 logical pixels (Material Design standard)
- All interactive elements must meet this requirement
- Buttons, links, icon buttons, checkboxes, etc.

**Spacing:** 8px minimum between adjacent touch targets
- Prevents accidental interaction
- Improves user experience for diverse hand sizes

**Test:** Use device with different hand sizes, test one-handed interaction

### Text Scaling

**Support Range:** 1.0x to 2.0x system text scaling
- Design responsive to text size changes
- Don't hardcode text sizes beyond 16px for body text
- Use scalable font sizes: small (12px), medium (14px), large (16px)

**Testing:**
- Test with 1.5x and 2.0x scaling
- Verify layout doesn't break or truncate
- Ensure still readable and usable

### Semantic Structure

**Semantic Labels:**
- All interactive elements must have labels
- Use Semantics widget appropriately
- Provide meaningful content descriptions

**Navigation Structure:**
- Clear heading hierarchy (h1 → h2 → h3, not h1 → h3)
- Logical tab order
- Skip navigation links for web

**Form Accessibility:**
- Each input has associated label
- Error messages linked to fields
- Form grouping where appropriate

### Screen Reader Support

**Content Descriptions:**
- Icons have descriptive labels
- Images have alt text
- Hidden decorative elements marked as such

**Semantic Widget Usage:**
```dart
Semantics(
  label: 'Save chart',
  child: IconButton(
    icon: Icon(Icons.save),
    onPressed: () {},
  ),
)
```

### Focus Management

**Keyboard Navigation:**
- All interactive elements focusable
- Visible focus indicators (2px outline)
- Logical tab order

**Focus First:**
- Design keyboard-first
- Test full interactions using keyboard only
- No keyboard traps

---

## Implementation Guidelines

### Using the Design System

#### 1. Always Use Design Tokens

**Colors:**
```dart
// Good - Use theme system
Color textColor = Theme.of(context).colorScheme.primary;

// Avoid - Hardcoded colors
Color textColor = Color(0xFF6366F1);
```

**Spacing:**
```dart
// Good
padding: AppSpacing.paddingMd

// Avoid
padding: EdgeInsets.all(16),
```

**Typography:**
```dart
// Good
style: AppTypography.bodyLarge

// Avoid
style: TextStyle(fontSize: 16, fontWeight: FontWeight.normal)
```

#### 2. Component Composition

**Build from Existing Components:**
```dart
// Good - Compose from existing component
MyCard(
  child: Column(
    children: [
      Text('Title', style: AppTypography.headlineSmall),
      Text('Description', style: AppTypography.bodyMedium),
    ],
  ),
)

// Avoid - Creating new component from scratch
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(...),
  child: Column(...),
)
```

#### 3. Responsive Design

**Mobile-First Approach:**
```dart
// Good - Mobile first, then enhance
if (MediaQuery.of(context).size.width > 768)
  // Tablet/desktop layout
else
  // Mobile layout

// Single column on mobile, 2+ columns on tablet
int crossAxisCount = context.isMobile ? 1 : 2;
```

#### 4. Theme Integration

**Always Reference Theme:**
```dart
// Good - Uses theme colors
Container(
  color: Theme.of(context).colorScheme.surface,
)

// Avoid - Hardcoded colors
Container(
  color: Color(0xFF1A1A2E),
)
```

#### 5. Animation Implementation

**Profile Before Shipping:**
```dart
// Always test with DevTools
// Target: 60fps minimum
// Durations: 200-500ms
// Curves: easeInOut as default
```

### File Organization

**Theme Files:**
```
lib/core/theme/
  ├── app_colors.dart       # Color definitions
  ├── app_typography.dart   # Font styles
  ├── app_spacing.dart      # Spacing/sizing system
  └── app_theme.dart        # Complete theme definitions
```

**Widget Files:**
```
lib/core/widgets/
  ├── buttons.dart            # All button variants
  ├── cards.dart              # All card variants
  ├── inputs.dart             # All input variants
  ├── loading_indicators.dart # Loading states
  ├── error_states.dart       # Error states
  └── index.dart              # Barrel export
```

**Screen Files:**
```
lib/presentation/screens/
  ├── auth/
  ├── dashboard/
  ├── charts/
  ├── horoscope/
  └── profile/
```

### Code Quality Checklist

Before committing UI code:

- [ ] Uses AppSpacing constants (no magic numbers)
- [ ] Uses AppColors or theme system (no hardcoded colors)
- [ ] Uses AppTypography or AppTextStyles (no raw TextStyle)
- [ ] Uses const constructors where possible
- [ ] No deeply nested widget trees (extracted components)
- [ ] All interactive elements have semantics/labels
- [ ] Touch targets are 48x48 minimum
- [ ] Tested on multiple screen sizes
- [ ] Animations tested for 60fps performance
- [ ] Contrast ratios verified (WCAG AA minimum)
- [ ] Works in both light and dark modes
- [ ] No console errors or warnings

### Common Pitfalls to Avoid

**Avoid:**
- Hardcoded colors, sizes, or strings
- Deeply nested widget trees without extraction
- setState() for complex state (use BLoC/Provider)
- Ignoring accessibility requirements
- Animations without purpose or performance testing
- Inconsistent component usage across screens
- Magic numbers instead of constants
- Ignoring design system documentation

**DO:**
- Extract widgets into separate, reusable components
- Use const constructors to reduce rebuilds
- Delegate state management properly
- Test with accessibility tools
- Reference design system for every decision
- Use naming conventions consistently
- Document complex widgets with examples
- Test in both light and dark modes

---

## Design System Constants Reference

### Quick Reference

**Colors:**
- Primary: `#6366F1` (AppColors.primary)
- Secondary: `#DB7093` (AppColors.secondary)
- Success: `#10B981` (AppColors.success)
- Error: `#EF4444` (AppColors.error)
- Warning: `#F59E0B` (AppColors.warning)

**Spacing:** 4px, 8px, 16px, 24px, 32px, 48px, 64px

**Border Radius:** 4px, 8px, 12px, 16px, 24px (or circular)

**Font Families:**
- Headlines: Playfair Display
- Body: Lora
- UI: Montserrat

**Shadows:** Light, Medium, High, Elevated (4 levels)

**Animation Durations:** 200ms (fast), 300ms (normal), 500ms (slow)

---

## Related Documentation

- **Design System (Original):** `/docs/design/design-system.md`
- **UI Mockups:** `/docs/design/ui-mockups.md`
- **Color Palette Details:** `/docs/design/color-palette.md`
- **Component Library:** `client/lib/core/widgets/` directory
- **Theme Configuration:** `client/lib/core/theme/` directory

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 2024 | Initial complete documentation |

---

**Last Review:** November 21, 2024
**Next Review:** Quarterly or when design changes are made

This design system document serves as the source of truth for all UI/UX decisions in the Astrology App. All team members should reference this document when making design decisions, implementing components, or reviewing code.
