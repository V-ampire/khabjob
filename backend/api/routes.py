"""Set up API routes."""
from api.views import public, private, auth, search


def setup_routes(app):
    """Set up API routes."""
    app.router.add_view('/public/vacancies', public.Vacancies, name='vacancy_public_list')
    app.router.add_view('/public/vacancies/{id}', public.Vacancies, name='vacancy_public_detail')
    
    app.router.add_view('/search/vacancies', search.SearchVacancies, name='search_vacancies')

    app.router.add_view('/private/vacancies', private.Vacancies, name='vacancy_private_list')
    app.router.add_view('/private/vacancies/{id}', private.Vacancies, name='vacancy_private_detail')
    
    app.router.add_view('/auth/login', auth.LoginView, name='login')
    app.router.add_view('/auth/logout', auth.LogoutView, name='logout')
    app.router.add_view('/auth/reset_password', auth.ResetPasswordView, name='reset_password')
    