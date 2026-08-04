from ott.utils.template_base import TemplateBase


class BaseTemplate(TemplateBase):
    """ NOTE: thru inheritance, the template lookup routine will now search this class' directory for .mustache templates """

    @classmethod
    def workspace(cls, data):
        return cls.render('workspace.mustache', data)

    @classmethod
    def namespace(cls, data):
        return cls.render('namespace.mustache', data)


if __name__=='__main__':
    data = {'workspace': 'my-workspace'}
    p = BaseTemplate.style_config(data)
    print(p)
