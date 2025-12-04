/// Application Configuration
/// Centralized configuration for the entire app
class AppConfig {
  // API Configuration - Development URLs
  // localhost: For Flutter Web (Chrome) or running from same machine
  // 192.168.0.107: For physical devices on your network (RECOMMENDED)
  // 10.0.2.2: For Android Emulator running on your computer

  static const String apiBaseUrlLocalhost = 'http://127.0.0.1:8000/api';
  static const String apiBaseUrlNetworkIP = 'http://192.168.0.107:8000/api';
  static const String apiBaseUrlAndroidEmulator = 'http://10.0.2.2:8000/api';
  static const String apiBaseUrlProduction = 'https://api.kundali-app.com/api';
  static const String apiBaseUrlRailway = 'https://web-production-743d0.up.railway.app/api';

  // CHANGE THIS based on where you're running the app:
  // - Physical Device or iOS Simulator: use apiBaseUrlNetworkIP
  // - Android Emulator: use apiBaseUrlAndroidEmulator
  // - Flutter Web (Chrome): use apiBaseUrlLocalhost
  // - Railway Deployment: use apiBaseUrlRailway
  // - Production: use apiBaseUrlProduction
  static const String apiBaseUrl =
      apiBaseUrlRailway; // <-- USING RAILWAY DEPLOYMENT

  // Network Timeouts
  // Increased to 120 seconds for Kundali generation (complex calculations take 30-60s)
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(minutes: 2); // 120 seconds

  /// Get the appropriate API base URL based on environment
  /// Can be used for dynamic environment detection
  static String getApiBaseUrl({bool isProduction = false}) {
    return isProduction ? apiBaseUrlProduction : apiBaseUrlProduction;
  }
}
