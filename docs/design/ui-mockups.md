# UI Mockups & Screen Layouts - Astrology App

## Document Purpose

This document provides **detailed screen-by-screen mockups** for the astrology app, including layout specifications, component placement, user flows, and interaction patterns. All designs follow the cosmic mysticism theme defined in `design-system.md`.

---

## Design Principles Recap

Before diving into mockups, remember these core principles:

1. **Cosmic Yet Clear** - Mystical aesthetics never compromise clarity
2. **Dark Theme First** - Deep space purple as the foundation
3. **Generous Spacing** - Use 8px grid, breathable layouts
4. **Smooth Transitions** - Every interaction feels magical
5. **Information Hierarchy** - Most important content stands out

---

## Screen Inventory

### **Core Screens (11 Total):**

1. Splash Screen
2. Onboarding Flow (3 screens)
3. Home/Dashboard
4. Daily Horoscope
5. Birth Chart
6. Compatibility Checker
7. Profile/Settings
8. Notifications
9. Premium/Upgrade
10. Chat with Astrologer (Optional)

---

# 1. SPLASH SCREEN

## Layout Specification

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│           [App Logo/Icon]           │  ← Centered, animated
│                                     │
│           [App Name]                │  ← Cinzel font, 28sp
│         "Your Cosmic Guide"         │  ← Tagline, 14sp
│                                     │
│                                     │
│         [Loading Indicator]         │  ← Cosmic spinner
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

### **Visual Details:**

**Background:**
- Gradient: Top → Bottom
  - Start: `#0A0A14` (Deep space)
  - Middle: `#1F1B79` (Primary 900)
  - End: `#0A0A14` (Deep space)
- Add subtle star particles (animated twinkling)

**App Logo/Icon:**
- Size: 120x120 dp
- Design: Cosmic mandala or stylized zodiac wheel
- Animation: Gentle pulsing glow effect (2s loop)
- Glow color: `#7F4BAF` (Primary 500)

**App Name:**
- Font: Cinzel Bold, 28sp
- Color: `#FFFFFF` (White)
- Letter spacing: 2.0
- Animation: Fade in after logo appears

**Tagline:**
- Font: Inter Regular, 14sp
- Color: `#A680DB` (Primary 300)
- Position: 8dp below app name

**Loading Indicator:**
- Custom cosmic spinner (rotating constellation)
- Size: 32x32 dp
- Color: Gradient purple to pink
- Position: 48dp from bottom

### **Behavior:**
- Duration: 2-3 seconds
- Auto-transition to Onboarding (first launch) or Home (returning user)
- Preload user data during splash

---

# 2. ONBOARDING FLOW (3 Screens)

## Screen 2.1: Welcome & Birth Date

```
┌─────────────────────────────────────┐
│  [Skip]                             │  ← Top-right, text button
│                                     │
│                                     │
│      [Cosmic Illustration]          │  ← 200x200 dp, animated
│         Zodiac Wheel                │
│                                     │
│    "Discover Your Cosmic Path"      │  ← H2, Poppins SemiBold
│                                     │
│   "Enter your birth details to      │  ← Body text, center
│   unlock personalized insights      │
│     from the cosmos"                │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  Birth Date: MM/DD/YYYY     │   │  ← Date picker input
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │    Continue   →             │   │  ← Primary button
│   └─────────────────────────────┘   │
│                                     │
│         ○ ● ○                       │  ← Progress dots
│                                     │
└─────────────────────────────────────┘
```

### **Component Details:**

**Skip Button:**
- Position: Top-right, 16dp padding
- Font: Inter Medium, 14sp
- Color: `#B0B0C8` (Secondary text)
- Action: Navigate to Home with limited features

**Illustration:**
- Cosmic zodiac wheel with subtle rotation animation
- Colors: Purple gradients with gold accents
- Size: 200x200 dp
- Margin top: 80dp

**Heading:**
- Font: Poppins SemiBold, 28sp
- Color: `#FFFFFF`
- Margin: 24dp top from illustration

**Body Text:**
- Font: Inter Regular, 16sp
- Color: `#B0B0C8`
- Alignment: Center
- Max width: 280dp
- Line height: 1.5

**Date Input Field:**
- Height: 56dp
- Border radius: 12dp
- Background: `#1A1A2E` (Surface)
- Border: 1dp, `#3A3A58`
- Focused border: 2dp, `#7F4BAF` (Primary 500)
- Icon: Calendar icon on the right
- Placeholder: "Select your birth date"
- Opens native date picker on tap

**Continue Button:**
- Width: Match parent - 32dp margin
- Height: 56dp
- Border radius: 12dp
- Background: Linear gradient
  - Start: `#492C9B`
  - End: `#7F4BAF`
- Text: "Continue", Poppins Medium, 16sp
- Color: `#FFFFFF`
- Shadow: Purple glow
- Disabled state: Gray, 40% opacity

**Progress Indicators:**
- 3 dots, 8dp each
- Active: `#7F4BAF`
- Inactive: `#3A3A58`
- Spacing: 8dp between
- Position: 24dp from bottom

