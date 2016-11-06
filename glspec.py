import sqlite3
import sys
import os

if len(sys.argv) < 2:
	print 'Missing argument DB_NAME'
	exit(1)

if os.path.isfile(sys.argv[1]):
	os.system('rm %s' % sys.argv[1])

conn = sqlite3.connect(sys.argv[1])

c = conn.cursor()

r = c.execute('''
	CREATE TABLE functions
	(
		func_id INT PRIMARY KEY NOT NULL,
		func_name TEXT NOT NULL,
		func_type TEXT NOT NULL
	)
''')

c.execute('''
	CREATE TABLE arguments
	(
		arg_id INT PRIMARY KEY NOT NULL,
		func_id INT NOT NULL,
		arg_order INT NOT NULL,
		arg_name TEXT NOT NULL,
		arg_type TEXT NOT NULL,
		FOREIGN KEY (func_id) REFERENCES functions(func_id)
	)
''')

c.execute('''
	CREATE TABLE versions
	(
		version_id INT PRIMARY KEY NOT NULL,
		major_version INT NOT NULL,
		minor_version INT NOT NULL
	)
''')

c.execute('''
	CREATE TABLE function_availabilities
	(
		availability_id INT PRIMARY KEY NOT NULL,
		func_id INT,
		version_id INT,
		FOREIGN KEY (func_id) REFERENCES functions(func_id),
		FOREIGN KEY (version_id) REFERENCES versions(version_id)
	)
''')

class GlVersion:
	def __init__(self, major, minor):
		global c

		c.execute('''
			INSERT INTO versions
			VALUES ((SELECT count(*) FROM versions), %d, %d)
		''' % (major, minor))

		c.execute('''
			SELECT count(*) - 1 FROM versions
		''')

		self.version_id, = c.fetchone()

		self.major = major
		self.minor = minor

class GlArg:
	def __init__(self, name, c_type):
		self.name = name
		self.c_type = c_type

class GlApi:
	def __init__(self, name, return_type, args):
		global c

		c.execute('''
			INSERT INTO functions
			VALUES ((SELECT count(*) FROM functions), '%s', '%s')
		''' % (name, return_type))

		c.execute('''
			SELECT count(*) - 1 FROM functions
		''')

		self.func_id, = c.fetchone()

		arg_order = 0

		for arg in args:
			c.execute('''
				INSERT INTO arguments
				VALUES
				(
					(SELECT count(*) FROM arguments),
					(SELECT count(*) FROM functions) - 1,
					%d,
					'%s',
					'%s'
				)
			''' % (arg_order, arg.name, arg.c_type))

			c.execute('''
				SELECT count(*) - 1 FROM arguments
			''')

			arg.arg_id, = c.fetchone()

			arg_order += 1

		self.args = args

class GlAvailability:
	def __init__(self, func, version):
		self.func = func
		self.version = version

		c.execute('''
			INSERT INTO function_availabilities
			VALUES
			(
				(SELECT count(*) FROM function_availabilities),
				%d,
				%d
			)
		''' % (func.func_id, version.version_id))

		c.execute('''
			SELECT count(*) - 1 FROM function_availabilities
		''')

		self.availability_id, = c.fetchone()

glv_1_0 = GlVersion(1, 0)
glv_1_1 = GlVersion(1, 1)
glv_1_2 = GlVersion(1, 2)
glv_1_3 = GlVersion(1, 3)
glv_1_4 = GlVersion(1, 4)
glv_1_5 = GlVersion(1, 5)
glv_2_0 = GlVersion(2, 0)
glv_2_1 = GlVersion(2, 1)
glv_3_0 = GlVersion(3, 0)
glv_3_1 = GlVersion(3, 1)
glv_3_2 = GlVersion(3, 2)
glv_3_3 = GlVersion(3, 3)
glv_4_0 = GlVersion(4, 0)
glv_4_1 = GlVersion(4, 1)
glv_4_2 = GlVersion(4, 2)
glv_4_3 = GlVersion(4, 3)
glv_4_4 = GlVersion(4, 4)
glv_4_5 = GlVersion(4, 5)

glActiveShaderProgram = GlApi('glActiveShaderProgram', 'void', [
	GlArg('pipeline', 'GLuint'),
	GlArg('program', 'GLuint')
])

GlAvailability(glActiveShaderProgram, glv_4_1)
GlAvailability(glActiveShaderProgram, glv_4_2)
GlAvailability(glActiveShaderProgram, glv_4_3)
GlAvailability(glActiveShaderProgram, glv_4_4)
GlAvailability(glActiveShaderProgram, glv_4_5)

glActiveTexture = GlApi('glActiveTexture', 'void', [
	GlArg('texture', 'GLenum')
])

glAttachShader = GlApi('glAttachShader', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shader', 'GLuint')
])

glBeginConditionalRender = GlApi('glBeginConditionalRender', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('mode', 'GLenum')
])

glEndConditionalRender = GlApi('glEndConditionalRender', 'void', [])

glBeginQuery = GlApi('glBeginQuery', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('id', 'GLuint')
])

glEndQuery = GlApi('glEndQuery', 'void', [
	GlArg('target', 'GLenum')
])

glBeginQueryIndexed = GlApi('glBeginQueryIndexed', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('id', 'GLuint')
])

glEndQueryIndexed = GlApi('glEndQueryIndexed', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint')
])

glBeginTransformFeedback = GlApi('glBeginTransformFeedback', 'void', [
	GlArg('primitiveMode', 'GLenum')
])

glEndTransformFeedback = GlApi('glEndTransformFeedback', 'void', [])

glBindAttribLocation = GlApi('glBindAttribLocation', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('name', 'const GLchar *')
])

glBindBuffer = GlApi('glBindBuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('buffer', 'GLuint')
])

glBindBufferBase = GlApi('glBindBufferBase', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('buffer', 'GLuint')
])

glBindBufferRange = GlApi('glBindBufferRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('buffer', 'GLuint'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr')
])

glBindBuffersBase = GlApi('glBindBuffersBase', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('buffers', 'const GLuint *')
])

glBindBuffersRange = GlApi('glBindBuffersRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('buffers', 'const GLuint *'),
	GlArg('offsets', 'const GLintptr *'),
	GlArg('sizes', 'const GLintptr *')
])

glBindFragDataLocation = GlApi('glBindFragDataLocation', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('colorNumber', 'GLuint'),
	GlArg('name', 'const char *')
])

glBindFragDataLocationIndexed = GlApi('glBindFragDataLocationIndexed', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('colorNumber', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('name', 'const char *')
])

glBindFramebuffer = GlApi('glBindFramebuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('framebuffer', 'GLuint')
])

glBindImageTexture = GlApi('glBindImageTexture', 'void', [
	GlArg('unit', 'GLuint'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('GLboolean', 'layered'),
	GlArg('layer', 'GLint'),
	GlArg('access', 'GLenum'),
	GlArg('format', 'GLenum')
])

glBindImageTextures = GlApi('glBindImageTextures', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('textures', 'const GLuint *')
])

glBindProgramPipeline = GlApi('glBindProgramPipeline', 'void', [
	GlArg('pipeline', 'GLuint')
])

glBindRenderbuffer = GlApi('glBindRenderbuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('renderbuffer', 'GLuint')
])

glBindSampler = GlApi('glBindSampler', 'void', [
	GlArg('unit', 'GLuint'),
	GlArg('sampler', 'GLuint')
])

glBindSamplers = GlApi('glBindSamplers', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('samplers', 'const GLuint *')
])

glBindTexture = GlApi('glBindTexture', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('texture', 'GLuint')
])

glBindTextures = GlApi('glBindTextures', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('textures', 'const GLuint *')
])

glBindTransformFeedback = GlApi('glBindTransformFeedback', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('id', 'GLuint')
])

glBindVertexArray = GlApi('glBindVertexArray', 'void', [
	GlArg('array', 'GLuint')
])

glBindVertexBuffer = GlApi('glBindVertexBuffer', 'void', [
	GlArg('bindingindex', 'GLuint'),
	GlArg('buffer', 'GLuint'),
	GlArg('offset', 'GLintptr'),
	GlArg('stride', 'GLintptr')
])

glBlendColor = GlApi('glBlendColor', 'void', [
	GlArg('red', 'GLfloat'),
	GlArg('green', 'GLfloat'),
	GlArg('blue', 'GLfloat'),
	GlArg('alpha', 'GLfloat')
])

glBlendEquation = GlApi('glBlendEquation', 'void', [
	GlArg('mode', 'GLenum')
])

