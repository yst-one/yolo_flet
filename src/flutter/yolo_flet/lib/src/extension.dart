import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'yolo_flet.dart';

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "YoloFlet":
        return YoloFletControl(control: control);
      default:
        return null;
    }
  }
}
