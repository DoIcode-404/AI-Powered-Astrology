# Testing Strategy

## Overview

This document outlines the comprehensive testing strategy for the Astrology Flutter Application. We follow the **Testing Pyramid** approach: 70% widget/unit tests (fast feedback), 20% integration tests (feature-level validation), and 10% E2E tests (critical user flows).

## Testing Pyramid Distribution

```
        ╱╲
       ╱  ╲     E2E Tests (10%)
      ╱────╲    - Critical user journeys
     ╱      ╲   - Playwright browser tests
    ╱────────╲
   ╱          ╲  Integration Tests (20%)
  ╱            ╲ - Feature workflows
 ╱──────────────╲- State management flows
╱                ╲ Widget/Unit Tests (70%)
──────────────────── - Individual components
                    - Business logic
                    - Data transformations
```

## Test Coverage Goals

| Test Type | Target Coverage | Execution Time | CI/CD Frequency |
|-----------|-----------------|-----------------|-----------------|
| Widget/Unit | 80%+ in critical paths | < 1 minute | Every commit |
| Integration | Core features fully tested | < 2 minutes | PR merges |
| E2E | Critical user flows | < 5 minutes | Staging deployments |

## Critical User Flows (E2E Priority)

### Tier 1: Must Test (Critical Business Logic)
1. **Onboarding Flow**
   - User registration with birth details
   - Timezone and location selection
   - Permission requests (notifications, calendar)
   - Initial chart generation

2. **Daily Horoscope Access**
   - View today's horoscope by zodiac sign
   - Navigate between different signs
   - Share horoscope functionality
   - Historical horoscope access

3. **Birth Chart Visualization**
   - Chart generation for user's birth data
   - Interactive chart exploration (pan, zoom)
   - Planetary position details
   - House and aspect interpretation

4. **Compatibility Checking**
   - Partner birth data input
   - Compatibility percentage calculation
   - Element and planet comparison
   - Result sharing

5. **Authentication & Profile**
   - User login/logout
   - Profile edit (update birth information)
   - Theme preference changes
   - Notification settings

### Tier 2: Important Features (Integration Tests)
- Moon phase displays
- Transits information
- Multiple horoscope categories (Love, Career, Health)
- Caching and offline functionality
- Navigation between major screens

### Tier 3: Polish & UX (Widget Tests)
- Loading states and skeleton screens
- Error message displays
- Form validation
- Animation smoothness
- Accessibility features

## Widget Testing Strategy

### Organization
```
test/
├── widgets/
│   ├── horoscope_card_test.dart
│   ├── zodiac_selector_test.dart
│   ├── birth_chart_widget_test.dart
│   ├── compatibility_card_test.dart
│   └── common/
│       ├── app_button_test.dart
│       └── theme_test.dart
├── providers/
│   ├── auth_provider_test.dart
│   ├── horoscope_provider_test.dart
│   └── birth_chart_provider_test.dart
└── utils/
    ├── date_formatter_test.dart
    └── astro_calculations_test.dart
```

### Widget Test Patterns

All widget tests follow the **Arrange-Act-Assert** pattern:

```dart
testWidgets('HoroscopeCard displays zodiac sign and content', (WidgetTester tester) async {
  // Arrange: Set up test data and widgets
  const horoscope = Horoscope(
    sign: 'Aries',
    content: 'Today is your day',
    date: '2024-11-20',
  );

  // Act: Build widget and perform interactions
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: HoroscopeCard(horoscope: horoscope),
      ),
    ),
  );

  // Assert: Verify expected outcomes
  expect(find.text('Aries'), findsOneWidget);
  expect(find.text('Today is your day'), findsOneWidget);
});
```

### Coverage Requirements
- **UI Components**: Test rendering, state changes, user interactions
- **Business Logic**: Test calculations, data transformations, edge cases
- **Error States**: Test loading states, error messages, retry logic
- **Accessibility**: Test semantic labels, contrast ratios, touch targets

## Integration Testing Strategy

### Scope
Integration tests validate complete feature workflows within the app, testing interactions between multiple widgets and business logic layers.

### Test Organization
```
integration_test/
├── onboarding_flow_test.dart
├── horoscope_feature_test.dart
├── birth_chart_feature_test.dart
├── compatibility_feature_test.dart
└── auth_feature_test.dart
```

### Execution Approach
- Launch the full app using `IntegrationTestWidgetsFlutterBinding`
- Perform real navigation flows
- Test state management integration
- Verify data persistence (local storage, caching)

### Example Integration Test
```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Complete horoscope viewing flow', (WidgetTester tester) async {
    // Launch app
    app.main();
    await tester.pumpAndSettle();

    // Navigate to horoscope feature
    await tester.tap(find.text('Horoscope'));
    await tester.pumpAndSettle();

    // Select zodiac sign
    await tester.tap(find.byKey(Key('zodiac_selector')));
    await tester.pumpAndSettle();

    // Verify horoscope loads
    expect(find.byType(HoroscopeContent), findsOneWidget);
  });
}
```

## E2E Testing Strategy

### Scope
E2E tests validate critical user journeys from a user's perspective using Playwright for browser-based testing.