glBlendEquationi = GlApi('glBlendEquationi', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('mode', 'GLenum')
])

glBlendEquationSeparate = GlApi('glBlendEquationSeparate', 'void', [
	GlArg('modeRGB', 'GLenum'),
	GlArg('modeAlpha', 'GLenum')
])

glBlendEquationSeparatei = GlApi('glBlendEquationSeparatei', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('modeRGB', 'GLenum'),
	GlArg('modeAlpha', 'GLenum')
])

glBlendFunc = GlApi('glBlendFunc', 'void', [
	GlArg('sfactor', 'GLenum'),
	GlArg('dfactor', 'GLenum')
])

glBlendFunci = GlApi('glBlendFunci', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('sfactor', 'GLenum'),
	GlArg('dfactor', 'GLenum')
])

glBlendFuncSeparate = GlApi('glBlendFuncSeparate', 'void', [
	GlArg('srcRGB', 'GLenum'),
	GlArg('dstRGB', 'GLenum'),
	GlArg('srcAlpha', 'GLenum'),
	GlArg('dstAlpha', 'GLenum')
])

glBlendFuncSeparatei = GlApi('glBlendFuncSeparatei', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('srcRGB', 'GLenum'),
	GlArg('dstRGB', 'GLenum'),
	GlArg('srcAlpha', 'GLenum'),
	GlArg('dstAlpha', 'GLenum')
])

glBlitFramebuffer = GlApi('glBlitFramebuffer', 'void', [
	GlArg('srcX0', 'GLint'),
	GlArg('srcY0', 'GLint'),
	GlArg('srcX1', 'GLint'),
	GlArg('srcY1', 'GLint'),
	GlArg('dstX0', 'GLint'),
	GlArg('dstY0', 'GLint'),
	GlArg('dstX1', 'GLint'),
	GlArg('dstY1', 'GLint'),
	GlArg('mask', 'GLbitfield'),
	GlArg('filter', 'GLenum')
])

glBufferData = GlApi('glBufferData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('ize', 'GLsizeiptr'),
	GlArg('data', 'const GLvoid *'),
	GlArg('usage', 'GLenum')
])

glBufferStorage = GlApi('glBufferStorage', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('data', 'const GLvoid *'),
	GlArg('flags', 'GLbitfield')
])

glBufferSubData = GlApi('glBufferSubData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('data', 'const GLvoid *')
])

glCheckFramebufferStatus = GlApi('glCheckFramebufferStatus', 'GLenum', [
	GlArg('target', 'GLenum')
])

glClampColor = GlApi('glClampColor', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('clamp', 'GLenum')
])

glClear = GlApi('glClear', 'void', [
	GlArg('mask', 'GLbitfield')
])

glClearBufferiv = GlApi('glClearBufferiv', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('value', 'const GLint *')
])

glClearBufferuiv = GlApi('glClearBufferuiv', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('value', 'const GLuint *')
])

glClearBufferfv = GlApi('glClearBufferfv', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('value', 'const GLfloat *')
])

glClearBufferfi = GlApi('glClearBufferfi', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('depth', 'GLfloat'),
	GlArg('stencil', 'GLint')
])

glClearBufferData = GlApi('glClearBufferData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

glClearBufferSubData = GlApi('glClearBufferSubData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

glClearColor = GlApi('glClearColor', 'void', [
	GlArg('red', 'GLfloat'),
	GlArg('green', 'GLfloat'),
	GlArg('blue', 'GLfloat'),
	GlArg('alpha', 'GLfloat')
])

glClearDepth = GlApi('glClearDepth', 'void', [
	GlArg('depth', 'GLdouble')
])

glClearDepthf = GlApi('glClearDepthf', 'void', [
	GlArg('depth', 'GLfloat')
])

glClearStencil = GlApi('glClearStencil', 'void', [
	GlArg('s', 'GLint')
])

glClearTexImage = GlApi('glClearTexImage', 'void', [
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

glClearTexSubImage = GlApi('glClearTexSubImage', 'void', [
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('zoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

glClientWaitSync = GlApi('glClientWaitSync', 'GLenum', [
	GlArg('sync', 'GLsync'),
	GlArg('flags', 'GLbitfield'),
	GlArg('timeout', 'GLuint64')
])

glColorMask = GlApi('glColorMask', 'void', [
	GlArg('red', 'GLboolean'),
	GlArg('green', 'GLboolean'),
	GlArg('blue', 'GLboolean'),
	GlArg('alpha', 'GLboolean')
])

glColorMaski = GlApi('glColorMaski', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('red', 'GLboolean'),
	GlArg('green', 'GLboolean'),
	GlArg('blue', 'GLboolean'),
	GlArg('alpha', 'GLboolean')
])

glCompileShader = GlApi('glCompileShader', 'void', [
	GlArg('shader', 'GLuint')
])

GlApi('glCompressedTexImage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('border', 'GLint'),
	GlArg('imageSize', 'GLsizei'),
	GlArg('data', 'const GLvoid *')
])

GlApi('glCompressedTexImage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('border', 'GLint'),
	GlArg('imageSize', 'GLsizei'),
	GlArg('data', 'const GLvoid *')
])

GlApi('glCompressedTexImage3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('border', 'GLint'),
	GlArg('imageSize', 'GLsizei'),
	GlArg('data', 'const GLvoid *')
])

GlApi('glCompressedTexSubImage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('imageSize', 'GLsizei'),
	GlArg('data', 'const GLvoid *')
])

GlApi('glCompressedTexSubImage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('imageSize', 'GLsizei'),
	GlArg('data', 'const GLvoid *')
])

GlApi('glCompressedTexSubImage3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('zoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('imageSize', 'GLsizei'),
	GlArg('data', 'const GLvoid *')
])

glCopyBufferSubData = GlApi('glCopyBufferSubData', 'void', [
	GlArg('readtarget', 'GLenum'),
	GlArg('writetarget', 'GLenum'),
	GlArg('readoffset', 'GLintptr'),
	GlArg('writeoffset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr')
])

glCopyImageSubData = GlApi('glCopyImageSubData', 'void', [
	GlArg('srcName', 'GLuint'),
	GlArg('srcTarget', 'GLenum'),
	GlArg('srcLevel', 'GLint'),
	GlArg('srcX', 'GLint'),
	GlArg('srcY', 'GLint'),
	GlArg('srcZ', 'GLint'),
	GlArg('dstName', 'GLuint'),
	GlArg('dstTarget', 'GLenum'),
	GlArg('dstLevel', 'GLint'),
	GlArg('dstX', 'GLint'),
	GlArg('dstY', 'GLint'),
	GlArg('dstZ', 'GLint'),
	GlArg('srcWidth', 'GLsizei'),
	GlArg('srcHeight', 'GLsizei'),
	GlArg('srcDepth', 'GLsizei')
])

GlApi('glCopyTexImage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalformat', 'GLenum'),
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('border', 'GLint')
])

GlApi('glCopyTexImage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalformat', 'GLenum'),
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('border', 'GLint')
])

GlApi('glCopyTexSubImage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei')
])

GlApi('glCopyTexSubImage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

GlApi('glCopyTexSubImage3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('zoffset', 'GLint'),
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glBindVertexBuffers = GlApi('glBindVertexBuffers', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('buffers', 'const GLuint *'),
	GlArg('offsets', 'const GLintptr *'),
	GlArg('strides', 'const GLsizei *')
])

glCreateProgram = GlApi('glCreateProgram', 'GLuint', [])

glCreateShaders = GlApi('glCreateShaders', 'GLuint', [
	GlArg('shaderType', 'GLenum')
])

glCreateShaderProgramv = GlApi('glCreateShaderProgramv', 'GLuint', [
	GlArg('type', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('strings', 'const char **')
])

glCullFace = GlApi('glCullFace', 'void', [
	GlArg('mode', 'GLenum')
])

glDebugMessageCallback = GlApi('glDebugMessageCallback', 'void', [
	GlArg('callback', 'DEBUGPROC'),
	GlArg('userParam', 'void *')
])

glDebugMessageControl = GlApi('glDebugMessageControl', 'void', [
	GlArg('source', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('severity', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('ids', 'const GLuint *'),
	GlArg('enabled', 'GLboolean')
])

glDebugMessageInsert = GlApi('glDebugMessageInsert', 'void', [
	GlArg('source', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('severity', 'GLenum'),
	GlArg('length', 'GLsizei'),
	GlArg('message', 'const char *')
])

glDeleteBuffers = GlApi('glDeleteBuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('buffers', 'const GLuint *')
])

glDeleteFramebuffers = GlApi('glDeleteFramebuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('framebuffers', 'GLuint *')
])

glDeleteProgram = GlApi('glDeleteProgram', 'void', [
	GlArg('program', 'GLuint')
])

glDeleteProgramPipelines = GlApi('glDeleteProgramPipelines', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('pipelines', 'const GLuint *')
])

glDeleteQueries = GlApi('glDeleteQueries', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'const GLuint *')
])