---

## Screen 2.2: Birth Time & Location

```
┌─────────────────────────────────────┐
│  [Back]                    [Skip]   │
│                                     │
│                                     │
│      [Clock Illustration]           │  ← Cosmic clock animation
│                                     │
│    "Complete Your Birth Chart"      │
│                                     │
│   "Precise time and location help   │
│    us create your unique natal      │
│            chart"                   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  Birth Time: HH:MM AM/PM    │   │  ← Time picker
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  📍 Birth Location          │   │  ← Location search
│   │  [Search or use GPS]        │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │    Continue   →             │   │
│   └─────────────────────────────┘   │
│                                     │
│         ○ ● ○                       │
│                                     │
└─────────────────────────────────────┘
```

### **Component Details:**

**Back Button:**
- Position: Top-left
- Icon: Left arrow
- Size: 24x24 dp
- Color: `#B0B0C8`

**Clock Illustration:**
- Animated cosmic clock with moving hands
- Size: 180x180 dp
- Shows current time with celestial overlay

**Time Input:**
- Format: 12-hour with AM/PM
- Opens time picker wheel on tap
- Validation: Can't be future time

**Location Input:**
- Autocomplete search field
- GPS icon on right side
- Tap GPS icon: Auto-fill current location
- Shows city, state, country format
- Dropdown with search suggestions
- Required for accurate birth chart

**Note Text (Optional):**
- Font: Inter Regular, 12sp
- Color: `#6A6A88`
- Text: "Don't know exact time? That's okay, we'll estimate"
- Position: Below time input

---

## Screen 2.3: Preferences & Permissions

```
┌─────────────────────────────────────┐
│  [Back]                             │
│                                     │
│      [Notification Bell Icon]       │  ← Animated bell
│                                     │
│    "Stay Connected to Cosmos"       │
│                                     │
│   "Get daily insights and cosmic    │
│   updates tailored to you"          │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Daily Horoscope    [Toggle] │   │  ← ON by default
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Planetary Transits [Toggle] │   │  ← ON by default
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Moon Phases        [Toggle] │   │  ← OFF by default
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  Get Started   ✨           │   │  ← Primary button
│   └─────────────────────────────┘   │
│                                     │
│         ○ ○ ●                       │
│                                     │
└─────────────────────────────────────┘
```

### **Component Details:**

**Notification Icon:**
- Animated: Gentle swing + glow pulse
- Size: 120x120 dp
- Color: Gold gradient

**Preference Cards:**
- Height: 64dp each
- Background: `#1A1A2E`
- Border radius: 12dp
- Padding: 16dp
- Spacing: 12dp between cards

**Toggle Switches:**
- iOS-style switch
- ON: `#7F4BAF` with glow
- OFF: `#3A3A58`
- Thumb: White circle with shadow

**Labels:**
- Font: Poppins Medium, 16sp
- Color: `#FFFFFF`
- Sublabel: Inter Regular, 12sp, `#B0B0C8`

**Get Started Button:**
- Same style as Continue button
- Text: "Get Started" with sparkle emoji
- Action: Complete onboarding, navigate to Home
- Trigger: Request notification permission
- Success animation: Confetti burst

---

# 3. HOME/DASHBOARD SCREEN

## Layout Specification

```
┌─────────────────────────────────────┐
│  ☰                        🔔  👤    │  ← Header
│                                     │
│   ┌─────────────────────────────┐   │
│   │  "Good Morning, [Name]"     │   │  ← Greeting card
│   │  ⭐ Aries ⭐                │   │  ← User's sun sign
│   │  "Today's energy: ⚡⚡⚡"    │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  TODAY'S HOROSCOPE          │   │  ← Main card (large)
│   │  ────────────────           │   │
│   │  [Preview text 2 lines...]  │   │
│   │                             │   │
│   │  Read More →                │   │
│   └─────────────────────────────┘   │
│                                     │
│  Quick Actions ─────────────────    │  ← Section header
│                                     │
│  ┌──────┐  ┌──────┐  ┌──────┐      │  ← 3-column grid
│  │ 🌙   │  │ 💕   │  │ ⭐   │      │
│  │Birth │  │Compat│  │Transit│      │
│  │Chart │  │ility │  │      │      │
│  └──────┘  └──────┘  └──────┘      │
│                                     │
│  Explore More ──────────────────    │
│                                     │
│  [Horizontal scrolling cards]       │  ← Scroll cards
│  ┌───────┐ ┌───────┐ ┌───────┐     │
│  │ Moon  │ │Tarot  │ │ Lucky │     │
│  │Phases │ │Reading│ │Numbers│     │
│  └───────┘ └───────┘ └───────┘     │
│                                     │
└─────────────────────────────────────┘
```

### **Header Section:**

**Hamburger Menu (Left):**
- Icon: 3 horizontal lines
- Size: 24x24 dp
- Color: `#B0B0C8`
- Action: Open navigation drawer

