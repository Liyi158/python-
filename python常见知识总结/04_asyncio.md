[TOC]

# 介绍

​	`asyncio` 是Python的一个库，用于编写单线程的并发代码，主要用于异步I/O操作。它利用协程（coroutine）提供了一种高效的编程方式，特别适合处理大量网络连接和I/O密集型任务。

# 关键概念

1. **协程（Coroutine）**：通过`async def`定义的函数。协程可以被“暂停”和“恢复”，适用于异步操作。
2. **任务（Task）**：用于调度协程的执行。任务是对协程的进一步封装。
3. **事件循环（Event Loop）**：程序的核心，负责管理和调度任务。
4. **`await`关键字**：用于挂起协程的执行，直到等待的异步操作完成。

# `async def`

 	当你定义了一个使用 `async def` 的函数，比如 `async def func():`，这个函数实际上是一个协程函数（coroutine function），而不是一个普通的同步函数。当你调用 `func()` 时，它不会像普通函数那样直接运行，而是返回一个协程对象。为了执行这个协程对象，你需要在一个异步环境中“等待（await）”它，或者将其封装在一个任务（task）中。

**不能直接调用**

直接调用 `func()` 不会像你可能期望的那样执行函数体中的代码。它只会返回一个协程对象，这个对象需要被安排进事件循环中才会执行。

```python
# 错误的调用方式
async def func():
    print("Hello from coroutine")
func()  # 这不会打印任何东西
```

**正确的调用方式**

要运行协程函数 `func()` 的代码，你需要使用 `await` 关键字（在另一个协程函数中）或者通过 `asyncio.run()`（在最顶层代码中）运行它。

1. **在协程中使用 `await`**：
   如果你已经在一个协程函数内部，可以使用 `await` 来调用另一个协程函数。

   ```python
   async def func():
       print("Hello from coroutine")
   
   async def main():
       await func()  # 这会执行 func() 中的代码
   
   asyncio.run(main())
   ```

2. **在顶层代码中使用 `asyncio.run()`**：
   如果你在顶层代码中（不在任何协程函数内），可以使用 `asyncio.run()` 来运行协程函数。

   ```python
   async def func():
       print("Hello from coroutine")
   
   asyncio.run(func())  # 这会执行 func() 中的代码
   ```

3. **另一个选项是使用 `asyncio.create_task()` 来创建一个任务。这在你想要并发运行多个协程时特别有用。**

```python
async def func():
    print("Hello from coroutine")

async def main():
    task = asyncio.create_task(func())  # 创建任务，协程开始执行
    await task  # 等待任务完成

asyncio.run(main())
```

**结论**

总的来说，使用 `async def` 定义的协程函数不能像普通函数那样直接调用。为了执行协程，你需要将其安排在异步环境中，使用 `await`、`asyncio.run()` 或者将其封装在一个任务中。这是异步编程模型的一个基本特性，它与传统的同步编程模型有着根本的不同。

# 协程函数的暂停与恢复

	在Python中，通过使用`async def`定义的协程函数可以利用`await`关键字被暂停和恢复。这是异步编程的一个核心特性，允许程序在等待异步操作完成时释放控制权，以便可以执行其他任务。下面通过一个例子来具体说明这一过程：

## 示例说明1

假设我们有两个异步函数，一个模拟了耗时操作（如网络请求或I/O操作），另一个是主协程，它调用这些耗时操作：

```python
import asyncio

async def fetch_data():
    print("开始获取数据...")
    await asyncio.sleep(2)  # 模拟I/O操作，比如网络请求
    print("数据获取完成")
    return {'data': 1}

async def main_function():
    print("主函数开始")
    
    # 暂停主函数并等待 fetch_data 协程完成
    data = await fetch_data()
    print("主函数恢复")
    print(f"获取到的数据: {data}")

# 运行主协程
asyncio.run(main_function())
```

### 暂停和恢复的过程

1. **暂停**：当执行到`await fetch_data()`时，`main_function` 协程暂停执行。控制权被交回给事件循环，允许它运行其他任务。

2. **fetch_data 执行**：事件循环开始执行 `fetch_data` 协程。当遇到 `await asyncio.sleep(2)` 时，`fetch_data` 也暂停，并且控制权再次返回到事件循环。在这个等待期间，事件循环可以运行其他协程或任务。

3. **恢复**：2秒后，`asyncio.sleep` 完成，`fetch_data` 协程恢复执行，直到完成并返回数据。此时，控制权再次回到了 `main_function`。

