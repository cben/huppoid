/* start module: huppa */
var huppa = $pyjs.loaded_modules["huppa"] = function (__mod_name__) {
if(huppa.__was_initialized__) return huppa;
huppa.__was_initialized__ = true;
if (__mod_name__ == null) __mod_name__ = 'huppa';
var __name__ = huppa.__name__ = __mod_name__;
 pyjslib.__import__(['pyjd'], 'pyjd', 'huppa');
 huppa.pyjd = $pyjs.__modules__.pyjd;
huppa.zip = function() {
	var lists = new Array();
	for (var pyjs__va_arg = 0; pyjs__va_arg < arguments.length; pyjs__va_arg++) {
		var pyjs__arg = arguments[pyjs__va_arg];
		lists.push(pyjs__arg);
	}
	lists = pyjslib.Tuple(lists);


	return function(){
var listcomp000001 = pyjslib.List();
	var __i = pyjslib.range(pyjslib.len(lists.__getitem__(0))).__iter__();
	try {
		while (true) {
			var i = __i.next();
			
			listcomp000001.append(pyjslib.tuple(function(){
var listcomp000002 = pyjslib.List();
			var __l = lists.__iter__();
			try {
				while (true) {
					var l = __l.next();
					
					listcomp000002.append(l.__getitem__(i));
				}
			} catch (e) {
				if (e.__name__ != 'StopIteration') {
					throw e;
				}
			}
return listcomp000002;}()));
		}
	} catch (e) {
		if (e.__name__ != 'StopIteration') {
			throw e;
		}
	}
return listcomp000001;}();
};
huppa.zip.__name__ = 'zip';

huppa.zip.__bind_type__ = 0;
huppa.zip.__args__ = ['lists',null];
huppa.concat = function() {
	var seqs = new Array();
	for (var pyjs__va_arg = 0; pyjs__va_arg < arguments.length; pyjs__va_arg++) {
		var pyjs__arg = arguments[pyjs__va_arg];
		seqs.push(pyjs__arg);
	}
	seqs = pyjslib.Tuple(seqs);


	return function(){
var listcomp000003 = pyjslib.List();
	var __seq = seqs.__iter__();
	try {
		while (true) {
			var seq = __seq.next();
			
			var __item = seq.__iter__();
			try {
				while (true) {
					var item = __item.next();
					
					listcomp000003.append(item);
				}
			} catch (e) {
				if (e.__name__ != 'StopIteration') {
					throw e;
				}
			}
		}
	} catch (e) {
		if (e.__name__ != 'StopIteration') {
			throw e;
		}
	}
return listcomp000003;}();
};
huppa.concat.__name__ = 'concat';

huppa.concat.__bind_type__ = 0;
huppa.concat.__args__ = ['seqs',null];
huppa.Line = (function(){
	var cls_instance = pyjs__class_instance('Line');
	var cls_definition = new Object();
	cls_definition.__md5__ = '15953062e7e8942aadba249853877d94';
	cls_definition.cap = String('round');
	cls_definition.color = String('black');
	cls_definition.mode = String('source-over');
	cls_definition.width = 10;
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjslib.list));
})();
huppa.style_lines = function(lines, width) {
	var line;
	lines = pyjslib.map(huppa.Line, lines);
	var __line = lines.__iter__();
	try {
		while (true) {
			var line = __line.next();
			
			line.width = width;
		}
	} catch (e) {
		if (e.__name__ != 'StopIteration') {
			throw e;
		}
	}
	return lines;
};
huppa.style_lines.__name__ = 'style_lines';

huppa.style_lines.__bind_type__ = 0;
huppa.style_lines.__args__ = [null,null,'lines', 'width'];
 pyjslib.__import__(['math'], 'math', 'huppa');
 huppa.math = $pyjs.__modules__.math;