glDeleteRenderbuffers = GlApi('glDeleteRenderbuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('renderbuffers', 'GLuint *')
])

glDeleteSamplers = GlApi('glDeleteSamplers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('samplers', 'const GLuint *')
])

glDeleteShader = GlApi('glDeleteShader', 'void', [
	GlArg('shader', 'GLuint')
])

glDeleteSync = GlApi('glDeleteSync', 'void', [
	GlArg('sync', 'GLsync')
])

glDeleteTextures = GlApi('glDeleteTextures', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('textures', 'const GLuint *')
])

glDeleteTransformFeedbacks = GlApi('glDeleteTransformFeedbacks', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'const GLuint *')
])

glDeleteVertexArrays = GlApi('glDeleteVertexArrays', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('arrays', 'const GLuint *')
])

glDepthFunc = GlApi('glDepthFunc', 'void', [
	GlArg('func', 'GLenum')
])

glDepthMask = GlApi('glDepthMask', 'void', [
	GlArg('flag', 'GLboolean')
])

glDepthRange = GlApi('glDepthRange', 'void', [
	GlArg('nearVal', 'GLdouble'),
	GlArg('farVal', 'GLdouble')
])

glDepthRangef = GlApi('glDepthRangef', 'void', [
	GlArg('nearVal', 'GLfloat'),
	GlArg('farVal', 'GLfloat')
])

glDepthRangeArrayv = GlApi('glDepthRangeArrayv', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('v', 'const GLdouble *')
])

glDepthRangeIndexed = GlApi('glDepthRangeIndexed', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('nearVal', 'GLdouble'),
	GlArg('farVal', 'GLdouble')
])

glDetatchShader = GlApi('glDetatchShader', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shader', 'GLuint')
])

glEnable = GlApi('glEnable', 'void', [
	GlArg('cap', 'GLenum')
])

glDisable = GlApi('glDisable', 'void', [
	GlArg('cap', 'GLenum')
])

glEnablei = GlApi('glEnablei', 'void', [
	GlArg('cap', 'GLenum'),
	GlArg('index', 'GLuint')
])

glDisablei = GlApi('glDisablei', 'void', [
	GlArg('cap', 'GLenum'),
	GlArg('index', 'GLuint')
])

glEnableVertexAttribArray = GlApi('glEnableVertexAttribArray', 'void', [
	GlArg('index', 'GLuint')
])

glDisableVertexAttribArray = GlApi('glDisableVertexAttribArray', 'void', [
	GlArg('index', 'GLuint')
])

glDispatchCompute = GlApi('glDispatchCompute', 'void', [
	GlArg('num_groups_x', 'GLuint'),
	GlArg('num_groups_y', 'GLuint'),
	GlArg('num_groups_z', 'GLuint')
])

glDispatchComputeIndirect = GlApi('glDispatchComputeIndirect', 'void', [
	GlArg('indirect', 'GLintptr')
])

glDrawArrays = GlApi('glDrawArrays', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'GLint'),
	GlArg('count', 'GLsizei')
])

glDrawArraysIndirect = GlApi('glDrawArraysIndirect', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('indirect', 'const void *')
])

glDrawArraysInstanced = GlApi('glDrawArraysInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('primcount', 'GLsizei')
])

glDrawArraysInstancedBaseInstance = GlApi('glDrawArraysInstancedBaseInstance', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('primcount', 'GLsizei'),
	GlArg('baseinstance', 'GLuint')
])

glDrawBuffer = GlApi('glDrawBuffer', 'void', [
	GlArg('mode', 'GLenum')
])

glDrawBuffers = GlApi('glDrawBuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('bufs', 'const GLenum *')
])

glDrawElements = GlApi('glDrawElements', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const GLvoid *')
])

glDrawElementsBaseVertex = GlApi('glDrawElementsBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('basevertex', 'GLint')
])

glDrawElementsIndirect = GlApi('glDrawElementsIndirect', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('indirect', 'const void *')
])

glDrawElementsInstanced = GlApi('glDrawElementsInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const void *'),
	GlArg('primcount', 'GLsizei')
])

glDrawElementsInstancedBaseInstance = GlApi('glDrawElementsInstancedBaseInstance', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const void *'),
	GlArg('primcount', 'GLsizei'),
	GlArg('baseinstance', 'GLuint')
])

glDrawElementsInstancedBaseVertex = GlApi('glDrawElementsInstancedBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('primcount', 'GLsizei'),
	GlArg('basevertex', 'GLint')
])

glDrawElementsInstanceBaseVertexBaseInstance = GlApi('glDrawElementsInstanceBaseVertexBaseInstance', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('primcount', 'GLsizei'),
	GlArg('basevertex', 'GLint'),
	GlArg('baseinstance', 'GLuint')
])

glDrawRangeElements = GlApi('glDrawRangeElements', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('start', 'GLuint'),
	GlArg('end', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const GLvoid *')
])

glDrawRangeElementsBaseVertex = GlApi('glDrawRangeElementsBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('start', 'GLuint'),
	GlArg('end', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('basevertex', 'GLint')
])

glDrawTransformFeedback = GlApi('glDrawTransformFeedback', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint')
])

glDrawTransformFeedbackInstanced = GlApi('glDrawTransformFeedbackInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('instancecount', 'GLsizei')
])

glDrawTransformFeedbackStream = GlApi('glDrawTransformFeedbackStream', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('stream', 'GLuint')
])

glDrawTransformFeedbackStreamInstanced = GlApi('glDrawTransformFeedbackStreamInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('stream', 'GLuint'),
	GlArg('instancecount', 'GLsizei')
])

glFenceSync = GlApi('glFenceSync', 'GLsync', [
	GlArg('condition', 'GLenum'),
	GlArg('flags', 'GLbitfield')
])

glFinish = GlApi('glFinish', 'void', [])

glFlush = GlApi('glFlush', 'void', [])

glFlushMappedBufferRange = GlApi('glFlushMappedBufferRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('length', 'GLsizeiptr')
])

glFramebufferParameteri = GlApi('glFramebufferParameteri', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLint')
])

glFramebufferRenderbuffer = GlApi('glFramebufferRenderbuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('renderbuffertarget', 'GLenum'),
	GlArg('renderbuffer', 'GLuint')
])

glFramebufferTexture = GlApi('glFramebufferTexture', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

glFramebufferTexture1D = GlApi('glFramebufferTexture1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('textarget', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

glFramebufferTexture2D = GlApi('glFramebufferTexture2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('textarget', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

glFramebufferTexture3D = GlApi('glFramebufferTexture3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('textarget', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('layer', 'GLint')
])

glFramebufferTextureLayer = GlApi('glFramebufferTextureLayer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('layer', 'GLint')
])

glFrontFace = GlApi('glFrontFace', 'void', [
	GlArg('mode', 'GLenum')
])

glGenBuffers = GlApi('glGenBuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('buffers', 'GLuint *')
])

glGenerateMipmap = GlApi('glGenerateMipmap', 'void', [
	GlArg('target', 'GLenum')
])

glGenFramebuffers = GlApi('glGenFramebuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('id', 'GLuint *')
])

glGenProgramPipelines = GlApi('glGenProgramPipelines', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('pipelines', 'GLuint')
])

glGenQueries = GlApi('glGenQueries', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'GLuint *')
])

glGenRenderbuffers = GlApi('glGenRenderbuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('renderbuffers', 'GLuint *')
])

glGenSamplers = GlApi('glGenSamplers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('samplers', 'GLuint *')
])

glGenTextures = GlApi('glGenTextures', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('textures', 'GLuint *')
])

glGenTransformFeedbacks = GlApi('glGenTransformFeedbacks', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'GLuint *')
])

glGenVertexArrays = GlApi('glGenVertexArrays', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('arrays', 'GLuint *')
])

glGetBooleanv = GlApi('glGetBooleanv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLboolean *')
])

glGetDoublev = GlApi('glGetDoublev', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLdouble *')
])

