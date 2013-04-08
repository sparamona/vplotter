
class C:
    a = "my text"
    def f(self):
        print self.a
        return

c = C()
c.f()
c.a = "something else"
c.f()
d = C()
d.f()
C.f(c)
C.f(d)
