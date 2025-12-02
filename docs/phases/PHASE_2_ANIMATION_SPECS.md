# Phase 2: Animation Specifications

Detailed animation specifications for all 4 authentication screens with implementation examples.

---

## Animation Design Tokens

All animations use centralized tokens from `AppAnimations` class.

### Durations
```dart
AppAnimations.durationFast      // 150ms  - micro-interactions
AppAnimations.durationNormal    // 300ms  - standard transitions
AppAnimations.durationSlow      // 500ms  - prominent animations
AppAnimations.durationVerySlow  // 800ms  - dramatic entrances
AppAnimations.durationLoading   // 1200ms - continuous loops
```

### Curves
```dart
AppAnimations.curveEaseOut      // Standard entrance
AppAnimations.curveEaseInOut    // Standard transitions
AppAnimations.curveEaseIn       // Acceleration effect
AppAnimations.curveLinear       // Uniform motion
AppAnimations.curveBouncy       // Elastic, celebratory
AppAnimations.curveGentle       // Smooth, subtle
```

---

## Animation Patterns

### Pattern 1: Page Entry (Fade + Slide)

**When:** Screen first appears
**Duration:** 500ms
**Curve:** easeOut
**Effect:** Content fades in while sliding up slightly

```dart
// Create animations
Animation<double> opacity = Tween<double>(begin: 0, end: 1)
    .animate(CurvedAnimation(
        parent: _controller,
        curve: AppAnimations.curveEaseOut));

Animation<Offset> slide = Tween<Offset>(
    begin: const Offset(0, 0.05),
    end: Offset.zero)
    .animate(CurvedAnimation(
        parent: _controller,
        curve: AppAnimations.curveEaseOut));

// Apply animations
SlideTransition(
  position: slide,
  child: FadeTransition(opacity: opacity, child: content),
)

// Start animation
_controller.forward();
```

### Pattern 2: Cascade/Waterfall

**When:** Multiple elements enter sequentially
**Duration:** Each element 300-400ms
**Delay:** 100ms between elements
**Effect:** Elements slide in from bottom with fade, one after another

```dart
// Element 1
Future.delayed(Duration.zero, () {
  if (mounted) _field1Controller.forward(); // starts immediately
});

// Element 2 (100ms later)
Future.delayed(const Duration(milliseconds: 100), () {
  if (mounted) _field2Controller.forward();
});

// Element 3 (200ms later)
Future.delayed(const Duration(milliseconds: 200), () {
  if (mounted) _field3Controller.forward();
});

// Creates smooth waterfall effect
```

### Pattern 3: Button Press Feedback

**When:** User taps button
**Duration:** 150ms down, 100ms up
**Curve:** easeInOut
**Effect:** Button scales down slightly, then back to normal

```dart
GestureDetector(
  onTapDown: (_) {
    _scaleController.forward(); // scale to 0.95
  },
  onTapUp: (_) {
    _scaleController.reverse(); // scale back to 1.0
    onPressed();
  },
  onTapCancel: () {
    _scaleController.reverse();
  },
  child: ScaleTransition(
    scale: _scaleAnimation,
    child: ElevatedButton(...),
  ),
)
```

### Pattern 4: Loading State

**When:** Button shows loading spinner
**Duration:** 200ms fade
**Effect:** Button text fades out, spinner fades in

```dart
AnimatedOpacity(
  opacity: isLoading ? 0 : 1,
  duration: AppAnimations.durationFast,
  child: Text(label),
)

AnimatedOpacity(
  opacity: isLoading ? 1 : 0,
  duration: AppAnimations.durationFast,
  child: CircularProgressIndicator(),
)
```

### Pattern 5: Success State

**When:** Operation completes successfully
**Duration:** 500ms scale
**Curve:** bouncy
**Effect:** Checkmark scales from 0 to 1.2 then settles to 1

```dart
Animation<double> scale = Tween<double>(begin: 0, end: 1)
    .animate(CurvedAnimation(
        parent: _successController,
        curve: AppAnimations.curveBouncy));

ScaleTransition(
  scale: scale,
  child: Container(
    decoration: BoxDecoration(shape: BoxShape.circle),
    child: Icon(Icons.check_circle, size: 80),
  ),
)

_successController.forward();
```

### Pattern 6: Error Message

**When:** Validation error occurs
**Duration:** 300ms
**Curve:** easeOut
**Effect:** Message slides in from top/bottom, fades in

