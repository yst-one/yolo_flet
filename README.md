# yolo-flet
YoloFlet control for Flet

## Installation

Add dependency to `pyproject.toml` of your Flet app:

* **Git dependency**

Link to git repository:

```
dependencies = [
  "yolo-flet @ git+https://github.com/yst-one/yolo_flet",
  "flet>=0.85.3",
]
```

* **uv/pip dependency**

If the package is published on pypi.org:

```
dependencies = [
  "yolo-flet",
  "flet>=0.85.3",
]
```

Build your app:
```
flet build macos -v
```

## Documentation
```python
async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    yolo_flet = YoloService(src=str(fp))
    page.services.append(yolo_flet)


    async def detect() :
        log.debug("/。。。。。。。。。。开始识别中。。。。。。。。。。")


        with open(default_assets_dir / "test.jpg", "rb") as f:

            image_bytes = f.read()
            for i in range(100):
                start = time.time()
                a:list[types.DetectionResult] =await yolo_flet.detect_frame(image_bytes)
                end = time.time()
                log.debug("耗时" + str((end - start) * 1000))
                await update_text(f"这是第{i}次推理--" + "耗时:" + str((end - start) * 1000))
                await asyncio.sleep(0.001)


                # for i in a:
                #     log.debug(i)

    async def update_text(i: str):
        text.value =i
        text.update()

    bt =ft.Button(content="start detect" , on_click=detect)
    text =ft.Text(value="aaa")
    page.add(
        bt,text
    )


ft.run(main, assets_dir="assets")
```

[Link to documentation](https://github.com/yst-one/yolo_flet)
