# This is a Brython script, which means roughly Python 3.

# TODO: painfully slow under Brython (was much faster with Pyjamas).
# I'm not sure why I used <canvas> when I wrote this in 2009 but I
# think SVG had even less support then?  Anyway, nowdays could use SVG
# or WebGL - but it's not the drawing that's slow, it's EVERYTHING in Brython!
# Just computing the Huppoid's 16 points and 92 lines takes many seconds :-(

"""
Render a Schlegel diagram (outer cube connected to inner cube) of a 4-D Huppa.
"""

# Lots of print()s here - poor man's profiler.  Goes to browser console.
print("Is this thing on?")

import math

# Brython
import browser
import browser.html as html
import javascript


# Geometric model (and canvas drawing)
# ====================================
# Ideally these should be drawing-independent.
# But the final drawing is done by z-sorting points, lines, and the image all together
# and drawing them all.  So it's simplest if every object can draw itself.

class Point(tuple):
    """A point in some number of dimensions.
    Sometimes will have a .z_order attribute added."""

    def draw_on_canvas(self, context, scale):
        """Only works for 2D points."""
        context.save()
        context.fillStyle = 'black'

        context.beginPath()
        x, y = self
        context.arc(x * scale, y * scale, 5, 0, math.pi * 2, False)
        context.fill()
        context.restore()


class Line(list):
    """A sequence of points, with some style attributes.  Each point is a list of coordinates.
    (Use as many coordinates as the dimensions you work in.)"""
    cap = 'round'
    color = 'black'
    mode = 'source-over'
    width = 10  # highlight mistakes

    def draw_on_canvas(self, context, scale):
        """Only works for 2D points."""
        context.save()
        context.lineJoin = 'round'
        context.lineWidth = self.width
        context.lineCap = self.cap
        context.strokeStyle = self.color
        context.globalCompositeOperation = self.mode

        context.beginPath()
        p0 = self[0]
        context.moveTo(p0[0] * scale, p0[1] * scale)
        for p1 in self[1:]:
            context.lineTo(p1[0] * scale, p1[1] * scale)
            p0 = p1
        context.stroke()
        context.restore()


class FlatImage():
    """An image drawn on the XY plane."""
    def __init__(self, img_element, corner0, corner1):
        self.img_element = img_element
        self.corner0 = corner0
        self.corner1 = corner1

    def draw_on_canvas(self, context, scale):
        x0, y0 = self.corner0
        x1, y1 = self.corner1

        # In math coords (Y grows up), the image should have negative height.
        # Firefox doesn't (didn't in 2009?) support negative height.
        # => Work around by temporarily returning to Y-down coords.
        y0, y1 = -y1, -y0
        context.save()
        context.scale(1, -1)
        context.drawImage(self.img_element,
                          x0 * scale, y0 * scale,
                          (x1 - x0) * scale, (y1 - y0) * scale)
        context.restore()


def style_lines(lines, width):
    lines = list(map(Line, lines))
    for line in lines:
        line.width = width
    return lines


