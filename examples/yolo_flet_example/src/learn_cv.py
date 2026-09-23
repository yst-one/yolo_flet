import asyncio
import time


async def load_model():
    print(f"[{time.strftime('%H:%M:%S')}] 1. 模型开始加载...")
    await asyncio.sleep(2)  # 模拟耗时 2 秒
    print(f"[{time.strftime('%H:%M:%S')}] 2. 模型加载完成！")
    return "YOLO_MODEL"


async def main():
    print(f"[{time.strftime('%H:%M:%S')}] --- 程序启动 ---")

    # 【关键点】：这里没有 await！但 create_task 会立即把任务放入后台
    task = asyncio.create_task(load_model())

    print(f"[{time.strftime('%H:%M:%S')}] --- 做别的事情 3 秒钟 ---")
    await asyncio.sleep(3)  # 主程序去忙别的了

    print(f"[{time.strftime('%H:%M:%S')}] --- 准备使用模型，开始 await ---")
    # 此时模型其实在 1 秒前就已经加载好了！
    model = await task
    print(f"[{time.strftime('%H:%M:%S')}] 拿到模型: {model}")


asyncio.run(main())