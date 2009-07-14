"""
Render a Schlegel diagram of a 4-D Huppa.
"""

# Compatibility stubs
# ===================

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
def concat(*seqs):
    res = []
    for seq in seqs:
        res.extend(seq)
    return res

# Geometric model
# ===============

class Line(tuple):
    pass

def style_lines(lines, width):
    res = []
    for line in lines:
        line = Line(line)
        line.width = width
        res.append(line)
    return res

import math

def interpolate(p0, p1, ratio):
    """
    Linear interpolation - ratio=0 gives p0, 1 gives p1.
    """
    p = []
    for x0, x1 in zip(p0, p1):
        p.append(x0 * (1 - ratio) + x1 * ratio)
    return p

class Cuboid(object):
    """
    N-dimentional cuboid.
    """
    def __init__(self, sizes, fixed_axes={}):
        """
        `sizes` and `fixed_axes` are dicts.
        Their keys together should be range(N).
        """
        if len(sizes) == 0:
            # A 0-dimentional cuboid = a single point.
            self.lines = []
            # convert dict to list.
            point = []
            for axis in range(len(fixed_axes.keys())):
                point.append(fixed_axes[axis])
            self.points = [point]
        else:
            # Recursive construction: 2 facets + lines between them.
            axis, size = sizes[0]
            fixed0 = fixed_axes.copy()
            fixed0[axis] = -size
            facet0 = Cuboid(sizes[1:], fixed0)
            fixed1 = fixed_axes.copy()
            fixed1[axis] = +size
            facet1 = Cuboid(sizes[1:], fixed1)
            self.points = concat(facet0.points, facet1.points)
            self.lines = concat(
                facet0.lines,
                zip(facet0.points, facet1.points),
                facet1.lines,
                )

class Huppoid(Cuboid):
    """
    4-dimentional cuboid with tweaks.
    """
    def __init__(self, sizes):
        # Recursive construction: 2 facets + lines between them.
        (y_axis, y_size) = sizes[0]
        facet0 = Cuboid(sizes[1:], {y_axis: -y_size})
        facet1 = Cuboid(sizes[1:], {y_axis: +y_size})
        self.points = concat(facet0.points, facet1.points)

        self.lines = []
        self.lines.extend(style_lines(facet0.lines, 1))
        self.lines.extend(style_lines(zip(facet0.points, facet1.points), 3))

        # add a pretty wavy fabric
        for line in facet1.lines:
            wavy = []
            p0, p1 = line
            N = 30
            HEIGHT = 0.1
            for i in range(N + 1):
                t = i / N
                # vertical drop from point along the line
                p = interpolate(p0, p1, t)
                p[y_axis] = p[y_axis] - abs(math.sin(t * math.pi * 3)) * HEIGHT
                wavy.append(p)
            # the stright line should obscure the wavy fabric
            self.lines.extend(style_lines([line], 3))
            self.lines.extend(style_lines([wavy], 1))
                
class Project2D(object):
    """
    Perspective projection onto XYZ space, then onto XY plane.
    """
    
    def __init__(self, camera):
        self.camera = camera
        
    def transform(self, point):
        xc, yc, zc, wc = self.camera
        x, y, z, w = point
        # translate relative to (0, 0, 0, wc) camera
        w -= wc
        # project onto XYZ
        x *= -wc / w
        y *= -wc / w
        z *= -wc / w
        # translate relative to (xc, yc, zc) camera
        x -= xc
        y -= yc
        z -= zc
        # project onto XY
        x *= -zc / z
        y *= -zc / z
        # translate back to be relative to XY origin
        x += xc
        y += yc
        
	return (x, y)

# Canvas interface
# ================

from pyjamas import Window
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.Canvas2D import Canvas, CanvasImage
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.Button import Button

class LinesCanvas(Canvas):

    def __init__(self, w, h):
        Canvas.__init__(self, w, h)

        # center coordinates on (0,0); scaling will be done on-demand
        self.context.translate(w/2, h/2)
        # use math coords: y should grow upwards, not downwards
        self.context.scale(1, -1)
        # TODO: can we use context.scale to [-1,1] range?
        self.w = w
        self.h = h
        
    def draw(self, lines, image, transform):
        self.context.clearRect(-self.w/2, -self.h/2, self.w, self.h)

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
        
        # draw lines
        for line in lines:
            width = line.width
            line = map(transform, line)
            line.width = width
            for (extra_width, color, cap) in [
                (3, 'white', 'butt'),
                (0, 'black', 'round'),
                ]:
                self.context.lineWidth = getattr(line, 'width', 5) + extra_width
                self.context.strokeStyle = color
                self.context.fillStyle = 'white'
                self.context.lineCap = cap
                self.context.beginPath()
                p0 = line[0]
                self.context.moveTo(p0[0] * scale, p0[1] * scale)
                for p1 in line[1:]:
                    if extra_width > 0:
                        # YIKES :(
                        orig0, orig1 = p0, p1
                        if orig1 == line[1]:  # first
                            p0 = interpolate(orig0, orig1, 0.1)
                            self.context.moveTo(p0[0] * scale, p0[1] * scale)
                        if orig1 == line[-1]: # last
                            p1 = interpolate(orig0, orig1, 0.9)
                    self.context.lineTo(p1[0] * scale, p1[1] * scale)
                    p0 = p1
##                # fill frilly canvas
##                if len(line) > 2:
##                    self.context.fill()
                self.context.stroke()

        # draw image
        x0, y0, x1, y1, img = image
        # In math coords (Y grows up), the image should have negative height.
        # Firefox doesn't support negative height.
        # => Work around by temporarily returning to Y-down coords.
        y0, y1 = -y1, -y0
        self.context.save()
        self.context.scale(1, -1)
        self.context.drawImage(img,
                               x0 * scale, y0 * scale,
                               (x1 - x0) * scale, (y1 - y0) * scale)
        self.context.restore()

class Main(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self)
        self.canvas = LinesCanvas(1000, 1000)
        self.add(self.canvas)
        
        self.boxes = []
        for axis, c in zip("xyzw", (0, 1.8, 5, 12)):
            self.add(Label("Camera %s:" % axis))
            box = TextBox()
            box.setText(c)
            self.boxes.append(box)
            self.add(box)
            box.addKeyboardListener(self)
        self.camera = None  # force first redraw
        # first axis is Y - direction of huppoid
        # second axis is Z for correct Z-order.
        self.lines = Huppoid([(1,1), (2,1), (3,1), (0,1)]).lines
        #self.lines.extend(figures())
        self.figs = Image()
        self.figs.src = 'figures.png'
        self.draw()

    def draw(self):
        camera = []
        for box in self.boxes:
            camera.append(float(box.getText()))
        # guard against spurious redrawing (e.g. arrows or Tab presses)
        if camera != self.camera:
            self.camera = camera
            self.projection = Project2D(camera)
            self.canvas.draw(self.lines,
                             # assume source image is square
                             (-.8, -1, .8, .6, self.figs),
                             self.projection.transform)

        
    def onKeyUp(self, sender, keyCode, modifiers):
        self.draw()

    def onKeyDown(self, sender, keyCode, modifiers):
        pass
    
    def onKeyPress(self, sender, keyCode, modifiers):
        pass    

if __name__ == '__main__':
    RootPanel().add(Main())
