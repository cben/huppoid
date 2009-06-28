"""
Render a Schlegel diagram of a 4-D Huppa.
"""

from pyjamas.ui.RootPanel import RootPanel
from pyjamas.Canvas2D import Canvas
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox

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
def concat(*tuples):
    res = []
    for t in tuples:
        res.extend(t)
    return res

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
            facet0 = Cuboid(sizes[1:], concat(fixed_axes, (-sizes[0],)))
            facet1 = Cuboid(sizes[1:], concat(fixed_axes, (+sizes[0],)))

            self.points = concat(facet0.points, facet1.points)
            self.lines = concat(facet0.lines,
                                    facet1.lines,
                                    zip(facet0.points, facet1.points))

def scale(point, factors):
    coords = []
    for (coord, factor) in zip(point, factors):
        coords.append(coord * factor)
    return coords    

def figures(legsh=0.2, legsv=0.7, torsov=0.6,
            handh=0.7, handv0=0.2, handv1=0.3,
            headv=0.2, headh=0.2,
            size=1, fixed_axes=(0, 0)):
    """A schematic drawing of us on a 2D canvas"""
    # groom: x in [-1,0], y in [TODO: 0,1]  (will scale & mirror later...)
    gx = -handh
    gleftfoot = (gx - legsh, -1)
    grightfoot = (gx + legsh, -1)
    glowtorso = (gx, -1 + legsv)
    hightorso = glowtorso[1] + torsov
    ghightorso = (gx, hightorso)
    ghandlow = (0, hightorso - handv0)
    ghandhigh = (0, hightorso - handv1)
    gheadtop = (gx + headh, hightorso + headv)
    g = [(gleftfoot, glowtorso), (grightfoot, glowtorso),
         (glowtorso, ghightorso), (ghightorso, gheadtop),
         (ghightorso, ghandlow), (ghightorso, ghandhigh)]

    # List comprehensions don't work in pyjamas.
    lines = []
    for p0, p1 in g:
        # 2 figures
        for scaling in [(size, size), (-size, size)]:
            s0 = scale(p0, scaling)
            s1 = scale(p1, scaling)
            lines.append((concat(s0, fixed_axes),
                          concat(s1, fixed_axes)))
    return lines

    
class LinesCanvas(Canvas):

    def __init__(self, w, h):
        Canvas.__init__(self, w, h)

        # center coordinates on (0,0); scaling will be done on-demand
        self.context.translate(w/2, h/2)
        # TODO: can we use context.scale to [-1,1] range?
        self.w = w
        self.h = h

    def draw(self, lines, transform):
        self.context.fillStyle = '#FFFFFF' # white
        self.context.fillRect(-self.w/2, -self.h/2, self.w, self.h)
        
        # find bounding square (centered around 0,0)
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
        
        # draw
        for line in lines:
            p0, p1 = line
            x0, y0 = transform(p0)
            x1, y1 = transform(p1)
            # use math coords: y should grow upwards
            self.context.moveTo(x0 * scale, -y0 * scale)
            self.context.lineTo(x1 * scale, -y1 * scale)
            self.context.stroke()
        
        
class Project2D(object):
    """
    Perspective projection onto XY plane.
    """
    
    def __init__(self, camera):
        self.camera = camera
        
    def transform(self, point):
        rel_point = []
        for p, c in zip(point, self.camera):
            rel_point.append(p - c)
        x, y, z, w = rel_point
        xc, yc, zc, wc = self.camera
        scale = (zc / z) * (wc / w)
        x *= scale
        y *= scale
	return (x + xc, y + yc)

class Main(object):
    def __init__(self):
        self.canvas = LinesCanvas(300, 300)
        RootPanel().add(self.canvas)
        self.boxes = []
        for axis, c in zip("xyzw", (0, 0.5, 4, 20)):
            RootPanel().add(Label("Camera %s:" % axis))
            box = TextBox()
            box.setText(c)
            self.boxes.append(box)
            RootPanel().add(box)
            box.addKeyboardListener(self)
        self.lines = concat(Cuboid([1, 1, 1, 1]).lines, figures())
        self.draw()

    def draw(self):
        camera = []
        for box in self.boxes:
            camera.append(float(box.getText()))
        self.projection = Project2D(camera)
        print camera
        self.canvas.draw(self.lines, self.projection.transform)
        
    def onKeyUp(self, sender, keyCode, modifiers):
        self.draw()

    def onKeyDown(self, sender, keyCode, modifiers):
        pass
    
    def onKeyPress(self, sender, keyCode, modifiers):
        pass    

if __name__ == '__main__':
    m = Main()
