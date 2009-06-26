from pyjamas.ui.RootPanel import RootPanel
from pyjamas.Canvas2D import Canvas
from pyjamas.ui.Label import Label

# Pyjamas has no zip()!
def zip(*lists):
    # Pyjamas seems to fail on list comprehensions.  Sigh :(
    res = []
    for i in range(len(lists[0])):
        t = []
        for l in lists:
            t.append(l[i])
        res.append(tuple(t))
    return res

# Pyjamas doesn't support + operator overloading!
# + on anything other than numbers returns concatenation of their
# string representations, e.g.: [1]+[2,3]=="[1][2,3]".
def add_tuples(*tuples):
    res = []
    for t in tuples:
        res.extend(t)
    return tuple(res)

class Cuboid(object):
    """
    N-dimentional cuboid.
    """
    def __init__(self, sizes, fixed_axes=()):
        if len(sizes) == 0:
            self.points = [fixed_axes]
            self.lines = []
        else:
            # Recursive construction: 2 facets + lines between them.
            facet0 = Cuboid(sizes[1:], add_tuples(fixed_axes, (-sizes[0],)))
            facet1 = Cuboid(sizes[1:], add_tuples(fixed_axes, (+sizes[0],)))

            self.points = add_tuples(facet0.points, facet1.points)
            self.lines = add_tuples(facet0.lines,
                                    facet1.lines,
                                    zip(facet0.points, facet1.points))


class LinesCanvas(Canvas):

    def __init__(self, w, h):
        Canvas.__init__(self, w, h)

        # center coordinates on (0,0); scaling will be done on-demand
        self.context.translate(w/2, h/2)
        self.w = w
        self.h = h

    def draw(self, lines, transform):
        # find bounding box
        xs = []
        ys = []
        for line in lines:
            for p in line:
                x, y = transform(p)
                xs.append(abs(x))
                ys.append(abs(y))
        # scale to leave small margin
        scale = 0.9 * min(self.w / 2 / max(xs),
                          self.h / 2 / max(ys))
        print 'scale =', scale
        # draw
        for line in lines:
            p0, p1 = line
            x0, y0 = transform(p0)
            x1, y1 = transform(p1)
            print '(%s,%s)-(%s,%s)' % (x0, y0, x1, y1)
            self.context.moveTo(x0 * 100, y0 * 100)
            self.context.lineTo(x1 * 100, y1 * 100)
            self.context.stroke()

class Project2D(object):
    """
    Ad-hoc aphine projection onto XY plane.
    
    Treat all coordinates except X and Y as you would treat Z in 3D.
    """
    
    def __init__(self, *cameras):
        self.cameras = cameras
        
    def transform(self, point):
        x = point[0]
        y = point[1]
        for z, camera in zip(point[2:], self.cameras):
            xc, yc, zc = camera
            try:
                x += (x - xc) * z / (zc - z)
                y += (y - yc) * z / (zc - z)
            except ZeroDivisionError:
                pass
        return (x, y)

if __name__ == '__main__':
    canvas = LinesCanvas(300, 300)
    RootPanel().add(canvas)
    projection = Project2D((0, 0.5, 10), (0, 0, 40))
    canvas.draw(Cuboid([1, 1, 1, 1]).lines, projection.transform)