glFloatv = GlApi('glFloatv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLfloat *')
])

glGetIntegerv = GlApi('glGetIntegerv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetInteger64v = GlApi('glGetInteger64v', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint64 *')
])

GlApi('glGetBooleani_v', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('data', 'GLboolean *')
])

GlApi('glGetIntegeri_v', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('data', 'GLint *')
])

GlApi('glGetFloati_v', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('data', 'GLfloat *')
])

GlApi('glGetDoublei_v', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('data', 'GLdouble *')
])

GlApi('glGetInteger64i_v', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('data', 'GLint64 *')
])

glGetActiveAtomicCounterBufferiv = GlApi('glGetActiveAtomicCounterBufferiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('bufferIndex', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetActiveAttrib = GlApi('glGetActiveAttrib', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('size', 'GLint *'),
	GlArg('type', 'GLenum *'),
	GlArg('name', 'GLchar *')
])

glGetActiveSubroutineName = GlApi('glGetActiveSubroutineName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('bufsize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('name', 'GLchar *')
])

glGetActiveSubroutineUniformiv = GlApi('glGetActiveSubroutineUniformiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('values', 'GLint *')
])

glGetActiveSubroutineUniformName = GlApi('glGetActiveSubroutineUniformName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('bufsize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('name', 'GLchar *')
])

glGetActiveUniform = GlApi('glGetActiveUniform', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('size', 'GLint *'),
	GlArg('type', 'GLenum *'),
	GlArg('name', 'GLchar *')
])

glGetActiveUniformBlockiv = GlApi('glGetActiveUniformBlockiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformBlockIndex', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetActiveUniformBlockName = GlApi('glGetActiveUniformBlockName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformBlockIndex', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('uniformBlockName', 'GLchar *')
])

glGetActiveUniformName = GlApi('glGetActiveUniformName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformIndex', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('uniformName', 'GLchar *')
])

glGetActiveUniformsiv = GlApi('glGetActiveUniformsiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformCount', 'GLsizei'),
	GlArg('uniformIndices', 'const GLuint *'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetAttachedShaders = GlApi('glGetAttachedShaders', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('maxCount', 'GLsizei'),
	GlArg('count', 'GLsizei *'),
	GlArg('shaders', 'GLuint *')
])

glGetAttribLocation = GlApi('glGetAttribLocation', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('name', 'const GLchar *')
])

glGetBufferParameteriv = GlApi('glGetBufferParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('value', 'GLenum'),
	GlArg('data', 'GLint *')
])

glGetBufferParameteri64v = GlApi('glGetBufferParameteri64v', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('value', 'GLenum'),
	GlArg('data', 'GLint64 *')
])

glGetBufferPointerv = GlApi('glGetBufferPointerv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLvoid **')
])

glGetBufferSubData = GlApi('glGetBufferSubData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('data', 'GLvoid *')
])

glGetCompressedTexImage = GlApi('glGetCompressedTexImage', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('lod', 'GLint'),
	GlArg('img', 'GLvoid *')
])

glGetDebugMessageLog = GlApi('glGetDebugMessageLog', 'GLuint', [
	GlArg('count', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('sources', 'GLenum *'),
	GlArg('types', 'GLenum *'),
	GlArg('ids', 'GLuint *'),
	GlArg('severities', 'GLenum *'),
	GlArg('lengths', 'GLsizei *'),
	GlArg('messageLog', 'GLchar *')
])

glGetError = GlApi('glGetError', 'GLenum', [])

glGetFragDataIndex = GlApi('glGetFragDataIndex', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('name', 'const char *')
])

glGetFragDataLocation = GlApi('glGetFragDataLocation', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('name', 'const char *')
])

glGetFramebufferAttachmentParameteriv = GlApi('glGetFramebufferAttachmentParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetFramebufferParameteriv = GlApi('glGetFramebufferParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetInternalformativ = GlApi('glGetInternalformativ', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('params', 'GLint *')
])

glGetInternalformati64v = GlApi('glGetInternalformati64v', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('params', 'GLint64 *')
])

glGetMultisamplefv = GlApi('glGetMultisamplefv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('val', 'GLfloat *')
])

glGetObjectLabel = GlApi('glGetObjectLabel', 'void', [
	GlArg('identifier', 'GLenum'),
	GlArg('name', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('label', 'char *')
])

glGetObjectPtrLabel = GlApi('glGetObjectPtrLabel', 'void', [
	GlArg('ptr', 'void *'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('label', 'char *')
])

glGetProgramiv = GlApi('glGetProgramiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetProgramBinary = GlApi('glGetProgramBinary', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('binaryFormat', 'GLenum *'),
	GlArg('binary', 'void *')
])

glGetProgramInfoLog = GlApi('glGetProgramInfoLog', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('maxLength', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('infoLog', 'GLchar *')
])

glGetProgramInterfaceiv = GlApi('glGetProgramInterfaceiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('programInterface', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetProgramPipelineiv = GlApi('glGetProgramPipelineiv', 'void', [
	GlArg('pipeline', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetProgramPipelineInfoLog = GlApi('glGetProgramPipelineInfoLog', 'void', [
	GlArg('pipeline', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('infoLog', 'GLchar *')
])

glGetProgramResourceiv = GlApi('glGetProgramResourceiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('programInterface', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('propCount', 'GLsizei'),
	GlArg('props', 'const GLenum *'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('params', 'GLint *')
])

glGetProgramResourceLocation = GlApi('glGetProgramResourceLocation', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('programInterface', 'GLenum'),
	GlArg('name', 'const char *')
])

glGetProgramResourceLocationIndex = GlApi('glGetProgramResourceLocationIndex', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('programInterface', 'GLenum'),
	GlArg('name', 'const char *')
])

glGetProgramResourceIndex = GlApi('glGetProgramResourceIndex', 'GLuint', [
	GlArg('program', 'GLuint'),
	GlArg('programInterface', 'GLenum'),
	GlArg('name', 'const char *')
])

glGetProgramResourceName = GlApi('glGetProgramResourceName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('programInterface', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('name', 'char *')
])

glGetProgramStageiv = GlApi('glGetProgramStageiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('values', 'GLint *')
])

glGetQueryiv = GlApi('glGetQueryiv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetQueryIndexediv = GlApi('glGetQueryIndexediv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetQueryObjectiv = GlApi('glGetQueryObjectiv', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetQueryObjectuiv = GlApi('glGetQueryObjectuiv', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLuint *')
])

glGetQueryObjecti64v = GlApi('glGetQueryObjecti64v', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint64 *')
])

glGetQueryObjectui64v = GlApi('glGetQueryObjectui64v', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLuint64 *')
])

glGetRenderbufferParameteriv = GlApi('glGetRenderbufferParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetSamplerParameterfv = GlApi('glGetSamplerParameterfv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLfloat *')
])

glGetSamplerParameteriv = GlApi('glGetSamplerParameteriv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetSamplerParameterIiv = GlApi('glGetSamplerParameterIiv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetSamplerParameterIuiv = GlApi('glGetSamplerParameterIuiv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLuint *')
])

glGetShaderiv = GlApi('glGetShaderiv', 'void', [
	GlArg('shader', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetShaderInfoLog = GlApi('glGetShaderInfoLog', 'void', [
	GlArg('shader', 'GLuint'),
	GlArg('maxLength', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('infoLog', 'GLchar *')
])

glGetShaderPrecisionFormat = GlApi('glGetShaderPrecisionFormat', 'void', [
	GlArg('shaderType', 'GLenum'),
	GlArg('precisionType', 'GLenum'),
	GlArg('range', 'GLint *'),
	GlArg('precision', 'GLint *')
])

glGetShaderSource = GlApi('glGetShaderSource', 'void', [
	GlArg('shader', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('source', 'GLchar *')
])

glGetString = GlApi('glGetString', 'const GLubyte *', [
	GlArg('name', 'GLenum')
])

glGetStringi = GlApi('glGetStringi', 'const GLubyte *', [
	GlArg('name', 'GLenum'),
	GlArg('index', 'GLuint')
])

glGetSubroutineIndex = GlApi('glGetSubroutineIndex', 'GLuint', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('name', 'const GLchar *')
])

glGetSubroutineUniformLocation = GlApi('glGetSubroutineUniformLocation', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('name', 'const GLchar *')
])

glGetSynciv = GlApi('glGetSynciv', 'void', [
	GlArg('sync', 'GLsync'),
	GlArg('pname', 'GLenum'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('values', 'GLint *')
])

glGetTexImage = GlApi('glGetTexImage', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('img', 'GLvoid *')
])

glGetTexLevelParameterfv = GlApi('glGetTexLevelParameterfv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLfloat *')
])

glGetTexLevelParameteriv = GlApi('glGetTexLevelParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetTexParameterfv = GlApi('glGetTexParameterfv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLfloat *')
])

