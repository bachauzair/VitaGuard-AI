// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'VitaGuard AI';

  @override
  String get selectDiagnostics => 'Select Diagnostics';

  @override
  String get chooseModel =>
      'Choose a clinical model to generate an explainable AI risk assessment.';

  @override
  String get retryConnection => 'Retry Connection';

  @override
  String get history => 'Assessment History';

  @override
  String get clearHistory => 'Clear All';

  @override
  String get noHistory =>
      'No history available.\\nComplete an assessment first!';

  @override
  String get aiConfidence => 'AI Confidence';

  @override
  String get savePdf => 'Save as PDF';

  @override
  String get startNew => 'Start New Assessment';

  @override
  String get visualImpact => 'Visual Impact Analysis';
}