huppa.interpolate = function(p0, p1, ratio) {

	return function(){
var listcomp000004 = pyjslib.List();
	var __temp_x0 = huppa.zip(p0, p1).__iter__();
	try {
		while (true) {
			var temp_x0 = __temp_x0.next();
				var x0 = temp_x0.__getitem__(0);	var x1 = temp_x0.__getitem__(1);
			listcomp000004.append( (  ( x0 *  ( 1 - ratio )  )  +  ( x1 * ratio )  ) );
		}
	} catch (e) {
		if (e.__name__ != 'StopIteration') {
			throw e;
		}
	}
return listcomp000004;}();
};
huppa.interpolate.__name__ = 'interpolate';

huppa.interpolate.__bind_type__ = 0;
huppa.interpolate.__args__ = [null,null,'p0', 'p1', 'ratio'];
huppa.Cuboid = (function(){
	var cls_instance = pyjs__class_instance('Cuboid');
	var cls_definition = new Object();
	cls_definition.__md5__ = '18c6692331c3e073df67be4e3bf14e11';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(sizes, fixed_axes) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sizes = arguments[1];
			fixed_axes = arguments[2];
		}
		if (typeof fixed_axes == 'undefined') fixed_axes=new pyjslib.Dict([]);
		var point,facet1,facet0,fixed0,fixed1,size,axis;
		if (pyjslib.bool(pyjslib.eq(pyjslib.len(sizes), 0))) {
			self.lines = new pyjslib.List([]);
			point = function(){
var listcomp000005 = pyjslib.List();
			var __axis = pyjslib.range(pyjslib.len(fixed_axes.keys())).__iter__();
			try {
				while (true) {
					var axis = __axis.next();
					
					listcomp000005.append(fixed_axes.__getitem__(axis));
				}
			} catch (e) {
				if (e.__name__ != 'StopIteration') {
					throw e;
				}
			}
return listcomp000005;}();
			self.points = new pyjslib.List([point]);
		}
		else {
			var __tupleassign__000001 = sizes.__getitem__(0);
			axis = __tupleassign__000001.__getitem__(0);
			size = __tupleassign__000001.__getitem__(1);
			fixed0 = fixed_axes.copy();
			fixed0.__setitem__(axis, -size);
			facet0 = huppa.Cuboid(pyjslib.slice(sizes, 1, null), fixed0);
			fixed1 = fixed_axes.copy();
			fixed1.__setitem__(axis, size);
			facet1 = huppa.Cuboid(pyjslib.slice(sizes, 1, null), fixed1);
			self.points = huppa.concat((typeof facet0.points == 'function' && facet0.__is_instance__?pyjslib.getattr(facet0, 'points'):facet0.points), (typeof facet1.points == 'function' && facet1.__is_instance__?pyjslib.getattr(facet1, 'points'):facet1.points));
			self.lines = huppa.concat((typeof facet0.lines == 'function' && facet0.__is_instance__?pyjslib.getattr(facet0, 'lines'):facet0.lines), huppa.zip((typeof facet0.points == 'function' && facet0.__is_instance__?pyjslib.getattr(facet0, 'points'):facet0.points), (typeof facet1.points == 'function' && facet1.__is_instance__?pyjslib.getattr(facet1, 'points'):facet1.points)), (typeof facet1.lines == 'function' && facet1.__is_instance__?pyjslib.getattr(facet1, 'lines'):facet1.lines));
		}
		return null;
	}
	, 1, [null,null,'self', 'sizes', 'fixed_axes']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjslib.object));
})();
huppa.Huppoid = (function(){
	var cls_instance = pyjs__class_instance('Huppoid');
	var cls_definition = new Object();
	cls_definition.__md5__ = '2caab1a409965c39e5610f4cf6dc86ac';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(sizes) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sizes = arguments[1];
		}
		var y_size,facet1,facet0,wavy,y_axis,line;
		var __tupleassign__000002 = sizes.__getitem__(0);
		y_axis = __tupleassign__000002.__getitem__(0);
		y_size = __tupleassign__000002.__getitem__(1);
		facet0 = huppa.Cuboid(pyjslib.slice(sizes, 1, null), new pyjslib.Dict([[y_axis, -y_size]]));
		facet1 = huppa.Cuboid(pyjslib.slice(sizes, 1, null), new pyjslib.Dict([[y_axis, y_size]]));
		self.points = huppa.concat((typeof facet0.points == 'function' && facet0.__is_instance__?pyjslib.getattr(facet0, 'points'):facet0.points), (typeof facet1.points == 'function' && facet1.__is_instance__?pyjslib.getattr(facet1, 'points'):facet1.points));
		self.lines = new pyjslib.List([]);
		var __line = facet0.lines.__iter__();
		try {
			while (true) {
				var line = __line.next();
				
				self.lines.extend(huppa.style_lines(self.dash(line), 2));
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		self.lines.extend(huppa.style_lines(huppa.zip((typeof facet0.points == 'function' && facet0.__is_instance__?pyjslib.getattr(facet0, 'points'):facet0.points), (typeof facet1.points == 'function' && facet1.__is_instance__?pyjslib.getattr(facet1, 'points'):facet1.points)), 4));
		var __line = facet1.lines.__iter__();
		try {
			while (true) {
				var line = __line.next();
				
				wavy = self.wavy(line, y_axis);
				self.lines.extend(huppa.style_lines(new pyjslib.List([line]), 5));
				self.lines.extend(huppa.style_lines(wavy, 3));
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		return null;
	}
	, 1, [null,null,'self', 'sizes']);
	cls_definition.dash = pyjs__bind_method(cls_instance, 'dash', function(line, segments) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			line = arguments[1];
			segments = arguments[2];
		}
		if (typeof segments == 'undefined') segments=9;
		var p1,p0;
		var __tupleassign__000003 = line;
		p0 = __tupleassign__000003.__getitem__(0);
		p1 = __tupleassign__000003.__getitem__(1);
		return function(){
var listcomp000006 = pyjslib.List();
		var __i = pyjslib.range(segments).__iter__();
		try {
			while (true) {
				var i = __i.next();
				
				if (pyjslib.bool(pyjslib.eq(i % 2, 0))) {
					listcomp000006.append(new pyjslib.List([huppa.interpolate(p0, p1,  ( i / segments ) ), huppa.interpolate(p0, p1,  (  ( i + 1 )  / segments ) )]));
				}
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
return listcomp000006;}();
	}
	, 1, [null,null,'self', 'line', 'segments']);
	cls_definition.wavy = pyjs__bind_method(cls_instance, 'wavy', function(line, y_axis, drop, periods, segments) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			line = arguments[1];
			y_axis = arguments[2];
			drop = arguments[3];
			periods = arguments[4];
			segments = arguments[5];
		}
		if (typeof drop == 'undefined') drop=0.1;
		if (typeof periods == 'undefined') periods=3;
		if (typeof segments == 'undefined') segments=30;
		var p0,p1,i,p,wavy,t;
		wavy = new pyjslib.List([]);
		var __tupleassign__000004 = line;
		p0 = __tupleassign__000004.__getitem__(0);
		p1 = __tupleassign__000004.__getitem__(1);
		var __i = pyjslib.range( ( segments + 1 ) ).__iter__();
		try {
			while (true) {
				var i = __i.next();
				
				t =  ( i / segments ) ;
				p = huppa.interpolate(p0, p1, t);
				p.__setitem__(y_axis,  ( p.__getitem__(y_axis) -  ( pyjslib.abs(huppa.math.sin( (  ( t * (typeof huppa.math.pi == 'function' && huppa.math.__is_instance__?pyjslib.getattr(huppa.math, 'pi'):huppa.math.pi) )  * periods ) )) * drop )  ) );
				wavy.append(p);
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		return new pyjslib.List([wavy]);
	}
	, 1, [null,null,'self', 'line', 'y_axis', 'drop', 'periods', 'segments']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(huppa.Cuboid));
})();
huppa.Point = (function(){
	var cls_instance = pyjs__class_instance('Point');
	var cls_definition = new Object();
	cls_definition.__md5__ = 'f75489d009db706ac812e203c3bc2868';
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjslib.tuple));
})();
huppa.Project2D = (function(){
	var cls_instance = pyjs__class_instance('Project2D');
	var cls_definition = new Object();
	cls_definition.__md5__ = '2e143b996dbc7d917db65a43b19d5896';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(camera) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			camera = arguments[1];
		}

		self.camera = camera;
		return null;
	}
	, 1, [null,null,'self', 'camera']);
	cls_definition.transform = pyjs__bind_method(cls_instance, 'transform', function(point) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			point = arguments[1];
		}
		var wc,xc,zc,w,res,y,x,z,yc;
		var __tupleassign__000005 = (typeof self.camera == 'function' && self.__is_instance__?pyjslib.getattr(self, 'camera'):self.camera);
		xc = __tupleassign__000005.__getitem__(0);
		yc = __tupleassign__000005.__getitem__(1);
		zc = __tupleassign__000005.__getitem__(2);
		wc = __tupleassign__000005.__getitem__(3);
		var __tupleassign__000006 = point;
		x = __tupleassign__000006.__getitem__(0);
		y = __tupleassign__000006.__getitem__(1);
		z = __tupleassign__000006.__getitem__(2);
		w = __tupleassign__000006.__getitem__(3);
		w -= wc;
		x *=  ( -wc / w ) ;
		y *=  ( -wc / w ) ;
		z *=  ( -wc / w ) ;
		x -= xc;
		y -= yc;
		z -= zc;
		x *=  ( -zc / z ) ;
		y *=  ( -zc / z ) ;
		x += xc;
		y += yc;
		res = huppa.Point(new pyjslib.Tuple([x, y]));
		res.z_order = z;
		return res;
	}
	, 1, [null,null,'self', 'point']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjslib.object));
})();
 pyjslib.__import__(['pyjamas.Window', 'pyjamas'], 'pyjamas.Window', 'huppa');
 huppa.Window = $pyjs.__modules__.pyjamas.Window;
 pyjslib.__import__(['pyjamas.ui.RootPanel.RootPanel', 'pyjamas.ui.RootPanel'], 'pyjamas.ui.RootPanel.RootPanel', 'huppa');
 huppa.RootPanel = $pyjs.__modules__.pyjamas.ui.RootPanel.RootPanel;
 pyjslib.__import__(['pyjamas.Canvas2D.Canvas', 'pyjamas.Canvas2D'], 'pyjamas.Canvas2D.Canvas', 'huppa');
 huppa.Canvas = $pyjs.__modules__.pyjamas.Canvas2D.Canvas;
 pyjslib.__import__(['pyjamas.Canvas2D.CanvasImage', 'pyjamas.Canvas2D'], 'pyjamas.Canvas2D.CanvasImage', 'huppa');
 huppa.CanvasImage = $pyjs.__modules__.pyjamas.Canvas2D.CanvasImage;
 pyjslib.__import__(['pyjamas.ui.Label.Label', 'pyjamas.ui.Label'], 'pyjamas.ui.Label.Label', 'huppa');
 huppa.Label = $pyjs.__modules__.pyjamas.ui.Label.Label;
 pyjslib.__import__(['pyjamas.ui.TextBox.TextBox', 'pyjamas.ui.TextBox'], 'pyjamas.ui.TextBox.TextBox', 'huppa');
 huppa.TextBox = $pyjs.__modules__.pyjamas.ui.TextBox.TextBox;
 pyjslib.__import__(['pyjamas.ui.VerticalPanel.VerticalPanel', 'pyjamas.ui.VerticalPanel'], 'pyjamas.ui.VerticalPanel.VerticalPanel', 'huppa');
 huppa.VerticalPanel = $pyjs.__modules__.pyjamas.ui.VerticalPanel.VerticalPanel;
 pyjslib.__import__(['pyjamas.ui.Button.Button', 'pyjamas.ui.Button'], 'pyjamas.ui.Button.Button', 'huppa');
 huppa.Button = $pyjs.__modules__.pyjamas.ui.Button.Button;
 huppa.math = $pyjs.__modules__.math;
