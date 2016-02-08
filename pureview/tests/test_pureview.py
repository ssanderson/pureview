from ..pureview import View


def test_pureview():

    class MyView(View):
        __slots__ = ('a', 'b', 'c')

        def foo(a, b, c):
            return a + b + c

        def bar(foo, a):
            return foo + a

        def buzz(foo, bar):
            return foo + bar

    view = MyView(1, 2, 3)
    assert view.a == 1
    assert view.b == 2
    assert view.c == 3

    assert view.foo == view.a + view.b + view.c
    assert view.bar == view.foo + view.a
    assert view.buzz == view.foo + view.bar