**Notification Bell (Right):**
- Icon: Bell outline
- Badge: Red dot if unread (8dp circle)
- Color: `#B0B0C8`
- Action: Open notifications list

**Profile Icon (Right):**
- Size: 32x32 dp
- Circular avatar or zodiac symbol
- Border: 2dp, `#7F4BAF`
- Margin left: 16dp from bell

### **Greeting Card:**

**Dimensions:**
- Height: 140dp
- Margin: 16dp all sides
- Border radius: 16dp
- Background: Gradient card
  - Start: `#492C9B` (Dark purple)
  - End: `#7F4BAF` (Medium purple)
- Shadow: Purple glow (subtle)

**Content Layout:**
- Greeting: "Good Morning/Afternoon/Evening, [Name]"
  - Font: Poppins SemiBold, 20sp
  - Color: `#FFFFFF`
  - Dynamic based on time of day

- Zodiac Sign:
  - Icon + Text: "♈ Aries" (example)
  - Font: Cinzel Medium, 16sp
  - Color: `#FFD700` (Gold)
  - Centered, margin top: 8dp

- Energy Indicator:
  - Text: "Today's energy: ⚡⚡⚡"
  - Font: Inter Regular, 14sp
  - Color: `#E4B3FF`
  - Shows 1-5 lightning bolts based on astrological data

### **Today's Horoscope Card:**

**Dimensions:**
- Height: 180dp (collapsed), 300dp (expanded)
- Margin: 16dp horizontal, 8dp vertical
- Border radius: 16dp
- Background: `#1A1A2E` (Surface)
- Border: 1dp, `#3A3A58`
- Shadow: Subtle glow

**Header:**
- Title: "TODAY'S HOROSCOPE"
- Font: Poppins SemiBold, 14sp
- Letter spacing: 1.0
- Color: `#A680DB`
- Divider: 2dp height, `#7F4BAF`, 40dp width

**Preview Content:**
- First 2 lines of horoscope text
- Font: Inter Regular, 15sp
- Line height: 1.5
- Color: `#FFFFFF`
- Margin: 12dp top

**Read More Button:**
- Text: "Read More →"
- Font: Poppins Medium, 14sp
- Color: `#7F4BAF`
- Position: Bottom-right, 16dp padding
- Action: Expand card or navigate to full horoscope

**Expanded State:**
- Shows full horoscope text (scrollable)
- Category tabs: General, Love, Career, Health
- Swipeable between categories
- Close icon at top-right

### **Quick Actions Section:**

**Section Header:**
- Text: "Quick Actions"
- Font: Poppins SemiBold, 18sp
- Color: `#FFFFFF`
- Divider line: Full width, 1dp, `#3A3A58`
- Margin: 24dp top, 16dp horizontal

**Action Cards Grid:**
- 3 columns, equal width
- Spacing: 12dp between cards
- Each card height: 100dp

**Individual Action Card:**
```
┌──────────────────┐
│                  │
│     [Icon]       │  ← 48x48 dp, gradient fill
│      🌙          │
│                  │
│   Birth Chart    │  ← Label, 14sp
│                  │
└──────────────────┘
```

**Card Styling:**
- Background: `#1A1A2E`
- Border radius: 12dp
- Border: 1dp, `#3A3A58`
- Hover/Press: Scale to 0.95, add glow
- Padding: 12dp

**Icons:**
- Size: 48x48 dp
- Style: Gradient filled
- Colors: Purple to pink gradient
- Common icons:
  - 🌙 Birth Chart (crescent moon)
  - 💕 Compatibility (heart)
  - ⭐ Transits (sparkle/planet)

**Labels:**
- Font: Poppins Medium, 14sp
- Color: `#FFFFFF`
- Alignment: Center
- Margin top: 8dp from icon

### **Explore More Section:**

**Horizontal Scroll Cards:**
- Card size: 140x160 dp
- Spacing: 12dp between
- Padding: 16dp start, continuous scroll
- Snap to nearest card

**Individual Explore Card:**
```
┌──────────────┐
│   [Image]    │  ← Themed illustration
│              │
│  Moon Phases │  ← Title
│              │
└──────────────┘
```

**Card Design:**
- Background: `#1A1A2E`
- Border radius: 12dp
- Image: 140x100 dp (top portion)
- Title: Bottom section, 60dp
- Font: Poppins Medium, 14sp
- Padding: 12dp

**Content Options:**
1. Moon Phases (with current phase visual)
2. Tarot Reading (card deck image)
3. Lucky Numbers (mystical numbers)
4. Planetary Hours (clock visual)
5. Crystal Guide (crystal images)
6. Meditation (cosmic meditation visual)

---

# 4. DAILY HOROSCOPE SCREEN

## Layout Specification