4. **主函数恢复**：`main_function` 从 `await fetch_data()` 恢复执行。现在它有了从 `fetch_data` 返回的数据，并继续执行直到完成。

## 示例说明2

​	在这个例子中，我们将创建一个模拟的场景，其中包含两个异步任务：一个是下载数据，另一个是处理数据。我们将看到这些任务是如何被暂停和恢复的，以及它们是如何与事件循环交互的。

```python
import asyncio
import random

async def download_data(data_id):
    download_time = random.randint(1, 3)  # 随机下载时间
    print(f"开始下载数据 {data_id}，预计耗时 {download_time} 秒")
    await asyncio.sleep(download_time)  # 模拟异步下载过程
    print(f"数据 {data_id} 下载完成")
    return f"数据{data_id}"

async def process_data(data_id, data):
    process_time = random.randint(1, 3)  # 随机处理时间
    print(f"开始处理数据 {data_id}，预计耗时 {process_time} 秒")
    await asyncio.sleep(process_time)  # 模拟异步处理过程
    print(f"数据 {data_id} 处理完成")

async def main():
    print("主任务开始")

    # 下载数据 1 和 2
    data1 = await download_data(1)
    data2 = await download_data(2)

    # 同时处理数据 1 和 2
    task1 = asyncio.create_task(process_data(1, data1))
    task2 = asyncio.create_task(process_data(2, data2))

    # 等待处理任务完成
    await task1
    await task2

    print("主任务结束")

asyncio.run(main())
```

​	假设我们有一个异步函数 `download_data` 用于模拟数据下载，另一个异步函数 `process_data` 用于模拟数据处理。我们将在 `main` 协程中调用这些函数，并观察执行流程。

### 暂停和恢复的过程

1. **下载数据**：当`main`协程到达`await download_data(1)`时，它暂停并等待下载完成。这期间，控制权返回给事件循环，可以执行其他任务（比如其他协程）。
2. **数据下载完成**：一旦`download_data(1)`完成，`main`协程恢复执行，然后再次暂停，等待`download_data(2)`的完成。
3. **处理数据**：当两个数据下载任务都完成后，`main`协程继续执行，创建两个处理数据的任务，并立即开始它们。由于`process_data`也是异步的，`main`协程会在`await task1`处暂停，等待这两个处理任务完成。
4. **并行处理**：`process_data(1, data1)`和`process_data(2, data2)`会并行执行。由于它们各自含有`await asyncio.sleep(process_time)`，这两个任务会在执行时交替暂停和恢复。
5. **主任务结束**：一旦所有处理任务完成，`main`协程会恢复并执行到结束。

### 代码细节讲解

```python
当你在一个协程中使用 `await` 关键字，比如 `await download_data(1)`，执行流程确实会转到 `download_data` 函数中。但是，这个过程不仅仅是一个简单的函数调用。在异步编程中，`await` 关键字有一些特殊的含义和行为：
```

1. **暂停执行**：`await download_data(1)` 暂停当前协程（在这个示例中是 `main` 协程）。这意味着控制权被交回到事件循环（event loop）。

2. **执行协程函数**：事件循环接着开始执行 `download_data(1)` 协程。如果 `download_data` 协程内部也有 `await` 语句，它也会相应地暂停，并将控制权交回给事件循环。

3. **等待协程完成**：当前协程（`main`）会等待 `download_data(1)` 协程完成。在这个等待期间，事件循环可以运行其他协程或任务。

4. **恢复执行**：一旦 `download_data(1)` 完成，`main` 协程将从暂停的地方恢复执行。此时，它会获得 `download_data(1)` 的返回值，并继续执行后续代码。

在示例中：

- 当 `main` 函数中的 `await download_data(1)` 被执行时，`main` 协程暂停，开始执行 `download_data(1)`。
- 如果 `download_data` 函数中存在 `await`（比如 `await asyncio.sleep(x)`），它会在等待期间暂停，这时事件循环可以执行其他协程或任务。
- 一旦 `download_data(1)` 完成其操作（比如模拟的数据下载），它返回到 `main` 协程，继续执行 `await download_data(1)` 之后的代码。

```python
使用 task1 = asyncio.create_task(process_data(1, data1)) 和直接使用 await process_data(1, data1) 之间的主要区别在于任务的执行方式：并行（concurrent）与串行（sequential）。
```

**`asyncio.create_task()`**

