# Kundali Astrology - Flutter Frontend

A production-ready Flutter application for personalized Vedic astrology readings, birth chart generation, and AI-powered life predictions.

**Status:** 🟡 Phase 1-2 In Development (40% Complete)

---

## 🎯 Project Overview

This Flutter application provides users with:
- 🔮 **Daily Horoscope** - Personalized daily readings
- 📊 **Birth Chart Generation** - Complete Kundali with planetary positions
- 💕 **Compatibility Checker** - Relationship compatibility analysis
- 🪐 **Planetary Transits** - Current planetary movements and meanings
- 🌙 **Moon Phases** - Lunar calendar and phase information


---

## 🏗️ Project Structure

```
lib/
├── core/                          # Core utilities and configurations
│   ├── theme/                     # Design system
│   │   ├── app_colors.dart        # 29+ colors (planets, elements, semantic)
│   │   ├── app_typography.dart    # Material 3 typography (Playfair, Lora, Montserrat)
│   │   ├── app_spacing.dart       # 8-point grid system
│   │   └── app_theme.dart         # Light/dark Material 3 themes
│   │
│   ├── widgets/                   # 40+ reusable components
│   │   ├── buttons.dart           # 7 button variants
│   │   ├── cards.dart             # 8 card variants
│   │   ├── inputs.dart            # 7 input field variants
│   │   ├── loading_indicators.dart  # 8+ loading components
│   │   ├── error_states.dart      # 11 error/empty state components
│   │   └── index.dart             # Barrel export
│   │
│   └── navigation/                # Routing & navigation
│       ├── app_routes.dart        # 22 named routes
│       ├── navigation_service.dart # Global navigation service
│       ├── route_generator.dart    # Route handling
│       ├── app_shell.dart         # Main app scaffold with bottom nav
│       └── index.dart             # Barrel export
│
├── data/                          # Data layer
│   ├── models/                    # Data models
│   │   ├── auth_models.dart       # Auth request/response models
│   │   └── kundali_models.dart    # (To be implemented)
│   │
│   └── services/                  # API & business logic
│       ├── auth_service.dart      # JWT token management
│       ├── api_client.dart        # HTTP client with JWT interceptor
│       ├── kundali_service.dart   # (To be implemented)
│       └── index.dart             # Barrel export
│
└── presentation/                  # UI layer (Screens)
    ├── screens/                   # All app screens
    │   ├── auth/                  # Login, signup, password reset (To build)
    │   ├── onboarding/            # Birth date, time, location collection (To build)
    │   ├── home/                  # Dashboard (To build)
    │   ├── kundali/               # Birth chart (To build)
    │   ├── predictions/           # Life predictions (To build)
    │   └── profile/               # User settings (To build)
    │
    ├── widgets/                   # Screen-specific widgets
    └── shell/
        └── app_shell.dart         # Navigation shell with bottom nav
```

---

## 🚀 Getting Started

### Prerequisites
- Flutter SDK (3.0.0 or higher)
- Dart SDK (included with Flutter)
- IDE: Android Studio, VS Code, or Xcode
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/kundali-astrology.git
cd kundali-astrology/client
```

2. **Install dependencies**
```bash
flutter pub get
```

3. **Generate code**
```bash
# For Hive and other code generation
flutter pub run build_runner build
```

4. **Run the app**
```bash
# Development
flutter run

# Release build
flutter run --release

# Specific platform
flutter run -d chrome      # Web
flutter run -d emulator    # Android emulator
flutter run -d simulator   # iOS simulator
```

---

## 📦 Dependencies

### Core Framework
- **flutter**: Flutter SDK
- **cupertino_icons**: iOS icons

### State Management (To Switch to Riverpod)
- **provider**: Current state management (planning to migrate to Riverpod)

### HTTP & Networking
- **dio**: HTTP client for API calls
- **dio_cache_interceptor**: Response caching

### Local Storage
- **hive**: Local database for offline support
- **hive_flutter**: Hive integration
- **shared_preferences**: Token and settings storage

### UI & Design
- **google_fonts**: Custom fonts (Playfair, Lora, Montserrat)
- **flutter_svg**: SVG support
- **flutter_animate**: Smooth animations
- **carousel_slider**: Card carousels

### Data Visualization
- **fl_chart**: Beautiful charts for predictions and transits
- **shimmer**: Shimmer loading effects

### Utilities
- **intl**: Date/time formatting

### Dev Dependencies
- **hive_generator**: Code generation for Hive
- **build_runner**: Code generation runner

---

## 🎨 Design System

### Colors
- **Primary:** Indigo (#6366F1)
- **Secondary:** Pale Violet Red (#DB7093)
- **Planetary Colors:** Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- **Element Colors:** Fire (Red), Earth (Brown), Air (Yellow), Water (Blue)
- **Semantic:** Success (Green), Warning (Orange), Error (Red), Info (Blue)
- **Gradients:** Cosmic, Nebula, Sunset

### Typography
- **Headings:** Playfair Display (elegant, astrological)
- **Body:** Lora (readable, serif for interpretations)
- **UI:** Montserrat (clean, sans-serif for buttons/labels)

### Spacing
- **Grid System:** 8-point grid
- **Scales:** 4px, 8px, 16px, 24px, 32px, 48px, 64px
- **Responsive:** Adapts to screen size

### Themes
- **Light Mode:** Soft backgrounds, dark text
- **Dark Mode:** Deep backgrounds, light text
- **Accessibility:** WCAG-compliant contrast ratios (4.5:1 minimum)

---

## 🔐 Authentication Flow

The app uses JWT tokens for secure authentication:

```
1. User enters login credentials
   ↓
