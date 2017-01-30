class ModelSerialize():

    def serialize(self, fields=[]):

        if len(fields) == 0:
            fields = self.default_fields

        response = {}
        for fd in fields:
            # print(fd,self.serializable_value(fd))
            response[fd] = self.serializable_value(fd)
        return response