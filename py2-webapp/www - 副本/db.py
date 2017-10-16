# db.py
import threading




class _Engine(object):
	def __init__(self,connect):
		self._connect = connect
	def connect(self):
		return self._connect()

engine = None

class _DbCtx(threading.local):
	def __init__(self):
		self.connection = None
		self.transcations = 0

	def is_init(self):
		return not self.connection is None

	def init(self):
		self.connection = _LasyConnection()
		self.transcations = 0

	def cleanup(self):
		self.connection.cleanup()
		self.connection = None

	def cursor(self):
		return self.connection.cursor()

_db_ctx = _DbCtx()


class _ConnectionCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_cleanup = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_cleanup = True
		return self

	def __exit__(self, exctype, excvalue, traceback):
		global _db_ctx
		if self.should_cleanup:
			_db_ctx.cleanup()

def connection():
	return _ConnectionCtx()


class _TranscationCtx(object):
	def __enter__(self):
		global _db_ctx
		self.should_close_conn = False
		if not _db_ctx.is_init():
			_db_ctx.init()
			self.should_close_conn = True
		_db_ctx.transcations = _db_ctx.transcations + 1
		return self

	def __exit__(self, exctype,excvalue,traceback):
		global _db_ctx
		_db_ctx.transcations = _db_ctx.transcations -1
		try:
			if _db_ctx.transcations == 0:
				if exctype is None:
					self.commit()
				else:
					self.rollback()
		finally:
			if self.should_close_conn:
				_db_ctx.cleanup()

	
	def commit(self):
		global _db_ctx
		try:
			_db_ctx.connection.commit()
		except:
			_db_ctx.connection.rollback()
			raise

	def rollback(self):
		global _db_ctx
		_db_ctx.connection.rollback()