glGetTexParameteriv = GlApi('glGetTexParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetTexParameterIiv = GlApi('glGetTexParameterIiv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetTexParameterIuiv = GlApi('glGetTexParameterIuiv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLuint *')
])

glGetTransformFeedbackVarying = GlApi('glGetTransformFeedbackVarying', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('size', 'GLsizei'),
	GlArg('type', 'GLenum *'),
	GlArg('name', 'char *')
])

glGetUniformfv = GlApi('glGetUniformfv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('params', 'GLfloat *')
])

glGetUniformiv = GlApi('glGetUniformiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('params', 'GLint *')
])

glGetUniformuiv = GlApi('glGetUniformuiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('params', 'GLuint *')
])

glGetUniformdv = GlApi('glGetUniformdv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('params', 'GLdouble *')
])

glGetUniformBlockIndex = GlApi('glGetUniformBlockIndex', 'GLuint', [
	GlArg('program', 'GLuint'),
	GlArg('uniformBlockName', 'const GLchar *')
])

glGetUniformIndices = GlApi('glGetUniformIndices', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformCount', 'GLsizei'),
	GlArg('uniformNames', 'const GLchar **'),
	GlArg('uniformIndices', 'GLuint *')
])

glGetUniformLocation = GlApi('glGetUniformLocation', 'GLint', [
	GlArg('program', 'GLuint'),
	GlArg('name', 'const GLchar *')
])

glGetUniformSubroutineuiv = GlApi('glGetUniformSubroutineuiv', 'void', [
	GlArg('shadertype', 'GLenum'),
	GlArg('location', 'GLint'),
	GlArg('values', 'GLuint *')
])

glGetVertexAttribdv = GlApi('glGetVertexAttribdv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLdouble *')
])

glGetVertexAttribfv = GlApi('glGetVertexAttribfv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLfloat *')
])

glGetVertexAttribiv = GlApi('glGetVertexAttribiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetVertexAttribIiv = GlApi('glGetVertexAttribIiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

glGetVertexAttribIuiv = GlApi('glGetVertexAttribIuiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLuint *')
])

glGetVertexAttribLdv = GlApi('glGetVertexAttribLdv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLdouble *')
])

glGetVertexAttribPointerv = GlApi('glGetVertexAttribPointerv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('pointer', 'GLvoid **')
])

glHint = GlApi('glHint', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('mode', 'GLenum')
])

glInvalidateBufferData = GlApi('glInvalidateBufferData', 'void', [
	GlArg('buffer', 'GLuint')
])

glInvalidateBufferSubData = GlApi('glInvalidateBufferSubData', 'void', [
	GlArg('buffer', 'GLuint'),
	GlArg('offset', 'GLintptr'),
	GlArg('length', 'GLsizeiptr')
])

glInvalidateFramebuffer = GlApi('glInvalidateFramebuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('numAttachments', 'GLsizei'),
	GlArg('attachments', 'const GLenum *')
])

glInvalidateSubFramebuffer = GlApi('glInvalidateSubFramebuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('numAttachments', 'GLsizei'),
	GlArg('attachments', 'const GLenum *'),
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLint'),
	GlArg('height', 'GLint')
])

glInvalidateTexImage = GlApi('glInvalidateTexImage', 'void', [
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

glInvalidateTexSubImage = GlApi('glInvalidateTexSubImage', 'void', [
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('zoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei')
])

glIsBuffer = GlApi('glIsBuffer', 'GLboolean', [
	GlArg('buffer', 'GLuint')
])

glIsEnabled = GlApi('glIsEnabled', 'GLboolean', [
	GlArg('cap', 'GLenum')
])

glIsEnabledi = GlApi('glIsEnabledi', 'GLboolean', [
	GlArg('cap', 'GLenum'),
	GlArg('index', 'GLuint')
])

glIsFramebuffer = GlApi('glIsFramebuffer', 'GLboolean', [
	GlArg('framebuffer', 'GLuint')
])

glIsProgram = GlApi('glIsProgram', 'GLboolean', [
	GlArg('program', 'GLuint')
])

glIsProgramPipeline = GlApi('glIsProgramPipeline', 'GLboolean', [
	GlArg('pipeline', 'GLuint')
])

glIsQuery = GlApi('glIsQuery', 'GLboolean', [
	GlArg('id', 'GLuint')
])

glIsRenderbuffer = GlApi('glIsRenderbuffer', 'GLboolean', [
	GlArg('renderbuffer', 'GLuint')
])

glIsSampler = GlApi('glIsSampler', 'GLboolean', [
	GlArg('id', 'GLuint')
])

glIsShader = GlApi('glIsShader', 'GLboolean', [
	GlArg('shader', 'GLuint')
])

glIsSync = GlApi('glIsSync', 'GLboolean', [
	GlArg('sync', 'GLsync')
])

glIsTexture = GlApi('glIsTexture', 'GLboolean', [
	GlArg('texture', 'GLuint')
])

glIsTransformFeedback = GlApi('glIsTransformFeedback', 'GLboolean', [
	GlArg('id', 'GLuint')
])

glIsVertexArray = GlApi('glIsVertexArray', 'GLboolean', [
	GlArg('array', 'GLuint')
])

glLineWidth = GlApi('glLineWidth', 'void', [
	GlArg('width', 'GLfloat')
])

glLinkProgram = GlApi('glLinkProgram', 'void', [
	GlArg('program', 'GLuint')
])

glLogicOp = GlApi('glLogicOp', 'void', [
	GlArg('opcode', 'GLenum')
])

glMapBuffer = GlApi('glMapBuffer', 'void *', [
	GlArg('target', 'GLenum'),
	GlArg('access', 'GLenum')
])

glUnmapBuffer = GlApi('glUnmapBuffer', 'GLboolean', [
	GlArg('target', 'GLenum')
])

glMapBufferRange = GlApi('glMapBufferRange', 'void *', [
	GlArg('target', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('length', 'GLsizeiptr'),
	GlArg('access', 'GLbitfield')
])

glMemoryBarrier = GlApi('glMemoryBarrier', 'void', [
	GlArg('barriers', 'GLbitfield')
])

glMinSampleShading = GlApi('glMinSampleShading', 'void', [
	GlArg('value', 'GLfloat')
])

glMultiDrawArrays = GlApi('glMultiDrawArrays', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'const GLint *'),
	GlArg('count', 'const GLsizei *'),
	GlArg('drawcount', 'GLsizei')
])

glMultiDrawArraysIndirect = GlApi('glMultiDrawArraysIndirect', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('indirect', 'const void *'),
	GlArg('drawcount', 'GLsizei'),
	GlArg('stride', 'GLsizei')
])

glMultiDrawElements = GlApi('glMultiDrawElements', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'const GLsizei *'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const GLvoid * const *'),
	GlArg('drawcount', 'GLsizei')
])

glMultiDrawElementsBaseVertex = GlApi('glMultiDrawElementsBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'const GLsizei *'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const GLvoid * const *'),
	GlArg('drawcount', 'GLsizei'),
	GlArg('basevertex', 'const GLint *')
])

glMultiDrawElementsIndirect = GlApi('glMultiDrawElementsIndirect', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('indirect', 'const void *'),
	GlArg('drawcount', 'GLsizei'),
	GlArg('stride', 'GLsizei')
])

glObjectLabel = GlApi('glObjectLabel', 'void', [
	GlArg('identifier', 'GLenum'),
	GlArg('name', 'GLuint'),
	GlArg('length', 'GLsizei'),
	GlArg('label', 'const char *')
])

glObjectPtrLabel = GlApi('glObjectPtrLabel', 'void', [
	GlArg('ptr', 'void *'),
	GlArg('length', 'GLsizei'),
	GlArg('label', 'const char *')
])

glPatchParameteri = GlApi('glPatchParameteri', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('value', 'GLint')
])

glPatchParameterfv = GlApi('glPatchParameterfv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('values', 'const GLfloat *')
])

glPauseTransformFeedback = GlApi('glPauseTransformFeedback', 'void', [])

glPixelStoref = GlApi('glPixelStoref', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLfloat')
])

glPixelStorei = GlApi('glPixelStorei', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLint')
])

