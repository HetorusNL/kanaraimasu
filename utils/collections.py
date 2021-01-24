class Collections:
    _collections = {}

    @classmethod
    def register(cls, obj_type, obj):
        if not cls._collections.get(obj_type):
            cls._collections[obj_type] = []
        cls._collections[obj_type].append(obj)

    @classmethod
    def reapply_theme(cls):
        for obj_type, obj_list in cls._collections.items():
            for obj in obj_list:
                obj.reapply_theme()
