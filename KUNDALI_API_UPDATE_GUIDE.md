# Kundali Generation API - Update Guide

This guide shows exactly how to update the API integration to use latitude/longitude from Google Maps.

---

## Current Status

**Location:** `client/lib/presentation/screens/onboarding/onboarding_confirmation_screen.dart`

**Method:** `_handleGenerateChart()` (Lines 358-397)

**Current Status:** Simulated with 2-second delay (TODO)

---

## What Data is Available

After user selects location with Google Maps, the `widget.birthData` contains:

```dart
{
  'birthDate': DateTime,           // e.g., DateTime(2000, 5, 15)
  'birthTime': TimeOfDay,          // e.g., TimeOfDay(hour: 14, minute: 30)
  'timeUnknown': bool,             // e.g., false
  'city': String,                  // e.g., 'Mumbai'
  'state': String,                 // e.g., 'Maharashtra'
  'country': String,               // e.g., 'India'
  'latitude': double,              // e.g., 19.0760 (NEW from map picker)
  'longitude': double,             // e.g., 72.8777 (NEW from map picker)
}
```

---

## Updated Implementation

### Option 1: Using Dio HttpClient (Recommended)

If your project uses Dio for HTTP requests:

```dart
/// Handle chart generation with coordinates
Future<void> _handleGenerateChart() async {
  setState(() => _isLoading = true);

  try {
    // Extract data from birthData
    final birthData = widget.birthData ?? {};
    final birthDate = birthData['birthDate'] as DateTime?;
    final birthTime = birthData['birthTime'] as TimeOfDay?;
    final timeUnknown = birthData['timeUnknown'] as bool? ?? false;

    // Location data (with coordinates from map picker)
    final city = birthData['city'] as String? ?? '';
    final state = birthData['state'] as String? ?? '';
    final country = birthData['country'] as String? ?? '';
    final latitude = birthData['latitude'] as double?;
    final longitude = birthData['longitude'] as double?;

    // Format time for API (handle if time is unknown)
    String birthTimeStr;
    if (timeUnknown) {
      birthTimeStr = '12:00'; // Default noon if time unknown
    } else {
      final hour = birthTime?.hour.toString().padLeft(2, '0') ?? '12';
      final minute = birthTime?.minute.toString().padLeft(2, '0') ?? '00';
      birthTimeStr = '$hour:$minute';
    }

    // Format date for API (ISO 8601)
    final birthDateStr = birthDate?.toIso8601String().split('T').first ?? '';

    // Prepare request data
    final requestData = {
      'birthDate': birthDateStr,        // e.g., "2000-05-15"
      'birthTime': birthTimeStr,        // e.g., "14:30"
      'timeUnknown': timeUnknown,       // e.g., false
      'city': city,                     // e.g., "Mumbai"
      'state': state,                   // e.g., "Maharashtra"
      'country': country,               // e.g., "India"
      // NEW: Include coordinates for accurate timezone calculation
      if (latitude != null) 'latitude': latitude,   // e.g., 19.0760
      if (longitude != null) 'longitude': longitude, // e.g., 72.8777
    };

    // Log request for debugging (remove in production)
    print('Generating Kundali with data: $requestData');

    // Call backend API
    final response = await Dio().post(
      'https://your-api-domain.com/astrology/kundali/generate',
      data: requestData,
      options: Options(
        headers: {
          'Content-Type': 'application/json',
          // Add auth token if needed:
          // 'Authorization': 'Bearer $token',
        },
      ),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      // Success - navigate to dashboard
      if (mounted) {
        Navigator.of(context).pushNamedAndRemoveUntil(
          AppRoutes.dashboard,
          (Route<dynamic> route) => false,
        );

        ScaffoldMessenger.of(context).showSnackBar(
          SuccessSnackBar.show(
            message: 'Your Vedic birth chart has been generated successfully!',
          ),
        );
      }
    } else {
      throw Exception('API returned status ${response.statusCode}');
    }
  } on DioException catch (e) {
    // Handle Dio errors
    String errorMessage = 'Failed to generate chart';

    if (e.response != null) {
      // Server error with response
      final errorData = e.response?.data;
      if (errorData is Map && errorData.containsKey('message')) {
        errorMessage = errorData['message'] as String;
      }
    } else if (e.type == DioExceptionType.connectionTimeout) {
      errorMessage = 'Connection timeout. Please check your internet.';
    } else if (e.type == DioExceptionType.receiveTimeout) {
      errorMessage = 'Server response timeout. Please try again.';
    }

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        ErrorSnackBar.show(message: errorMessage),
      );
    }
  } catch (e) {
    // Handle other errors
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        ErrorSnackBar.show(
          message: 'Error: ${e.toString()}',
        ),
      );
    }
  } finally {
    if (mounted) {
      setState(() => _isLoading = false);
    }
  }
}
```

---

### Option 2: Using Http Package

