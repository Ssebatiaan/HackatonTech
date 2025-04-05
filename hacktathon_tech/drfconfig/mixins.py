class OverrideToPepresentationMixin:
    """
        Update a model instance to presentation.
    """

    def to_representation(self, instance):
        """
        Se sobre escribe el to_representation, para evitar los valores nulos, ya que se remplazan por
         cadenas vacias
        :param instance:
        :return Dict:
        """
        data = super().to_representation(instance)
        keys = [key for key, value in data.items() if value is None]
        data.update({key: '' for key in keys})
        return data

    def compare_values(self, instance, validate_data):
        pass