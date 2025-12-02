# Authentication Screens - Implementation Guide

## Quick Reference: Enhancement Checklist

### Login Screen (`login_screen.dart`)
- [ ] Add `import '../../../core/theme/app_animations.dart';`
- [ ] Replace `State<LoginScreen>` with `State<LoginScreen> with TickerProviderStateMixin`
- [ ] Add AnimationController for page load
- [ ] Wrap body with cosmic gradient container
- [ ] Add _buildHeader() method with mystical branding
- [ ] Add _buildLoginCard() method
- [ ] Implement FadeTransition for header
- [ ] Implement SlideTransition for card
- [ ] Update button label to show "Signing In..." when loading
- [ ] Verify all typography uses design system

### Signup Screen (`signup_screen.dart`)
- [ ] Add cosmic gradient background
- [ ] Replace AppBar with custom mystical header
- [ ] Create visual password strength indicator
- [ ] Add field-by-field animation
- [ ] Implement loading state animation
- [ ] Create success celebration animation
- [ ] Update typography to design system
- [ ] Verify form validation visual feedback

### Forgot Password Screen (`forgot_password_screen.dart`)
- [ ] Add cosmic gradient background
- [ ] Implement AnimatedCrossFade between states
- [ ] Add loading animation for email send
- [ ] Animate success icon appearance
- [ ] Create success state celebration
- [ ] Replace simulated delay with actual API call

### Reset Password Screen (`reset_password_screen.dart`)
- [ ] Add cosmic gradient background
- [ ] Animate requirement indicators
- [ ] Implement AnimatedCrossFade for state change
- [ ] Add loading animation
- [ ] Create success celebration
- [ ] Integrate with backend API

---

## Code Templates

### 1. Add Cosmic Gradient Background

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    body: Container(
      decoration: const BoxDecoration(
        gradient: AppColors.cosmicGradient,
      ),
      child: // ... rest of build
    ),
  );
}
```

### 2. Add Page Load Animations

```dart
class _LoginScreenState extends State<LoginScreen> with TickerProviderStateMixin {
  late AnimationController _fadeController;

  @override
  void initState() {
    super.initState();
    _fadeController = AnimationController(
      vsync: this,
      duration: AppAnimations.durationNormal,
    );
    _fadeController.forward();
  }

  @override
  void dispose() {
    _fadeController.dispose();
    super.dispose();
  }