```dart
if (errorMessage != null)
  AnimatedOpacity(
    opacity: errorMessage != null ? 1 : 0,
    duration: AppAnimations.durationNormal,
    child: ErrorMessage(message: errorMessage!),
  )
```

---

## Screen-Specific Animations

### Login Screen

#### Header Animation
```
Delay: 100ms after page starts
Duration: 400ms
Curve: easeOut
Motion: Slide from top (-0.03 offset) + fade in
Position: CosmicHeader widget
```

#### Card Animation
```
Delay: 100ms after header
Duration: 400ms
Curve: easeOut
Motion: Slide from bottom (+0.08 offset) + fade in
Position: CosmicAuthCard widget
```

#### Email Field
```
Delay: 150ms after card
Duration: 300ms
Curve: easeOut
Motion: Slide from bottom (+0.03 offset) + fade in
Position: EmailTextField
```

#### Password Field
```
Delay: 250ms after card (100ms after email)
Duration: 300ms
Curve: easeOut
Motion: Slide from bottom (+0.03 offset) + fade in
Position: PasswordTextField
```

#### Button Press
```
Trigger: User taps "Sign In"
1. Scale down to 0.95x (150ms, easeInOut)
2. Show loading spinner (200ms fade)
3. On success: Scale in checkmark (500ms, bouncy)
4. Navigate away (300ms fade out)
```

---

### Signup Screen

#### Header Animation (in SliverAppBar)
```
Delay: 100ms
Duration: 400ms
Curve: easeOut
Motion: Slide from top + fade in
Position: Title in expanded height section
```

#### Form Card
```
Delay: 200ms after header
Duration: 400ms
Curve: easeOut
Motion: Slide from bottom + fade in
Position: CosmicAuthCard
```

#### Form Fields (5 total)
```
Field 1 (Name):
- Delay: 350ms total (150 + 200)
- Duration: 300ms
- Motion: Slide up + fade in

Field 2 (Email):
- Delay: 450ms total (150 + 300)
- Duration: 300ms
- Motion: Slide up + fade in

Field 3 (Phone):
- Delay: 550ms total (150 + 400)
- Duration: 300ms
- Motion: Slide up + fade in

Field 4 (Password):
- Delay: 650ms total (150 + 500)
- Duration: 300ms
- Motion: Slide up + fade in

Field 5 (Confirm):
- Delay: 750ms total (150 + 600)
- Duration: 300ms
- Motion: Slide up + fade in
```

#### Checkbox
```
Delay: 850ms total (150 + 700)
Duration: 300ms
Motion: Slide up + fade in
```

#### Submission
```
1. Button scale on press (150ms)
2. Loading state (200ms fade)
3. Success checkmark (500ms, bouncy)
4. Navigate to onboarding (300ms fade)
```

---

### Forgot Password Screen

#### Input State

Header, Card, Field, Button animations same as Login Screen

#### Success State

```
1. Icon appears with scale animation
   - Duration: 500ms
   - Curve: bouncy
   - From: 0 scale
   - To: 1.0 scale

2. Success message fades in
   - Delay: 300ms after icon appears
   - Duration: 300ms
   - Curve: easeOut
   - Motion: Fade from 0 to 1 opacity

3. Action buttons appear
   - "Try Another Email" - resets animations
   - "Back to Login" - navigates away
```

#### Animation Reset
```
When user clicks "Try Another Email":
1. Success checkmark animation resets
2. Success text opacity resets
3. Input fields re-animate in
4. Back to input state
```

---

### Reset Password Screen

#### Input State

Header, Card animations as standard pattern

#### Password Fields
```
Field 1 (New Password):
- Delay: 150ms after card
- Duration: 300ms
- Motion: Slide up + fade

Field 2 (Confirm Password):
- Delay: 250ms after card
- Duration: 300ms
- Motion: Slide up + fade
```

#### Requirements Box
```
Delay: 350ms after card
Duration: 300ms
Motion: Slide up + fade

DYNAMIC ANIMATIONS:
- Each requirement updates in real-time
- Icon switches: Circle → Checkmark (150ms, easeOut)
- Text color: Secondary → Primary (150ms, easeOut)
- Uses AnimatedSwitcher for icon changes
- Uses AnimatedDefaultTextStyle for text color

4 Requirements:
1. Length (8+ chars) - checks as user types
2. Uppercase letter - checks as user types
3. Lowercase letter - checks as user types
4. Number - checks as user types
```