当使用 `asyncio.create_task()` 创建任务时，实际上是在告诉事件循环：“开始执行这个协程，但不要等它完成，立即继续执行当前协程的下一行代码”。这允许你并行运行多个协程。

```python
task1 = asyncio.create_task(process_data(1, data1))
task2 = asyncio.create_task(process_data(2, data2))
```

在这个例子中，`process_data(1, data1)` 和 `process_data(2, data2)` 会几乎同时开始执行。事件循环会在这两个任务之间切换，允许它们并行执行。这种方式特别适合于I/O密集型任务，例如同时处理多个网络请求。

**`await`**

另一方面，当你直接在协程中使用 `await process_data(1, data1)` 时，当前协程会暂停并等待 `process_data(1, data1)` 完成才继续执行。这意味着如果你有多个 `await` 调用，它们将会按顺序一个接一个地执行。

```python
await process_data(1, data1)
await process_data(2, data2)
```

在这个例子中，`process_data(2, data2)` 只有在 `process_data(1, data1)` 完全完成后才会开始执行。这是一种串行执行方式。

### 选择哪一种

- 如果你的协程是相互独立的，且你想同时执行它们以提高效率，使用 `asyncio.create_task()` 是一个更好的选择。
- 如果你需要一个协程完全执行完成后才开始另一个协程，或者后一个协程依赖于前一个协程的结果，那么直接使用 `await` 是更合适的。

在很多实际应用中，`asyncio.create_task()` 被广泛用于启动并发任务，因为它允许程序在等待一个操作完成时继续执行其他任务，从而提高了程序的整体效率和响应性。

## 总结

# 任务(task)

### 任务（Task）的详细解释

`asyncio` 任务是对协程的封装，它在事件循环中执行协程。任务允许协程被调度为并发执行，同时提供了管理它们的状态和结果的方法。

#### 创建任务

任务是通过调用 `asyncio.create_task(coroutine)` 创建的，其中 `coroutine` 是一个协程对象。这个函数返回一个 `Task` 对象，代表在事件循环中执行的协程。

#### 等待任务完成

任务可以被 `await` 关键字等待。使用 `await task` 会暂停当前协程，直到 `task` 完成。

#### 获取任务结果

一旦任务完成，你可以使用 `task.result()` 方法获取协程的返回值。

#### 示例 1：基本任务创建和等待

```python
import asyncio

async def my_coroutine():
    print("协程执行")
    await asyncio.sleep(1)
    return "结果"

async def main():
    # 创建任务
    task = asyncio.create_task(my_coroutine())

    # 等待任务完成
    result = await task
    print("任务结果:", result)

asyncio.run(main())
```

在这个示例中，`main` 函数创建了一个任务来执行 `my_coroutine` 协程，并等待该任务完成，然后打印结果。

#### 示例 2：并发执行多个任务

任务非常适合于并发执行多个协程：

```python
import asyncio

async def my_coroutine(id):
    print(f"协程 {id} 开始")
    await asyncio.sleep(2)  # 假设的异步操作
    print(f"协程 {id} 结束")
    return f"结果{id}"

async def main():
    # 创建并同时启动多个任务
    tasks = [asyncio.create_task(my_coroutine(i)) for i in range(3)]

    # 并发等待所有任务完成
    results = await asyncio.gather(*tasks)
    print("所有任务的结果:", results)

asyncio.run(main())
```

这里，`main` 函数创建了三个 `my_coroutine` 的任务，并使用 `asyncio.gather()` 来并发等待这些任务完成。

#### 示例 3：任务的取消

任务也可以被取消，这在需要终止长时间运行的协程时很有用：

```python
import asyncio

async def my_coroutine():
    try:
        await asyncio.sleep(10)  # 长时间运行的协程
    except asyncio.CancelledError:
        print("协程被取消")
    else:
        return "完成"

async def main():
    task = asyncio.create_task(my_coroutine())

    # 1秒后取消任务
    await asyncio.sleep(1)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("主函数中：任务被取消")

asyncio.run(main())
```

在这个示例中，`main` 函数创建了一个任务，然后在等待了1秒后取消它。被取消的任务会引发 `asyncio.CancelledError` 异常。

### 总结

`asyncio` 的任务提供了一种强大的方式来并发执行和管理协程。它们使得异步代码更容易编写和维护，同时提供了并发执行、任务取消、获取结果等功能。通过这些示例，你可以看到任务是如何在实践中使用的，以及它们如何使异步编程变得更加高效和灵活。


