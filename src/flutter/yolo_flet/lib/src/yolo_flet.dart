import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:ultralytics_yolo/ultralytics_yolo.dart';

class YoloService extends FletService {
  YoloService({required super.control});

  DataChannel? _frames;
  StreamSubscription<Uint8List>? _framesSub;
  Future<YOLO>? _model;

  @override
  void init() {
    super.init(); // keep init() synchronous: Flet doesn't await it
    control.addInvokeMethodListener(_invokeMethod);

    // No BuildContext needed: control.backend is the same FletBackend
    // that FletBackend.of(context) returns.
    final frames = _frames = control.backend.openDataChannel();
    _framesSub = frames.messages.listen(_onFrame);
    control.triggerEvent("data_channel_open", {
      "channel_name": "frames",
      "channel_id": frames.id,
    });

    _model = _loadModel()..ignore(); // load errors surface in _detect()
  }

  @override
  void dispose() {
    control.removeInvokeMethodListener(_invokeMethod);
    _framesSub?.cancel();
    _frames?.close();
    unawaited(_model?.then((yolo) => yolo.dispose(), onError: (Object _) {}));
    super.dispose();
  }

  Future<YOLO> _loadModel() async {
    final src = control.getString("src");
    if (src == null) throw ArgumentError("src is not set");
    final yolo = YOLO(
      // absolute path of a file in the Flet app's assets dir
      modelPath: control.backend.getAssetSource(src).path,
      task: YOLOTask.detect,
    );
    if (!await yolo.loadModel()) throw StateError("Failed to load '$src'");
    return yolo;
  }

  Future<List<dynamic>> _detect(Uint8List image) async {
    int startTime = DateTime.now().millisecondsSinceEpoch;
    final yolo = await _model!; // waits while the model is still loading
    final result = await yolo.predict(image);
    int endTime = DateTime.now().millisecondsSinceEpoch;
    debugPrint("dart------推理耗时: ${endTime - startTime} 毫秒");
    return result["boxes"] as List? ?? const [];
  }

  // One-off images: `await yolo.detect_objects(jpeg)` in Python.
  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "detectObjects":
        return _detect(args["image_bytes"] as Uint8List);
      default:
        throw Exception("Method $name is not implemented");
    }
  }

  // Camera frames over the DataChannel.
  // Python -> Dart: [request id: 4 bytes][JPEG/PNG]; Dart -> Python: [same id][JSON]
  Future<void> _onFrame(Uint8List packet) async {
    if (packet.length < 4) return;
    final frame =
        Uint8List.fromList(packet); // own it: the buffer may be reused
    Object reply;
    try {
      reply = {"boxes": await _detect(Uint8List.sublistView(frame, 4))};
    } catch (e) {
      reply = {"error": "$e"};
    }
    _frames?.send(Uint8List.fromList(
        [...frame.take(4), ...utf8.encode(jsonEncode(reply))]));
  }
}

class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "YoloService": // must match @ft.control("YoloService") in Python
        return YoloService(control: control);
      default:
        return null;
    }
  }
}
