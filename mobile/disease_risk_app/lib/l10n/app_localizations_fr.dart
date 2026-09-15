// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for French (`fr`).
class AppLocalizationsFr extends AppLocalizations {
  AppLocalizationsFr([String locale = 'fr']) : super(locale);

  @override
  String get appTitle => 'VitaGuard AI';

  @override
  String get selectDiagnostics => 'Sélectionner les Diagnostics';

  @override
  String get chooseModel =>
      'Choisissez un modèle clinique pour générer une évaluation des risques par IA explicable.';

  @override
  String get retryConnection => 'Réessayer la Connexion';

  @override
  String get history => 'Historique des Évaluations';

  @override
  String get clearHistory => 'Tout Effacer';

  @override
  String get noHistory =>
      'Aucun historique disponible.\\nComplétez d\'abord une évaluation !';

  @override
  String get aiConfidence => 'Confiance de l\'IA';

  @override
  String get savePdf => 'Enregistrer en PDF';

  @override
  String get startNew => 'Commencer une Nouvelle Évaluation';

  @override
  String get visualImpact => 'Analyse d\'Impact Visuel';
}