def interpolate(p0, p1, ratio):
    """
    Linear interpolation - ratio=0 gives p0, 1 gives p1.
    """
    return Point(map(lambda x: x[0] * (1 - ratio) + x[1] * ratio, zip(p0, p1)))


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
            self.points = facet0.points + facet1.points
            self.lines = facet0.lines + list(zip(facet0.points, facet1.points)) + facet1.lines


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
        self.points = facet0.points + facet1.points

        self.lines = []
        # bottom cube - make dashed lines
        for line in facet0.lines:
            self.lines.extend(style_lines(self.dash(line), width=2))
        print("  added dashed.")

        self.lines.extend(style_lines(zip(facet0.points, facet1.points), width=4))
        print("  added vertical.")

        # top cube - add a pretty wavy fabric
        for line in facet1.lines:
            self.lines.extend(style_lines([line], width=5))
            self.lines.extend(style_lines(self.wavy(line, y_axis), width=3))
        print("  added wavy.")

    def dash(self, line, segments=9):
        p0, p1 = line
        return [[interpolate(p0, p1, i / segments),
                 interpolate(p0, p1, (i + 1) / segments)]
                for i in range(0, segments, 2)]

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

    def transform_point(self, point):
        """Transform a 4D point into a 2D point."""
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
        z += zc

        res = Point((x, y))
        res.z = z  # For z-order computations
        return res

    # Z-Order (Painter's algorithm) is a lie
    # --------------------------------------
    #
    # First, the goals.  The *only* reason drawing order matters is that
    # I'm drawing white lines under black lines to create a
    # front-obscures-back effect: -|-
    #
    # I also want corners with a fat point to look "clean" with points not
    # obscured by any of the meeting lines - even back points by lines
    # coming from front.  However, unrelated lines in front should obscure
    # points.  Sounds tricky, but that's not the hard part.
    #
    # Mistake 1: I'd thought that since my projection is always onto a fixed-Z
    # plane, I can order objects solely by their absolute Z coordinate (after
    # 4D->3D transform, but disregarding camera location).  I can't, because when
    # camera looks from the left, the left side should obscure the right part
    # (with exactly same Z coordinates), and vice versa.
    #
    # Mistake 2: Expecting I just need a better formula for an object's z-order, e.g.
    # distance from camera to infinite continuation of a line (doesn't work).
    #
    # Mistake 3: Expecting I can at least write a pairwise comparison function.
    # In *general position*, lines obsrcuring might not be transitive!
    # You can lay sticks like this:
    #      |  |
    #     ----|-
    #      |  |
    #     -|----
    #      |  |
    # (That's why per-pixel Z-buffer got invented!  Hard to implement with Canvas.)
    #
    # => Can I still get away with a (almost correct) lie for Huppoid?!?
    #
    # Unfortunately I don't have time to debug this further, so here is my
    # heuristic from 2009:
    #
    # 1. Sort lines by (farthest_point, closest_point).  This way front lines
    #    obscure back-front connecting lines which obscure back lines.  The order
    #    of the 2 is not very important for lines [*]_, but having farthest first
    #    allows a fat point at line's back end to still not be obscured by white line
    #    whose depth starts with farthest_point + epsilon.  Kludge...
    #
    #    .. [*] It is important outer vs inner line crossings, but either way gets
    #       some of them wrong.
    #
    # with a mild improvements:
    #
    # 2. Sort points as (depth, depth) for consistency, and the image as
    #    (farthest_corner, closest_corner).  [In 2009 I always drew points and
    #    image after lines.]
    #
    # 3. Measure point depth by (z, -pythagorean distance) to camera.  Distance
    #    to camera gets the right-vs-left depending on camera position part
    #    mostly right, and *mostly* doesn't cause other bugs.  (z, -distance) causes
    #    slightly less bugs.

    # These are methods of `Project2D` so they know where the camera is.

    def point_depth(self, point):
        """Pythagorean distance to camera."""
        x, y = point
        z = point.z
        xc, yc, zc, wc = self.camera
        distance_to_camera = ((x - xc)**2 + (y - yc)**2 + (z - zc)**2) #**0.5 -- same order
        return ((z, -distance_to_camera), (z, -distance_to_camera))

    def line_depth(self, line):
        ds = [self.point_depth(p)[0] for p in line]
        # (min, max) order ensures front-back connecting lines are
        # drawn after back and before front.
        return (min(ds), max(ds))

    def image_depth(self, image):
        # TODO: all 4 corners
        return self.line_depth([image.corner0, image.corner1])


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

    def draw(self, projection, lines, points, images):
        print("draw()")
        context = self.context

        context.clearRect(-self.w/2, -self.h/2, self.w, self.h)
        print("  clearRect.")

        # We'll transform some points several times, both as
        # standalone points and as ends of (several) lines.  But most
        # of the points are intermediate points on dashed/wavy lines;
        # we have 460 unique points and do about 548 transforms total,
        # so optimizing it is hardly worth it.
        transform_point = projection.transform_point

        # Transform lines, add wider white lines slightly behind real lines
        # to create front-obscures-back effect at crossings: -|-
        lines2d = []
        for line in lines:
            black_line = Line(map(transform_point, line))
            black_line.width = line.width
            black_line.cap = line.cap
            black_line.color = line.color
            black_line.mode = line.mode
            lines2d.append(black_line)

            white_line = Line()
            for black_p in black_line:
                white_p = Point(black_p)
                white_p.z = black_p.z - 0.05  # a tiny bit behind
                white_line.append(white_p)
            white_line.width = line.width + 5
            white_line.cap = 'butt'
            white_line.color = 'white'
            white_line.mode = 'destination-out'
            lines2d.append(white_line)
        print("  created white and black 2d lines, total", len(lines2d), ".")

        points2d = list(map(transform_point, points))

        images2d = [FlatImage(image.img_element,
                              transform_point(image.corner0),
                              transform_point(image.corner1))
                    for image in images]

        print("  sort()")
        # ``lines2d.sort(key=projection.line_depth)`` takes 14sec under Brython 3.2.3!
        # z_order() runs twice per comparison :-(
        # decorate-sort-undecorate takes ~1sec by only running z_order() once per line.
        depths_objects = ([(projection.line_depth(l), l) for l in lines2d] +
                          [(projection.point_depth(p), p) for p in points2d] +
                          [(projection.image_depth(i), i) for i in images2d])
        global objects, tosort, lines2d, points2d, images2d  # DEBUG
        tosort = [(depth, i) for (i, (depth, obj)) in enumerate(depths_objects)]
        tosort.sort()
        objects = [depths_objects[i][1] for (unused, i) in tosort]
        print("  z-sorted.")

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
        # TODO: use context.scale instead of passing scale around?

        for obj in objects:
            obj.draw_on_canvas(context, scale)
        print("  drew.")


