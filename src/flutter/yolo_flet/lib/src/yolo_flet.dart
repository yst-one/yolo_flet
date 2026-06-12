import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:ultralytics_yolo/ultralytics_yolo.dart';

class YoloFletControl extends FletService {
  YOLO? yolo;
  YoloFletControl({
    required super.control,
  });

  @override
  void init() async {
    super.init();
    control.addInvokeMethodListener(_invokeMethod);

    final assetsSrc = control.backend.getAssetSource(control.getString("src")!);
    debugPrint("assetsSrc: $assetsSrc");
    yolo = YOLO(modelPath: assetsSrc.path);
    print('Loading model...');
    try {
      await yolo?.loadModel();
    } catch (e) {
      throw Exception("Error loading model: $e");
    }

    print('Model loaded successfully');
  }

  Future<Map<String, dynamic>> _detectObjects(Uint8List imageBytesList) async {
    final results = await yolo?.predict(imageBytesList);
    return results ?? {};
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
//     debugPrint("YoloFletControl.$name($args)");
    switch (name) {
      case "detectObjects":
//         debugPrint("YoloFletControl.$name($args)");
        final imageBytesList = args["image_bytes"];
//         debugPrint(
//             "imageBytesList: $imageBytesList, runtimeType: ${imageBytesList.runtimeType.toString()}");
        int startTime = DateTime.now().millisecondsSinceEpoch;
        final results = await _detectObjects(imageBytesList);
        final List<Map<String, dynamic>> results_list =
            results["boxes"]?.toList() ?? [];
        int endTime = DateTime.now().millisecondsSinceEpoch;
        debugPrint("推理耗时: ${endTime - startTime} 毫秒");
        return results_list;
      default:
        throw Exception("Method $name is not implemented");
    }
  }

  @override
  void dispose() {
    debugPrint("YoloFletControl(${control.id}).dispose()");
    yolo?.dispose();
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