  // In build():
  FadeTransition(
    opacity: Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _fadeController, curve: Curves.easeOut),
    ),
    child: SlideTransition(
      position: Tween<Offset>(
        begin: const Offset(0, 0.3),
        end: Offset.zero,
      ).animate(
        CurvedAnimation(parent: _fadeController, curve: Curves.easeOut),
      ),
      child: _buildLoginCard(context),
    ),
  )
}
```

### 3. Mystical Header with Shader Mask

```dart
Widget _buildHeader(BuildContext context) {
  return Column(
    children: [
      ShaderMask(
        shaderCallback: (bounds) => const LinearGradient(
          colors: [Colors.white, Color(0xFFB0B0C0)],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ).createShader(bounds),
        child: Text(
          '✨ Kundali',
          style: Theme.of(context).textTheme.displayLarge?.copyWith(
            color: Colors.white,
            fontWeight: FontWeight.w700,
            letterSpacing: 1.5,
          ),
        ),
      ),
      const SizedBox(height: AppSpacing.sm),
      Text(
        'Your Cosmic Guide to the Stars',
        style: Theme.of(context).textTheme.labelLarge?.copyWith(
          color: Colors.white.withValues(alpha: 0.9),
          letterSpacing: 0.5,
        ),
      ),
    ],
  );
}
```

### 4. Error Message with Animation

```dart
if (_errorMessage != null) ...[
  AnimatedOpacity(
    opacity: _errorMessage != null ? 1.0 : 0.0,
    duration: AppAnimations.fadeInDuration,
    child: ErrorMessage(message: _errorMessage!),
  ),
  const SizedBox(height: AppSpacing.md),
],
```

### 5. Loading Button with State Text

```dart
SizedBox(
  width: double.infinity,
  child: PrimaryButton(
    label: _isLoading ? 'Signing In...' : 'Sign In',
    onPressed: _isLoading ? () {} : _handleLogin,
    isLoading: _isLoading,
  ),
)
```

### 6. Animated State Transition

```dart
AnimatedCrossFade(
  firstChild: _buildEmailInput(),
  secondChild: _buildSuccessState(),
  crossFadeState: _emailSent
    ? CrossFadeState.showSecond
    : CrossFadeState.showFirst,
  duration: AppAnimations.durationNormal,
  firstCurve: Curves.easeOut,
  secondCurve: Curves.easeOut,
)
```

### 7. Password Requirement Indicator with Animation

```dart
Widget _buildRequirement(String text, bool met) {
  return Padding(
    padding: const EdgeInsets.symmetric(vertical: AppSpacing.xs),
    child: Row(
      children: [
        AnimatedContainer(
          duration: AppAnimations.durationFast,
          child: Icon(
            met ? Icons.check_circle : Icons.circle_outlined,
            size: 16,
            color: met
              ? AppColors.success
              : Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Text(
          text,
          style: Theme.of(context).textTheme.bodySmall?.copyWith(
            color: met
              ? AppColors.success
              : Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    ),
  );
}
```

### 8. API Call Pattern (Replace TODOs)

```dart
// BEFORE (TODO placeholder):
// TODO: Call backend API to send reset email
await Future.delayed(const Duration(seconds: 2));

// AFTER (Real API call):
try {
  final authService = AuthService();
  await authService.init();

  await authService.resetPassword(
    email: _emailController.text.trim(),
  );

  setState(() => _emailSent = true);
} catch (e) {
  _showError('Failed to send reset email: ${e.toString()}');
}
```

---

## Design Tokens Quick Reference

### Colors
```dart
AppColors.primary           // Indigo (#6366F1)
AppColors.error             // Red (#EF4444)
AppColors.success           // Green (#10B981)
AppColors.cosmicGradient    // Gradient for backgrounds
AppColors.textPrimaryDark   // Almost White (#F0F0F5)
AppColors.textSecondaryDark // Light Gray (#B0B0C0)
```

### Spacing
```dart
AppSpacing.xs   // 4px
AppSpacing.sm   // 8px
AppSpacing.md   // 16px
AppSpacing.lg   // 24px
AppSpacing.xl   // 32px
AppSpacing.xxl  // 48px
AppSpacing.xxxl // 64px
```

### Animations
```dart
AppAnimations.durationFast      // 150ms
AppAnimations.durationNormal    // 300ms - USE THIS FOR AUTH
AppAnimations.durationSlow      // 500ms
AppAnimations.fadeInDuration    // 300ms
AppAnimations.fadeOutDuration   // 150ms
AppAnimations.curveEaseInOut    // Smooth, polished
AppAnimations.curveEaseOut      // For appearing elements
```

### Typography
Use Theme.of(context).textTheme instead of hardcoded sizes:
```dart
displayLarge   // App title
headlineMedium // Card titles
labelLarge     // Form labels
bodyMedium     // Form input text
bodySmall      // Supporting text
```

---

## Migration Path

### Step 1: Visual Enhancement (No Logic Changes)
1. Add gradients to all screens
2. Create header widgets
3. Enhance card styling
4. No behavior changes

### Step 2: Animation System
1. Import AppAnimations
2. Add AnimationControllers
3. Implement fade/slide transitions
4. Test 60fps performance

### Step 3: Missing Screens
1. Create onboarding_screen.dart
2. Create auth_splash_screen.dart
3. Create session_expired_screen.dart
4. Connect to routes

### Step 4: API Integration
1. Replace TODO placeholders
2. Implement error handling
3. Add timeout handling
4. Test with real backend

### Step 5: Polish & Accessibility
1. Add Semantics widgets
2. Enhance focus indicators
3. Test with screen readers
4. Final design review

---

## Testing Checklist

### Visual Testing
- [ ] Login screen shows cosmic gradient
- [ ] Animations are smooth 60fps
- [ ] Error messages appear and disappear smoothly
- [ ] Loading spinner shows during API calls
- [ ] All text is readable on all screen sizes
- [ ] Dark mode works correctly

### Functional Testing
- [ ] Empty email shows validation error
- [ ] Invalid email shows validation error
- [ ] Empty password shows validation error
- [ ] API success navigates to dashboard
- [ ] API failure shows error message
- [ ] Navigation links work correctly

### Accessibility Testing
- [ ] Screen reader announces all fields
- [ ] Touch targets are 48px minimum
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Contrast ratios exceed 4.5:1
- [ ] Focus indicators are visible

### Performance Testing
- [ ] Animations run at 60fps in DevTools
- [ ] No unnecessary rebuilds
- [ ] Controllers disposed properly
- [ ] Memory stable during long form use

---

## Common Pitfalls to Avoid

### Animation Issues
❌ Using Duration.zero (animations won't show)
❌ Mixing multiple overlapping animations (janky feel)
❌ Animations longer than 500ms (feels slow)
❌ No curve (linear looks robotic)

✅ Use 300ms standard duration
✅ Stagger animations if needed
✅ Use easeInOut for polish
✅ Always dispose AnimationControllers

### Form Issues
❌ Modifying controller text in onChanged (awkward)
❌ Not validating required fields
❌ No visual feedback on errors
❌ Forgetting to clear error on focus

✅ Use controller.text for reading
✅ Validate all inputs before submit
✅ Show error message + snackbar
✅ Clear errors when user starts typing

### Navigation Issues
❌ Using pushNamed without RemoveUntil (back stack grows)
❌ Not popping dialogs before navigation
❌ No animation between route changes
❌ Not clearing controller state

✅ Use pushNamedAndRemoveUntil for auth transitions
✅ Always pop before navigation
✅ Add custom route animations
✅ Dispose controllers in widget dispose

---

## Performance Guidelines

### Animation Performance
- Profile with Flutter DevTools
- Target 60fps minimum
- Use const constructors wherever possible
- Avoid layout-triggering animations

### Build Performance
- Extract complex widgets
- Use StatelessWidget when possible
- Lazy load heavy widgets
- Use Provider/Riverpod for state

### Network Performance
- Add proper timeout handling
- Show loading state immediately
- Handle network errors gracefully
- Cache authentication tokens

---

## Accessibility Guidelines

### Screen Reader Support
```dart
Semantics(
  label: 'Email address input field',
  textField: true,
  enabled: true,
  child: EmailTextField(...),
)
```

### Focus Management
```dart
FocusScope.of(context).requestFocus(_passwordFocus);
```

### Contrast Checking
- Text: minimum 4.5:1 ratio
- UI components: minimum 3:1 ratio
- Use WebAIM or similar tool

---

## File Templates

### Enhanced Login Screen Structure
```dart
class _LoginScreenState extends State<LoginScreen> with TickerProviderStateMixin {
  late AnimationController _fadeController;

  @override
  void initState() { /* Setup animations */ }

  @override
  void dispose() { /* Cleanup */ }

  Future<void> _handleLogin() async { /* Logic */ }

  void _showError(String message) { /* Error display */ }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: AppColors.cosmicGradient,
        ),
        child: FadeTransition(
          opacity: /* animation */,
          child: SingleChildScrollView(
            child: Column(
              children: [
                _buildHeader(context),
                SlideTransition(
                  position: /* animation */,
                  child: _buildLoginCard(context),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) { /* Header */ }

  Widget _buildLoginCard(BuildContext context) { /* Card */ }
}
```

---

## Resources

### Documentation
- Flutter Animation: https://flutter.dev/docs/development/ui/animations
- Material Design 3: https://m3.material.io/
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/

### Design System
- Design tokens: `/docs/design/COMPLETE_DESIGN_SYSTEM.md`
- Colors: `core/theme/app_colors.dart`
- Spacing: `core/theme/app_spacing.dart`
- Animations: `core/theme/app_animations.dart`

### Related Code
- Widgets: `core/widgets/`
- Navigation: `core/navigation/app_routes.dart`
- Auth Service: `data/services/auth_service.dart`

---

## Questions & Support

### Common Questions

**Q: Should I use Hero animations?**
A: No, for auth screens use simple fade/slide. Hero is better for cross-screen shared elements.

**Q: How do I handle loading between screens?**
A: Show loading state in current screen, then navigate. Consider auth_splash_screen for app startup.

**Q: Can I use Lottie animations?**
A: Yes, for special effects (success celebration, loading state), but keep simple for performance.

**Q: Should each screen have its own gradient?**
A: Use cosmicGradient consistently. Don't override unless specific design reason.

---

## Maintenance Notes

### Things to Update When Design System Changes
- AppColors values → All screens automatically update
- AppSpacing values → All spacing automatically adjusts
- AppTypography → All text automatically updates
- AppAnimations → All animations update (but logic needs review)

### Version History
- v1.0: Initial audit and implementation guide
- [Future versions to be documented]
