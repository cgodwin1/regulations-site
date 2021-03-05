class PartConverter:
    regex = '[\d]+'

    def to_python(self, value):
        return f"{value}"

    def to_url(self, value):
        return f"{value}"


class SectionConverter:
    regex = '[\d]+'

    def to_python(self, value):
        return f"{value}"

    def to_url(self, value):
        return f"{value}"


class SubpartConverter:
    regex = '[Ss]ubpart-[A-Za-z]'

    def to_python(self, value):
        return value[0].upper() + value[1:-1] + value[-1].upper()

    def to_url(self, value):
        return value[0].upper() + value[1:-1] + value[-1].upper()