```
┌─────────────────────────────────────┐
│  ← Daily Horoscope        🔖  ⋮     │  ← Header
│                                     │
│  ┌─────────────────────────────┐    │
│  │      ♈                      │    │  ← Large zodiac icon
│  │     ARIES                   │    │
│  │  March 21 - April 19        │    │
│  └─────────────────────────────┘    │
│                                     │
│  November 19, 2025                  │  ← Date
│  ────────────────                   │
│                                     │
│  [Tabs: General Love Career Health] │  ← Category tabs
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │  [Horoscope Reading Text]   │    │  ← Main content
│  │  Lorem ipsum dolor sit...   │    │  (Scrollable)
│  │                             │    │
│  │  Today, the cosmos align... │    │
│  │                             │    │
│  │  Your energy levels are...  │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Scores ────────────────            │
│                                     │
│  💕 Love        ████████  8/10      │  ← Score bars
│  💼 Career      ██████    6/10      │
│  🏃 Health      █████████ 9/10      │
│  💰 Finance     ███████   7/10      │
│                                     │
│  Lucky Attributes ──────────        │
│                                     │
│  🎨 Color: Purple                   │
│  🔢 Number: 7                       │
│  🌸 Stone: Amethyst                 │
│                                     │
│  ┌─────────────────────────────┐    │
│  │       Share Reading         │    │  ← Share button
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### **Header:**

**Back Button:**
- Icon: Left arrow
- Size: 24x24 dp
- Color: `#B0B0C8`

**Title:**
- Text: "Daily Horoscope"
- Font: Poppins SemiBold, 20sp
- Color: `#FFFFFF`

**Bookmark Icon:**
- Right side, before menu
- Outline when not saved
- Filled when saved
- Color: `#FFD700` (gold) when saved

**Menu (3 dots):**
- Opens options: Change date, View history, Settings

### **Zodiac Header Card:**

**Dimensions:**
- Height: 180dp
- Full width, margin: 16dp
- Border radius: 16dp
- Background: Gradient (zodiac-specific)
  - Aries: Red-orange gradient
  - Taurus: Green gradient
  - etc. (refer to zodiac element colors)

**Zodiac Symbol:**
- Size: 80x80 dp
- Center top, margin: 16dp from top
- Color: White with glow effect
- Animated: Gentle pulsing

**Sign Name:**
- Font: Cinzel Bold, 28sp
- Color: `#FFFFFF`
- Center aligned
- Letter spacing: 2.0

**Date Range:**
- Font: Inter Regular, 14sp
- Color: `#E4B3FF`
- Center aligned
- Margin: 4dp below sign name

### **Date Selector:**

**Current Date:**
- Font: Poppins Medium, 16sp
- Color: `#B0B0C8`
- Left aligned, 16dp margin

**Divider:**
- Height: 2dp
- Width: 60dp
- Color: `#7F4BAF`
- Margin: 4dp below text

**Navigation:**
- Left/Right arrows on sides (optional)
- Swipe left/right to change dates
- Date picker opens on tap

### **Category Tabs:**

**Tab Bar:**
- Height: 48dp
- Background: Transparent
- Horizontal scroll if needed

**Individual Tab:**
- Min width: 80dp
- Padding: 16dp horizontal, 12dp vertical
- Font: Poppins Medium, 14sp
- Inactive: `#6A6A88`
- Active: `#FFFFFF`
- Indicator: Bottom border, 3dp, `#7F4BAF`

**Tab Options:**
1. General (overview)
2. Love (relationships)
3. Career (work, success)
4. Health (wellness)

### **Reading Content Area:**

**Container:**
- Scrollable
- Padding: 20dp
- Background: `#1A1A2E`
- Border radius: 16dp
- Margin: 16dp horizontal

**Text Styling:**
- Font: Inter Regular, 16sp
- Line height: 1.6
- Color: `#FFFFFF`
- Paragraph spacing: 16dp

**Formatting:**
- First paragraph: Larger (18sp)
- Important phrases: Medium weight
- Smooth reading experience

### **Score Bars Section:**

**Section Header:**
- Text: "Scores"
- Font: Poppins SemiBold, 16sp
- Divider line below

**Score Item:**
```
💕 Love        ████████░░  8/10
```

**Layout:**
- Icon: 24x24 dp emoji
- Label: Poppins Medium, 14sp, `#FFFFFF`
- Bar: 
  - Width: Remaining space
  - Height: 8dp
  - Border radius: 4dp
  - Background: `#3A3A58`
  - Fill: Gradient based on category
    - Love: Pink-red
    - Career: Blue
    - Health: Green
    - Finance: Gold
- Score: "8/10", Inter Medium, 14sp
- Spacing: 12dp between items

### **Lucky Attributes:**

**Section Header:**
- Text: "Lucky Attributes"
- Font: Poppins SemiBold, 16sp

**Attribute Items:**
- Icon + Label + Value
- Icon: 20x20 dp emoji
- Label: Inter Medium, 14sp, `#B0B0C8`
- Value: Inter SemiBold, 14sp, `#FFFFFF`
- Spacing: 8dp vertical

**Examples:**
- 🎨 Color: Purple
- 🔢 Number: 7
- 🌸 Stone: Amethyst
- 🕐 Time: 3-5 PM
- 🌿 Element: Fire

