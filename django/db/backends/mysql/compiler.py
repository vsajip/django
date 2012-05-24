from django.db.models.sql import compiler
from django.utils.itercompat import izip_longest

class SQLCompiler(compiler.SQLCompiler):
    def resolve_columns(self, row, fields=()):
        values = []
        index_extra_select = len(list(self.query.extra_select.keys()))
        for value, field in izip_longest(row[index_extra_select:], fields):
            if (field and field.get_internal_type() in ("BooleanField", "NullBooleanField") and
                value in (0, 1)):
                value = bool(value)
            values.append(value)
        return row[:index_extra_select] + tuple(values)

class SQLInsertCompiler(compiler.SQLInsertCompiler, SQLCompiler):
    pass

class SQLDeleteCompiler(compiler.SQLDeleteCompiler, SQLCompiler):
    pass

class SQLUpdateCompiler(compiler.SQLUpdateCompiler, SQLCompiler):
    pass

class SQLAggregateCompiler(compiler.SQLAggregateCompiler, SQLCompiler):
    pass

class SQLDateCompiler(compiler.SQLDateCompiler, SQLCompiler):
    pass