glPointParameterf = GlApi('glPointParameterf', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLfloat')
])

glPointParameteri = GlApi('glPointParameteri', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLint')
])

glPointParameterfv = GlApi('glPointParameterfv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLfloat *')
])

glPointParameteriv = GlApi('glPointParameteriv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLint *')
])

glPointSize = GlApi('glPointSize', 'void', [
	GlArg('size', 'GLfloat')
])

glPolygonMode = GlApi('glPolygonMode', 'void', [
	GlArg('face', 'GLenum'),
	GlArg('mode', 'GLenum')
])

glPolygonOffset = GlApi('glPolygonOffset', 'void', [
	GlArg('factor', 'GLfloat'),
	GlArg('units', 'GLfloat')
])

glPopDebugGroup = GlApi('glPopDebugGroup', 'void', [])

glPrimitiveRestartIndex = GlApi('glPrimitiveRestartIndex', 'void', [
	GlArg('index', 'GLuint')
])

glProgramBinary = GlApi('glProgramBinary', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('binaryFormat', 'GLenum'),
	GlArg('binary', 'const void *'),
	GlArg('length', 'GLsizei')
])

glProgramParameteri = GlApi('glProgramParameteri', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('value', 'GLint')
])

glProgramUniform1f = GlApi('glProgramUniform1f', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat')
])

glProgramUniform2f = GlApi('glProgramUniform2f', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat')
])

glProgramUniform3f = GlApi('glProgramUniform3f', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat'),
	GlArg('v2', 'GLfloat')
])

glProgramUniform4f = GlApi('glProgramUniform4f', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat'),
	GlArg('v2', 'GLfloat'),
	GlArg('v3', 'GLfloat')
])

glProgramUniform1i = GlApi('glProgramUniform1i', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint')
])

glProgramUniform2i = GlApi('glProgramUniform2i', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint')
])

glProgramUniform3i = GlApi('glProgramUniform3i', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint'),
	GlArg('v2', 'GLint')
])

glProgramUniform4i = GlApi('glProgramUniform4i', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint'),
	GlArg('v2', 'GLint'),
	GlArg('v3', 'GLint')
])

glProgramUniform1ui = GlApi('glProgramUniform1ui', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint')
])

glProgramUniform2ui = GlApi('glProgramUniform2ui', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint')
])

glProgramUniform3ui = GlApi('glProgramUniform3ui', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint'),
	GlArg('v2', 'GLuint')
])

glProgramUniform4ui = GlApi('glProgramUniform4ui', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint'),
	GlArg('v2', 'GLuint'),
	GlArg('v3', 'GLuint')
])

glProgramUniform1fv = GlApi('glProgramUniform1fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniform2fv = GlApi('glProgramUniform2fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniform3fv = GlApi('glProgramUniform3fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniform4fv = GlApi('glProgramUniform4fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniform1iv = GlApi('glProgramUniform1iv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glProgramUniform2iv = GlApi('glProgramUniform2iv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glProgramUniform3iv = GlApi('glProgramUniform3iv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glProgramUniform4iv = GlApi('glProgramUniform4iv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glProgramUniform1uiv = GlApi('glProgramUniform1uiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glProgramUniform2uiv = GlApi('glProgramUniform2uiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glProgramUniform3uiv = GlApi('glProgramUniform3uiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glProgramUniform4uiv = GlApi('glProgramUniform4uiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glProgramUniformMatrix2fv = GlApi('glProgramUniformMatrix2fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix3fv = GlApi('glProgramUniformMatrix3fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix4fv = GlApi('glProgramUniformMatrix4fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix2x3fv = GlApi('glProgramUniformMatrix2x3fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix3x2fv = GlApi('glProgramUniformMatrix3x2fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix2x4fv = GlApi('glProgramUniformMatrix2x4fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix4x2fv = GlApi('glProgramUniformMatrix4x2fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix3x4fv = GlApi('glProgramUniformMatrix3x4fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProgramUniformMatrix4x3fv = GlApi('glProgramUniformMatrix4x3fv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glProvokingVertex = GlApi('glProvokingVertex', 'void', [
	GlArg('provokeMode', 'GLenum')
])

glPushDebugGroup = GlApi('glPushDebugGroup', 'void', [
	GlArg('source', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('length', 'GLsizei'),
	GlArg('message', 'const char *')
])

glQueryCounter = GlApi('glQueryCounter', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('target', 'GLenum')
])

glReadBuffer = GlApi('glReadBuffer', 'void', [
	GlArg('mode', 'GLenum')
])

glReadPixels = GlApi('glReadPixels', 'void', [
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'GLvoid *')
])

glReleaseShaderCompiler = GlApi('glReleaseShaderCompiler', 'void', [])

glRenderbufferStorage = GlApi('glRenderbufferStorage', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glRenderbufferStorageMultisample = GlApi('glRenderbufferStorageMultisample', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('samples', 'GLsizei'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glResumeTransformFeedback = GlApi('glResumeTransformFeedback', 'void', [])

glSampleCoverage = GlApi('glSampleCoverage', 'void', [
	GlArg('value', 'GLfloat'),
	GlArg('invert', 'GLboolean')
])

glSampleMaski = GlApi('glSampleMaski', 'void', [
	GlArg('maskNumber', 'GLuint'),
	GlArg('mask', 'GLbitfield')
])

glSamplerParameterf = GlApi('glSamplerParameterf', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLfloat')
])

glSamplerParameteri = GlApi('glSamplerParameteri', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLint')
])

glSamplerParameterfv = GlApi('glSamplerParameterfv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLfloat *')
])

glSamplerParameteriv = GlApi('glSamplerParameteriv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLint *')
])

glSamplerParameterIiv = GlApi('glSamplerParameterIiv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLint *')
])

glSamplerParameterIuiv = GlApi('glSamplerParameterIuiv', 'void', [
	GlArg('sampler', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLuint *')
])

glScissor = GlApi('glScissor', 'void', [
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glScissorArrayv = GlApi('glScissorArrayv', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('v', 'const GLint *')
])

glScissorIndexed = GlApi('glScissorIndexed', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('left', 'GLint'),
	GlArg('bottom', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glScissorIndexedv = GlApi('glScissorIndexedv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glShaderBinary = GlApi('glShaderBinary', 'void', [
	GlArg('count', 'GLsizei'),
	GlArg('shaders', 'const GLuint *'),
	GlArg('binaryFormat', 'GLenum'),
	GlArg('binary', 'const void *'),
	GlArg('length', 'GLsizei')
])

glShaderSource = GlApi('glShaderSource', 'void', [
	GlArg('shader', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('string', 'const GLchar **'),
	GlArg('length', 'const GLint *')
])

glShaderStorageBlockBinding = GlApi('glShaderStorageBlockBinding', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('storageBlockIndex', 'GLuint'),
	GlArg('storageBlockBinding', 'GLuint')
])

glStencilFunc = GlApi('glStencilFunc', 'void', [
	GlArg('func', 'GLenum'),
	GlArg('ref', 'GLint'),
	GlArg('mask', 'GLuint')
])

glStencilFuncSeparate = GlApi('glStencilFuncSeparate', 'void', [
	GlArg('face', 'GLenum'),
	GlArg('func', 'GLenum'),
	GlArg('ref', 'GLint'),
	GlArg('mask', 'GLuint')
])

glStencilMask = GlApi('glStencilMask', 'void', [
	GlArg('mask', 'GLuint')
])

glStencilMaskSeparate = GlApi('glStencilMaskSeparate', 'void', [
	GlArg('face', 'GLenum'),
	GlArg('mask', 'GLuint')
])

glStencilOp = GlApi('glStencilOp', 'void', [
	GlArg('sfail', 'GLenum'),
	GlArg('dpfail', 'GLenum'),
	GlArg('dppass', 'GLenum')
])

glStencilOpSeparate = GlApi('glStencilOpSeparate', 'void', [
	GlArg('face', 'GLenum'),
	GlArg('sfail', 'GLenum'),
	GlArg('dpfail', 'GLenum'),
	GlArg('dppass', 'GLenum')
])

glTexBuffer = GlApi('glTexBuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalFormat', 'GLenum'),
	GlArg('buffer', 'GLuint')
])

glTexBufferRange = GlApi('glTexBufferRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalFormat', 'GLenum'),
	GlArg('buffer', 'GLuint'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr')
])

glTexImage1D = GlApi('glTexImage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalFormat', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('border', 'GLint'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const GLvoid *')
])

glTexImage2D = GlApi('glTexImage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalFormat', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('border', 'GLint'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const GLvoid *')
])

glTexImage2DMultisample = GlApi('glTexImage2DMultisample', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalFormat', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('fixedsamplelocations', 'GLboolean')
])

glTexImage3D = GlApi('glTexImage3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalFormat', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('border', 'GLint'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const GLvoid *')
])

glTexImage3DMultisample = GlApi('glTexImage3DMultisample', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('internalFormat', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('fixedsamplelocations', 'GLboolean')
])

glTexParameterf = GlApi('glTexParameterf', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLfloat')
])

glTexParameterf = GlApi('glTexParameterf', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLint')
])

