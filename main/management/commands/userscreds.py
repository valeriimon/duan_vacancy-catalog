import textwrap

from django.core.management import BaseCommand, CommandError
from user.models import User, UserRole
from django.db.models import Q

class Command(BaseCommand):
    help = 'Допомагає подивитись доступи юзерів після генерації даних'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, help='Вивід лімітованої кількості юзерів')
        parser.add_argument('--with_content_only', type=bool, help='Вивід тих юзерів, у яких є або резюме, або вакансія')
        parser.add_argument('--specific', type=str, help='Вивід специфічного юзера вказавши або юзернейм, або ел.пошту')

    def handle(self, *args, **kwargs):
        specific = kwargs['specific']
        if specific:
            self.print_specific_user(specific)
            return

        limit = kwargs['limit']
        if limit and limit > 0:
            with_content_only = kwargs['with_content_only']
            self.print_users(limit, with_content_only)

        CommandError('No arguments passed')


    def print_specific_user(self, term: str):
        user = User.objects.filter(
            Q(email=term) | Q(username=term)
        )
        if not user:
            print(f'Юзер не знайден для {term}')

        self._print_user_info(user)

    def print_users(self, limit, with_content_only):
        def get_qs(m):
            if with_content_only:
                return m.objects.filter(
                    Q(my_resumes__gt=0) | Q(my_vacancies__gt=0)
                )
            return m.objects

        users = get_qs(User).order_by('?').all()[:limit]
        for user in users:
            self._print_user_info(user)

    def _print_user_info(self, user):
        role = 'Роботодавець' if user.is_employer() else 'Шукач'
        output = textwrap.dedent(f"""
            ----------------------\n
            Eл.пошта: {user.email}\n
            Юзернейм: {user.username}\n
            Пароль: 123\n
            Роль: {role}\n
        """)
        print(output)


