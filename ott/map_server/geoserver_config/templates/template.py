from ott.utils.template_base import TemplateBase


class Template(TemplateBase):
    """ NOTE: thru inheritance, the template lookup routine will now search this class' directory for .mustache templates """

    @classmethod
    def data_store(cls, data):
        """ call the stores template"""
        return cls.render('stores.mustache', data)

    @classmethod
    def style_config(cls, data):
        """ call the style config template"""
        return cls.render('style_config.mustache', data)

    @classmethod
    def feature_type(cls, data):
        """ call the featuretype template"""
        return Template.render('feature_type.mustache', data)

    @classmethod
    def layer(cls, data):
        """ call the layer template"""
        return Template.render('layer.mustache', data)

    @classmethod
    def layer_group(cls, data):
        """ call the layergroup template"""
        return Template.render('layer_group.mustache', data)


def main():
    # bin/python ott/map_server/geoserver_config/templates/template.py

    data = {'id': 'FX', 'name': 'Frank X', 'type': 'sub-human', 'path': 'crooked'}
    #p = Template.render('style_config', data)
    #p = Template.render('style_config.mustache', data)
    #p = Template.render('ott/map_server/geoserver_config/templates/style_config', data)
    #p = Template.render('id {{id}} ... name {{name}}', data)
    p = Template.style_config(data)
    print(p)


if __name__=='__main__':
    main()