If your project uses the `http` package:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<void> _handleGenerateChart() async {
  setState(() => _isLoading = true);

  try {
    final birthData = widget.birthData ?? {};
    final birthDate = birthData['birthDate'] as DateTime?;
    final birthTime = birthData['birthTime'] as TimeOfDay?;

    // Format time
    String birthTimeStr;
    if (birthData['timeUnknown'] as bool? ?? false) {
      birthTimeStr = '12:00';
    } else {
      final hour = birthTime?.hour.toString().padLeft(2, '0') ?? '12';
      final minute = birthTime?.minute.toString().padLeft(2, '0') ?? '00';
      birthTimeStr = '$hour:$minute';
    }

    // Format date
    final birthDateStr = birthDate?.toIso8601String().split('T').first ?? '';

    // Prepare request body
    final requestBody = {
      'birthDate': birthDateStr,
      'birthTime': birthTimeStr,
      'timeUnknown': birthData['timeUnknown'] ?? false,
      'city': birthData['city'] ?? '',
      'state': birthData['state'] ?? '',
      'country': birthData['country'] ?? '',
      'latitude': birthData['latitude'],     // From map picker
      'longitude': birthData['longitude'],   // From map picker
    };

    // Make API call
    final response = await http.post(
      Uri.parse('https://your-api-domain.com/astrology/kundali/generate'),
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': 'Bearer $token',
      },
      body: jsonEncode(requestBody),
    ).timeout(const Duration(seconds: 30));

    if (response.statusCode == 200 || response.statusCode == 201) {
      // Success
      final responseData = jsonDecode(response.body);
      print('Kundali generated: ${responseData['id']}');

      if (mounted) {
        Navigator.of(context).pushNamedAndRemoveUntil(
          AppRoutes.dashboard,
          (Route<dynamic> route) => false,
        );

        ScaffoldMessenger.of(context).showSnackBar(
          SuccessSnackBar.show(
            message: 'Your Vedic birth chart has been generated!',
          ),
        );
      }
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(
        errorData['message'] ?? 'Failed with status ${response.statusCode}',
      );
    }
  } on TimeoutException {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        ErrorSnackBar.show(
          message: 'Request timeout. Please check your connection.',
        ),
      );
    }
  } catch (e) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        ErrorSnackBar.show(message: 'Error: ${e.toString()}'),
      );
    }
  } finally {
    if (mounted) {
      setState(() => _isLoading = false);
    }
  }
}
```

---

### Option 3: Using REST Service Class (Best Practice)

If your project has a dedicated service class:

```dart
// In your service/repository class
class AstrologyService {
  final Dio _dio;

  AstrologyService(this._dio);

  /// Generate Kundali chart with birth data and location coordinates
  Future<KundaliResponse> generateKundali({
    required DateTime birthDate,
    required TimeOfDay birthTime,
    required bool timeUnknown,
    required String city,
    required String state,
    required String country,
    double? latitude,    // From Google Maps picker
    double? longitude,   // From Google Maps picker
  }) async {
    try {
      // Format data
      final birthDateStr = birthDate.toIso8601String().split('T').first;
      final birthTimeStr = timeUnknown
          ? '12:00'
          : '${birthTime.hour.toString().padLeft(2, '0')}:'
            '${birthTime.minute.toString().padLeft(2, '0')}';

      // Prepare request
      final data = {
        'birthDate': birthDateStr,
        'birthTime': birthTimeStr,
        'timeUnknown': timeUnknown,
        'city': city,
        'state': state,
        'country': country,
        if (latitude != null) 'latitude': latitude,
        if (longitude != null) 'longitude': longitude,
      };

      // Make request
      final response = await _dio.post(
        '/astrology/kundali/generate',
        data: data,
      );

      // Parse response
      return KundaliResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Exception _handleDioError(DioException e) {
    if (e.response?.data is Map) {
      final message = e.response?.data['message'] ?? e.message;
      return Exception(message);
    }
    return Exception(e.message);
  }
}

// In your screen/widget
Future<void> _handleGenerateChart() async {
  setState(() => _isLoading = true);

  try {
    final birthData = widget.birthData ?? {};

    final response = await AstrologyService(_dioClient).generateKundali(
      birthDate: birthData['birthDate'] as DateTime,
      birthTime: birthData['birthTime'] as TimeOfDay,
      timeUnknown: birthData['timeUnknown'] as bool? ?? false,
      city: birthData['city'] as String? ?? '',
      state: birthData['state'] as String? ?? '',
      country: birthData['country'] as String? ?? '',
      latitude: birthData['latitude'] as double?,  // From map picker
      longitude: birthData['longitude'] as double?, // From map picker
    );

    if (mounted) {
      Navigator.of(context).pushNamedAndRemoveUntil(
        AppRoutes.dashboard,
        (Route<dynamic> route) => false,
      );
    }
  } catch (e) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        ErrorSnackBar.show(message: e.toString()),
      );
    }
  } finally {
    if (mounted) {
      setState(() => _isLoading = false);
    }
  }
}
```

---

## Backend API Request Format

### Expected API Endpoint

```
POST /astrology/kundali/generate
Content-Type: application/json
```

### Request Body Example

```json
{
  "birthDate": "2000-05-15",
  "birthTime": "14:30",
  "timeUnknown": false,
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "latitude": 19.0760,
  "longitude": 72.8777
}
```

### Response Example

```json
{
  "id": "kundali_12345",
  "userId": "user_789",
  "status": "success",
  "message": "Kundali generated successfully",
  "data": {
    "ascendant": "Leo",
    "sun": {
      "sign": "Taurus",
      "position": 45.23
    },
    "moon": {
      "sign": "Scorpio",
      "position": 205.67
    },
    // ... other planetary positions
  },
  "generatedAt": "2024-12-01T10:30:00Z"
}
```

---

## Key Changes from Previous Flow

| Aspect | Before | After |
|--------|--------|-------|
| **Location Input** | Manual text entry | Google Maps selection ✅ |
| **Coordinates** | Optional manual entry | Auto-captured from map ✅ |
| **Accuracy** | ~30-50km radius | ±11 meters ✅ |
| **API Data** | city, state, country | city, state, country, **latitude, longitude** ✅ |
| **Timezone Calc** | Approximate | **Precise** ✅ |
| **Ascendant Sign** | Potential error | **Accurate** ✅ |

---

## Testing the Integration

### 1. Local Testing

**Setup:**
```bash
# Start your backend on local machine
# e.g., http://localhost:5000