2. AuthService.login(email, password)
   ↓
3. ApiClient POST /auth/login
   ↓
4. Backend returns access_token + refresh_token
   ↓
5. AuthService stores tokens in SharedPreferences
   ↓
6. ApiClient interceptor auto-injects JWT in headers
   ↓
7. User navigates to Dashboard
   ↓
8. (Background) Automatic token refresh when <5 min remaining
```

### Token Management
- **Access Token:** Short-lived (15 minutes)
- **Refresh Token:** Long-lived (7 days)
- **Storage:** SharedPreferences (encrypted)
- **Auto-Refresh:** Automatic when near expiry

---

## 🏗️ Architecture

### Clean Architecture Pattern
- **Presentation Layer:** UI, screens, widgets
- **Data Layer:** API client, services, models
- **Domain Layer:** Business logic (via services)

### State Management
Currently using **Provider** (planning migration to **Riverpod**):
- Planned Providers:
  - AuthProvider: Authentication state
  - KundaliProvider: Birth chart data
  - PredictionProvider: Life predictions
  - SettingsProvider: User preferences

### API Integration
- **Base URL:** `http://localhost:8001` (dev) / `https://api.kundali.app` (prod)
- **JWT Injection:** Automatic via ApiClient interceptor
- **Error Handling:** Custom exceptions (AuthException, NetworkException, etc.)
- **Response Format:** Standardized APIResponse wrapper

---

## 📝 Code Style & Conventions

### Naming
- Classes: `PascalCase` (e.g., `AuthService`)
- Variables: `camelCase` (e.g., `birthDate`)
- Constants: `camelCase` (e.g., `defaultPadding`)
- Files: `snake_case` (e.g., `auth_service.dart`)
- Directories: `snake_case` (e.g., `core/widgets/`)

### Imports
- Organize in groups: Flutter, packages, relative imports
- Use barrel exports (`index.dart`) for clean imports

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:kundali/core/widgets/index.dart';
```

### Documentation
- All public classes and methods have docstrings
- Complex logic has inline comments
- Use `///` for documentation comments

---

## 🧪 Testing

### Run Tests
```bash
# Unit tests
flutter test

# Widget tests
flutter test test/widgets/

# Coverage
flutter test --coverage
```

### Test Structure
```
test/
├── unit/
│   ├── services/
│   └── models/
├── widget/
│   ├── screens/
│   └── widgets/
└── integration/
```

---

## 📱 Platform-Specific Setup

### Android
- Min SDK: API 21
- Target SDK: API 33+
- Run: `flutter run`

### iOS
- Min version: 11.0
- Run: `flutter run` (simulator or device)

### Web
- Chrome/Firefox support
- Run: `flutter run -d chrome`

---

## 🚀 Building for Release

### Android
```bash
# Build APK
flutter build apk

# Build app bundle
flutter build appbundle
```

### iOS
```bash
# Build framework
flutter build ios

# Build ipa
flutter build ipa
```

### Web
```bash
flutter build web
```

---

## 📚 Features & Status

| Feature | Status | Progress |
|---------|--------|----------|
| Design System | ✅ Complete | 100% |
| Widget Library | ✅ Complete | 100% |
| Navigation | ✅ Complete | 100% |
| Auth Service | ⚙️ In Progress | 80% |
| Auth Screens | ⏳ Pending | 0% |
| Dashboard | ⏳ Pending | 0% |
| Birth Chart | ⏳ Pending | 0% |
| Predictions | ⏳ Pending | 0% |
| Transits | ⏳ Pending | 0% |
| Profile | ⏳ Pending | 0% |

---

## 🔗 Related Documentation

- [API Documentation](../docs/api/api-complete-reference.md)
- [Design System Guide](../docs/design/design-system.md)
- [Development Progress](../docs/progress/development-status.md)
- [Master Control Document](../docs/claude.md)

---

## 🐛 Troubleshooting

### Build Issues
```bash
# Clean build
flutter clean
flutter pub get
flutter pub run build_runner clean
flutter pub run build_runner build

# Get latest packages
flutter pub upgrade
```

### Hot Reload Not Working
```bash
# Stop running instance
Ctrl+C (or Cmd+C)

# Run with verbose
flutter run -v
```

### Dependency Conflicts
```bash
# Resolve dependencies
flutter pub get

# Check pub.dev for latest versions
flutter pub outdated
```

---

## 📞 Support & Contact

- **Issues:** GitHub Issues
- **Documentation:** See `/docs` folder
- **Backend API:** See backend README
- **Team:** Development team

---

## 📄 License

This project is licensed under the MIT License.

---

## 🎯 Next Steps

1. **Run `flutter pub get`** to install dependencies
2. **Review design system** in `lib/core/theme/`
3. **Check widget library** in `lib/core/widgets/`
4. **Start building screens** in `lib/presentation/screens/`
5. **Integrate API** using auth service
6. **Setup state management** with Provider (or Riverpod)

---

**Last Updated:** November 2025
**Maintained by:** Development Team