huppa.LinesCanvas = (function(){
	var cls_instance = pyjs__class_instance('LinesCanvas');
	var cls_definition = new Object();
	cls_definition.__md5__ = 'b813fb43bd670b00c5f3055225e8e273';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(w, h) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			w = arguments[1];
			h = arguments[2];
		}
		var context;
		huppa.Canvas.__init__(self, w, h);
		self.w = w;
		self.h = h;
		context = (typeof self.context == 'function' && self.__is_instance__?pyjslib.getattr(self, 'context'):self.context);
		context.translate( ( w / 2 ) ,  ( h / 2 ) );
		context.scale(1, -1);
		return null;
	}
	, 1, [null,null,'self', 'w', 'h']);
	cls_definition.draw = pyjs__bind_method(cls_instance, 'draw', function(transform, lines, points, image) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			transform = arguments[1];
			lines = arguments[2];
			points = arguments[3];
			image = arguments[4];
		}
		var white_p,y0,black_line,xs,x0,scale,img,pyjs_try_err,line,white_line,lines2d,black_p,ys,x1,z_order,p0,p1,e,y1,p,context,y,x;
		context = (typeof self.context == 'function' && self.__is_instance__?pyjslib.getattr(self, 'context'):self.context);
		context.clearRect( ( -(typeof self.w == 'function' && self.__is_instance__?pyjslib.getattr(self, 'w'):self.w) / 2 ) ,  ( -(typeof self.h == 'function' && self.__is_instance__?pyjslib.getattr(self, 'h'):self.h) / 2 ) , (typeof self.w == 'function' && self.__is_instance__?pyjslib.getattr(self, 'w'):self.w), (typeof self.h == 'function' && self.__is_instance__?pyjslib.getattr(self, 'h'):self.h));
		lines2d = new pyjslib.List([]);
		var __line = lines.__iter__();
		try {
			while (true) {
				var line = __line.next();
				
				black_line = huppa.Line(pyjslib.map(transform, line));
				black_line.width = (typeof line.width == 'function' && line.__is_instance__?pyjslib.getattr(line, 'width'):line.width);
				black_line.cap = (typeof line.cap == 'function' && line.__is_instance__?pyjslib.getattr(line, 'cap'):line.cap);
				black_line.color = (typeof line.color == 'function' && line.__is_instance__?pyjslib.getattr(line, 'color'):line.color);
				black_line.mode = (typeof line.mode == 'function' && line.__is_instance__?pyjslib.getattr(line, 'mode'):line.mode);
				lines2d.append(black_line);
				white_line = huppa.Line();
				var __black_p = black_line.__iter__();
				try {
					while (true) {
						var black_p = __black_p.next();
						
						white_p = huppa.Point(black_p);
						white_p.z_order =  ( (typeof black_p.z_order == 'function' && black_p.__is_instance__?pyjslib.getattr(black_p, 'z_order'):black_p.z_order) - 0.05 ) ;
						white_line.append(white_p);
					}
				} catch (e) {
					if (e.__name__ != 'StopIteration') {
						throw e;
					}
				}
				white_line.width =  ( (typeof line.width == 'function' && line.__is_instance__?pyjslib.getattr(line, 'width'):line.width) + 5 ) ;
				white_line.cap = String('butt');
				white_line.color = String('white');
				white_line.mode = String('destination-out');
				lines2d.append(white_line);
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		xs = function(){
var listcomp000007 = pyjslib.List();
		var __line = lines2d.__iter__();
		try {
			while (true) {
				var line = __line.next();
				
				var __temp_x = line.__iter__();
				try {
					while (true) {
						var temp_x = __temp_x.next();
										var x = temp_x.__getitem__(0);				var y = temp_x.__getitem__(1);
						listcomp000007.append(pyjslib.abs(x));
					}
				} catch (e) {
					if (e.__name__ != 'StopIteration') {
						throw e;
					}
				}
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
return listcomp000007;}();
		ys = function(){
var listcomp000008 = pyjslib.List();
		var __line = lines2d.__iter__();
		try {
			while (true) {
				var line = __line.next();
				
				var __temp_x = line.__iter__();
				try {
					while (true) {
						var temp_x = __temp_x.next();
										var x = temp_x.__getitem__(0);				var y = temp_x.__getitem__(1);
						listcomp000008.append(pyjslib.abs(y));
					}
				} catch (e) {
					if (e.__name__ != 'StopIteration') {
						throw e;
					}
				}
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
return listcomp000008;}();
		scale =  ( 0.9 * pyjslib.min( (  ( (typeof self.w == 'function' && self.__is_instance__?pyjslib.getattr(self, 'w'):self.w) / 2 )  / pyjslib.max(xs) ) ,  (  ( (typeof self.h == 'function' && self.__is_instance__?pyjslib.getattr(self, 'h'):self.h) / 2 )  / pyjslib.max(ys) ) ) ) ;
		z_order = function(line) {
			var zs;
			zs = function(){
var listcomp000009 = pyjslib.List();
			var __p = line.__iter__();
			try {
				while (true) {
					var p = __p.next();
					
					listcomp000009.append((typeof p.z_order == 'function' && p.__is_instance__?pyjslib.getattr(p, 'z_order'):p.z_order));
				}
			} catch (e) {
				if (e.__name__ != 'StopIteration') {
					throw e;
				}
			}
return listcomp000009;}();
			return new pyjslib.Tuple([pyjslib.min(zs), pyjslib.max(zs)]);
		};
		z_order.__name__ = 'z_order';

		z_order.__bind_type__ = 0;
		z_order.__args__ = [null,null,'line'];
		pyjs_kwargs_call(lines2d, 'sort', null, null, [{keyFunc:z_order}]);
		context.lineJoin = String('round');
		var __line = lines2d.__iter__();
		try {
			while (true) {
				var line = __line.next();
				
				context.lineWidth = (typeof line.width == 'function' && line.__is_instance__?pyjslib.getattr(line, 'width'):line.width);
				context.lineCap = (typeof line.cap == 'function' && line.__is_instance__?pyjslib.getattr(line, 'cap'):line.cap);
				context.strokeStyle = (typeof line.color == 'function' && line.__is_instance__?pyjslib.getattr(line, 'color'):line.color);
				context.globalCompositeOperation = (typeof line.mode == 'function' && line.__is_instance__?pyjslib.getattr(line, 'mode'):line.mode);
				context.beginPath();
				p0 = line.__getitem__(0);
				context.moveTo( ( p0.__getitem__(0) * scale ) ,  ( p0.__getitem__(1) * scale ) );
				var __p1 = pyjslib.slice(line, 1, null).__iter__();
				try {
					while (true) {
						var p1 = __p1.next();
						
						context.lineTo( ( p1.__getitem__(0) * scale ) ,  ( p1.__getitem__(1) * scale ) );
						p0 = p1;
					}
				} catch (e) {
					if (e.__name__ != 'StopIteration') {
						throw e;
					}
				}
				context.stroke();
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		context.fillStyle = String('black');
		var __p = points.__iter__();
		try {
			while (true) {
				var p = __p.next();
				
				var __tupleassign__000007 = transform(p);
				x = __tupleassign__000007.__getitem__(0);
				y = __tupleassign__000007.__getitem__(1);
				context.beginPath();
				context.arc( ( x * scale ) ,  ( y * scale ) , 5, 0,  ( (typeof huppa.math.pi == 'function' && huppa.math.__is_instance__?pyjslib.getattr(huppa.math, 'pi'):huppa.math.pi) * 2 ) , false);
				context.fill();
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		var __tupleassign__000008 = image;
		x0 = __tupleassign__000008.__getitem__(0);
		y0 = __tupleassign__000008.__getitem__(1);
		x1 = __tupleassign__000008.__getitem__(2);
		y1 = __tupleassign__000008.__getitem__(3);
		img = __tupleassign__000008.__getitem__(4);
		var __tupleassign__000009 = new pyjslib.Tuple([-y1, -y0]);
		y0 = __tupleassign__000009.__getitem__(0);
		y1 = __tupleassign__000009.__getitem__(1);
		context.save();
		context.scale(1, -1);
		try {
			if (pyjslib.bool(img.isLoaded())) {
				context.drawImage(img.getElement(),  ( x0 * scale ) ,  ( y0 * scale ) ,  (  ( x1 - x0 )  * scale ) ,  (  ( y1 - y0 )  * scale ) );
			}
		} catch(pyjs_try_err) {
			var pyjs_try_err_name = (typeof pyjs_try_err.__name__ == 'undefined' ? pyjs_try_err.name : pyjs_try_err.__name__ );
			$pyjs.__last_exception__ = {error: pyjs_try_err, module: huppa, try_lineno: 263};
			if (pyjs_try_err_name == pyjslib.Exception.__name__) {
				$pyjs.__last_exception__.except_lineno = 271;
				e = pyjs_try_err;
			} else { throw pyjs_try_err; }
		}
		context.restore();
		return null;
	}
	, 1, [null,null,'self', 'transform', 'lines', 'points', 'image']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(huppa.Canvas));
})();
huppa.Main = (function(){
	var cls_instance = pyjs__class_instance('Main');
	var cls_definition = new Object();
	cls_definition.__md5__ = 'd4bfb886fb536ffb87f26716c9282ee4';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}
		var box,temp_axis,c,axis;
		huppa.VerticalPanel.__init__(self);
		self.canvas = huppa.LinesCanvas(500, 500);
		self.add((typeof self.canvas == 'function' && self.__is_instance__?pyjslib.getattr(self, 'canvas'):self.canvas));
		self.boxes = new pyjslib.List([]);
		var __temp_axis = huppa.zip(String('xyzw'), new pyjslib.Tuple([0, 1.7, 6, 20])).__iter__();
		try {
			while (true) {
				var temp_axis = __temp_axis.next();
						var axis = temp_axis.__getitem__(0);		var c = temp_axis.__getitem__(1);
				self.add(huppa.Label(pyjslib.sprintf(String('Camera %s:'), axis)));
				box = huppa.TextBox();
				box.setText(c);
				self.boxes.append(box);
				self.add(box);
				box.addKeyboardListener(self);
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		self.camera = null;
		self.huppoid = huppa.Huppoid(new pyjslib.List([new pyjslib.Tuple([1, 1]), new pyjslib.Tuple([2, 1]), new pyjslib.Tuple([3, 1]), new pyjslib.Tuple([0, 1])]));
		self.figures = huppa.CanvasImage(String('figures.png'));
		self.figures.addLoadListener(huppa.DrawOnLoad(self));
		return null;
	}
	, 1, [null,null,'self']);
	cls_definition.draw = pyjs__bind_method(cls_instance, 'draw', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}
		var camera;
		camera = function(){
var listcomp000010 = pyjslib.List();
		var __box = self.boxes.__iter__();
		try {
			while (true) {
				var box = __box.next();
				
				listcomp000010.append(pyjslib.float_(box.getText()));
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
return listcomp000010;}();
		if (pyjslib.bool(!pyjslib.eq(camera, (typeof self.camera == 'function' && self.__is_instance__?pyjslib.getattr(self, 'camera'):self.camera)))) {
			self.camera = camera;
			self.projection = huppa.Project2D(camera);
			self.canvas.draw((typeof self.projection.transform == 'function' && self.projection.__is_instance__?pyjslib.getattr(self.projection, 'transform'):self.projection.transform), (typeof self.huppoid.lines == 'function' && self.huppoid.__is_instance__?pyjslib.getattr(self.huppoid, 'lines'):self.huppoid.lines), (typeof self.huppoid.points == 'function' && self.huppoid.__is_instance__?pyjslib.getattr(self.huppoid, 'points'):self.huppoid.points), new pyjslib.Tuple([-0.8, -1, 0.8, 0.6, (typeof self.figures == 'function' && self.__is_instance__?pyjslib.getattr(self, 'figures'):self.figures)]));
		}
		return null;
	}
	, 1, [null,null,'self']);
	cls_definition.onKeyUp = pyjs__bind_method(cls_instance, 'onKeyUp', function(sender, keyCode, modifiers) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sender = arguments[1];
			keyCode = arguments[2];
			modifiers = arguments[3];
		}

		self.draw();
		return null;
	}
	, 1, [null,null,'self', 'sender', 'keyCode', 'modifiers']);
	cls_definition.onKeyDown = pyjs__bind_method(cls_instance, 'onKeyDown', function(sender, keyCode, modifiers) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sender = arguments[1];
			keyCode = arguments[2];
			modifiers = arguments[3];
		}

 		return null;
	}
	, 1, [null,null,'self', 'sender', 'keyCode', 'modifiers']);
	cls_definition.onKeyPress = pyjs__bind_method(cls_instance, 'onKeyPress', function(sender, keyCode, modifiers) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sender = arguments[1];
			keyCode = arguments[2];
			modifiers = arguments[3];
		}

 		return null;
	}
	, 1, [null,null,'self', 'sender', 'keyCode', 'modifiers']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(huppa.VerticalPanel));
})();
huppa.DrawOnLoad = (function(){
	var cls_instance = pyjs__class_instance('DrawOnLoad');
	var cls_definition = new Object();
	cls_definition.__md5__ = '4c572ccc9518339259fb8cfa699d0963';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(obj) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			obj = arguments[1];
		}

		self.obj = obj;
		return null;
	}
	, 1, [null,null,'self', 'obj']);
	cls_definition.onLoad = pyjs__bind_method(cls_instance, 'onLoad', function(x) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			x = arguments[1];
		}

		self.obj.draw();
		return null;
	}
	, 1, [null,null,'self', 'x']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjslib.object));
})();
if (pyjslib.bool(pyjslib.eq(huppa.__name__, String('__main__')))) {
	huppa.pyjd.setup(String('./output/huppa.html'));
	huppa.RootPanel().add(huppa.Main());
	huppa.pyjd.run();
}
return this;
}; /* end huppa */
$pyjs.modules_hash['huppa'] = $pyjs.loaded_modules['huppa'];


 /* end module: huppa */


/*
PYJS_DEPS: ['pyjd', 'math', 'pyjamas.Window', 'pyjamas', 'pyjamas.ui.RootPanel.RootPanel', 'pyjamas.ui', 'pyjamas.ui.RootPanel', 'pyjamas.Canvas2D.Canvas', 'pyjamas.Canvas2D', 'pyjamas.Canvas2D.CanvasImage', 'pyjamas.ui.Label.Label', 'pyjamas.ui.Label', 'pyjamas.ui.TextBox.TextBox', 'pyjamas.ui.TextBox', 'pyjamas.ui.VerticalPanel.VerticalPanel', 'pyjamas.ui.VerticalPanel', 'pyjamas.ui.Button.Button', 'pyjamas.ui.Button']
*/
