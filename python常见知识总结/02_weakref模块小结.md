[toc]

# 概念详解

​	在Python中，`weakref`模块提供了对对象的弱引用支持。弱引用与常规引用（强引用）不同，不会阻止其所指向的对象被垃圾回收器回收。这意味着，当一个对象只剩下弱引用时，它可以被自动销毁和回收内存。

# 主要用途

## 缓存应用

​	弱引用常用于缓存场景，其中对象可以在不再被需要时自动释放，从而避免内存泄漏。

```python
import weakref


class ExpensiveObject:
    def __init__(self, value):
        self.value = value
        print(f"Creating {self}")

    def __repr__(self):
        return f"ExpensiveObject({self.value})"

    def compute(self):
        return self.value ** 2


cache = weakref.WeakValueDictionary()


def get_cached_object(value):
    if value in cache:
        print(f"Cache hit for {value}")
        return cache[value]
    else:
        print(f"Cache miss for {value}, creating new object")
        obj = ExpensiveObject(value)
        cache[value] = obj
        return obj


def is_cached(value):
    """检查一个值的对象是否仍在缓存中"""
    return value in cache


# 使用示例
obj1 = get_cached_object(10)
print(obj1.compute())

obj2 = get_cached_object(10)
print(obj2.compute())

obj3 = get_cached_object(5)
print(obj3.compute())

# 检查缓存状态
print("Is 10 still cached?", is_cached(10))  # 应该是 True
print("Is 5 still cached?", is_cached(5))  # 应该是 True

# 删除对对象的引用，这可能导致它们被垃圾回收
del obj1
del obj2
del obj3

# 检查缓存状态
print("Is 10 still cached?", is_cached(10))  # 可能是 False，取决于垃圾回收器
print("Is 5 still cached?", is_cached(5))  # 可能是 False，取决于垃圾回收器

"""输出结果如下:"""
Cache miss for 10, creating new object
Creating ExpensiveObject(10)
100
Cache hit for 10
100
Cache miss for 5, creating new object
Creating ExpensiveObject(5)
25
Is 10 still cached? True
Is 5 still cached? True
Is 10 still cached? False
Is 5 still cached? False

Process finished with exit code 0
```

​	在这个例子中，`ExpensiveObject` 类代表一个计算密集型的对象，我们用它来模拟需要缓存的对象。`get_cached_object` 函数检查缓存中是否存在给定值的对象。如果不存在，它将创建一个新对象并将其存储在缓存中。由于我们使用的是 `WeakValueDictionary`，因此当没有其他对这些对象的强引用时，它们会自动被垃圾回收器回收。

​	`is_cached` 函数，它检查特定值的对象是否仍然在缓存中。请注意，由于Python的垃圾回收器可能不会立即回收对象，即使在删除所有强引用后，对象也可能仍然存在于缓存中，直到垃圾回收器运行。因此，这种检查可能不总是立即反映对象的状态。实际上，垃圾回收的时间取决于许多因素，包括对象的大小、当前内存使用情况和Python解释器的具体实现。

## 循环引用

### 查看对象的引用次数

​	在Python中，你可以使用标准库中的 `sys` 模块的 `getrefcount` 函数来查看一个对象的引用次数。这个函数返回传递给它的对象的引用计数。需要注意的是，`getrefcount` 本身也会创建一个临时引用，所以返回的计数会比实际的引用次数多一。

​	

```python
import sys

class MyClass:
    pass

obj = MyClass()
print("Initial reference count:", sys.getrefcount(obj))

another_reference = obj
print("Reference count after adding another reference:", sys.getrefcount(obj))

del another_reference
print("Reference count after deleting the additional reference:", sys.getrefcount(obj))


"""输出结果如下:"""

Initial reference count: 2
Reference count after adding another reference: 3
Reference count after deleting the additional reference: 2
```

### `weakraf.ref`()小讲

​	`weakref.ref` 是 Python `weakref` 模块中的一个函数，用于创建一个对象的弱引用。这种引用允许对象被引用而不增加它的引用计数。这是非常有用的，因为它可以防止对象因为被引用而不能被垃圾回收器（GC）回收，从而避免内存泄漏。

```python
import weakref
import sys


class MyClass:
    pass


obj = MyClass()
obj_c = MyClass()
print(f"id for obj is:{id(obj)}")
print(f"id for obj_c is:{id(obj_c)}")
r = weakref.ref(obj)
s = obj_c
print(sys.getrefcount(obj))
print(sys.getrefcount(obj_c))
temp = r
temp_c = s
print(sys.getrefcount(obj))
print(sys.getrefcount(obj_c))
print(r())  # 访问弱引用所引用的对象，输出：<__main__.MyClass object at 0x...>

del obj
print(r())  # 此时 obj 已被删除，弱引用返回 None，输出：None

"""输出结果如下:"""

id for obj is:2079585189256
id for obj_c is:2079585189320
2
3
2
4
<__main__.MyClass object at 0x000001E430EFBD88>
None
```

### 循环引用示例讲解

