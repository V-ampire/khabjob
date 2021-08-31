from api.views import public


def setup_routes(app):
    app.router.add_view("public/vacancies", public.Vacancies)
    app.router.add_view("public/vacancies/{id}", public.Vacancies)