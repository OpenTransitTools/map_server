from ott.utils.template_base import TemplateBase


class Template(TemplateBase):
    """ NOTE: thru inheritance, the template lookup routine will now search this class' directory for .mustache templates """

    @classmethod
    def coverage_store(cls, data):
        return cls.render('coveragestore.mustache', data)

    @classmethod
    def style_config(cls, data):
        return cls.render('style_config.mustache', data)

    @classmethod
    def gwc_layer(cls, data):
        return Template.render('gwc_layer.mustache', data)

    @classmethod
    def layer(cls, data):
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