### **Share Button:**

**Design:**
- Width: Match parent - 32dp margin
- Height: 56dp
- Border: 2dp, `#7F4BAF`
- Border radius: 12dp
- Background: Transparent
- Text: "Share Reading"
- Font: Poppins SemiBold, 16sp
- Color: `#7F4BAF`
- Margin: 24dp top

**Action:**
- Generate shareable image with reading
- Share via system share sheet

---

# 5. BIRTH CHART SCREEN

## Layout Specification

```
┌─────────────────────────────────────┐
│  ← Birth Chart           ⋮          │  ← Header
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │    [Natal Chart Visual]     │    │  ← Interactive chart
│  │         (Wheel)             │    │  (320x320 dp)
│  │                             │    │
│  │    [Zoom controls]          │    │
│  └─────────────────────────────┘    │
│                                     │
│  [Tabs: Planets Houses Aspects]     │  ← Category tabs
│                                     │
│  ┌─────────────────────────────┐    │
│  │  ☉ Sun in Aries (1st House)│    │  ← Scrollable list
│  │  Details: Leadership...     │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  ☽ Moon in Cancer (4th)     │    │
│  │  Details: Emotional...      │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  ☿ Mercury in Taurus (2nd)  │    │
│  │  Details: Communication...  │    │
│  └─────────────────────────────┘    │
│                                     │
│  [Load more...]                     │
│                                     │
│  ┌─────────────────────────────┐    │
│  │     Download Report         │    │  ← Action button
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### **Header:**

**Title:**
- Text: "Birth Chart"
- Subtitle: "[Name]'s Natal Chart"
- Birth details: "Born: Jan 15, 1990, 8:30 AM, New York"
- Font: Varies (see detail spec below)

**Menu:**
- Edit birth details
- View as table
- Share chart
- Print report

### **Chart Visual Section:**

**Natal Chart Wheel:**
- Size: 320x320 dp (responsive)
- Centered horizontally
- Background: Deep space (`#0A0A14`)
- Zodiac wheel with 12 houses
- Planet symbols at correct positions
- Aspect lines connecting planets
- Degree markers around edge

**Design Style:**
- Outer ring: Zodiac signs (colorful symbols)
- Middle ring: House numbers (1-12)
- Inner area: Planets connected by aspect lines
- Colors:
  - Zodiac signs: Traditional colors (Aries=Red, etc.)
  - Planets: Astronomical colors (Sun=Gold, Moon=Silver, etc.)
  - Aspects: 
    - Conjunction: Purple
    - Opposition: Red
    - Trine: Blue
    - Square: Orange
    - Sextile: Green

**Interactions:**
- Tap planet: Highlight and show info popup
- Pinch to zoom: Zoom in/out
- Drag: Pan around when zoomed
- Double tap: Reset zoom

**Zoom Controls:**
- Position: Bottom-right of chart
- Buttons: + and - (circular, 40dp)
- Background: `#1A1A2E`, 60% opacity
- Icons: White, 20dp

### **Info Popup (on tap):**

```
┌──────────────────┐
│  ☉ Sun          │
│  15° Aries      │
│  1st House      │
│                 │
│  Tap for more   │
└──────────────────┘
```

- Appears above tapped planet
- Arrow pointing to planet
- Quick info display
- Tap popup: Navigate to detailed view

### **Category Tabs:**

**Tab Options:**
1. **Planets** - All planetary positions
2. **Houses** - 12 houses and meanings
3. **Aspects** - Planet relationships

**Tab Design:**
- Same as Daily Horoscope tabs
- Indicator: `#7F4BAF` underline

### **Planets Tab Content:**

**Planet Card:**

```
┌─────────────────────────────────┐
│  ☉ SUN IN ARIES (1ST HOUSE)    │
│  ─────────────                  │
│  Position: 15°23' Aries         │
│                                 │
│  Interpretation:                │
│  Your core identity embodies... │
│  [Expandable text]              │
│                                 │
│  [Expand ▼]                     │
└─────────────────────────────────┘
```

**Card Styling:**
- Background: `#1A1A2E`
- Border radius: 12dp
- Padding: 16dp
- Margin: 12dp between cards
- Border: 1dp, `#3A3A58`

**Planet Symbol:**
- Size: 32x32 dp
- Color: Planet-specific (gold for sun, silver for moon, etc.)
- Inline with title

**Title:**
- Format: "[SYMBOL] [PLANET] IN [SIGN] ([HOUSE])"
- Font: Poppins SemiBold, 16sp
- Color: `#FFFFFF`

**Position:**
- Font: Inter Regular, 13sp
- Color: `#B0B0C8`
- Format: "15°23' Aries"

**Interpretation:**
- Font: Inter Regular, 15sp
- Line height: 1.5
- Color: `#FFFFFF`
- Initially: Show first 2 lines
- Expanded: Show full text (scrollable within card)

**Expand Button:**
- Text: "Expand ▼" / "Collapse ▲"
- Font: Poppins Medium, 14sp
- Color: `#7F4BAF`
- Margin: 8dp top

