import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class HistoryService {
  static const String _key = 'patient_history';

  static Future<void> saveResult(String diseaseName, Map<String, dynamic> resultData) async {
    final prefs = await SharedPreferences.getInstance();
    List<String> historyList = prefs.getStringList(_key) ?? [];

    final entry = {
      'disease': diseaseName,
      'timestamp': DateTime.now().toIso8601String(),
      'risk_level': resultData['risk_level'],
      'confidence': resultData['confidence_percentage'],
      'top_factors': resultData['top_factors'],
    };

    historyList.insert(0, jsonEncode(entry));
    await prefs.setStringList(_key, historyList);
  }

  static Future<List<Map<String, dynamic>>> getHistory() async {
    final prefs = await SharedPreferences.getInstance();
    List<String> historyList = prefs.getStringList(_key) ?? [];
    
    return historyList.map((e) => jsonDecode(e) as Map<String, dynamic>).toList();
  }

  static Future<void> clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_key);
  }
}
