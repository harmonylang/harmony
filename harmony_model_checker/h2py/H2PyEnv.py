class H2PyEnv:

    def __init__(self):
        self._parent = None

    def rep(self, **kwargs):
        child = H2PyEnv()
        child._parent = self
        for k, v in kwargs.items():
            setattr(child, k, v)
        return child

    def get(self, name):
        env = self
        while env is not None:
            v = getattr(env, name, None)
            if v is not None:
                return v
            env = env._parent
        return None