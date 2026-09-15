// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Urdu (`ur`).
class AppLocalizationsUr extends AppLocalizations {
  AppLocalizationsUr([String locale = 'ur']) : super(locale);

  @override
  String get appTitle => 'VitaGuard AI';

  @override
  String get selectDiagnostics => 'تشخیص منتخب کریں';

  @override
  String get chooseModel =>
      'قابل وضاحت اے آئی خطرے کی تشخیص پیدا کرنے کے لیے ایک کلینیکل ماڈل کا انتخاب کریں۔';

  @override
  String get retryConnection => 'کنکشن دوبارہ آزمائیں';

  @override
  String get history => 'تشخیص کی تاریخ';

  @override
  String get clearHistory => 'سب صاف کریں';

  @override
  String get noHistory => 'کوئی تاریخ دستیاب نہیں۔\\nپہلے ایک تشخیص مکمل کریں!';

  @override
  String get aiConfidence => 'اے آئی کا اعتماد';

  @override
  String get savePdf => 'پی ڈی ایف کے طور پر محفوظ کریں';

  @override
  String get startNew => 'نئی تشخیص شروع کریں';

  @override
  String get visualImpact => 'بصری اثرات کا تجزیہ';
}
