import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // ==========================================
  // ⚙️ GITHUB REPOSITORY CONFIGURATION
  // ==========================================
  // For Local Testing (Emulator): Use 'http://10.0.2.2:8000'
  // For Local Testing (Physical Device): Replace with your Wi-Fi IPv4 address (e.g., 'http://192.168.1.5:8000')
  // For Production Cloud (Render/AWS): Replace with your live HTTPS domain
  static const String baseUrl = 'http://127.0.0.1:8000'; // Default Placeholder

  static Future<List<dynamic>> fetchDiseases({String lang = 'en'}) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/diseases?lang=$lang'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['diseases'];
      } else {
        throw Exception('Failed to load diseases: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: Ensure the backend is running at $baseUrl');
    }
  }

  static Future<Map<String, dynamic>> predictRisk(String endpoint, Map<String, dynamic> patientData) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(patientData),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Server error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}
