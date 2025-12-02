# Google Maps Integration Setup Guide

This guide explains how to configure Google Maps API keys for both Android and iOS platforms.

## Prerequisites

1. Google Cloud Console account
2. Project with billing enabled
3. Google Maps and Places APIs enabled

---

## Step 1: Enable Required APIs in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps SDK for Android**
   - **Maps SDK for iOS**
   - **Places API**
   - **Geocoding API**

To enable APIs:
- Click "APIs & Services" → "Library"
- Search for each API and click "Enable"

---

## Step 2: Create API Keys

### For Android:

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Select **Application restrictions** → **Android apps**
4. Add your app's SHA-1 fingerprint and package name

**Get SHA-1 Fingerprint:**
```bash
# Windows (Command Prompt)
cd android
./gradlew signingReport

# macOS/Linux
cd android
./gradlew signingReport
```

Look for the line: `SHA-1: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

**Package Name:** `com.example.client` (from AndroidManifest.xml)

### For iOS:

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Select **Application restrictions** → **iOS apps**
4. Add your app's Bundle ID: `com.example.client`

**Get Bundle ID:**
- Open `ios/Runner.xcodeproj` in Xcode
- Select Runner → General tab
- Check "Bundle Identifier"

---

## Step 3: Configure Android

### Update `android/app/build.gradle.kts`:

```kotlin
android {
    // ... existing configuration ...

    defaultConfig {
        // ... existing config ...

        // Add Google Maps API key
        manifestPlaceholders["com.google.android.geo.API_KEY"] = "YOUR_ANDROID_API_KEY"
    }
}
```

### Update `android/app/src/main/AndroidManifest.xml`:

Add inside `<manifest>` (before `<application>`):

```xml
<!-- Google Maps API Key -->
<meta-data
    android:name="com.google.android.geo.API_KEY"
    android:value="YOUR_ANDROID_API_KEY" />
```

Or use the manifestPlaceholders approach above (recommended).

### Add Required Permissions:

```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

---

## Step 4: Configure iOS

### Update `ios/Runner/Info.plist`:

Add the following keys:

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>This app needs your location to calculate your accurate birth chart.</string>

<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>This app needs your location to calculate your accurate birth chart.</string>

<key>UIBackgroundModes</key>
<array>
    <string>location</string>
</array>

<key>NSLocationDefaultAccuracyReduction</key>
<false/>
```

### Update `ios/Runner/GeneratedPluginRegistrant.m`:

Add Google Maps API key in `ios/Podfile`:

```ruby
post_install do |installer|
  installer.pods_project.targets.each do |target|
    # ... existing code ...

    # Add Google Maps API Key
    target.build_configurations.each do |config|
      config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] ||= [
        '$(inherited)',
        'GOOGLE_MAPS_API_KEY=YOUR_IOS_API_KEY'
      ]
    end
  end
end
```

Or add to `ios/Runner/Info.plist`:

```xml
<key>com.google.ios.maps.API_KEY</key>
<string>YOUR_IOS_API_KEY</string>
```

---

## Step 5: Add Location Permissions Handler

### Update `ios/Runner/GeneratedPluginRegistrant.m` or use pubspec.yaml:

The `geolocator` plugin handles location permissions. Make sure you have proper setup.

**For iOS location permissions, update `ios/Runner/Info.plist`:**

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to calculate your birth chart accurately.</string>
```

---

## Step 6: Environment Variables (Optional but Recommended)

### Use Flutter's Build Arguments:

**For Android - in `android/local.properties`:**
```properties
MAPS_API_KEY=YOUR_ANDROID_API_KEY
```

**For iOS - in environment or Xcode build settings:**
```bash
export MAPS_API_KEY="YOUR_IOS_API_KEY"
```

---

## Step 7: Test the Integration

### Run the app:

```bash
# Clean build
flutter clean

# Get dependencies
flutter pub get

# Run on Android
flutter run -d <device_id>

# Run on iOS
flutter run -d <device_id>
```

### Test Checklist:

- [ ] Navigate to onboarding location screen
- [ ] Click "Pick from Map" button
- [ ] Map loads and shows current location
- [ ] Can tap on map to select location
- [ ] Address details populate automatically
- [ ] Coordinates are captured accurately
- [ ] "Confirm Location" saves data to form
- [ ] Latitude/Longitude are included in kundali generation request

---

## Step 8: Restrict API Keys (Security)

After testing, restrict your API keys:

1. Go to **APIs & Services** → **Credentials**
2. Click on each API key
3. Set **Application restrictions**:
   - **Android**: Select Android apps, add SHA-1 fingerprint and package name
   - **iOS**: Select iOS apps, add Bundle ID
4. Set **API restrictions**:
   - Maps SDK for Android
   - Maps SDK for iOS
   - Places API
   - Geocoding API

---

## Troubleshooting

### "Maps API key not found"
- Ensure API key is correctly added to build.gradle.kts and AndroidManifest.xml
- Check that the API key is enabled for Maps SDK for Android

### "Geocoding not working"
- Ensure Geocoding API is enabled in Google Cloud Console
- Check that API key has Geocoding API access

### "Permission denied"
- Android: Check that location permissions are requested at runtime
- iOS: Check Info.plist has required location permission keys

### Build fails
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter pub upgrade
flutter run
```

### Black screen on map
- Ensure your API key is valid
- Check that the Maps API is enabled
- Try restarting the app

---

## API Keys Storage (Production)

**NEVER commit API keys to version control!**

### Option 1: Environment Variables
```bash
# .env or .env.local (add to .gitignore)
MAPS_API_KEY=your_key_here
```

### Option 2: Secrets Management
Use Firebase Remote Config or similar service to manage keys securely.

### Option 3: Build Configuration
Use different keys for debug and release builds:
```gradle
buildTypes {
    debug {
        resValue "string", "maps_api_key", "DEBUG_KEY"
    }
    release {
        resValue "string", "maps_api_key", "RELEASE_KEY"
    }
}
```

---

## References

- [Google Maps Android SDK Docs](https://developers.google.com/maps/documentation/android-sdk/overview)
- [Google Maps iOS SDK Docs](https://developers.google.com/maps/documentation/ios-sdk/overview)
- [Google Cloud Console](https://console.cloud.google.com/)
- [google_maps_flutter Plugin](https://pub.dev/packages/google_maps_flutter)
- [geolocator Plugin](https://pub.dev/packages/geolocator)
- [geocoding Plugin](https://pub.dev/packages/geocoding)

---

## Next Steps

After configuring API keys:

1. Update kundali generation endpoint to use latitude/longitude
2. Test location selection end-to-end
3. Verify accurate timezone calculation with coordinates
4. Deploy to production with restricted API keys

---

## Support

If you encounter issues:
1. Check Google Cloud Console for API errors
2. Verify API quotas haven't been exceeded
3. Check device logs: `flutter logs`
4. Test with a different device or emulator
