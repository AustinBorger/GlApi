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
		func_name TEXT,
		func_type TEXT
	)
''')

c.execute('''
	CREATE TABLE arguments
	(
		arg_id INT PRIMARY KEY NOT NULL,
		func_id INT,
		arg_order INT,
		arg_name TEXT,
		arg_type TEXT,
		FOREIGN KEY (func_id) REFERENCES functions(func_id)
	)
''')

conn.commit()

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

			arg_order += 1

GlApi('glActiveShaderProgram', 'void', [
	GlArg('pipeline', 'GLuint'),
	GlArg('program', 'GLuint')
])

GlApi('glActiveTexture', 'void', [
	GlArg('texture', 'GLenum')
])

GlApi('glAttachShader', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shader', 'GLuint')
])

GlApi('glBeginConditionalRender', 'void', [
	GlArg('id', 'GLuint'),
	GlArg('mode', 'GLenum')
])

GlApi('glEndConditionalRender', 'void', [])

GlApi('glBeginQuery', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('id', 'GLuint')
])

GlApi('glEndQuery', 'void', [
	GlArg('target', 'GLenum')
])

GlApi('glBeginQueryIndexed', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('id', 'GLuint')
])

GlApi('glEndQueryIndexed', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint')
])

GlApi('glBeginTransformFeedback', 'void', [
	GlArg('primitiveMode', 'GLenum')
])

GlApi('glEndTransformFeedback', 'void', [])

GlApi('glBindAttribLocation', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('name', 'const GLchar *')
])

GlApi('glBindBuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('buffer', 'GLuint')
])

GlApi('glBindBufferBase', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('buffer', 'GLuint')
])

GlApi('glBindBufferRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('buffer', 'GLuint'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr')
])

GlApi('glBindBuffersBase', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('buffers', 'const GLuint *')
])

GlApi('glBindBuffersRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('buffers', 'const GLuint *'),
	GlArg('offsets', 'const GLintptr *'),
	GlArg('sizes', 'const GLintptr *')
])

GlApi('glBindFragDataLocation', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('colorNumber', 'GLuint'),
	GlArg('name', 'const char *')
])

GlApi('glBindFragDataLocationIndexed', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('colorNumber', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('name', 'const char *')
])

GlApi('glBindFramebuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('framebuffer', 'GLuint')
])

GlApi('glBindImageTexture', 'void', [
	GlArg('unit', 'GLuint'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('GLboolean', 'layered'),
	GlArg('layer', 'GLint'),
	GlArg('access', 'GLenum'),
	GlArg('format', 'GLenum')
])

GlApi('glBindImageTextures', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('textures', 'const GLuint *')
])

GlApi('glBindProgramPipeline', 'void', [
	GlArg('pipeline', 'GLuint')
])

GlApi('glBindRenderbuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('renderbuffer', 'GLuint')
])

GlApi('glBindSampler', 'void', [
	GlArg('unit', 'GLuint'),
	GlArg('sampler', 'GLuint')
])

GlApi('glBindSamplers', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('samplers', 'const GLuint *')
])

GlApi('glBindTexture', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('texture', 'GLuint')
])

GlApi('glBindTextures', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('textures', 'const GLuint *')
])

GlApi('glBindTransformFeedback', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('id', 'GLuint')
])

GlApi('glBindVertexArray', 'void', [
	GlArg('array', 'GLuint')
])

GlApi('glBindVertexBuffer', 'void', [
	GlArg('bindingindex', 'GLuint'),
	GlArg('buffer', 'GLuint'),
	GlArg('offset', 'GLintptr'),
	GlArg('stride', 'GLintptr')
])

GlApi('glBlendColor', 'void', [
	GlArg('red', 'GLfloat'),
	GlArg('green', 'GLfloat'),
	GlArg('blue', 'GLfloat'),
	GlArg('alpha', 'GLfloat')
])

GlApi('glBlendEquation', 'void', [
	GlArg('mode', 'GLenum')
])

GlApi('glBlendEquationi', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('mode', 'GLenum')
])

GlApi('glBlendEquationSeparate', 'void', [
	GlArg('modeRGB', 'GLenum'),
	GlArg('modeAlpha', 'GLenum')
])

GlApi('glBlendEquationSeparatei', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('modeRGB', 'GLenum'),
	GlArg('modeAlpha', 'GLenum')
])

GlApi('glBlendFunc', 'void', [
	GlArg('sfactor', 'GLenum'),
	GlArg('dfactor', 'GLenum')
])

GlApi('glBlendFunci', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('sfactor', 'GLenum'),
	GlArg('dfactor', 'GLenum')
])

GlApi('glBlendFuncSeparate', 'void', [
	GlArg('srcRGB', 'GLenum'),
	GlArg('dstRGB', 'GLenum'),
	GlArg('srcAlpha', 'GLenum'),
	GlArg('dstAlpha', 'GLenum')
])

GlApi('glBlendFuncSeparatei', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('srcRGB', 'GLenum'),
	GlArg('dstRGB', 'GLenum'),
	GlArg('srcAlpha', 'GLenum'),
	GlArg('dstAlpha', 'GLenum')
])

GlApi('glBlitFramebuffer', 'void', [
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

GlApi('glBufferData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('ize', 'GLsizeiptr'),
	GlArg('data', 'const GLvoid *'),
	GlArg('usage', 'GLenum')
])

GlApi('glBufferStorage', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('data', 'const GLvoid *'),
	GlArg('flags', 'GLbitfield')
])

GlApi('glBufferSubData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('data', 'const GLvoid *')
])

GlApi('glCheckFramebufferStatus', 'GLenum', [
	GlArg('target', 'GLenum')
])

GlApi('glClampColor', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('clamp', 'GLenum')
])

GlApi('glClear', 'void', [
	GlArg('mask', 'GLbitfield')
])

GlApi('glClearBufferiv', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('value', 'const GLint *')
])

GlApi('glClearBufferuiv', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('value', 'const GLuint *')
])

GlApi('glClearBufferfv', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('value', 'const GLfloat *')
])

GlApi('glClearBufferfi', 'void', [
	GlArg('buffer', 'GLenum'),
	GlArg('drawBuffer', 'GLint'),
	GlArg('depth', 'GLfloat'),
	GlArg('stencil', 'GLint')
])

GlApi('glClearBufferData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

GlApi('glClearBufferSubData', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('internalformat', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

GlApi('glClearColor', 'void', [
	GlArg('red', 'GLfloat'),
	GlArg('green', 'GLfloat'),
	GlArg('blue', 'GLfloat'),
	GlArg('alpha', 'GLfloat')
])

GlApi('glClearDepth', 'void', [
	GlArg('depth', 'GLdouble')
])

GlApi('glClearDepthf', 'void', [
	GlArg('depth', 'GLfloat')
])

GlApi('glClearStencil', 'void', [
	GlArg('s', 'GLint')
])

GlApi('glClearTexImage', 'void', [
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('format', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('data', 'const void *')
])

GlApi('glClearTexSubImage', 'void', [
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

GlApi('glClientWaitSync', 'GLenum', [
	GlArg('sync', 'GLsync'),
	GlArg('flags', 'GLbitfield'),
	GlArg('timeout', 'GLuint64')
])

GlApi('glColorMask', 'void', [
	GlArg('red', 'GLboolean'),
	GlArg('green', 'GLboolean'),
	GlArg('blue', 'GLboolean'),
	GlArg('alpha', 'GLboolean')
])

GlApi('glColorMaski', 'void', [
	GlArg('buf', 'GLuint'),
	GlArg('red', 'GLboolean'),
	GlArg('green', 'GLboolean'),
	GlArg('blue', 'GLboolean'),
	GlArg('alpha', 'GLboolean')
])

GlApi('glCompileShader', 'void', [
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

GlApi('glCopyBufferSubData', 'void', [
	GlArg('readtarget', 'GLenum'),
	GlArg('writetarget', 'GLenum'),
	GlArg('readoffset', 'GLintptr'),
	GlArg('writeoffset', 'GLintptr'),
	GlArg('size', 'GLsizeiptr')
])

GlApi('glCopyImageSubData', 'void', [
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

GlApi('glBindVertexBuffers', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('buffers', 'const GLuint *'),
	GlArg('offsets', 'const GLintptr *'),
	GlArg('strides', 'const GLsizei *')
])

GlApi('glCreateProgram', 'GLuint', [])

GlApi('glCreateShaders', 'GLuint', [
	GlArg('shaderType', 'GLenum')
])

GlApi('glCreateShaderProgramv', 'GLuint', [
	GlArg('type', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('strings', 'const char **')
])

GlApi('glCullFace', 'void', [
	GlArg('mode', 'GLenum')
])

GlApi('glDebugMessageCallback', 'void', [
	GlArg('callback', 'DEBUGPROC'),
	GlArg('userParam', 'void *')
])

GlApi('glDebugMessageControl', 'void', [
	GlArg('source', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('severity', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('ids', 'const GLuint *'),
	GlArg('enabled', 'GLboolean')
])

GlApi('glDebugMessageInsert', 'void', [
	GlArg('source', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('severity', 'GLenum'),
	GlArg('length', 'GLsizei'),
	GlArg('message', 'const char *')
])

GlApi('glDeleteBuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('buffers', 'const GLuint *')
])

GlApi('glDeleteFramebuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('framebuffers', 'GLuint *')
])

GlApi('glDeleteProgram', 'void', [
	GlArg('program', 'GLuint')
])

GlApi('glDeleteProgramPipelines', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('pipelines', 'const GLuint *')
])

GlApi('glDeleteQueries', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'const GLuint *')
])

GlApi('glDeleteRenderbuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('renderbuffers', 'GLuint *')
])

GlApi('glDeleteSamplers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('samplers', 'const GLuint *')
])

GlApi('glDeleteShader', 'void', [
	GlArg('shader', 'GLuint')
])

GlApi('glDeleteSync', 'void', [
	GlArg('sync', 'GLsync')
])

GlApi('glDeleteTextures', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('textures', 'const GLuint *')
])

GlApi('glDeleteTransformFeedbacks', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'const GLuint *')
])

GlApi('glDeleteVertexArrays', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('arrays', 'const GLuint *')
])

GlApi('glDepthFunc', 'void', [
	GlArg('func', 'GLenum')
])

GlApi('glDepthMask', 'void', [
	GlArg('flag', 'GLboolean')
])

GlApi('glDepthRange', 'void', [
	GlArg('nearVal', 'GLdouble'),
	GlArg('farVal', 'GLdouble')
])

GlApi('glDepthRangef', 'void', [
	GlArg('nearVal', 'GLfloat'),
	GlArg('farVal', 'GLfloat')
])

GlApi('glDepthRangeArrayv', 'void', [
	GlArg('first', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('v', 'const GLdouble *')
])

GlApi('glDepthRangeIndexed', 'void', [
	GlArg('index', 'GLuint'),
	GlArg('nearVal', 'GLdouble'),
	GlArg('farVal', 'GLdouble')
])

GlApi('glDetatchShader', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shader', 'GLuint')
])

GlApi('glEnable', 'void', [
	GlArg('cap', 'GLenum')
])

GlApi('glDisable', 'void', [
	GlArg('cap', 'GLenum')
])

GlApi('glEnablei', 'void', [
	GlArg('cap', 'GLenum'),
	GlArg('index', 'GLuint')
])

GlApi('glDisablei', 'void', [
	GlArg('cap', 'GLenum'),
	GlArg('index', 'GLuint')
])

GlApi('glEnableVertexAttribArray', 'void', [
	GlArg('index', 'GLuint')
])

GlApi('glDisableVertexAttribArray', 'void', [
	GlArg('index', 'GLuint')
])

GlApi('glDispatchCompute', 'void', [
	GlArg('num_groups_x', 'GLuint'),
	GlArg('num_groups_y', 'GLuint'),
	GlArg('num_groups_z', 'GLuint')
])

GlApi('glDispatchComputeIndirect', 'void', [
	GlArg('indirect', 'GLintptr')
])

GlApi('glDrawArrays', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'GLint'),
	GlArg('count', 'GLsizei')
])

GlApi('glDrawArraysIndirect', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('indirect', 'const void *')
])

GlApi('glDrawArraysInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('primcount', 'GLsizei')
])

GlApi('glDrawArraysInstancedBaseInstance', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('first', 'GLint'),
	GlArg('count', 'GLsizei'),
	GlArg('primcount', 'GLsizei'),
	GlArg('baseinstance', 'GLuint')
])

GlApi('glDrawBuffer', 'void', [
	GlArg('mode', 'GLenum')
])

GlApi('glDrawBuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('bufs', 'const GLenum *')
])

GlApi('glDrawElements', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const GLvoid *')
])

GlApi('glDrawElementsBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('basevertex', 'GLint')
])

GlApi('glDrawElementsIndirect', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('type', 'GLenum'),
	GlArg('indirect', 'const void *')
])

GlApi('glDrawElementsInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const void *'),
	GlArg('primcount', 'GLsizei')
])

GlApi('glDrawElementsInstancedBaseInstance', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const void *'),
	GlArg('primcount', 'GLsizei'),
	GlArg('baseinstance', 'GLuint')
])

GlApi('glDrawElementsInstancedBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('primcount', 'GLsizei'),
	GlArg('basevertex', 'GLint')
])

GlApi('glDrawElementsInstanceBaseVertexBaseInstance', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('primcount', 'GLsizei'),
	GlArg('basevertex', 'GLint'),
	GlArg('baseinstance', 'GLuint')
])

GlApi('glDrawRangeElements', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('start', 'GLuint'),
	GlArg('end', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'const GLvoid *')
])

GlApi('glDrawRangeElementsBaseVertex', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('start', 'GLuint'),
	GlArg('end', 'GLuint'),
	GlArg('count', 'GLsizei'),
	GlArg('type', 'GLenum'),
	GlArg('indices', 'GLvoid *'),
	GlArg('basevertex', 'GLint')
])

GlApi('glDrawTransformFeedback', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint')
])

GlApi('glDrawTransformFeedbackInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('instancecount', 'GLsizei')
])

GlApi('glDrawTransformFeedbackStream', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('stream', 'GLuint')
])

GlApi('glDrawTransformFeedbackStreamInstanced', 'void', [
	GlArg('mode', 'GLenum'),
	GlArg('id', 'GLuint'),
	GlArg('stream', 'GLuint'),
	GlArg('instancecount', 'GLsizei')
])

GlApi('glFenceSync', 'GLsync', [
	GlArg('condition', 'GLenum'),
	GlArg('flags', 'GLbitfield')
])

GlApi('glFinish', 'void', [])

GlApi('glFlush', 'void', [])

GlApi('glFlushMappedBufferRange', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('offset', 'GLintptr'),
	GlArg('length', 'GLsizeiptr')
])

GlApi('glFramebufferParameteri', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('pname', 'GLenum'),
	GlArg('param', 'GLint')
])

GlApi('glFramebufferRenderbuffer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('renderbuffertarget', 'GLenum'),
	GlArg('renderbuffer', 'GLuint')
])

GlApi('glFramebufferTexture', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

GlApi('glFramebufferTexture1D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('textarget', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

GlApi('glFramebufferTexture2D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('textarget', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint')
])

GlApi('glFramebufferTexture3D', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('textarget', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('layer', 'GLint')
])

GlApi('glFramebufferTextureLayer', 'void', [
	GlArg('target', 'GLenum'),
	GlArg('attachment', 'GLenum'),
	GlArg('texture', 'GLuint'),
	GlArg('level', 'GLint'),
	GlArg('layer', 'GLint')
])

GlApi('glFrontFace', 'void', [
	GlArg('mode', 'GLenum')
])

GlApi('glGenBuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('buffers', 'GLuint *')
])

GlApi('glGenerateMipmap', 'void', [
	GlArg('target', 'GLenum')
])

GlApi('glGenFramebuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('id', 'GLuint *')
])

GlApi('glGenProgramPipelines', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('pipelines', 'GLuint')
])

GlApi('glGenQueries', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'GLuint *')
])

GlApi('glGenRenderbuffers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('renderbuffers', 'GLuint *')
])

GlApi('glGenSamplers', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('samplers', 'GLuint *')
])

GlApi('glGenTextures', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('textures', 'GLuint *')
])

GlApi('glGenTransformFeedbacks', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('ids', 'GLuint *')
])

GlApi('glGenVertexArrays', 'void', [
	GlArg('n', 'GLsizei'),
	GlArg('arrays', 'GLuint *')
])

GlApi('glGetBooleanv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLboolean *')
])

GlApi('glGetDoublev', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLdouble *')
])

GlApi('glFloatv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLfloat *')
])

GlApi('glGetIntegerv', 'void', [
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

GlApi('glGetInteger64v', 'void', [
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

GlApi('glGetActiveAtomicCounterBufferiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('bufferIndex', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

GlApi('glGetActiveAttrib', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('size', 'GLint *'),
	GlArg('type', 'GLenum *'),
	GlArg('name', 'GLchar *')
])

GlApi('glGetActiveSubroutineName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('bufsize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('name', 'GLchar *')
])

GlApi('glGetActiveSubroutineUniformiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('values', 'GLint *')
])

GlApi('glGetActiveSubroutineUniformName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('shadertype', 'GLenum'),
	GlArg('index', 'GLuint'),
	GlArg('bufsize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('name', 'GLchar *')
])

GlApi('glGetActiveUniform', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('index', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('size', 'GLint *'),
	GlArg('type', 'GLenum *'),
	GlArg('name', 'GLchar *')
])

GlApi('glGetActiveUniformBlockiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformBlockIndex', 'GLuint'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

GlApi('glGetActiveUniformBlockName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformBlockIndex', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('uniformBlockName', 'GLchar *')
])

GlApi('glGetActiveUniformName', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformIndex', 'GLuint'),
	GlArg('bufSize', 'GLsizei'),
	GlArg('length', 'GLsizei *'),
	GlArg('uniformName', 'GLchar *')
])

GlApi('glGetActiveUniformsiv', 'void', [
	GlArg('program', 'GLuint'),
	GlArg('uniformCount', 'GLsizei'),
	GlArg('uniformIndices', 'const GLuint *'),
	GlArg('pname', 'GLenum'),
	GlArg('params', 'GLint *')
])

conn.commit()
conn.close()