import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):

    def get(self):
        self.render_template("index.html")

    def post(self):
        podatek = self.request.get("vnos")
        iskana_crka = self.request.get("iskana_crka")
        len_iskana_crka = len(iskana_crka)
        if len_iskana_crka > 1 or len_iskana_crka < 1:
            self.write("Tocno en znak in ne {} znakov".format(len_iskana_crka))
            return

        st_crk = podatek.count(iskana_crka)
        self.write("Stevilo '{0}' v '{1}' je {2}".format(iskana_crka, podatek, st_crk))


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