#### Reset Button
```
Delay: 450ms after card
Duration: 300ms
Motion: Slide up + fade

On press:
1. Scale down (150ms)
2. Loading spinner (200ms fade)
3. Success checkmark (500ms, bouncy)
4. Success message fades in (300ms, 300ms delay)
5. Navigate to login (300ms fade)
```

---

## Implementation Patterns

### Pattern 1: Simple Fade-in
```dart
FadeTransition(
  opacity: animation,
  child: widget,
)
```

### Pattern 2: Slide + Fade
```dart
SlideTransition(
  position: slideAnimation,
  child: FadeTransition(
    opacity: fadeAnimation,
    child: widget,
  ),
)
```

### Pattern 3: Scale + Fade
```dart
ScaleTransition(
  scale: scaleAnimation,
  child: FadeTransition(
    opacity: fadeAnimation,
    child: widget,
  ),
)
```

### Pattern 4: Multiple Animations with AnimatedBuilder
```dart
AnimatedBuilder(
  animation: Listenable.merge([
    _controller1,
    _controller2,
    _controller3,
  ]),
  builder: (context, _) {
    return SingleChildScrollView(
      child: Column(
        children: [
          Transform.translate(
            offset: _animation1.value,
            child: Opacity(
              opacity: _opacity1.value,
              child: Widget1(),
            ),
          ),
          Transform.translate(
            offset: _animation2.value,
            child: Opacity(
              opacity: _opacity2.value,
              child: Widget2(),
            ),
          ),
        ],
      ),
    );
  },
)
```

---

## Accessibility Considerations

### Respecting Motion Preferences
```dart
final disableAnimations = MediaQuery.of(context).disableAnimations;

if (disableAnimations) {
  // Instantly show content
  _controller.jumpToEnd();
} else {
  // Animate normally
  _controller.forward();
}
```

### Providing Instant Feedback
```dart
// Even without animations, buttons respond immediately
ElevatedButton(
  onPressed: onPressed,
  child: Text(label),
  // Animation layer is optional
)
```

### Touch Targets
```dart
// All interactive elements must be 48x48 dp minimum
SizedBox(
  width: 56,
  height: 56,
  child: Button(...),
)
```

---

## Performance Optimization Tips

### DO
- Use Transform.translate() for position changes (GPU accelerated)
- Use Opacity for fade effects (GPU accelerated)
- Use ScaleTransition for scaling (GPU accelerated)
- Use const constructors (minimize rebuilds)
- Use AnimatedBuilder with Listenable.merge()
- Profile with Flutter DevTools (Raster/UI thread)

### DON'T
- Animate layout/size (causes expensive layout recalculations)
- Use setState unnecessarily during animations
- Animate too many properties simultaneously
- Create new AnimationControllers on every build
- Forget to dispose AnimationControllers
- Use non-GPU-accelerated properties

---

## Testing Animations

### Visual Testing
1. Run app and navigate to each screen
2. Verify animations appear smooth (60fps)
3. Check timing - should feel natural, not rushed
4. Verify no jank or stuttering
5. Test on multiple devices

### Functional Testing
1. Verify animations don't block interactions
2. Test button taps during animations
3. Test back button during animations
4. Test form submission during animations

### Performance Testing
```dart
// In DevTools Raster tab:
- Green line (60fps) = good performance
- Yellow line (>16ms) = needs optimization
- Red line (>33ms) = performance issue
```

### Accessibility Testing
1. Disable animations in device settings
2. Verify all content still visible immediately
3. Test with screen reader
4. Verify touch targets are adequate
5. Check color contrast ratios

---

## Common Issues & Solutions

### Issue: Animation stutters
**Solution:** Check DevTools Raster tab. Likely animating layout. Use Transform instead.

### Issue: Animation feels slow
**Solution:** Reduce duration. Try durationNormal (300ms) instead of durationSlow (500ms).

### Issue: Animation doesn't reset
**Solution:** Call `_controller.reset()` before `_controller.forward()` again.

### Issue: Animation doesn't show
**Solution:** Verify AnimatedBuilder/FadeTransition wraps widget. Check if controller is forwarded.

### Issue: Memory leak
**Solution:** Verify all AnimationControllers are disposed in `dispose()` method.

---

## Summary

This specification provides detailed guidance for understanding, implementing, and maintaining animations across the authentication system. All patterns use AppAnimations tokens, ensuring consistency and easy maintenance throughout the codebase.
