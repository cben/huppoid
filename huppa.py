# This is a Brython script, which means roughly Python 3.

"""
Render a Schlegel diagram (outer cube connected to inner cube) of a 4-D Huppa.
"""
print("Is this thing on?")

import math

# Brython
import browser
import browser.html as html
import javascript

# Compatibility stubs
# ===================

# Pyjamas has no zip()!
def zip(*lists):
    return [tuple([l[i] for l in lists])
            for i in range(len(lists[0]))]

# Pyjamas doesn't support + operator overloading!
# + on anything other than numbers returns concatenation of their
# string representations, e.g.: [1]+[2,3]=="[1][2,3]".
def concat(*seqs):
    return [item for seq in seqs for item in seq]


# Geometric model
# ===============

class Point(tuple):
    """A point in some number of dimensions.
    Sometimes will have a .z_order attribute added."""
    pass

class Line(list):
    """A sequence of points, with some style attributes.  Each point is a list of coordinates.
    (Use as many coordinates as the dimensions you work in.)"""
    cap = 'round'
    color = 'black'
    mode = 'source-over'
    width = 10  # highlight mistakes

def style_lines(lines, width):
    lines = [Line(l) for l in lines]
    for line in lines:
        line.width = width
    return lines

def interpolate(p0, p1, ratio):
    """
    Linear interpolation - ratio=0 gives p0, 1 gives p1.
    """
    return [x0 * (1 - ratio) + x1 * ratio
            for x0, x1 in zip(p0, p1)]

class Cuboid(object):
    """
    N-dimentional cuboid.
    """
    def __init__(self, sizes, fixed_axes={}):
        """
        `sizes` is list of (axis, size) pairs, `fixed_axes` is {axis: value} dict.
        In both, axis is an int; all axes taken together should == set(range(N)).
        This is done so Huppoid can special-case Y axis easier.
        """
        if len(sizes) == 0:
            # A 0-dimentional cuboid = a single point.
            self.lines = []
            # convert dict to list.
            point = Point([fixed_axes[axis]
                           for axis in range(len(fixed_axes.keys()))])
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
        """`sizes` is list of (axis, size) pairs.
        First pair is taken to be the non-trivial Y axis.
        """
        print("Huppoid()")
        # Recursive construction: 2 facets + lines between them.
        (y_axis, y_size) = sizes[0]
        facet0 = Cuboid(sizes[1:], {y_axis: -y_size})
        facet1 = Cuboid(sizes[1:], {y_axis: +y_size})
        print("  2 Cuboids computed.")
        self.points = concat(facet0.points, facet1.points)

        self.lines = []
        # bottom cube - make dashed lines
        for line in facet0.lines:
            self.lines.extend(style_lines(self.dash(line), width=2))
        print("  added dashed.")

        self.lines.extend(style_lines(zip(facet0.points, facet1.points), width=4))
        print("  added vertical.")

        # add a pretty wavy fabric
        for line in facet1.lines:
            wavy = self.wavy(line, y_axis)
            # the stright line should obscure the wavy fabric
            self.lines.extend(style_lines([line], width=5))
            self.lines.extend(style_lines(wavy, width=3))
        print("  added wavy.")

    def dash(self, line, segments=9):
        p0, p1 = line
        return [[interpolate(p0, p1, i / segments),
                 interpolate(p0, p1, (i + 1) / segments)]
                for i in range(segments)
                if i % 2 == 0]

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


