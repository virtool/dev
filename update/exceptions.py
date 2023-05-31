class UnrecognizedYAMLTemplate(Exception):
    def __init__(self, value="Invalid template"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NonVirtoolRepository(Exception):
    def __init__(self, value="Repository is not a virtool repository"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NonUpdatableKindType(Exception):
    def __init__(self, value="Unknown image url"):
        self.value = value

    def __str__(self):
        return repr(self.value)