glTexParameterfv = GlApi('glTexParameterfv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLfloat *')
])

glTexParameteriv = GlApi('glTexParameteriv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLint *')
])

glTexParameterIiv = GlApi('glTexParameterIiv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLint *')
])

glTexParameterIuiv = GlApi('glTexParameterIuiv', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'const GLuint *')
])

glTexStorage1D = GlApi('glTexStorage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('levels', 'GLsizei'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei')
])

glTexStorage2D = GlApi('glTexStorage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('levels', 'GLsizei'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glTexStorage2DMultisample = GlApi('glTexStorage2DMultisample', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('samples', 'GLsizei'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('fixedsamplelocations', 'GLboolean')
])

glTexStorage3D = GlApi('glTexStorage3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('levels', 'GLsizei'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei')
])

glTexStorage3DMultisample = GlApi('glTexStorage3DMultisample', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('samples', 'GLsizei'),
	GlArg('internalformat', 'GLenum'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('fixedsamplelocations', 'GLboolean')
])

glTexSubImage1D = GlApi('glTexSubImage1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const GLvoid *')
])

glTexSubImage2D = GlApi('glTexSubImage2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const GLvoid *')
])

glTexSubImage3D = GlApi('glTexSubImage3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('level', 'GLint'),
	GlArg('xoffset', 'GLint'),
	GlArg('yoffset', 'GLint'),
	GlArg('zoffset', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei'),
	GlArg('depth', 'GLsizei'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const GLvoid *')
])

glTextureView = GlApi('glTextureView', 'void', [
	GlArg('texture', 'GLuint'),
	GlArg('target', 'GLenum'),
	GlArg('origtexture', 'GLuint'),
	GlArg('internalformat', 'GLenum'),
	GlArg('minlevel', 'GLuint'),
	GlArg('numlevels', 'GLuint'),
	GlArg('minlayer', 'GLuint'),
	GlArg('numlayers', 'GLuint')
])

glTransformFeedbackVaryings = GlApi('glTransformFeedbackVaryings', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('varyings', 'const char **'),
	GlArg('bufferMode', 'GLenum')
])

glUniform1f = GlApi('glUniform1f', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat')
])

glUniform2f = GlApi('glUniform2f', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat')
])

glUniform3f = GlApi('glUniform3f', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat'),
	GlArg('v2', 'GLfloat')
])

glUniform4f = GlApi('glUniform4f', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat'),
	GlArg('v2', 'GLfloat'),
	GlArg('v3', 'GLfloat')
])

glUniform1i = GlApi('glUniform1i', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint')
])

glUniform2i = GlApi('glUniform2i', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint')
])

glUniform3i = GlApi('glUniform3i', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint'),
	GlArg('v2', 'GLint')
])

glUniform4i = GlApi('glUniform4i', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint'),
	GlArg('v2', 'GLint'),
	GlArg('v3', 'GLint')
])

glUniform1ui = GlApi('glUniform1ui', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint')
])

glUniform2ui = GlApi('glUniform2ui', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint')
])

glUniform3ui = GlApi('glUniform3ui', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint'),
	GlArg('v2', 'GLuint')
])

glUniform4ui = GlApi('glUniform4ui', 'void', [
	GlArg('location', 'GLint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint'),
	GlArg('v2', 'GLuint'),
	GlArg('v3', 'GLuint')
])

glUniform1fv = GlApi('glUniform1fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glUniform2fv = GlApi('glUniform2fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glUniform3fv = GlApi('glUniform3fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glUniform4fv = GlApi('glUniform4fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLfloat *')
])

glUniform1iv = GlApi('glUniform1iv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glUniform2iv = GlApi('glUniform2iv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glUniform3iv = GlApi('glUniform3iv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glUniform4iv = GlApi('glUniform4iv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLint *')
])

glUniform1uiv = GlApi('glUniform1uiv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glUniform2uiv = GlApi('glUniform2uiv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glUniform3uiv = GlApi('glUniform3uiv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glUniform4uiv = GlApi('glUniform4uiv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('value', 'const GLuint *')
])

glUniformMatrix2fv = GlApi('glUniformMatrix2fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix3fv = GlApi('glUniformMatrix3fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix4fv = GlApi('glUniformMatrix4fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix2x3fv = GlApi('glUniformMatrix2x3fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix3x2fv = GlApi('glUniformMatrix3x2fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix2x4fv = GlApi('glUniformMatrix2x4fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix4x2fv = GlApi('glUniformMatrix4x2fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix3x4fv = GlApi('glUniformMatrix3x4fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformMatrix4x3fv = GlApi('glUniformMatrix4x3fv', 'void', [
	GlArg('location', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('transpose', 'GLboolean'),
	GlArg('value', 'const GLfloat *')
])

glUniformBlockBinding = GlApi('glUniformBlockBinding', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformBlockIndex', 'GLuint'),
	GlArg('uniformblockBinding', 'GLuint')
])

glUniformSubroutinesuiv = GlApi('glUniformSubroutinesuiv', 'void', [
	GlArg('shadertype', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('indices', 'const GLuint *')
])

glUseProgram = GlApi('glUseProgram', 'void', [
	GlArg('program', 'GLuint')
])

glUseProgramStages = GlApi('glUseProgramStages', 'void', [
	GlArg('pipeline', 'GLuint'),
	GlArg('stages', 'GLbitfield'),
	GlArg('program', 'GLuint')
])

glValidateProgram = GlApi('glValidateProgram', 'void', [
	GlArg('program', 'GLuint')
])

glValidateProgramPipeline = GlApi('glValidateProgramPipeline', 'void', [
	GlArg('pipeline', 'GLuint')
])

glVertexAttrib1f = GlApi('glVertexAttrib1f', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLfloat')
])

glVertexAttrib2f = GlApi('glVertexAttrib2f', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat')
])

glVertexAttrib3f = GlApi('glVertexAttrib3f', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat'),
	GlArg('v2', 'GLfloat')
])

glVertexAttrib4f = GlApi('glVertexAttrib4f', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLfloat'),
	GlArg('v1', 'GLfloat'),
	GlArg('v2', 'GLfloat'),
	GlArg('v3', 'GLfloat')
])

glVertexAttrib1s = GlApi('glVertexAttrib1s', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLshort')
])

glVertexAttrib2s = GlApi('glVertexAttrib2s', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLshort'),
	GlArg('v1', 'GLshort')
])

glVertexAttrib3s = GlApi('glVertexAttrib3s', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLshort'),
	GlArg('v1', 'GLshort'),
	GlArg('v2', 'GLshort')
])

glVertexAttrib4s = GlApi('glVertexAttrib4s', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLshort'),
	GlArg('v1', 'GLshort'),
	GlArg('v2', 'GLshort'),
	GlArg('v3', 'GLshort')
])

glVertexAttrib1d = GlApi('glVertexAttrib1d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble')
])

glVertexAttrib2d = GlApi('glVertexAttrib2d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble'),
	GlArg('v1', 'GLdouble')
])

glVertexAttrib3d = GlApi('glVertexAttrib3d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble'),
	GlArg('v1', 'GLdouble'),
	GlArg('v2', 'GLdouble')
])

glVertexAttrib4d = GlApi('glVertexAttrib4d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble'),
	GlArg('v1', 'GLdouble'),
	GlArg('v2', 'GLdouble'),
	GlArg('v3', 'GLdouble')
])

glVertexAttribI1i = GlApi('glVertexAttribI1i', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLint')
])

glVertexAttribI2i = GlApi('glVertexAttribI2i', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint')
])

glVertexAttribI3i = GlApi('glVertexAttribI3i', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint'),
	GlArg('v2', 'GLint')
])

