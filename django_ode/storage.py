from pipeline.storage import PipelineCachedStorage


class Storage(PipelineCachedStorage):
    def hashed_name(self, name, content=None):
        if name.startswith('zinnia/'):
            # Zinnia's JavaScript doesn't work with hashed filenames, so we
            # don't hash its filenames.
            return name
        else:
            return super(Storage, self).hashed_name(name, content)
