// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Spanish Castilian (`es`).
class AppLocalizationsEs extends AppLocalizations {
  AppLocalizationsEs([String locale = 'es']) : super(locale);

  @override
  String get appTitle => 'VitaGuard AI';

  @override
  String get selectDiagnostics => 'Seleccionar Diagnósticos';

  @override
  String get chooseModel =>
      'Elija un modelo clínico para generar una evaluación de riesgo de IA explicable.';

  @override
  String get retryConnection => 'Reintentar Conexión';

  @override
  String get history => 'Historial de Evaluaciones';

  @override
  String get clearHistory => 'Borrar Todo';

  @override
  String get noHistory =>
      'No hay historial disponible.\\n¡Complete una evaluación primero!';

  @override
  String get aiConfidence => 'Confianza de la IA';

  @override
  String get savePdf => 'Guardar como PDF';

  @override
  String get startNew => 'Iniciar Nueva Evaluación';

  @override
  String get visualImpact => 'Análisis de Impacto Visual';
}