glVertexAttribI4i = GlApi('glVertexAttribI4i', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLint'),
	GlArg('v1', 'GLint'),
	GlArg('v2', 'GLint'),
	GlArg('v3', 'GLint')
])

glVertexAttribI1ui = GlApi('glVertexAttribI1ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLuint')
])

glVertexAttribI2ui = GlApi('glVertexAttribI2ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint')
])

glVertexAttribI3ui = GlApi('glVertexAttribI3ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint'),
	GlArg('v2', 'GLuint')
])

glVertexAttribI4ui = GlApi('glVertexAttribI4ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLuint'),
	GlArg('v1', 'GLuint'),
	GlArg('v2', 'GLuint'),
	GlArg('v3', 'GLuint')
])

glVertexAttribL1d = GlApi('glVertexAttribL1d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble')
])

glVertexAttribL2d = GlApi('glVertexAttribL2d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble'),
	GlArg('v1', 'GLdouble')
])

glVertexAttribL3d = GlApi('glVertexAttribL3d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble'),
	GlArg('v1', 'GLdouble'),
	GlArg('v2', 'GLdouble')
])

glVertexAttribL4d = GlApi('glVertexAttribL4d', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLdouble'),
	GlArg('v1', 'GLdouble'),
	GlArg('v2', 'GLdouble'),
	GlArg('v3', 'GLdouble')
])

glVertexAttrib4Nub = GlApi('glVertexAttrib4Nub', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v0', 'GLubyte'),
	GlArg('v1', 'GLubyte'),
	GlArg('v2', 'GLubyte'),
	GlArg('v3', 'GLubyte')
])

glVertexAttrib1fv = GlApi('glVertexAttrib1fv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLfloat *')
])

glVertexAttrib2fv = GlApi('glVertexAttrib2fv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLfloat *')
])

glVertexAttrib3fv = GlApi('glVertexAttrib3fv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLfloat *')
])

glVertexAttrib4fv = GlApi('glVertexAttrib4fv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLfloat *')
])

glVertexAttrib1sv = GlApi('glVertexAttrib1sv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLshort *')
])

glVertexAttrib2sv = GlApi('glVertexAttrib2sv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLshort *')
])

glVertexAttrib3sv = GlApi('glVertexAttrib3sv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLshort *')
])

glVertexAttrib4sv = GlApi('glVertexAttrib4sv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLshort *')
])

glVertexAttrib1dv = GlApi('glVertexAttrib1dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttrib2dv = GlApi('glVertexAttrib2dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttrib3dv = GlApi('glVertexAttrib3dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttrib4dv = GlApi('glVertexAttrib4dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttribI1iv = GlApi('glVertexAttribI1iv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glVertexAttribI2iv = GlApi('glVertexAttribI2iv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glVertexAttribI3iv = GlApi('glVertexAttribI3iv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glVertexAttribI4iv = GlApi('glVertexAttribI4iv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glVertexAttribI1uiv = GlApi('glVertexAttribI1uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLuint *')
])

glVertexAttribI2uiv = GlApi('glVertexAttribI2uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLuint *')
])

glVertexAttribI3uiv = GlApi('glVertexAttribI3uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLuint *')
])

glVertexAttribI4uiv = GlApi('glVertexAttribI4uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLuint *')
])

glVertexAttribL1dv = GlApi('glVertexAttribL1dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttribL2dv = GlApi('glVertexAttribL2dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttribL3dv = GlApi('glVertexAttribL3dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttribL4dv = GlApi('glVertexAttribL4dv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLdouble *')
])

glVertexAttrib4iv = GlApi('glVertexAttrib4iv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glVertexAttrib4bv = GlApi('glVertexAttrib4bv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLbyte *')
])

glVertexAttrib4ubv = GlApi('glVertexAttrib4ubv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLubyte *')
])

glVertexAttrib4usv = GlApi('glVertexAttrib4usv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLushort *')
])

glVertexAttrib4uiv = GlApi('glVertexAttrib4uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLuint *')
])

glVertexAttrib4Nbv = GlApi('glVertexAttrib4Nbv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLbyte *')
])

glVertexAttrib4Nsv = GlApi('glVertexAttrib4Nsv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLshort *')
])

glVertexAttrib4Niv = GlApi('glVertexAttrib4Niv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLint *')
])

glVertexAttrib4Nubv = GlApi('glVertexAttrib4Nubv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLubyte *')
])

glVertexAttrib4Nusv = GlApi('glVertexAttrib4Nusv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLushort *')
])

glVertexAttrib4Nuiv = GlApi('glVertexAttrib4Nuiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLuiv *')
])

glVertexAttribI4bv = GlApi('glVertexAttribI4bv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLbyte *')
])

glVertexAttribI4ubv = GlApi('glVertexAttribI4ubv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLubyte *')
])

glVertexAttribI4sv = GlApi('glVertexAttribI4sv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLshort *')
])

glVertexAttribI4usv = GlApi('glVertexAttribI4usv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLushort *')
])

glVertexAttribP1ui = GlApi('glVertexAttribP1ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint')
])

glVertexAttribP2ui = GlApi('glVertexAttribP2ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint')
])

glVertexAttribP3ui = GlApi('glVertexAttribP3ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint')
])

glVertexAttribP4ui = GlApi('glVertexAttribP4ui', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint')
])

glVertexAttribP1uiv = GlApi('glVertexAttribP1uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint *')
])

glVertexAttribP2uiv = GlApi('glVertexAttribP2uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint *')
])

glVertexAttribP3uiv = GlApi('glVertexAttribP3uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint *')
])

glVertexAttribP4uiv = GlApi('glVertexAttribP4uiv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('value', 'GLuint *')
])

glVertexAttribBinding = GlApi('glVertexAttribBinding', 'void', [
	GlArg('attribindex', 'GLuint'),
	GlArg('bindingindex', 'GLuint')
])

glVertexAttribDivisor = GlApi('glVertexAttribDivisor', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('divisor', 'GLuint')
])

glVertexAttribFormat = GlApi('glVertexAttribFormat', 'void', [
	GlArg('attribindex', 'GLuint'),
	GlArg('size', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('relativeoffset', 'GLuint')
])

glVertexAttribIFormat = GlApi('glVertexAttribIFormat', 'void', [
	GlArg('attribindex', 'GLuint'),
	GlArg('size', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('relativeoffset', 'GLuint')
])

glVertexAttribLFormat = GlApi('glVertexAttribLFormat', 'void', [
	GlArg('attribindex', 'GLuint'),
	GlArg('size', 'GLuint'),
	GlArg('type', 'GLenum'),
	GlArg('relativeoffset', 'GLuint')
])

glVertexAttribPointer = GlApi('glVertexAttribPointer', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('size', 'GLint'),
	GlArg('type', 'GLenum'),
	GlArg('normalized', 'GLboolean'),
	GlArg('stride', 'GLsizei'),
	GlArg('pointer', 'const GLvoid *')
])

glVertexAttribIPointer = GlApi('glVertexAttribIPointer', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('size', 'GLint'),
	GlArg('type', 'GLenum'),
	GlArg('stride', 'GLsizei'),
	GlArg('pointer', 'const GLvoid *')
])

glVertexAttribLPointer = GlApi('glVertexAttribLPointer', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('size', 'GLint'),
	GlArg('type', 'GLenum'),
	GlArg('stride', 'GLsizei'),
	GlArg('pointer', 'const GLvoid *')
])

glVertexBindingDivisor = GlApi('glVertexBindingDivisor', 'void', [
	GlArg('bindingindex', 'GLuint'),
	GlArg('divisor', 'GLuint')
])

glViewport = GlApi('glViewport', 'void', [
	GlArg('x', 'GLint'),
	GlArg('y', 'GLint'),
	GlArg('width', 'GLsizei'),
	GlArg('height', 'GLsizei')
])

glViewportArrayv = GlApi('glViewportArrayv', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('v', 'const GLfloat *')
])

glViewportIndexedf = GlApi('glViewportIndexedf', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('x', 'GLfloat'),
	GlArg('y', 'GLfloat'),
	GlArg('w', 'GLfloat'),
	GlArg('h', 'GLfloat')
])

glViewportIndexedfv = GlApi('glViewportIndexedfv', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('v', 'const GLfloat *')
])

glWaitSync = GlApi('glWaitSync', 'void', [
	GlArg('sync', 'GLsync'),
	GlArg('flags', 'GLbitfield'),
	GlArg('timeout', 'GLuint64')
])

conn.commit()
conn.close()