### **Houses Tab Content:**

**House Card:**

```
┌─────────────────────────────────┐
│  1ST HOUSE - SELF & IDENTITY    │
│  ─────────────                  │
│  Cusp: 0° Aries                 │
│  Ruler: Mars in 5th House       │
│                                 │
│  The first house represents...  │
│  [Interpretation text]          │
└─────────────────────────────────┘
```

**Similar styling as Planet cards**
- 12 house cards total
- Each with cusp degree and ruler info

### **Aspects Tab Content:**

**Aspect Card:**

```
┌─────────────────────────────────┐
│  ☉ SUN TRINE ☽ MOON            │
│  ─────────────                  │
│  120° - Harmonious aspect       │
│  ★★★★★ (Strong)                │
│                                 │
│  This trine creates harmony...  │
│  [Interpretation text]          │
└─────────────────────────────────┘
```

**Aspect Types:**
- Conjunction (0°): ⚬
- Opposition (180°): ⚹  
- Trine (120°): △
- Square (90°): □
- Sextile (60°): ⚹

**Orb Display:**
- Exact orb shown: "Within 3°"
- Strength: 1-5 stars
- Color-coded by type

### **Download Report Button:**

**Design:**
- Width: Match parent - 32dp
- Height: 56dp
- Background: Gradient (purple)
- Border radius: 12dp
- Text: "Download Full Report"
- Icon: Download arrow
- Margin: 24dp top & bottom

**Action:**
- Generate PDF report
- Include full chart image
- All interpretations
- Professional formatting
- Share or save to device

---

# 6. COMPATIBILITY CHECKER SCREEN

## Layout Specification

```
┌─────────────────────────────────────┐
│  ← Compatibility                    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │       💕                    │    │
│  │   Compatibility             │    │  ← Header card
│  │  "Find your cosmic match"   │    │
│  └─────────────────────────────┘    │
│                                     │
│  Your Details ──────────────────    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  ♈ [Your Name]              │    │  ← User card (editable)
│  │  Aries · Jan 15, 1990       │    │
│  └─────────────────────────────┘    │
│                                     │
│  Partner Details ────────────────    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  + Add Partner Details      │    │  ← Empty state
│  │    (Tap to enter)           │    │  OR
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │  ← Filled state
│  │  ♎ [Partner Name]           │    │
│  │  Libra · Sep 25, 1991       │    │
│  │  [Edit] [Clear]             │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Calculate Compatibility →  │    │  ← Action button
│  └─────────────────────────────┘    │
│                                     │
│                                     │
│  ─── OR ───                         │  ← Divider
│                                     │
│  ┌─────────────────────────────┐    │
│  │  💬 Past Compatibility      │    │  ← History
│  │     Checks                  │    │
│  │                             │    │
│  │  • [Name] - 85% - 3 days ago│    │
│  │  • [Name] - 72% - 1 week ago│    │
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### **Results Screen (After Calculation):**

```
┌─────────────────────────────────────┐
│  ← Compatibility Results     ⋮      │
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │       ♈    💕    ♎          │    │  ← Visual
│  │     [You]  ↔  [Partner]     │    │
│  │                             │    │
│  │         85%                 │    │  ← Score (huge)
│  │    ★★★★☆                   │    │  ← Star rating
│  │   "Excellent Match!"        │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  [Tabs: Overall Love Career Friend] │
│                                     │
│  Category Breakdown ────────────    │
│                                     │
│  💕 Romantic        ████████ 90%    │
│  💬 Communication   ███████  85%    │
│  🎯 Goals          ██████   75%    │
│  🤝 Trust          █████████ 95%    │
│                                     │
│  Key Insights ──────────────────    │
│                                     │
│  ✨ Strengths                       │
│  • Both value communication         │
│  • Complementary elements           │
│  • Strong emotional connection      │
│                                     │
│  ⚠️ Challenges                      │
│  • Different approaches to...       │
│  • Need compromise on...            │
│                                     │
│  Advice ────────────────────────    │
│                                     │
│  [Personalized compatibility        │
│   advice based on both charts...]  │
│                                     │
│  ┌─────────────────────────────┐    │
│  │      Share Results          │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │    Check New Compatibility  │    │
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### **Input Screen Details:**

**Header Card:**
- Height: 160dp
- Background: Gradient (pink-purple)
- Heart emoji: 60dp size, animated pulse
- Title: Cinzel SemiBold, 24sp
- Tagline: Inter Regular, 14sp

**User Card:**
- Shows current user's details
- Zodiac symbol (32dp) + Name
- Birth date and sign
- Tap to edit (opens birth details)
- Background: `#1A1A2E`

**Partner Input Card (Empty):**
- Dashed border: 2dp, `#7F4BAF`
- Center icon: + symbol, 48dp
- Text: "Add Partner Details"
- Background: `#1A1A2E`, 40% opacity

**Partner Input Card (Filled):**
- Same design as user card
- Edit button: Text button, top-right
- Clear button: X icon, top-right
- Shows entered partner details

