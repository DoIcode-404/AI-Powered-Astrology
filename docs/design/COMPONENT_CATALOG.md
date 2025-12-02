# Component Catalog & Usage Guide

**Astrology App Flutter Component Library**

This document provides a quick visual reference and usage guide for all reusable components in the design system.

---

## Component Index

### Buttons
- [Primary Button](#primary-button)
- [Secondary Button](#secondary-button)
- [Text Button](#text-button)
- [Icon Button](#icon-button)
- [Chip Button](#chip-button)
- [Ghost Button](#ghost-button)
- [Gradient Button](#gradient-button)
- [FAB Button](#floating-action-button)

### Cards
- [Custom Card](#custom-card)
- [Info Card](#info-card)
- [Stat Card](#stat-card)
- [Gradient Card](#gradient-card)
- [Feature Card](#feature-card)
- [List Item Card](#list-item-card)
- [Highlight Card](#highlight-card)
- [Empty State Card](#empty-state-card)

### Inputs
- [Text Input](#text-input-field)
- [Email Input](#email-input)
- [Password Input](#password-input)
- [Phone Input](#phone-input)
- [Search Input](#search-input)
- [Date Picker](#date-picker)
- [Dropdown](#dropdown)

### Loading States
- [Shimmer Loading](#shimmer-loading)
- [Skeleton Loader](#skeleton-loader)
- [Text Skeleton](#text-skeleton)
- [Card Skeleton](#card-skeleton)
- [Skeleton List](#skeleton-list)
- [Skeleton Grid](#skeleton-grid)
- [Loading Indicator](#loading-indicator)
- [Minimal Loader](#minimal-loader)
- [Linear Loading Bar](#linear-loading-bar)
- [Pulsing Loader](#pulsing-loader)

### Error States
- [Error Message](#error-message)
- [Error Card](#error-card)
- [Error State Screen](#error-state-screen)
- [Empty State Screen](#empty-state-screen)
- [Snackbars](#snackbars)
- [Dialogs](#dialogs)

---

## Buttons

### Primary Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
PrimaryButton(
  label: 'Login',
  onPressed: () {
    // Handle login action
  },
)
```

**With Icon:**
```dart
PrimaryButton(
  label: 'Generate Chart',
  onPressed: () {},
  icon: Icons.star,
)
```

**With Loading State:**
```dart
PrimaryButton(
  label: 'Generate',
  onPressed: isLoading ? null : () {},
  isLoading: isLoading,
)
```

**Full Width:**
```dart
SizedBox(
  width: double.infinity,
  child: PrimaryButton(
    label: 'Continue',
    onPressed: () {},
  ),
)
```

**Custom Size:**
```dart
PrimaryButton(
  label: 'Small Button',
  onPressed: () {},
  height: 40,
)
```

**When to Use:**
- Main call-to-action on screen
- Form submissions
- Primary user flows
- One per screen maximum

**States:**
- Default: Enabled, interactive
- Disabled: Gray, not interactive (set isEnabled: false)
- Loading: Shows spinner, disabled
- Hover: Subtle elevation increase (web/desktop)

---

### Secondary Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
SecondaryButton(
  label: 'Cancel',
  onPressed: () {
    Navigator.pop(context);
  },
)
```

**Custom Border Color:**
```dart
SecondaryButton(
  label: 'Decline',
  onPressed: () {},
  borderColor: Colors.red,
)
```

**When to Use:**
- Cancellation actions
- Rejection/decline
- Secondary options paired with primary
- Less important alternatives

---

### Text Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
TextButtonCustom(
  label: 'Skip',
  onPressed: () {},
)
```

**With Icon:**
```dart
TextButtonCustom(
  label: 'Forgot Password?',
  onPressed: () {},
  icon: Icons.help_outline,
)
```

**Custom Color:**
```dart
TextButtonCustom(
  label: 'Delete',
  onPressed: () {},
  color: Colors.red,
)
```

**When to Use:**
- Tertiary actions
- Less critical flows
- Skip/optional actions
- Inline with content

---

### Icon Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
IconButtonCustom(
  icon: Icons.add,
  onPressed: () {},
  tooltip: 'Add new',
)
```

**Custom Colors:**
```dart
IconButtonCustom(
  icon: Icons.favorite,
  onPressed: () {},
  backgroundColor: Colors.pink.withValues(alpha: 0.1),
  iconColor: Colors.pink,
  tooltip: 'Add to favorites',
)
```

**Custom Size:**
```dart
IconButtonCustom(
  icon: Icons.settings,
  size: 64,
  onPressed: () {},
)
```

**When to Use:**
- Action buttons with icons
- Compact layouts
- Settings, menu icons
- Always include tooltip for accessibility

---

### Chip Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
ChipButtonCustom(
  label: 'Fire Signs',
  isSelected: selectedElement == 'fire',
  onPressed: () {
    setState(() => selectedElement = 'fire');
  },
)
```

**With Icon:**
```dart
ChipButtonCustom(
  label: 'Love',
  icon: Icons.favorite,
  isSelected: isSelected,
  onPressed: () {},
)
```

**In Row for Filtering:**
```dart
SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  child: Row(
    children: [
      ChipButtonCustom(
        label: 'All',
        isSelected: filter == 'all',
        onPressed: () => setFilter('all'),
      ),
      SizedBox(width: 8),
      ChipButtonCustom(
        label: 'Positive',
        isSelected: filter == 'positive',
        onPressed: () => setFilter('positive'),
      ),
      // More chips...
    ],
  ),
)
```

**When to Use:**
- Filter selections
- Category selection
- Tag display
- Toggle groups

---

### Ghost Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
GhostButton(
  label: 'Learn More',
  onPressed: () {},
)
```

**With Icon & Custom Color:**
```dart
GhostButton(
  label: 'Explore',
  icon: Icons.explore,
  borderColor: AppColors.primary,
  textColor: AppColors.primary,
  onPressed: () {},
)
```

**When to Use:**
- Less prominent alternatives
- Secondary navigation
- Subtle action links

---

### Gradient Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage (Cosmic Gradient):**
```dart
GradientButton(
  label: 'Premium Feature',
  onPressed: () {},
)
```

**Custom Gradient:**
```dart
GradientButton(
  label: 'Unlock',
  gradient: LinearGradient(
    colors: [Colors.orange, Colors.red],
  ),
  onPressed: () {},
)
```

**When to Use:**
- Premium features
- Special offers
- Brand emphasis
- Visual hierarchy highlight

---

### Floating Action Button

**Import:**
```dart
import 'package:client/core/widgets/buttons.dart';
```

**Basic Usage:**
```dart
PrimaryFAB(
  icon: Icons.add,
  onPressed: () {
    // Add new item
  },
  tooltip: 'New reading',
)
```

**Extended FAB:**
```dart
PrimaryFAB(
  icon: Icons.edit,
  label: 'Edit Profile',
  isExtended: true,
  onPressed: () {},
)
```

**When to Use:**
- Primary action in screen
- Only one per screen
- Bottom-right corner
- For frequently used actions

---

## Cards

### Custom Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
CustomCard(
  child: Column(
    children: [
      Text('Title', style: AppTypography.headlineSmall),
      SizedBox(height: 8),
      Text('Content', style: AppTypography.bodyMedium),
    ],
  ),
)
```

**With Custom Styling:**
```dart
CustomCard(
  padding: AppSpacing.paddingLg,
  elevation: 4,
  borderRadius: BorderRadius.circular(16),
  backgroundColor: AppColors.primary.withValues(alpha: 0.05),
  child: child,
)
```

**Tappable Card:**
```dart
CustomCard(
  onTap: () {
    Navigator.pushNamed(context, '/details');
  },
  child: child,
)
```

**When to Use:**
- Generic content container
- Base for other card variants
- Standard content grouping
- Consistent elevation/styling

---

### Info Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
InfoCard(
  icon: Icons.info_outline,
  title: 'Compatibility Score',
  description: 'Based on your birth charts',
  onTap: () {},
)
```

**Custom Colors:**
```dart
InfoCard(
  icon: Icons.favorite,
  title: 'Love Reading',
  description: 'Detailed insights for relationships',
  iconColor: Colors.red,
  backgroundColor: Colors.red.withValues(alpha: 0.05),
  onTap: () {},
)
```

**When to Use:**
- Feature highlights
- Information blocks
- Quick navigation items
- Calls to action

---

### Stat Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
StatCard(
  label: 'Compatibility',
  value: '92',
  unit: '%',
)
```

**With Progress Bar:**
```dart
StatCard(
  label: 'Mars Strength',
  value: '8.5',
  unit: '/10',
  percentage: 85,
  valueColor: AppColors.mars,
  icon: Icons.trending_up,
)
```

**When to Use:**
- Display metrics
- Score display
- Rating visualization
- KPI cards

---

### Gradient Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage (Cosmic):**
```dart
GradientCard(
  child: Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      Text(
        'Premium Features',
        style: AppTypography.headlineLarge.copyWith(color: Colors.white),
      ),
      SizedBox(height: 8),
      Text(
        'Unlock exclusive astrology readings',
        style: AppTypography.bodyMedium.copyWith(color: Colors.white70),
      ),
    ],
  ),
)
```

**Custom Gradient:**
```dart
GradientCard(
  gradient: LinearGradient(
    colors: [Colors.orange, Colors.red],
  ),
  child: child,
)
```

**When to Use:**
- Eye-catching sections
- Premium offers
- Brand messaging
- Call-to-action sections

---

### Feature Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
FeatureCard(
  icon: Icons.public,
  title: 'Global Horoscope',
  subtitle: 'Connect with users worldwide',
  onTap: () {},
)
```

**In Grid Layout:**
```dart
GridView.count(
  crossAxisCount: 2,
  mainAxisSpacing: 16,
  crossAxisSpacing: 16,
  children: [
    FeatureCard(
      icon: Icons.chart_line,
      title: 'Birth Chart',
      onTap: () {},
    ),
    FeatureCard(
      icon: Icons.favorite,
      title: 'Compatibility',
      onTap: () {},
    ),
    // More cards...
  ],
)
```

**When to Use:**
- Feature showcase
- Module selection
- Grid-based navigation
- Dashboard highlights

---

### List Item Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
ListItemCard(
  leading: CircleAvatar(
    child: Text('♈'),
  ),
  title: 'Aries',
  subtitle: 'March 21 - April 19',
  trailing: Icon(Icons.chevron_right),
  onTap: () {},
)
```

**Selected State:**
```dart
ListItemCard(
  leading: Icon(Icons.check_circle),
  title: 'Your Selection',
  isSelected: true,
  onTap: () {},
)
```

**In List:**
```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListItemCard(
      leading: items[index].icon,
      title: items[index].name,
      subtitle: items[index].description,
      onTap: () => selectItem(index),
      isSelected: selectedIndex == index,
    );
  },
)
```

**When to Use:**
- List items
- Navigation options
- Selectable lists
- Item browsing

---

### Highlight Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
HighlightCard(
  title: 'Lucky Number',
  value: '7',
  label: 'Today\'s fortune number',
  accentColor: AppColors.sun,
)
```

**When to Use:**
- Highlight important values
- Stand-out information
- Key metrics
- Special indicators

---

### Empty State Card

**Import:**
```dart
import 'package:client/core/widgets/cards.dart';
```

**Basic Usage:**
```dart
EmptyStateCard(
  icon: Icons.calendar_today,
  title: 'No Readings Yet',
  message: 'Generate your first birth chart to get started',
  actionLabel: 'Generate Chart',
  onAction: () {},
)
```

**When to Use:**
- No data states
- Empty lists
- First-time setup
- Content not available

---

## Inputs

### Text Input Field

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
CustomTextField(
  label: 'Full Name',
  hint: 'Enter your name',
  onChanged: (value) {
    setState(() => name = value);
  },
)
```

**With Validation:**
```dart
CustomTextField(
  label: 'Username',
  hint: 'Choose username',
  validator: (value) {
    if (value?.isEmpty ?? true) {
      return 'Username required';
    }
    if (value!.length < 3) {
      return 'Minimum 3 characters';
    }
    return null;
  },
)
```

**With Icon:**
```dart
CustomTextField(
  label: 'City',
  hint: 'Enter your city',
  prefixIcon: Icons.location_city,
  onChanged: (value) {},
)
```

**Multi-line (Textarea):**
```dart
CustomTextField(
  label: 'Notes',
  hint: 'Add your notes here',
  maxLines: 5,
  minLines: 3,
  onChanged: (value) {},
)
```

**When to Use:**
- Text input
- Names, descriptions
- General text entry
- Multiple lines (text areas)

---

### Email Input

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
EmailTextField(
  onChanged: (email) {
    setState(() => userEmail = email);
  },
)
```

**Custom Label:**
```dart
EmailTextField(
  label: 'Email Address',
  onChanged: (email) {},
)
```

**When to Use:**
- Email entry
- Automatic validation
- Registration/login forms

---

### Password Input

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
PasswordTextField(
  onChanged: (password) {
    setState(() => userPassword = password);
  },
)
```

**Custom Label:**
```dart
PasswordTextField(
  label: 'New Password',
  onChanged: (password) {},
)
```

**When to Use:**
- Password entry
- Automatic validation (min 8 chars)
- Show/hide toggle included
- Registration/login forms

---

### Phone Input

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
PhoneTextField(
  onChanged: (phone) {
    setState(() => userPhone = phone);
  },
)
```

**When to Use:**
- Phone number entry
- Digits-only formatting
- Optional validation

---

### Search Input

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
SearchTextField(
  hint: 'Search zodiac signs...',
  onChanged: (query) {
    setState(() => searchQuery = query);
    performSearch(query);
  },
)
```

**Controlled:**
```dart
final controller = TextEditingController();

SearchTextField(
  controller: controller,
  onChanged: (query) {},
  onClear: () {
    controller.clear();
    clearSearch();
  },
)
```

**When to Use:**
- Search functionality
- Filter fields
- Data lookup

---

### Date Picker

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
DatePickerField(
  label: 'Birth Date',
  firstDate: DateTime(1900),
  lastDate: DateTime.now(),
  onDateChanged: (date) {
    setState(() => birthDate = date);
  },
)
```

**With Initial Date:**
```dart
DatePickerField(
  label: 'Event Date',
  initialDate: DateTime.now(),
  firstDate: DateTime.now(),
  lastDate: DateTime.now().add(Duration(days: 365)),
  onDateChanged: (date) {},
)
```

**When to Use:**
- Birth date selection
- Event date selection
- Date input with picker

---

### Dropdown

**Import:**
```dart
import 'package:client/core/widgets/inputs.dart';
```

**Basic Usage:**
```dart
DropdownFieldCustom<String>(
  label: 'Zodiac Sign',
  items: zodiacSigns.map((sign) {
    return DropdownMenuItem<String>(
      value: sign,
      child: Text(sign),
    );
  }).toList(),
  onChanged: (selected) {
    setState(() => selectedSign = selected);
  },
)
```

**With Initial Value:**
```dart
DropdownFieldCustom<String>(
  label: 'Element',
  initialValue: 'Fire',
  items: elements.map((e) => DropdownMenuItem<String>(
    value: e,
    child: Text(e),
  )).toList(),
  onChanged: (selected) {},
)
```

**When to Use:**
- Selection from predefined list
- Dropdown menus
- Single selection required

---

## Loading States

### Shimmer Loading

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
ShimmerLoading(
  child: Container(
    height: 200,
    color: Colors.grey[800],
  ),
)
```

**For Image Placeholder:**
```dart
ShimmerLoading(
  child: Container(
    width: 100,
    height: 100,
    decoration: BoxDecoration(
      color: Colors.grey[800],
      borderRadius: BorderRadius.circular(8),
    ),
  ),
)
```

**When to Use:**
- Content loading placeholders
- Image loading shimmer
- Skeleton screen base

---

### Skeleton Loader

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
SkeletonLoader(
  height: 20,
  width: double.infinity,
)
```

**Custom Shape:**
```dart
SkeletonLoader(
  height: 40,
  width: 100,
  borderRadius: BorderRadius.circular(20),
)
```

**When to Use:**
- Individual placeholder lines
- Text placeholders
- Custom skeleton shapes

---

### Text Skeleton

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
TextSkeleton(
  lineCount: 3,
)
```

**Custom Spacing:**
```dart
TextSkeleton(
  lineCount: 5,
  lineHeight: 18,
  spacing: 12,
)
```

**When to Use:**
- Paragraph placeholders
- Multi-line text loading
- Content preview while loading

---

### Card Skeleton

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
CardSkeleton()
```

**With Custom Height:**
```dart
CardSkeleton(
  height: 250,
  showImage: true,
)
```

**When to Use:**
- Card content placeholders
- List item placeholders
- Content grid loading

---

### Skeleton List

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
SkeletonList(
  itemCount: 5,
  itemHeight: 80,
)
```

**When to Use:**
- Loading entire lists
- Skeleton for scrollable content
- List view placeholders

---

### Skeleton Grid

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
SkeletonGrid(
  itemCount: 6,
  crossAxisCount: 2,
  itemHeight: 150,
)
```

**When to Use:**
- Grid view loading states
- Multi-column layouts
- Responsive skeleton grids

---

### Loading Indicator

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
LoadingIndicator(
  label: 'Generating your chart...',
)
```

**Custom Size & Color:**
```dart
LoadingIndicator(
  label: 'Loading',
  size: 64,
  color: AppColors.primary,
)
```

**When to Use:**
- Full-screen loading
- Process loading with label
- Prominent loading indicator

---

### Minimal Loader

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
MinimalLoader()
```

**In Button:**
```dart
isLoading ? MinimalLoader() : Text('Click me')
```

**When to Use:**
- Inline loading (buttons, etc)
- Compact loading indicators
- Text replacement during loading

---

### Linear Loading Bar

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
LinearLoadingBar()
```

**Custom Colors:**
```dart
LinearLoadingBar(
  height: 3,
  foregroundColor: AppColors.primary,
  backgroundColor: Colors.grey[300],
)
```

**When to Use:**
- Progress indication
- File upload/download progress
- Top-of-screen loading bar

---

### Pulsing Loader

**Import:**
```dart
import 'package:client/core/widgets/loading_indicators.dart';
```

**Basic Usage:**
```dart
PulsingLoader(
  child: Icon(Icons.star, size: 48),
)
```

**Custom Duration:**
```dart
PulsingLoader(
  duration: Duration(milliseconds: 1500),
  child: Text('Loading...'),
)
```

**When to Use:**
- Emphasis during loading
- Gentle breathing animation
- Attention-grabbing

---

## Error States

### Error Message

**Import:**
```dart
import 'package:client/core/widgets/error_states.dart';
```

**Basic Usage:**
```dart
ErrorMessage(
  message: 'Birth date is required',
)
```

**Custom Colors:**
```dart
ErrorMessage(
  message: 'Invalid entry',
  backgroundColor: Colors.red.withValues(alpha: 0.05),
  textColor: Colors.red,
  icon: Icons.warning,
)
```

**When to Use:**
- Form validation errors
- Inline error messages
- Field-specific errors

---

### Error Card

**Import:**
```dart
import 'package:client/core/widgets/error_states.dart';
```

**Basic Usage:**
```dart
ErrorCard(
  title: 'Generation Failed',
  message: 'Unable to generate chart. Please try again.',
  actionLabel: 'Retry',
  onAction: () {},
)
```

**When to Use:**
- Larger error displays
- Error details with action
- Card-sized errors

---

### Error State Screen

**Import:**
```dart
import 'package:client/core/widgets/error_states.dart';
```

**Basic Usage:**
```dart
ErrorStateScreen(
  title: 'Connection Error',
  message: 'Unable to connect to server. Check your internet.',
  actionLabel: 'Retry',
  onAction: () => retryConnection(),
  secondaryActionLabel: 'Go Home',
  onSecondaryAction: () => Navigator.pop(context),
)
```

**When to Use:**
- Full-screen errors
- Network failures
- Critical errors

---

### Empty State Screen

**Import:**
```dart
import 'package:client/core/widgets/error_states.dart';
```

**Basic Usage:**
```dart
EmptyStateScreen(
  title: 'No Readings Yet',
  message: 'Start by creating your birth chart',
  icon: Icons.inbox_outlined,
  actionLabel: 'Create Chart',
  onAction: () {},
)
```

**When to Use:**
- No data states
- Empty list screens
- First-time experience

---

### Snackbars

**Import:**
```dart
import 'package:client/core/widgets/error_states.dart';
```

**Error Snackbar:**
```dart
ScaffoldMessenger.of(context).showSnackBar(
  ErrorSnackBar.show(
    message: 'Failed to save changes',
  ),
)
```

**Success Snackbar:**
```dart
ScaffoldMessenger.of(context).showSnackBar(
  SuccessSnackBar.show(
    message: 'Chart generated successfully!',
  ),
)
```

**Warning Snackbar:**
```dart
ScaffoldMessenger.of(context).showSnackBar(
  WarningSnackBar.show(
    message: 'Internet connection slow',
  ),
)
```

**Info Snackbar:**
```dart
ScaffoldMessenger.of(context).showSnackBar(
  InfoSnackBar.show(
    message: 'New feature available',
  ),
)
```

**Custom Duration:**
```dart
ErrorSnackBar.show(
  message: 'Network error occurred',
  duration: Duration(seconds: 5),
)
```

**When to Use:**
- Temporary notifications
- Action feedback
- Quick alerts
- Non-blocking messages

---

### Dialogs

**Network Error Dialog:**
```dart
showDialog(
  context: context,
  builder: (context) => NetworkErrorDialog(
    onRetry: () => retryRequest(),
    onCancel: () => Navigator.pop(context),
  ),
)
```

**Session Expired Dialog:**
```dart
showDialog(
  context: context,
  builder: (context) => SessionExpiredDialog(
    onLogin: () => navigateToLogin(),
  ),
)
```

**When to Use:**
- Network connectivity issues
- Session timeout
- User confirmation
- Critical alerts

---

## Best Practices

### Component Usage Rules

1. **Always provide meaningful context**
   ```dart
   // Good
   IconButtonCustom(
     icon: Icons.delete,
     onPressed: () => deleteItem(),
     tooltip: 'Delete reading', // ✓ Clear label
   )

   // Avoid
   IconButtonCustom(
     icon: Icons.delete,
     onPressed: () => deleteItem(),
     // Missing tooltip
   )
   ```

2. **Use consistent spacing**
   ```dart
   // Good - uses AppSpacing
   Column(
     spacing: AppSpacing.md,
     children: [...]
   )

   // Avoid - hardcoded spacing
   Column(
     spacing: 16,
     children: [...]
   )
   ```

3. **Handle loading and error states**
   ```dart
   // Good - shows appropriate state
   if (isLoading) {
     return LoadingIndicator();
   }
   if (error != null) {
     return ErrorCard(
       title: 'Error',
       message: error,
       actionLabel: 'Retry',
       onAction: retryLoad,
     );
   }
   return successWidget;
   ```

4. **Provide accessibility labels**
   ```dart
   // Good - accessible
   PrimaryButton(
     label: 'Generate Chart',
     onPressed: () {},
   )

   // Less accessible
   Icon(Icons.auto_fix_high) // No label
   ```

5. **Test all states**
   - Default state
   - Loading state
   - Error state
   - Disabled state
   - Selected/active state

---

## Component States Reference

### Button States
- **Default:** Interactive, full color
- **Disabled:** Gray, 50% opacity, no interaction
- **Loading:** Spinner, disabled interaction
- **Active:** Elevated shadow
- **Focus:** 2px outline (keyboard)

### Card States
- **Default:** Normal elevation, interactive if tappable
- **Hover:** Increased elevation, slight scale
- **Selected:** Different background color
- **Disabled:** Reduced opacity, gray

### Input States
- **Default:** Empty, placeholder visible
- **Focused:** Primary border (2px)
- **Filled:** Shows entered content
- **Error:** Red border, error message below
- **Disabled:** Gray background, no interaction

### Loading States
- **Initial:** Skeleton/shimmer
- **In Progress:** Spinner/animation
- **Complete:** Content loaded
- **Retry Option:** On failure

### Error States
- **Message:** Inline small error
- **Card:** Larger error with details
- **Screen:** Full-page error
- **Snackbar:** Temporary notification
- **Dialog:** User action required

---

## Quick Copy-Paste Examples

### Complete Form
```dart
class MyForm extends StatefulWidget {
  @override
  State<MyForm> createState() => _MyFormState();
}

class _MyFormState extends State<MyForm> {
  final _formKey = GlobalKey<FormState>();
  String? email, password;

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        spacing: AppSpacing.md,
        children: [
          EmailTextField(
            onChanged: (value) => email = value,
          ),
          PasswordTextField(
            onChanged: (value) => password = value,
          ),
          SizedBox(
            width: double.infinity,
            child: PrimaryButton(
              label: 'Login',
              onPressed: () {
                if (_formKey.currentState!.validate()) {
                  // Submit form
                }
              },
            ),
          ),
          TextButtonCustom(
            label: 'Forgot Password?',
            onPressed: () {},
          ),
        ],
      ),
    );
  }
}
```

### List with Loading/Error States
```dart
class MyList extends StatelessWidget {
  final bool isLoading;
  final List<Item> items;
  final String? error;

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return SkeletonList(itemCount: 5);
    }

    if (error != null) {
      return ErrorCard(
        title: 'Failed to Load',
        message: error!,
        actionLabel: 'Retry',
        onAction: () => retryLoad(),
      );
    }

    if (items.isEmpty) {
      return EmptyStateCard(
        icon: Icons.inbox_outlined,
        title: 'No Items',
        message: 'Start by creating your first item',
        actionLabel: 'Create',
        onAction: () {},
      );
    }

    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        return ListItemCard(
          leading: items[index].icon,
          title: items[index].name,
          subtitle: items[index].description,
          onTap: () {},
        );
      },
    );
  }
}
```

---

**Last Updated:** November 2024
**Framework:** Flutter with Material Design 3

This component catalog serves as a quick reference guide. For detailed specifications, refer to the main design system document.