class Main(html.DIV):
    def __init__(self):
        html.DIV.__init__(self)
        self.canvas = LinesCanvas(500, 500)
        self <= self.canvas

        # Start img fetch early, specifically before we compute the Huppoid.
        self.figures_img = html.IMG(src='figures.png')
        self.image = FlatImage(self.figures_img,
                               # Bottom center 1.6x1.6 (assumes source image is square).
                               corner0=Point((-0.8, -1.0, 0, 0)),
                               corner1=Point((+0.8, +0.6, 0, 0)))

        self.boxes = []
        for (axis, value) in zip("XYZW", (0, 1.7, 6, 20)):
            box = html.INPUT(type='number', step='0.5')
            box.value = str(value)
            box.bind('keyup', self.onedit)
            box.bind('input', self.onedit)
            self.boxes.append(box)
            self <= html.DIV(html.LABEL("Camera %s:" % axis) + box)
        self.set_boxes_from_hash()
        browser.window.onhashchange = self.onhashchange
        self.last_camera = None  # first draw() should always draw.

        # 4D coordinates are always in XYZW order (that's what Project2D assumes).
        # Huppoid constructor wants (axis, size) pairs where the first axis
        # should be the non-symmetric base-roof axis, i.e. Y = 1.
        self.huppoid = Huppoid([(1, 1.0), (2, 1.0), (3, 1.0), (0, 1.0)])

    def onhashchange(self, event):
        self.set_boxes_from_hash()
        self.draw()

    def set_boxes_from_hash(self):
        if ',' in browser.window.location.hash:
            camera = map(float, browser.window.location.hash.lstrip('#').split(','))
            for box, c in zip(self.boxes, camera):
                box.value = str(c)

    def onedit(self, event):
        self.draw()
        # I don't want this to appear for all visitors, only after they move the camera.
        browser.window.location.hash = '#%s,%s,%s,%s' % tuple(self.last_camera)

    def draw(self):
        camera = [float(box.value)
                  for box in self.boxes]
        # guard against spurious redrawing (e.g. arrows or Tab presses)
        if camera != self.last_camera:
            if not self.figures_img.complete:
                print("postponing draw() until img loads")
                self.figures_img.bind('load', lambda ev: self.draw())
                return

            print("(re)drawing for camera =", camera)
            self.last_camera = camera
            self.projection = Project2D(camera)
            self.canvas.draw(self.projection,
                             self.huppoid.lines,
                             self.huppoid.points,
                             [self.image])


def debug():
    """Poor man's python console.
    Useful because browser's JS console doesn't give sane access to Brython objects.
    """
    import traceback

    prompt = html.INPUT(type='text', size=80, style={'font-family': 'monospace'})
    output = html.PRE(style={'white-space': 'pre-wrap'})
    def rep():
        # Our console overwrites outputs in-place, so also dump full "history" into browser's console.
        print('>>> ' + prompt.value)
        try:
            value = eval(prompt.value)
            # Native JS objects (e.g. DOM nodes) are reflected as having no __repr__
            # but all seem to support str() - probably via ``.toString()``.
            try:
                res = repr(value)
            except:
                res = str(value)
        except SyntaxError:
            exec(prompt.value)
            res = ''
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


if __name__ == '__main__':
    if browser.document.query.getfirst('debug') is not None:
        debug()
    main = Main()
    target = browser.document.getElementById('huppoid_here')
    target.html = ''  # replace any fallback content
    target <= main
    main.draw()
