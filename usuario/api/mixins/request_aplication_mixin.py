class RequestAplicationMixin(object):

    def obtain_user_type(self):
        #user = get_user_model().objects.get(correo=self.request.data[get_user_model().USERNAME_FIELD])
        return {"tipo_usuario":"Usuario dashboard_udec"}