# In your code, use:
final apiUrl = 'http://localhost:5000/astrology/kundali/generate';
```

**Test with real map selection:**
1. Start app
2. Navigate to location screen
3. Click "Pick from Map"
4. Select a location on Google Maps
5. Coordinates auto-populate
6. Proceed to confirmation
7. Click "Generate My Chart"
8. Check backend receives coordinates

### 2. API Debugging

Add logging to see requests:

```dart
// Add to your Dio client setup
_dio.interceptors.add(
  LoggingInterceptor(),
);

class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    print('➡️ REQUEST[${options.method}] => PATH: ${options.path}');
    print('HEADERS: ${options.headers}');
    print('DATA: ${options.data}');
    super.onRequest(options, handler);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    print('⬅️ RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}');
    print('DATA: ${response.data}');
    super.onResponse(response, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    print('❌ ERROR[${err.response?.statusCode}] => PATH: ${err.requestOptions.path}');
    print('MESSAGE: ${err.message}');
    super.onError(err, handler);
  }
}
```

### 3. Verify Backend Receives Coordinates

**Backend validation:**
```python
# Example: Python Flask
@app.route('/astrology/kundali/generate', methods=['POST'])
def generate_kundali():
    data = request.get_json()

    # Verify coordinates are present
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is None or longitude is None:
        return jsonify({
            'error': 'Coordinates required',
            'message': 'Latitude and longitude must be provided for accurate calculation'
        }), 400

    # Validate coordinate ranges
    if not (-90 <= latitude <= 90):
        return jsonify({'error': 'Invalid latitude'}), 400
    if not (-180 <= longitude <= 180):
        return jsonify({'error': 'Invalid longitude'}), 400

    # Use coordinates for timezone calculation
    timezone = get_timezone(latitude, longitude)

    # Generate kundali with accurate timezone
    kundali = generate_kundali_chart(
        birth_date=data['birthDate'],
        birth_time=data['birthTime'],
        timezone=timezone,
        # ... other params
    )

    return jsonify(kundali), 201
```

---

## Deployment Checklist

- [ ] **Frontend:**
  - [ ] Google Maps API keys configured
  - [ ] LocationPickerWidget works on device
  - [ ] Coordinates captured and stored

- [ ] **Backend:**
  - [ ] Endpoint accepts `latitude` and `longitude` fields
  - [ ] Validates coordinate ranges
  - [ ] Uses coordinates for timezone calculation
  - [ ] Returns accurate planetary positions

- [ ] **Integration:**
  - [ ] API endpoint URL configured in Flutter
  - [ ] Authentication headers included if needed
  - [ ] Error handling covers all cases
  - [ ] Success/failure messages displayed to user

- [ ] **Testing:**
  - [ ] End-to-end onboarding works
  - [ ] Coordinates visible in confirmation
  - [ ] Backend receives coordinates
  - [ ] Kundali accuracy verified
  - [ ] User can view generated chart on dashboard

---

## Troubleshooting

### "Coordinates not in request"
- Check LocationPickerWidget returns LocationData correctly
- Verify latitude/longitude being saved in onboarding screen
- Check birthData passed to confirmation screen includes coordinates

### "API returns 400 Bad Request"
- Backend might be expecting different field names
- Verify JSON format matches backend schema
- Check coordinate values are numbers (not strings)

### "API returns 401 Unauthorized"
- Add authentication token to request headers
- Verify token is valid and not expired

### "Kundali still inaccurate"
- Verify coordinates are being used in timezone calculation
- Check backend is using coordinates and not just city name
- Test with known coordinates (e.g., major city center)

---

## Support

**Questions?**
1. Check `GOOGLE_MAPS_INTEGRATION_SUMMARY.md` for overview
2. Review this guide for implementation details
3. Check backend logs for coordinate values
4. Verify Google Maps widget captures correct coordinates

---

*Updated: December 2024*
*Status: Ready for Integration*
