# Cosmic Components Reference

Quick reference guide for using the new cosmic design components.

---

## CosmicHeader Component

### Location
`client/lib/core/widgets/cosmic_header.dart`

### Purpose
Creates a mystical, elegant header with:
- Gradient text effect (ShaderMask)
- Decorative celestial elements (stars)
- Responsive sizing
- Subtitle support

### Import
```dart
import 'package:kundali/core/widgets/index.dart';
```

### Basic Usage
```dart
CosmicHeader(
  title: 'Kundali',
  subtitle: 'Your Cosmic Guide',
)
```

### Full Parameters
```dart
CosmicHeader(
  title: 'Your Title',                          // Required
  subtitle: 'Your Subtitle',                    // Optional
  heightPercentage: 0.22,                       // Optional, default 0.22
  titleGradient: AppColors.cosmicGradient,      // Optional, custom gradient
  trailingIcon: Icon(...),                      // Optional, trailing widget
)
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| title | String | Required | Main header title text |
| subtitle | String? | null | Optional subtitle below title |
| heightPercentage | double | 0.22 | Height as % of screen (0.15-0.25) |
| titleGradient | LinearGradient? | cosmicGradient | Gradient for title text |
| trailingIcon | Widget? | null | Optional icon on right side |

### Examples

#### Login Screen Header
```dart
CosmicHeader(
  title: 'Kundali',
  subtitle: 'Your Cosmic Guide',
  heightPercentage: 0.20,
)
```

#### Signup Screen Header
```dart
CosmicHeader(
  title: 'Join Us',
  subtitle: 'Begin Your Cosmic Journey',
  heightPercentage: 0.20,
)
```

#### Custom Gradient Header
```dart
CosmicHeader(
  title: 'Reset Password',
  subtitle: 'Regain Access',
  heightPercentage: 0.18,
  titleGradient: AppColors.nebulaGradient,
)
```

### Visual Hierarchy
- Title: Large, bold, gradient-filled text
- Subtitle: Medium, italic, secondary gray color
- Decorative elements: Subtle stars with glow effect
- Background: Subtle gradient overlay

### Responsive Behavior
- Desktop: Larger header (25% height)
- Tablet: Medium header (22% height)
- Mobile: Compact header (18% height)

---

## CosmicAuthCard Component

### Location
`client/lib/core/widgets/cosmic_auth_card.dart`

### Purpose
Provides a beautifully styled form container with:
- Semi-transparent dark background
- Subtle accent border
- Floating shadow effect
- Consistent padding

### Import
```dart
import 'package:kundali/core/widgets/index.dart';
```

### Basic Usage
```dart
CosmicAuthCard(
  child: Column(
    children: [
      // Form content
    ],
  ),
)
```

### Full Parameters
```dart
CosmicAuthCard(
  child: Widget,                                // Required, card content
  padding: EdgeInsets? = null,                  // Optional, inner padding
  borderColor: Color? = null,                   // Optional, border color
  backgroundColor: Color? = null,               // Optional, bg color
  boxShadow: List<BoxShadow>? = null,          // Optional, custom shadow
  borderRadius: BorderRadius? = null,           // Optional, custom radius
)
```

### Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| child | Widget | Required | Content inside the card |
| padding | EdgeInsets? | AppSpacing.lg | Internal padding |
| borderColor | Color? | primary@0.2 | Border color (indigo with opacity) |
| backgroundColor | Color? | surfaceDark@0.85 | Background (semi-transparent dark) |
| boxShadow | List<BoxShadow>? | Dual-layer | Shadow for floating effect |
| borderRadius | BorderRadius? | 16px | Rounded corners |

### Examples

#### Standard Form Card
```dart
CosmicAuthCard(
  child: Column(
    children: [
      Text('Create Account', style: Theme.of(context).textTheme.headlineMedium),
      SizedBox(height: AppSpacing.xl),
      EmailTextField(...),
      SizedBox(height: AppSpacing.lg),
      PasswordTextField(...),
    ],
  ),
)
```

#### Success State Card
```dart
CosmicAuthCard(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
      Icon(Icons.check_circle, size: 64),
      SizedBox(height: AppSpacing.lg),
      Text('Success!'),
    ],
  ),
)
```

#### Custom Styled Card
```dart
CosmicAuthCard(
  padding: const EdgeInsets.all(AppSpacing.xl),
  borderColor: AppColors.success.withValues(alpha: 0.3),
  backgroundColor: AppColors.surfaceVariantDark,
  child: ...,
)
```

### Visual Properties
- Border: 1.5px, primary color at 20% opacity
- Background: Dark navy at 85% opacity (semi-transparent)
- Radius: 16px (modern, polished)
- Shadow: Dual-layer (glow + black shadow)
- Padding: 24px by default (AppSpacing.lg)

### Shadow Effect
Creates a floating effect in cosmic space:
- Layer 1: Primary color glow (indigo@10%, 16px blur)
- Layer 2: Black shadow (black@20%, 8px blur, 2px offset)

---

## Combined Usage Pattern

### Typical Auth Screen Structure
```dart
Scaffold(
  body: Container(
    // Cosmic gradient background
    decoration: BoxDecoration(
      gradient: LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          Color(0xFF0F0F23),
          Color(0xFF1a1a2e),
          Color(0xFF16213e),
        ],
      ),
    ),
    child: SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
        child: Column(
          children: [
            // Header section
            CosmicHeader(
              title: 'Screen Title',
              subtitle: 'Screen Subtitle',
              heightPercentage: 0.20,
            ),

            const SizedBox(height: AppSpacing.xl),

            // Form card section
            CosmicAuthCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Form content
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.xxl),
          ],
        ),
      ),
    ),
  ),
)
```

---

## Styling Guidelines

### Colors to Use
- Text: `AppColors.textPrimaryDark` (#F0F0F5)
- Secondary text: `AppColors.textSecondaryDark` (#B0B0C0)
- Interactive: `AppColors.primary` (#6366F1)
- Success: `AppColors.success` (#10B981)
- Error: `AppColors.error` (#EF4444)

### Spacing to Use
- Major sections: `AppSpacing.xxl` (64px), `AppSpacing.xl` (32px)
- Card padding: `AppSpacing.lg` (24px)
- Field spacing: `AppSpacing.lg` (24px)
- Small gaps: `AppSpacing.md` (16px), `AppSpacing.sm` (8px)

### Typography to Use
- Titles: `headlineMedium` (20px, SemiBold)
- Body: `bodySmall` (12px, Regular)
- Labels: `labelMedium` (12px, Medium)

---

## Do's and Don'ts

### Do's
- Do use consistent AppSpacing values
- Do apply AppColors for all colors
- Do use AppTypography for text styles
- Do keep cards within CosmicAuthCard
- Do use CosmicHeader for main headers
- Do maintain dark mode aesthetic
- Do respect touch targets (48x48 minimum)
- Do use const constructors

### Don'ts
- Don't hardcode colors
- Don't hardcode dimensions
- Don't mix custom and design token styles
- Don't create new card styles (use CosmicAuthCard)
- Don't ignore contrast ratios
- Don't use excessive shadows
- Don't ignore responsive design
- Don't break semantic hierarchy

---

## Accessibility Checklist

When using these components:
- [ ] Ensure text color contrast (4.5:1 minimum)
- [ ] Provide semantic labels for form fields
- [ ] Include proper error message styling
- [ ] Maintain focus indicators
- [ ] Keep touch targets at 48x48dp
- [ ] Test with screen readers
- [ ] Support keyboard navigation
- [ ] Provide alt text for icons

---

## Performance Tips

1. **Use const constructors:** Always use `const` where possible
```dart
CosmicHeader(
  title: 'Title',
  subtitle: 'Subtitle',
) // Missing const keyword
```

Should be:
```dart
const CosmicHeader(
  title: 'Title',
  subtitle: 'Subtitle',
)
```

2. **Minimize rebuilds:** Use efficient state management
3. **Cache gradients:** Gradients are const and cached
4. **Lazy load content:** Use SingleChildScrollView for forms
5. **Profile with DevTools:** Check frame rates

---

## Troubleshooting

### Header text not showing gradient
- Ensure ShaderMask is applied
- Check that title text color is white (required for ShaderMask)
- Verify gradient is properly defined

### Card shadows not visible
- Check background doesn't hide shadow
- Verify elevation is set correctly
- Ensure shadow colors have sufficient opacity

### Text color contrast issues
- Use AppColors for all text
- Check contrast ratio in dark mode
- Verify background opacity isn't too high

### Layout issues on small screens
- Use responsive padding (AppSpacing tokens)
- Test on actual devices/emulators
- Check overflow and scrolling behavior

---

## Examples by Use Case

### Login Form
```dart
CosmicHeader(title: 'Kundali', subtitle: 'Your Cosmic Guide'),
CosmicAuthCard(
  child: Column(
    children: [
      Text('Welcome Back'),
      EmailTextField(...),
      PasswordTextField(...),
      PrimaryButton(label: 'Sign In'),
    ],
  ),
)
```

### Signup Form
```dart
CosmicHeader(title: 'Join Us', subtitle: 'Begin Your Journey'),
CosmicAuthCard(
  child: Column(
    children: [
      Text('Create Account'),
      CustomTextField(label: 'Name'),
      EmailTextField(...),
      PasswordTextField(...),
      PrimaryButton(label: 'Create Account'),
    ],
  ),
)
```

### Success Message
```dart
CosmicHeader(title: 'Success', subtitle: 'Action completed'),
CosmicAuthCard(
  child: Column(
    children: [
      Icon(Icons.check_circle, color: AppColors.success),
      Text('Your message'),
      PrimaryButton(label: 'Continue'),
    ],
  ),
)
```

---

## Migration Guide

If updating existing screens to use these components:

### Before
```dart
Scaffold(
  appBar: AppBar(title: Text('Title')),
  body: Padding(
    padding: EdgeInsets.all(16),
    child: Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(...),
      ),
    ),
  ),
)
```

### After
```dart
Scaffold(
  body: Container(
    decoration: BoxDecoration(gradient: cosmicGradient),
    child: SafeArea(
      child: SingleChildScrollView(
        child: Column(
          children: [
            CosmicHeader(title: 'Title', subtitle: 'Subtitle'),
            CosmicAuthCard(
              child: Column(...),
            ),
          ],
        ),
      ),
    ),
  ),
)
```

---

## Component File References

### Source Files
- **CosmicHeader:** `client/lib/core/widgets/cosmic_header.dart`
- **CosmicAuthCard:** `client/lib/core/widgets/cosmic_auth_card.dart`
- **Index:** `client/lib/core/widgets/index.dart`

### Usage Examples
- **Login:** `client/lib/presentation/screens/auth/login_screen.dart`
- **Signup:** `client/lib/presentation/screens/auth/signup_screen.dart`
- **Forgot Password:** `client/lib/presentation/screens/auth/forgot_password_screen.dart`
- **Reset Password:** `client/lib/presentation/screens/auth/reset_password_screen.dart`

---

**Last Updated:** 2025-11-24
**Status:** Phase 1 Complete
**Design System:** Cosmic Mysticism
