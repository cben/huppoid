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

class Line(list):
    cap = 'round'
    color = 'black'
    width = 10  # highlight mistakes

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
        # bottom cube - make dashed lines
        for line in facet0.lines:
            self.lines.extend(style_lines(self.dash(line), 1))
        self.lines.extend(style_lines(zip(facet0.points, facet1.points), 4))

        # add a pretty wavy fabric
        for line in facet1.lines:
            wavy = self.wavy(line, y_axis)
            # the stright line should obscure the wavy fabric
            self.lines.extend(style_lines([line], 4))
            self.lines.extend(style_lines(wavy, 2))

    def dash(self, line, segments=13):
        dash = []
        p0, p1 = line
        for i in range(segments):
            if i % 2 == 0:
                dash.append([interpolate(p0, p1, i / segments),
                             interpolate(p0, p1, (i + 1) / segments)])
        return dash
        
    def wavy(self, line, y_axis, drop=0.1, periods=3, segments=30):
        wavy = []
        p0, p1 = line
        for i in range(segments + 1):
            t = i / segments
            # vertical drop from point along the line
            p = interpolate(p0, p1, t)
            p[y_axis] = p[y_axis] - abs(math.sin(t * math.pi * periods)) * drop
            wavy.append(p)
        return [wavy]
        

class Point(tuple):
    pass
                
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

        res = Point((x, y))
        res.z_order = z
	return res

# Canvas interface
# ================

from pyjamas import Window
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.Canvas2D import Canvas, CanvasImage
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.Button import Button
import math

class LinesCanvas(Canvas):

    def __init__(self, w, h):
        Canvas.__init__(self, w, h)
        self.w = w
        self.h = h        
        
        context = self.context
        # center coordinates on (0,0); scaling will be done on-demand
        context.translate(w/2, h/2)
        # use math coords: y should grow upwards, not downwards
        context.scale(1, -1)

    def draw(self, transform, lines, points, image):
        context = self.context
        
        context.clearRect(-self.w/2, -self.h/2, self.w, self.h)

        # transform, add white lines slightly behind real lines
        lines2d = []
        for line in lines:
            black_line = Line(map(transform, line))
            black_line.width = line.width
            black_line.cap = line.cap
            black_line.color = line.color
            lines2d.append(black_line)
            
            white_line = Line()
            for black_p in black_line:
                white_p = Point(black_p)
                white_p.z_order = black_p.z_order - 0.05
                white_line.append(white_p)
            white_line.width = line.width + 5
            white_line.cap = 'butt'
            white_line.color = 'white'
            lines2d.append(white_line)

        # find bounding square (centered around 0,0)
        xs = []
        ys = []
        for line in lines2d:
            for (x, y) in line:
                xs.append(abs(x))
                ys.append(abs(y))
        # scale to leave small margin
        scale = 0.9 * min(self.w / 2 / max(xs),
                          self.h / 2 / max(ys))

        # draw lines
        def z_order(line):
            zs = []
            for p in line:
                zs.append(p.z_order)
            return (min(zs), max(zs))
            
        lines2d.sort(keyFunc=z_order)  # key= in normal python

        context.lineJoin = 'round'
        for line in lines2d:
            context.lineWidth = line.width
            context.lineCap = line.cap
            context.strokeStyle = line.color

            context.beginPath()
            p0 = line[0]
            context.moveTo(p0[0] * scale, p0[1] * scale)
            for p1 in line[1:]:
##                if extra_width > 0:
##                    # YIKES :(
##                    orig0, orig1 = p0, p1
##                    if orig1 == line[1]:  # first
##                        p0 = interpolate(orig0, orig1, 0.1)
##                        context.moveTo(p0[0] * scale, p0[1] * scale)
##                    if orig1 == line[-1]: # last
##                        p1 = interpolate(orig0, orig1, 0.9)
                context.lineTo(p1[0] * scale, p1[1] * scale)
                p0 = p1
            context.stroke()

        # draw points
        context.fillStyle = 'black'
        for p in points:
            x, y = transform(p)
            context.beginPath()
            context.arc(x * scale, y * scale, 5, 0, math.pi * 2, False)
            context.fill()

        # draw image
        x0, y0, x1, y1, img = image
        # In math coords (Y grows up), the image should have negative height.
        # Firefox doesn't support negative height.
        # => Work around by temporarily returning to Y-down coords.
        y0, y1 = -y1, -y0
        context.save()
        context.scale(1, -1)
        try:
            # This fails with a mysterious NS_ERROR_NOT_AVAILABLE error
            # if the image is not already in cache (at least on Firefox).
            # Attempt to continue instead of dying horribly - doesn't work(?).
            context.drawImage(img,
                              x0 * scale, y0 * scale,
                              (x1 - x0) * scale, (y1 - y0) * scale)
        except Exception, e:
            print e
        context.restore()

class Main(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self)
        self.canvas = LinesCanvas(1000, 1000)
        self.add(self.canvas)
        
        self.boxes = []
        for axis, c in zip("xyzw", (0, 1.7, 6, 20)):
            self.add(Label("Camera %s:" % axis))
            box = TextBox()
            box.setText(c)
            self.boxes.append(box)
            self.add(box)
            box.addKeyboardListener(self)
        self.camera = None  # force first redraw
        # first axis is Y - direction of huppoid
        # second axis is Z for correct Z-order.
        self.huppoid = Huppoid([(1,1), (2,1), (3,1), (0,1)])
        self.figures = Image()
        self.figures.src = 'figures.png'
##        print self.figures.isLoaded()
        self.draw()

    def draw(self):
        camera = []
        for box in self.boxes:
            camera.append(float(box.getText()))
        # guard against spurious redrawing (e.g. arrows or Tab presses)
        if camera != self.camera:
            self.camera = camera
            self.projection = Project2D(camera)
            self.canvas.draw(self.projection.transform,
                             self.huppoid.lines,
                             self.huppoid.points,
                             # assume source image is square
                             (-.8, -1, .8, .6, self.figures))

        
    def onKeyUp(self, sender, keyCode, modifiers):
        self.draw()

    def onKeyDown(self, sender, keyCode, modifiers):
        pass
    
    def onKeyPress(self, sender, keyCode, modifiers):
        pass    

if __name__ == '__main__':
    RootPanel().add(Main())