​	弱引用可以帮助打破循环引用，从而避免内存泄漏。

```python
import weakref

class TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = weakref.ref(parent) if parent else None
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = weakref.ref(self)

    def __repr__(self):
        return f"TreeNode({self.name})"

# 创建树节点示例
root = TreeNode("root")
child1 = TreeNode("child1", root)
child2 = TreeNode("child2", root)
root.add_child(child1)
root.add_child(child2)

# 创建更多的节点和循环引用
subchild = TreeNode("subchild", child1)
child1.add_child(subchild)

# 打印树结构
def print_tree(node, level=0):
    print(" " * level * 2 + repr(node))
    for child in node.children:
        print_tree(child, level + 1)

print_tree(root)

# 检查父节点是否存在
print("Parent of child1:", child1.parent())
print("Parent of subchild:", subchild.parent())
```

​	在这个示例中，每个 `TreeNode` 对象可以有多个子节点和一个父节点。父节点通过弱引用 (`weakref.ref`) 存储，这样即使子节点存在，也不会阻止父节点被垃圾回收。`add_child` 方法用于将子节点添加到父节点的子节点列表中，并设置子节点的父节点。

该代码还包括一个 `print_tree` 函数，用于打印树的结构，以及一些代码来创建树节点并将它们相互连接。

在这种设计下，当树的某个分支不再被使用时，即使它们彼此间存在引用，分支上的节点也可以被垃圾回收器回收。这是因为父节点的引用是弱引用，不足以单独保持对象存活。

## 观察者模式

### `weakref.Weakset`小讲

​	`weakref.WeakSet` 是 Python `weakref` 模块中的一个类，用于创建一个存储弱引用的集合。在 `WeakSet` 中，元素的引用是弱引用，这意味着：

​	`weakref.WeakSet` 是 Python `weakref` 模块中的一个类，用于创建一个存储弱引用的集合。在 `WeakSet` 中，元素的引用是弱引用，这意味着：

1. **自动垃圾回收**：如果一个对象仅被 `WeakSet` 引用（即没有其他强引用指向该对象），该对象可以被垃圾回收（GC）。这与普通的 `set` 不同，普通 `set` 会通过其元素的强引用阻止元素被垃圾回收。
2. **用途**：`WeakSet` 常用于需要跟踪一组对象，但不想因为跟踪它们而阻止它们被自动回收的场合。这在管理缓存、实现观察者模式等场景中非常有用。

​	**示例:**

​	假设你有一个应用，需要跟踪一组活动的监听器或回调，但不希望这些监听器因为被跟踪就永远不被回收。

```python
import weakref

class EventListener:
    def __init__(self, name):
        self.name = name

    def on_event(self, message):
        print(f"{self.name} received event with message: {message}")

listeners = weakref.WeakSet()

listener1 = EventListener("Listener 1")
listener2 = EventListener("Listener 2")

listeners.add(listener1)
listeners.add(listener2)

# 假设发生了一个事件
for listener in listeners:
    listener.on_event("Hello World!")

# 删除一个监听器的引用
del listener1

# 再次假设发生了一个事件
# 如果 listener1 被正确垃圾回收，它将不会接收到这个事件
for listener in listeners:
    listener.on_event("Another event!")

```

​	在这个示例中，当 `listener1` 的引用被删除后，由于 `WeakSet` 中存储的是弱引用，`listener1` 可能被垃圾回收（取决于Python垃圾回收器的具体实现和运行时机）。这意味着在第二次事件发生时，`listener1` 可能不再存在于 `listeners` 集合中，因此不会接收到事件通知。这就展示了 `WeakSet` 如何在不影响对象生命周期的前提下跟踪对象。

### 观察者模式示例讲解

​	在观察者模式中，有一个被观察的对象（通常称为“主题”）和多个观察者。当主题的状态发生变化时，所有的观察者都会得到通知。



```python
import weakref

class Observable:
    def __init__(self):
        self._observers = weakref.WeakSet()

    def register_observer(self, observer):
        self._observers.add(observer)

    def unregister_observer(self, observer):
        self._observers.discard(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.notify(message)

class Observer:
    def __init__(self, name):
        self.name = name

    def notify(self, message):
        print(f"{self.name} received message: {message}")

# 创建被观察对象和观察者
observable = Observable()
observer1 = Observer("Observer 1")
observer2 = Observer("Observer 2")

# 注册观察者
observable.register_observer(observer1)
observable.register_observer(observer2)

# 发送通知
observable.notify_observers("Hello Observers!")

# 注销一个观察者并再次发送通知
observable.unregister_observer(observer1)
observable.notify_observers("Second message")

```

​	在这个例子中，`Observable` 类代表了被观察的对象，它有方法来注册和注销观察者，以及通知所有注册的观察者。观察者是 `Observer` 类的实例，它们有一个 `notify` 方法，当被通知时会被调用。

使用 `weakref.WeakSet` 来存储观察者的好处是，当没有其他强引用指向观察者时，它们会自动从观察者集合中移除，从而避免了因观察者长时间存活而导致的内存问题。