**Calculate Button:**
- Full width, primary button style
- Gradient background
- Text: "Calculate Compatibility →"
- Disabled until partner details added
- Loading state: Spinner with "Analyzing..."

**History Section:**
- Collapsible list
- Shows last 5 compatibility checks
- Each item:
  - Partner name/sign
  - Percentage score
  - Time ago
  - Tap to view full results

### **Results Screen Details:**

**Score Card:**
- Height: 280dp
- Background: Gradient based on score
  - 80-100%: Green-gold gradient
  - 60-79%: Purple gradient
  - 40-59%: Blue gradient
  - <40%: Gray gradient
- Zodiac symbols: User's and Partner's (48dp each)
- Heart between: 40dp, animated
- Score: 72sp, bold, white
- Star rating: 5 stars, filled based on %
- Rating text: Based on score range
  - 90-100%: "Perfect Match!"
  - 80-89%: "Excellent Match!"
  - 70-79%: "Great Compatibility"
  - 60-69%: "Good Match"
  - 50-59%: "Moderate Compatibility"
  - <50%: "Challenging Match"

**Category Tabs:**
- Overall, Love, Career, Friendship
- Shows different aspects based on context

**Breakdown Bars:**
- Similar to daily horoscope scores
- 4-6 categories
- Gradient colors based on value
- Percentages on right

**Insights Sections:**
- Strengths: Checkmark icon (green)
- Challenges: Warning icon (amber)
- Bullet points, expandable
- Font: Inter Regular, 15sp

**Advice Section:**
- Personalized tips
- Based on both birth charts
- 2-3 paragraphs
- Scrollable

---

# 7. PROFILE/SETTINGS SCREEN

## Layout Specification

```
┌─────────────────────────────────────┐
│  ≡ Profile                          │
│                                     │
│  ┌─────────────────────────────┐    │
│  │                             │    │
│  │      [Profile Photo]        │    │  ← Avatar (100dp)
│  │                             │    │
│  │       [User Name]           │    │
│  │    ♈ Aries · Level 5 ⭐     │    │  ← Zodiac & level
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│  Birth Details ──────────────────   │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ 📅 January 15, 1990         │    │
│  │ 🕐 8:30 AM                  │    │
│  │ 📍 New York, NY, USA        │    │
│  │        [Edit]               │    │
│  └─────────────────────────────┘    │
│                                     │
│  Preferences ────────────────────   │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ 🔔 Notifications     >      │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ 🎨 App Theme         >      │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ 🌐 Language          >      │    │
│  └─────────────────────────────┘    │
│                                     │
│  Account ────────────────────────   │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ ⭐ Upgrade to Premium  >    │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ 👤 Account Settings    >    │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ ❓ Help & Support      >    │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ ℹ️ About               >    │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │      🚪 Sign Out            │    │  ← Danger zone
│  └─────────────────────────────┘    │
│                                     │
└─────────────────────────────────────┘
```

### **Profile Header Card:**

