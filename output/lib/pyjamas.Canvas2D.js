/* start module: pyjamas.Canvas2D */
pyjamas.Canvas2D = $pyjs.loaded_modules["pyjamas.Canvas2D"] = function (__mod_name__) {
if(pyjamas.Canvas2D.__was_initialized__) return pyjamas.Canvas2D;
pyjamas.Canvas2D.__was_initialized__ = true;
if (__mod_name__ == null) __mod_name__ = 'pyjamas.Canvas2D';
var __name__ = pyjamas.Canvas2D.__name__ = __mod_name__;
var Canvas2D = pyjamas.Canvas2D;

 pyjslib.__import__(['pyjamas.pyjamas.DOM', 'pyjamas.pyjamas', 'pyjamas.DOM', 'pyjamas'], 'pyjamas.DOM', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.DOM = $pyjs.__modules__.pyjamas.DOM;
 pyjslib.__import__(['pyjamas.pyjamas.ui.Image.Image', 'pyjamas.pyjamas.ui.Image', 'pyjamas.ui.Image.Image', 'pyjamas.ui.Image'], 'pyjamas.ui.Image.Image', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.Image = $pyjs.__modules__.pyjamas.ui.Image.Image;
 pyjslib.__import__(['pyjamas.pyjamas.ui.Widget.Widget', 'pyjamas.pyjamas.ui.Widget', 'pyjamas.ui.Widget.Widget', 'pyjamas.ui.Widget'], 'pyjamas.ui.Widget.Widget', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.Widget = $pyjs.__modules__.pyjamas.ui.Widget.Widget;
 pyjslib.__import__(['pyjamas.pyjamas.ui.Event', 'pyjamas.pyjamas.ui', 'pyjamas.ui.Event', 'pyjamas.ui'], 'pyjamas.ui.Event', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.Event = $pyjs.__modules__.pyjamas.ui.Event;
 pyjslib.__import__(['pyjamas.pyjamas.ui.MouseListener', 'pyjamas.pyjamas.ui', 'pyjamas.ui.MouseListener', 'pyjamas.ui'], 'pyjamas.ui.MouseListener', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.MouseListener = $pyjs.__modules__.pyjamas.ui.MouseListener;
 pyjslib.__import__(['pyjamas.pyjamas.ui.KeyboardListener', 'pyjamas.pyjamas.ui', 'pyjamas.ui.KeyboardListener', 'pyjamas.ui'], 'pyjamas.ui.KeyboardListener', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.KeyboardListener = $pyjs.__modules__.pyjamas.ui.KeyboardListener;
 pyjslib.__import__(['pyjamas.pyjamas.ui.Focus', 'pyjamas.pyjamas.ui', 'pyjamas.ui.Focus', 'pyjamas.ui'], 'pyjamas.ui.Focus', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.Focus = $pyjs.__modules__.pyjamas.ui.Focus;
 pyjslib.__import__(['pyjamas.pyjamas.ui.FocusListener', 'pyjamas.pyjamas.ui', 'pyjamas.ui.FocusListener', 'pyjamas.ui'], 'pyjamas.ui.FocusListener', 'pyjamas.Canvas2D');
 pyjamas.Canvas2D.FocusListener = $pyjs.__modules__.pyjamas.ui.FocusListener;
pyjamas.Canvas2D.Canvas = (function(){
	var cls_instance = pyjs__class_instance('Canvas');
	var cls_definition = new Object();
	cls_definition.__md5__ = 'c7326af7a3275c69f4a48de353cbb852';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(width, height) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			width = arguments[1];
			height = arguments[2];
		}
		var canvas;
		pyjamas.Canvas2D.Widget.__init__(self);
		self.context = null;
		self.setElement(pyjamas.Canvas2D.DOM.createDiv());
		canvas = pyjamas.Canvas2D.DOM.createElement(String('canvas'));
		self.setWidth(width);
		self.setHeight(height);
		canvas.width = width;
		canvas.height = height;
		pyjamas.Canvas2D.DOM.appendChild(self.getElement(), canvas);
		self.setStyleName(String('gwt-Canvas'));
		self.init();
		self.context.fillStyle = String('black');
		self.context.strokeStyle = String('black');
		self.focusable = null;
		self.focusable = pyjamas.Canvas2D.Focus.createFocusable();
		self.focusListeners = new pyjslib.List([]);
		self.clickListeners = new pyjslib.List([]);
		self.mouseListeners = new pyjslib.List([]);
		self.keyboardListeners = new pyjslib.List([]);
		pyjamas.Canvas2D.DOM.appendChild(self.getElement(), (typeof self.focusable == 'function' && self.__is_instance__?pyjslib.getattr(self, 'focusable'):self.focusable));
		pyjamas.Canvas2D.DOM.sinkEvents(canvas, (((typeof pyjamas.Canvas2D.Event.ONCLICK == 'function' && pyjamas.Canvas2D.Event.__is_instance__?pyjslib.getattr(pyjamas.Canvas2D.Event, 'ONCLICK'):pyjamas.Canvas2D.Event.ONCLICK) | (typeof pyjamas.Canvas2D.Event.MOUSEEVENTS == 'function' && pyjamas.Canvas2D.Event.__is_instance__?pyjslib.getattr(pyjamas.Canvas2D.Event, 'MOUSEEVENTS'):pyjamas.Canvas2D.Event.MOUSEEVENTS) | pyjamas.Canvas2D.DOM.getEventsSunk(canvas))));
		pyjamas.Canvas2D.DOM.sinkEvents((typeof self.focusable == 'function' && self.__is_instance__?pyjslib.getattr(self, 'focusable'):self.focusable), (((typeof pyjamas.Canvas2D.Event.FOCUSEVENTS == 'function' && pyjamas.Canvas2D.Event.__is_instance__?pyjslib.getattr(pyjamas.Canvas2D.Event, 'FOCUSEVENTS'):pyjamas.Canvas2D.Event.FOCUSEVENTS) | (typeof pyjamas.Canvas2D.Event.KEYEVENTS == 'function' && pyjamas.Canvas2D.Event.__is_instance__?pyjslib.getattr(pyjamas.Canvas2D.Event, 'KEYEVENTS'):pyjamas.Canvas2D.Event.KEYEVENTS))));
		return null;
	}
	, 1, [null,null,'self', 'width', 'height']);
	cls_definition.addClickListener = pyjs__bind_method(cls_instance, 'addClickListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.clickListeners.append(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.addMouseListener = pyjs__bind_method(cls_instance, 'addMouseListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.mouseListeners.append(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.addFocusListener = pyjs__bind_method(cls_instance, 'addFocusListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.focusListeners.append(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.addKeyboardListener = pyjs__bind_method(cls_instance, 'addKeyboardListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.keyboardListeners.append(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.onBrowserEvent = pyjs__bind_method(cls_instance, 'onBrowserEvent', function(event) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			event = arguments[1];
		}
		var listener,type;
		type = pyjamas.Canvas2D.DOM.eventGetType(event);
		if (pyjslib.bool(pyjslib.eq(type, String('click')))) {
			var __listener = self.clickListeners.__iter__();
			try {
				while (true) {
					var listener = __listener.next();
					
					if (pyjslib.bool(pyjslib.hasattr(listener, String('onClick')))) {
						listener.onClick(self);
					}
					else {
						listener(self, event);
					}
				}
			} catch (e) {
				if (e.__name__ != 'StopIteration') {
					throw e;
				}
			}
		}
		else if (pyjslib.bool((pyjslib.eq(type, String('blur'))) || (pyjslib.eq(type, String('focus'))))) {
			pyjamas.Canvas2D.FocusListener.fireFocusEvent((typeof self.focusListeners == 'function' && self.__is_instance__?pyjslib.getattr(self, 'focusListeners'):self.focusListeners), self, event);
		}
		else if (pyjslib.bool((pyjslib.eq(type, String('keydown'))) || (pyjslib.eq(type, String('keypress'))) || (pyjslib.eq(type, String('keyup'))))) {
			pyjamas.Canvas2D.MouseListener.fireMouseEvent((typeof self.mouseListeners == 'function' && self.__is_instance__?pyjslib.getattr(self, 'mouseListeners'):self.mouseListeners), self, event);
		}
		return null;
	}
	, 1, [null,null,'self', 'event']);
	cls_definition.removeClickListener = pyjs__bind_method(cls_instance, 'removeClickListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.clickListeners.remove(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.removeMouseListener = pyjs__bind_method(cls_instance, 'removeMouseListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.mouseListeners.remove(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.removeFocusListener = pyjs__bind_method(cls_instance, 'removeFocusListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.focusListeners.remove(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.removeKeyboardListener = pyjs__bind_method(cls_instance, 'removeKeyboardListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.keyboardListeners.remove(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.setFocus = pyjs__bind_method(cls_instance, 'setFocus', function(focused) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			focused = arguments[1];
		}

		if (pyjslib.bool(focused)) {
			pyjamas.Canvas2D.Focus.focus((typeof self.focusable == 'function' && self.__is_instance__?pyjslib.getattr(self, 'focusable'):self.focusable));
		}
		else {
			pyjamas.Canvas2D.Focus.blur((typeof self.focusable == 'function' && self.__is_instance__?pyjslib.getattr(self, 'focusable'):self.focusable));
		}
		return null;
	}
	, 1, [null,null,'self', 'focused']);
	cls_definition.getContext = pyjs__bind_method(cls_instance, 'getContext', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}

		return (typeof self.context == 'function' && self.__is_instance__?pyjslib.getattr(self, 'context'):self.context);
	}
	, 1, [null,null,'self']);
	cls_definition.isEmulation = pyjs__bind_method(cls_instance, 'isEmulation', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}

		return false;
	}
	, 1, [null,null,'self']);
	cls_definition.init = pyjs__bind_method(cls_instance, 'init', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}
		var el,ctx;
		el = (typeof self.getElement().firstChild == 'function' && self.getElement().__is_instance__?pyjslib.getattr(self.getElement(), 'firstChild'):self.getElement().firstChild);
		ctx = el.getContext(String('2d'));
		self.context = ctx;
		return null;
	}
	, 1, [null,null,'self']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjamas.Canvas2D.Widget));
})();
pyjamas.Canvas2D.CanvasImage = (function(){
	var cls_instance = pyjs__class_instance('CanvasImage');
	var cls_definition = new Object();
	cls_definition.__md5__ = '407abd05200f69648ef755cc18a94efe';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(url, load_listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			url = arguments[1];
			load_listener = arguments[2];
		}
		if (typeof url == 'undefined') url=String('');
		if (typeof load_listener == 'undefined') load_listener=null;

		pyjamas.Canvas2D.Image.__init__(self, url);
		if (pyjslib.bool(load_listener)) {
			self.addLoadListener(load_listener);
		}
		self.onAttach();
		return null;
	}
	, 1, [null,null,'self', 'url', 'load_listener']);
	cls_definition.isLoaded = pyjs__bind_method(cls_instance, 'isLoaded', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}

		return (typeof self.getElement().complete == 'function' && self.getElement().__is_instance__?pyjslib.getattr(self.getElement(), 'complete'):self.getElement().complete);
	}
	, 1, [null,null,'self']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjamas.Canvas2D.Image));
})();
pyjamas.Canvas2D.ImageLoadListener = (function(){
	var cls_instance = pyjs__class_instance('ImageLoadListener');
	var cls_definition = new Object();
	cls_definition.__md5__ = '9840ff102282037c5e0fa45c09bdc11f';
	cls_definition.__init__ = pyjs__bind_method(cls_instance, '__init__', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}
		if (typeof listener == 'undefined') listener=null;

		self.wait_list = new pyjslib.List([]);
		self.loadListeners = new pyjslib.List([]);
		if (pyjslib.bool(listener)) {
			self.addLoadListener(listener);
		}
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.add = pyjs__bind_method(cls_instance, 'add', function(sender) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sender = arguments[1];
		}

		self.wait_list.append(sender);
		sender.addLoadListener(self);
		return null;
	}
	, 1, [null,null,'self', 'sender']);
	cls_definition.addLoadListener = pyjs__bind_method(cls_instance, 'addLoadListener', function(listener) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			listener = arguments[1];
		}

		self.loadListeners.append(listener);
		return null;
	}
	, 1, [null,null,'self', 'listener']);
	cls_definition.isLoaded = pyjs__bind_method(cls_instance, 'isLoaded', function() {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
		}

		if (pyjslib.bool(pyjslib.len((typeof self.wait_list == 'function' && self.__is_instance__?pyjslib.getattr(self, 'wait_list'):self.wait_list)))) {
			return false;
		}
		return true;
	}
	, 1, [null,null,'self']);
	cls_definition.onError = pyjs__bind_method(cls_instance, 'onError', function(sender) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sender = arguments[1];
		}
		var listener;
		var __listener = self.loadListeners.__iter__();
		try {
			while (true) {
				var listener = __listener.next();
				
				listener.onError(sender);
			}
		} catch (e) {
			if (e.__name__ != 'StopIteration') {
				throw e;
			}
		}
		return null;
	}
	, 1, [null,null,'self', 'sender']);
	cls_definition.onLoad = pyjs__bind_method(cls_instance, 'onLoad', function(sender) {
		if (this.__is_instance__ === true) {
			var self = this;
		} else {
			var self = arguments[0];
			sender = arguments[1];
		}
		var listener;
		self.wait_list.remove(sender);
		if (pyjslib.bool(self.isLoaded())) {
			var __listener = self.loadListeners.__iter__();
			try {
				while (true) {
					var listener = __listener.next();
					
					listener.onLoad(self);
				}
			} catch (e) {
				if (e.__name__ != 'StopIteration') {
					throw e;
				}
			}
		}
		return null;
	}
	, 1, [null,null,'self', 'sender']);
	return pyjs__class_function(cls_instance, cls_definition, 
	                            new Array(pyjslib.object));
})();
return this;
}; /* end pyjamas.Canvas2D */
$pyjs.modules_hash['pyjamas.Canvas2D'] = $pyjs.loaded_modules['pyjamas.Canvas2D'];


 /* end module: pyjamas.Canvas2D */


/*
PYJS_DEPS: ['pyjamas.DOM', 'pyjamas', 'pyjamas.ui.Image.Image', 'pyjamas.ui', 'pyjamas.ui.Image', 'pyjamas.ui.Widget.Widget', 'pyjamas.ui.Widget', 'pyjamas.ui.Event', 'pyjamas.ui.MouseListener', 'pyjamas.ui.KeyboardListener', 'pyjamas.ui.Focus', 'pyjamas.ui.FocusListener']
*/
