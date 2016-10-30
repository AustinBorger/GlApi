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

c.execute('''
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

conn.commit()
conn.close()