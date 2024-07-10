from core.models.userinfo import UserInfo


class InfoService:
    @classmethod
    def find(cls, **kwargs):
        return UserInfo.objects.filter(**kwargs)

    @classmethod
    def upsert(cls, email: str, verbs: list[str], names: list[str]):
        obj: UserInfo = cls.find(email=email).first()
        if not obj:
            obj = UserInfo.objects.create(email=email)
        obj.names = names
        obj.verbs = verbs
        obj.save()
        return obj