### Test Organization
```
tests/e2e/
├── onboarding.spec.ts
├── horoscope.spec.ts
├── birth-chart.spec.ts
├── compatibility.spec.ts
└── auth.spec.ts
```

### Critical Paths for E2E Coverage

1. **Complete Onboarding**
   - Sign up with email
   - Enter birth details
   - Complete tutorial
   - View initial horoscope

2. **Daily Horoscope Workflow**
   - Select zodiac sign
   - View horoscope content
   - Share horoscope
   - Navigate historical horoscopes

3. **Chart Generation & Viewing**
   - Generate natal chart
   - Interact with chart (zoom, pan)
   - View interpretations
   - Share chart

4. **Partner Compatibility**
   - Enter partner details
   - View compatibility score
   - Explore detailed comparisons
   - Share results

### Test Data & Mocking

- **API Mocking**: Mock backend responses for fast, reliable tests
- **Test Data**: Use consistent, realistic test data across all tests
- **Database**: Reset state between test runs

## Error Scenarios to Test

### Network Errors
- API timeout (> 30 seconds)
- Connection refused
- Network disconnected
- Slow network (simulate with throttling)

### User Input Errors
- Invalid birth date (future date, very old date)
- Invalid timezone selection
- Incomplete form submissions
- Duplicate entries

### System Errors
- Memory constraints (low device memory)
- Storage full
- App background/foreground transitions
- Device orientation changes

### Edge Cases
- Empty horoscope data
- Very long text content
- Rapid navigation between screens
- Concurrent requests (rapid sign changes)

## Performance Testing

### Widget Test Performance
- Each test should complete in < 500ms
- Group related tests to reduce setup overhead
- Measure test execution times regularly

### Integration Test Performance
- Complete feature flows should complete in < 5 seconds
- Monitor for slow animations or janky scrolling
- Test with realistic data volumes

### E2E Test Performance
- Page load time target: < 3 seconds
- API response time target: < 1 second
- Animation smoothness: maintain 60fps

## Accessibility Testing

### Widget Level
- Test semantic labels with screen readers
- Verify minimum touch target sizes (48x48 logical pixels)
- Check color contrast ratios (4.5:1 for text)
- Test keyboard navigation

### Integration Level
- Full app navigation with keyboard only
- Screen reader usability for complete workflows
- Color contrast across all UI elements

### E2E Level
- Use Playwright's accessibility testing
- Verify WCAG 2.1 AA compliance
- Test with actual screen readers

## CI/CD Integration

### Pre-commit
- Fast linting checks
- Quick smoke tests (< 30 seconds)

### On-commit
- Widget tests run (< 1 minute)
- Code coverage analysis
- Coverage report generated

### On-PR
- All widget tests (< 2 minutes)
- Integration tests (< 5 minutes)
- Coverage comparison with main branch

### Pre-staging Deployment
- Full widget + integration test suite
- E2E tests on staging environment (< 10 minutes)
- Performance tests
- Accessibility audit

### Pre-production Deployment
- Full test suite passing
- Manual QA sign-off
- Smoke tests on production

## Test Metrics & Monitoring

### Coverage Metrics
- Line coverage target: > 80% in critical paths
- Branch coverage: > 70%
- Function coverage: > 85%

### Quality Metrics
- Test pass rate: 99%+ (no flaky tests)
- Test execution time: < 5 minutes total (CI/CD)
- Defect detection rate: Tests catch regressions before production

### Maintenance Metrics
- Test-to-code ratio: Aim for 1:1 or higher
- Test refactoring: Update tests proactively as code evolves
- Flaky test monitoring: Zero tolerance for flakiness

## Flaky Test Resolution

When encountering flaky tests:
1. **Add explicit waits** instead of arbitrary delays
2. **Use pumpAndSettle()** to wait for animations
3. **Use waitForLoadState()** for network activity
4. **Increase timing tolerances** only after identifying root cause
5. **Review test design** - Is it testing the right thing at the right level?

## Testing Best Practices

### Do's ✅
- Keep tests focused and independent
- Use meaningful test names that describe expected behavior
- Test user behavior, not implementation details
- Mock external dependencies
- Maintain consistent test data
- Run tests locally before committing
- Review test coverage regularly

### Don'ts ❌
- Don't test the test framework
- Don't hardcode values in tests
- Don't create overly complex test fixtures
- Don't skip tests "just to move fast"
- Don't test implementation details
- Don't create flaky tests with arbitrary delays
- Don't ignore test failures

## Documentation References

- [Playwright Setup Guide](./playwright-setup.md)
- [Flutter Testing Documentation](https://flutter.dev/docs/testing)
- [Riverpod Testing Patterns](https://docs.riverpod.dev/docs/essentials/testing)
- [Testing Agent](../agents/testing-agent.md)

## Getting Started

1. Read the [Playwright Setup Guide](./playwright-setup.md) for E2E test environment setup
2. Review existing widget tests as examples
3. Follow the patterns outlined in this document
4. Use the testing-agent for complex testing scenarios

## Questions & Support

For testing-related questions or support, refer to the [testing-agent](../agents/testing-agent.md) for expert guidance on test design, implementation, and troubleshooting.
