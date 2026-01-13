// import 'dart:io';
// import 'package:flutter/foundation.dart' show kIsWeb;

// /// Application Configuration
// /// Centralized configuration for the entire app
// class AppConfig {
//   // API Configuration
//   static const int serverPort = 8000; // Your backend server port

//   // Fallback IPs to try in order (your most common networks)
//   static const List<String> fallbackIPs = [
//     '192.168.100.31', // Your current network
//     '192.168.0.103',
//     // Your previous network
//     // Another known network
//     '192.168.1.1', // Common router IP range
//     '10.0.0.1', // Another common range
//   ];

//   // static const String apiBaseUrlLocalhost = 'http://127.0.0.1:8000/api';
//   static const String apiBaseUrlAndroidEmulator = 'http://10.0.2.2:8000/api';
//   static const String apiBaseUrlLocalhost = 'http://10.10.10.117:8000/api';
//   static const String apiBaseUrlProduction = 'https://api.kundali-app.com/api';
//   static const String apiBaseUrlRailway =
//       'https://web-production-743d0.up.railway.app/api';

//   // Network Timeouts
//   static const Duration connectTimeout = Duration(seconds: 30);
//   static const Duration receiveTimeout = Duration(minutes: 2);

//   /// Automatically detect the best API URL based on platform and network
//   static Future<String> getApiBaseUrl({bool isProduction = false}) async {
//     if (isProduction) {
//       return apiBaseUrlProduction;
//     }

//     // Web platform - use localhost
//     if (kIsWeb) {
//       return apiBaseUrlLocalhost;
//     }

//     // Android Emulator detection
//     if (Platform.isAndroid) {
//       try {
//         // Try to detect if running in emulator
//         final interfaces = await NetworkInterface.list();
//         final isEmulator = interfaces.any(
//           (interface) => interface.addresses.any(
//             (addr) => addr.address.startsWith('10.0.2'),
//           ),
//         );
//         if (isEmulator) {
//           return apiBaseUrlAndroidEmulator;
//         }
//       } catch (e) {
//         print('Error detecting emulator: $e');
//       }
//     }

//     // Physical device - auto-detect server IP
//     return await _detectServerIP();
//   }

//   /// Detect server IP by scanning the local network
//   static Future<String> _detectServerIP() async {
//     try {
//       // Get device's own IP to determine network range
//       final interfaces = await NetworkInterface.list();

//       for (var interface in interfaces) {
//         for (var addr in interface.addresses) {
//           // Look for IPv4 addresses (not loopback)
//           if (addr.type == InternetAddressType.IPv4 && !addr.isLoopback) {
//             final deviceIP = addr.address;
//             print('Device IP: $deviceIP');

//             // Extract network prefix (e.g., 192.168.100 from 192.168.100.45)
//             final parts = deviceIP.split('.');
//             if (parts.length == 4) {
//               final networkPrefix = '${parts[0]}.${parts[1]}.${parts[2]}';

//               // Try common server IPs in the same network
//               final ipsToTry = [
//                 '$networkPrefix.1', // Router (often the dev machine)
//                 '$networkPrefix.100', // Common static IP
//                 '$networkPrefix.101',
//                 '$networkPrefix.31', // Your current server IP suffix
//                 '$networkPrefix.103', // Your previous server IP suffix
//                 ...fallbackIPs, // Fallback to known IPs
//               ];

//               // Test each IP
//               for (var ip in ipsToTry) {
//                 final url = 'http://$ip:$serverPort/api';
//                 if (await _testConnection(url)) {
//                   print('✓ Found server at: $url');
//                   return url;
//                 }
//               }
//             }
//           }
//         }
//       }
//     } catch (e) {
//       print('Error during IP detection: $e');
//     }

//     // Final fallback - use first fallback IP
//     final fallbackUrl = 'http://${fallbackIPs.first}:$serverPort/api';
//     print('⚠ Using fallback URL: $fallbackUrl');
//     return fallbackUrl;
//   }

//   /// Test if server is reachable at given URL
//   static Future<bool> _testConnection(String url) async {
//     try {
//       final socket = await Socket.connect(
//         url.replaceAll('http://', '').split(':')[0],
//         serverPort,
//         timeout: Duration(milliseconds: 500),
//       );
//       socket.destroy();
//       return true;
//     } catch (e) {
//       return false;
//     }
//   }

//   /// Cached API URL (call getApiBaseUrl() once and cache the result)
//   static String? _cachedApiUrl;

//   /// Get cached API URL or detect it
//   static Future<String> get apiBaseUrl async {
//     _cachedApiUrl ??= await getApiBaseUrl();
//     return _cachedApiUrl!;
//   }

//   /// Force refresh the API URL (useful when switching networks)
//   static Future<String> refreshApiUrl() async {
//     _cachedApiUrl = await getApiBaseUrl();
//     return _cachedApiUrl!;
//   }
// }

import 'package:flutter/foundation.dart' show kIsWeb;

/// Application Configuration
/// Centralized configuration for the entire app
class AppConfig {
  /// API Base URLs
  static const String apiBaseUrlRailway =
      'https://web-production-743d0.up.railway.app/api';

  /// Network Timeouts
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(minutes: 2);

  /// Cached API URL
  static String? _cachedApiUrl;

  /// Get API Base URL (always Railway – production)
  static Future<String> get apiBaseUrl async {
    _cachedApiUrl ??= apiBaseUrlRailway;
    return _cachedApiUrl!;
  }

  /// Force refresh API URL (kept for future flexibility)
  static Future<String> refreshApiUrl() async {
    _cachedApiUrl = apiBaseUrlRailway;
    return _cachedApiUrl!;
  }
}