class Project2D(object):
    """
    Perspective projection onto XYZ space, then onto XY plane.
    I'd hoped there is a "natural" 4D->2D projection that looks like I want,
    but it seems no, I need first to project into 3D and then —
    from a different point! — into 2D.
    Which is known as "Schlegel diagram".
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

class LinesCanvas(html.CANVAS):

    def __init__(self, w, h):
        html.CANVAS.__init__(self, width=w, height=h)
        # fallback content
        self <= "Your browser doesn't support the <CANVAS> tag.  Try Firefox or Chrome?"

        self.w = w
        self.h = h

        self.context = context = self.getContext('2d')
        # center coordinates on (0,0); scaling will be done on-demand
        context.translate(w/2, h/2)
        # use math coords: y should grow upwards, not downwards
        context.scale(1, -1)

    def draw(self, transform, lines, points, figures_coords_and_img):
        print("draw()")
        context = self.context

        context.clearRect(-self.w/2, -self.h/2, self.w, self.h)
        print("  clearRect.")

        # Transform, add white lines slightly behind real lines.
        lines2d = []
        for line in lines:
            black_line = Line(map(transform, line))
            black_line.width = line.width
            black_line.cap = line.cap
            black_line.color = line.color
            black_line.mode = line.mode
            lines2d.append(black_line)

            white_line = Line()
            for black_p in black_line:
                white_p = Point(black_p)
                white_p.z_order = black_p.z_order - 0.05
                white_line.append(white_p)
            white_line.width = line.width + 5
            white_line.cap = 'butt'
            white_line.color = 'white'
            white_line.mode = 'destination-out'
            lines2d.append(white_line)
        print("  created white and black 2d lines, total", len(lines2d), ".")

        # Find bounding square (centered around 0,0).
        xs = [abs(x)
              for line in lines2d
              for (x, y) in line]
        ys = [abs(y)
              for line in lines2d
              for (x, y) in line]
        # scale to leave small margin
        scale = 0.9 * min(self.w / 2 / max(xs),
                          self.h / 2 / max(ys))
        print("  computed scale =", scale, ".")

        # Draw lines.
        def z_order(line):
            zs = [p.z_order for p in line]
            return (min(zs), max(zs))
        # ``lines2d.sort(key=z_order)`` takes 14sec under Brython 3.2.3!
        # z_order() runs twice per comparison :-(
        # This decorate-sort-undecorate takes <1sec by only running z_order() once per line.
        print("  sort()")
        lines2d_sortkeys = [(z_order(line), i) for (i, line) in enumerate(lines2d)]
        lines2d_sortkeys.sort()
        lines2d = [lines2d[i] for (unused, i) in lines2d_sortkeys]
        print("  computed and z-sorted. drawing...")

        context.lineJoin = 'round'
        for line in lines2d:
            context.lineWidth = line.width
            context.lineCap = line.cap
            context.strokeStyle = line.color
            context.globalCompositeOperation = line.mode

            context.beginPath()
            p0 = line[0]
            context.moveTo(p0[0] * scale, p0[1] * scale)
            for p1 in line[1:]:
                context.lineTo(p1[0] * scale, p1[1] * scale)
                p0 = p1
            context.stroke()
        print("  drew lines")

        # Draw points.
        # No white points underneath them => no need for z-order, black is additive.
        # TODO: This is not strictly true in point-lines and point-image interactions!
        context.fillStyle = 'black'
        for p in points:
            x, y = transform(p)
            context.beginPath()
            context.arc(x * scale, y * scale, 5, 0, math.pi * 2, False)
            context.fill()
        print("  drew points")

        # Draw image.
        # TODO: Always on top is wrong, should observe z-order.
        x0, y0, x1, y1, img = figures_coords_and_img
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
        except Exception as e:
            print(e)
        context.restore()
        print("  drew img")

# Load JS image objects (bug in Brython 3.0 : can't load IMG object directly wthout using a javascript.JSConstructor object) -- http://webswap.free.fr/brythonrocks/simple.html
# Was known to not work in OSX Safari?
Image = javascript.JSConstructor(browser.window.Image)

class Main(html.DIV):
    def __init__(self):
        html.DIV.__init__(self)
        self.canvas = LinesCanvas(500, 500)
        self <= self.canvas

        # Start img fetch early, specifically before we compute the Huppoid.
        self.figures_img = Image()
        self.figures_img.src = 'figures.png'

        self.boxes = []
        for axis, c in zip("xyzw", (0, 1.7, 6, 20)):
            box = html.INPUT(type='number', step='0.5')
            box.value = str(c)
            box.bind('keyup', lambda ev: self.draw())
            box.bind('input', lambda ev: self.draw())
            self.boxes.append(box)
            self <= html.DIV(html.LABEL("Camera %s:" % axis) + box)
        self.camera = None  # force first redraw
        # first axis is Y - direction of huppoid
        # second axis is Z for correct Z-order.
        self.huppoid = Huppoid([(1,1), (2,1), (3,1), (0,1)])

    def draw(self):
        camera = [float(box.value)
                  for box in self.boxes]
        # guard against spurious redrawing (e.g. arrows or Tab presses)
        if camera != self.camera:
            if not self.figures_img.complete:
                print("postponing draw() until img loads")
                self.figures_img.bind('load', lambda ev: self.draw())
                return

            print("(re)drawing for camera =", camera)
            self.camera = camera
            self.projection = Project2D(camera)
            self.canvas.draw(self.projection.transform,
                             self.huppoid.lines,
                             self.huppoid.points,
                             # Bottom center (assume source image is square).
                             (-0.8, -1.0, 0.8, 0.6, self.figures_img))

def debug():
    """Poor man's python console.
    Useful because browser's JS console doesn't give sane access to Brython objects.
    """
    import traceback
    prompt = html.INPUT(type='text', size=80, style={'font-family': 'monospace'})
    output = html.PRE()
    def rep():
        # Our console overwrites outputs in-place, so also dump full "history" into browser's console.
        print('>>> ' + prompt.value)
        try:
            try:
                code = compile(prompt.value, "<debug input>", 'eval')
            except SyntaxError:
                code = compile(prompt.value, "<debug input>", 'exec')
            value = eval(code)
            # Native JS objects (e.g. DOM nodes) are reflected as having no __repr__
            # but all seem support str() via toString().
            try:
                res = repr(value)
            except:
                res = str(value)
        except:
            res = traceback.format_exc()
        output.text = res
        output.scrollIntoView({'block': 'end'})
        print(res)
    # 'change' fires when you press Enter (or change focus)
    prompt.bind('change', lambda ev: rep())
    browser.document <= html.DIV(html.HR() +
                                 html.DIV(">>> " + prompt) +
                                 output +
                                 html.HR())

l = [1.0, 2.0, 3.0]
p = Point(l)
q = list(p)
print(l, p, q, q is p)
x = l[0]
x += 10
y = p[1]
y += 20
z = q[2]
z += 30
print(l, p, q, p is l, q is p)

if __name__ == '__main__':
    main = Main()
    browser.document <= main
    main.draw()
    debug()
