Python 3 中的异步
=========================

coroutine, Future, Task
------------------------------
Pyhton 3 的 `asyncio` 模块引入了 `coroutine` `Future` `Task` 三个新概念，要使用 `asyncio` 模块进行异步程序开发，就必须要先了解这三个概念。

    * `coroutine` 译为协程，是 `asyncio` 事件循环的最小调度单位，类比于操作系统中的进程与线程，是 `asyncio` 事件循环中的最小调度单位。
    * `Future` 暂时没有明确的翻译，类比于js中的 `promise` ，用于等待一个未来发生的事件，常见于 io 操作，用于封装回调函数中的异步执行部分。
    * `Task` 是 `Future` 的子类，用于调度 `coroutine` 的执行。

`Future` 是异步操作中的核心概念，封装了一个 `coroutine` 中的异步操作，常见于 io 等待。 `coroutine` 是一个静态概念，处在未执行状态，执行状态的 `coroutine` 就是 `Task` 。

在一个事件循环中同时只调度一个 `Task` 在执行，与操作系统中的时间片调度不同， 只有一个 `Task` 需要等待 `Future` 发生时才能调度其他的 `Task` 执行。

因此 `coroutine` 中理应至少有一个需要等待的 `Future` 操作，否则无法实现异步操作，也就没有了意义。不过这并非强制性的，我们完全可以定义一个与一般函数一样的 `coroutine` 。

coroutine的创建
-------------------
`@asyncio.coroutine` 或者使用新的关键字 `async def`

coroutine 的执行
-------------------
像调用其他函数一样调用一个 `coroutine` 并不会执行，只会返回一个 `coroutine` 对象。调度这个 `coroutine` 对象的方法包括：

    * 在其他协程中调用: await coroutine / yield from coroutine -- await 应该优先使用。
    * 使用 `ensure_future()` 或 `AbstractEventLoop.create_task()` 方法来调度协程执行

Future 的创建
------------------
不推荐使用 `future = asyncio.Future()` ，优先使用 `AbstractEventLoop.create_future()` ，事件循环的不同实现可能会实现不同的 `Future` 类。

concurrent.futures.Future
-----------------------------
`concurrent.futures.Future` 由 `Executor.submit()` 创建。

可以使用 `asyncio.wrap_future(Future)` 将 `concurrent.futures.Future` 包装为 `asyncio.future` 。

异常捕获
------------
应该在 `coroutine` 执行的地方捕获异常，在从 `Future` 获取结果的时候获得异常的详细信息， `Future.exception()` 可以获得设置给 `Future` 的异常。