**Dimensions:**
- Height: 200dp
- Background: Gradient (user's zodiac color)
- Border radius: 16dp (bottom only)

**Avatar:**
- Size: 100x100 dp
- Circular
- Border: 4dp, white
- Shadow: Soft glow
- Tap to change: Opens photo picker
- Default: Zodiac symbol if no photo

**Name:**
- Font: Poppins SemiBold, 24sp
- Color: White
- Center aligned below avatar
- Editable (tap to edit inline)

**Zodiac & Level:**
- Font: Inter Medium, 14sp
- Color: `#E4B3FF`
- Format: "♈ Aries · Level 5 ⭐"
- Level based on app usage/engagement
- Center aligned

### **Birth Details Card:**

**Container:**
- Background: `#1A1A2E`
- Border radius: 12dp
- Padding: 16dp
- Margin: 16dp horizontal

**Detail Items:**
- Icon (20dp) + Label + Value
- Font: Inter Regular, 15sp
- Color: `#FFFFFF`
- Spacing: 12dp between items

**Edit Button:**
- Text button, bottom-right
- Opens edit modal
- Color: `#7F4BAF`

### **Settings Menu Items:**

**Standard Card:**
- Height: 56dp
- Background: `#1A1A2E`
- Border radius: 12dp
- Margin: 8dp vertical, 16dp horizontal
- Press: Scale 0.98, add shadow

**Content Layout:**
- Icon (24dp) left, 16dp margin
- Label: Poppins Medium, 16sp, `#FFFFFF`
- Chevron right (20dp) right, 16dp margin
- Divider: If multiple items in section

### **Menu Options:**

**Notifications:**
- Opens notification preferences
- Toggle for each notification type
- Time selector for daily reminders

**App Theme:**
- Dark (default)
- Light
- Auto (system)
- Preview shown

**Language:**
- List of supported languages
- Search functionality
- Current language checkmark

**Upgrade to Premium:**
- Special styling: Gold accent
- Badge: "Premium" label
- Opens upgrade flow

**Account Settings:**
- Email, password
- Privacy settings
- Data management

**Help & Support:**
- FAQs
- Contact support
- Video tutorials
- Community forum link

**About:**
- App version
- Terms of service
- Privacy policy
- Licenses
- Rate app

### **Sign Out Button:**

**Design:**
- Width: Match parent - 32dp
- Height: 56dp
- Background: Transparent
- Border: 2dp, `#F44336` (Error red)
- Border radius: 12dp
- Text: "🚪 Sign Out"
- Font: Poppins Medium, 16sp
- Color: `#F44336`
- Margin: 32dp top

**Action:**
- Confirmation dialog
- Clear local data
- Return to login/onboarding

---

# 8. ADDITIONAL SCREENS (Brief)

## 8.1 Notifications Screen

- List of all notifications
- Grouped by: Today, Yesterday, This Week
- Types: Daily horoscope, transits, moon phases
- Swipe to delete
- Mark all as read button
- Settings link

## 8.2 Premium/Upgrade Screen

- Hero section: Premium benefits
- Feature comparison: Free vs Premium
- Pricing cards: Monthly, yearly
- "Start Free Trial" CTA
- Testimonials section
- FAQ accordion
- Restore purchases button

## 8.3 Search/Explore Screen

- Search bar at top
- Recent searches
- Trending topics
- Categories:
  - Learn Astrology
  - Articles & Guides
  - Planetary Events
  - Community Posts
- Filter by category
- Bookmark articles

---

# Design Tokens Quick Reference

## Spacing
- **xs:** 4dp - Tight spacing
- **sm:** 8dp - Small spacing
- **md:** 16dp - Standard (most common)
- **lg:** 24dp - Section spacing
- **xl:** 32dp - Large gaps
- **xxl:** 48dp - Major sections

## Border Radius
- **sm:** 8dp - Small elements
- **md:** 12dp - Cards, buttons
- **lg:** 16dp - Large cards
- **xl:** 24dp - Modals

## Typography Sizes
- **H1:** 32sp - Page titles
- **H2:** 28sp - Section headers
- **H3:** 24sp - Sub-sections
- **H4:** 20sp - Card titles
- **Body Large:** 16sp - Main text
- **Body Medium:** 14sp - Secondary
- **Caption:** 12sp - Hints

---

# Interaction Patterns

## Touch Targets
- Minimum: 44x44 dp
- Recommended: 48x48 dp
- Comfortable spacing: 8dp between

## Press States
- Scale: 0.95-0.98
- Opacity: 0.6 for text buttons
- Shadow: Increase elevation
- Duration: 100ms

## Transitions
- Page: 300ms, easeInOut
- Card: 200ms, easeOut
- Micro: 150ms, ease

## Loading States
- Skeleton screens for content
- Spinners for actions
- Progress bars for processes
- Shimmer effect where appropriate

---

# Accessibility Notes

## Color Contrast
- Text on dark: 4.5:1 minimum
- Large text: 3:1 minimum
- Interactive elements: Clear focus states

## Touch Targets
- 44dp minimum
- 8dp spacing between
- Extended hit area if needed

## Screen Readers
- Meaningful labels
- Proper heading hierarchy
- Announce state changes

## Text Scaling
- Support 1x to 2x
- Test at 1.5x minimum
- Reflow layouts gracefully

---

# Responsive Breakpoints

## Mobile (Default)
- Width: 360-420 dp
- Single column layouts
- Bottom navigation
- Full-screen modals

## Tablet
- Width: 600-900 dp
- Two-column where appropriate
- Side navigation option
- Larger cards with more content

## Desktop (Future)
- Width: 900+ dp
- Multi-column layouts
- Persistent side navigation
- Richer visualizations

---

# Animation Specifications

## Entrance Animations
- Fade in: 200ms
- Slide up: 300ms + fade
- Scale in: 200ms, 0.9 to 1.0
- Stagger: 50ms delay between items

## Exit Animations
- Fade out: 150ms
- Slide down: 250ms + fade
- Scale out: 150ms, 1.0 to 0.95

## Continuous Animations
- Pulse: 2000ms, easeInOut, repeat
- Rotate: 1500ms, linear, repeat
- Shimmer: 1500ms, linear, repeat
- Float: 3000ms, easeInOut, repeat

---

# Component State Matrix

| Component | Default | Hover | Pressed | Disabled | Error |
|-----------|---------|-------|---------|----------|-------|
| Button | Solid | Shadow | Scale 0.95 | 40% opacity | Red border |
| Card | Subtle border | Glow | Scale 0.98 | Dimmed | Red accent |
| Input | Border | Blue border | Blue border | Gray | Red border |
| Toggle | Gray | Gray | - | Dimmed | - |

---

**END OF UI MOCKUPS DOCUMENT**

This comprehensive guide provides detailed specifications for every major screen in this astrology app. Use this document alongside `design-system.md` for complete implementation guidance.

**Remember:** These are blueprints. Feel free to iterate and improve 

---

*