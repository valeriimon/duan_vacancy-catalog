from random import randint, sample, choice

from django.core.management import BaseCommand, CommandError
from faker import Faker

from main.models import JobPosition, JobSkill
from resume.models import Resume
from user.models import User, UserRole, REGIONS, Company, EMPLOYMENT_TYPE
from vacancy.models import Vacancy


class Command(BaseCommand):
    help = 'Information of our command generate.'
    job_positions: list
    job_skills: list
    job_skills_sample = [
        "Комунікабельність", "Лідерство", "Робота в команді", "Критичне мислення",
        "Управління часом", "Креативність", "Гнучкість", "Емпатія",
        "Розв'язання проблем", "Ділове спілкування", "Організованість",
        "Управління стресом", "Мультизадачність", "Переговори",
        "Планування проєктів", "Аналітичні здібності", "Презентаційні навички",
        "Досвід користувача (UX)", "Візуальний дизайн", "Тестування програмного забезпечення",
        "Team management", "Public speaking", "Critical thinking", "Python programming",
        "JavaScript development", "UI/UX Design", "SEO Optimization",
        "Database management", "Networking", "Data analysis", "Agile methodology",
        "Копірайтинг", "Дизайн презентацій", "Інноваційне мислення",
        "Маркетинг у соціальних мережах", "Фінансовий аналіз", "Технічна підтримка",
        "DevOps", "Cloud computing", "Machine Learning", "Artificial Intelligence",
        "Ведення документації", "Контент-менеджмент", "Проєктний менеджмент",
        "Обробка даних", "Робота з клієнтами", "Глибокий аналіз даних",
        "Front-end Development", "Back-end Development", "Cybersecurity"
    ]

    def add_arguments(self, parser):
        parser.add_argument('total-employers', type=int, help='Кількість')
        parser.add_argument('total-job-seekers', type=int, help='Кількість')
        parser.add_argument('max-resumes-per-user', type=int, help='')
        parser.add_argument('max-vacancies-per-user', type=int, help='')

    def handle(self, *args, **kwargs):
        total_employers = kwargs['total-employers']
        total_job_seekers = kwargs['total-job-seekers']
        if total_employers or total_job_seekers:
            self._preset_dependencies()

        if total_employers:
            users = self.create_employers(total_employers)
            max_vacancies_per_user = kwargs['max-vacancies-per-user'] or 0
            if max_vacancies_per_user > 0 and len(users):
                self.create_vacancies(randint(1, max_vacancies_per_user), users)

        if total_job_seekers:
            users = self.create_job_seekers(total_job_seekers)
            max_resumes_per_user = kwargs['max-resumes-per-user'] or 0
            if max_resumes_per_user > 0 and len(users):
                self.create_resumes(randint(1, max_resumes_per_user), users)

    def _preset_dependencies(self):
        self.job_positions = list(JobPosition.objects.all())
        if list(self.job_positions) == 0:
            for i in range(50):
                f = self._get_faker()
                p = JobPosition.objects.create(title=f.job())
                self.job_positions.append(p)

        self.job_skills = list(JobSkill.objects.all())
        if len(self.job_skills) == 0:
            skills = map(lambda sk_sample: JobSkill(name=sk_sample), self.job_skills_sample)
            skills = JobSkill.objects.bulk_create(skills)
            self.job_skills = list(skills)

    def create_employers(self, count):
        users = self._create_users(UserRole.EMPLOYER, count)
        for u in users:
            self._create_company(u)

        return users

    def create_job_seekers(self, count):
        return self._create_users(UserRole.JOB_SEEKER, count)

    def create_vacancies(self, count, users):
        for user in users:
            for i in range(count):
                print(f'Створення вакансії {i+1}')
                self._create_vacancy(user)

    def create_resumes(self, count, users):
        for user in users:
            for i in range(count):
                print(f'Створення резюме {i+1}')
                self._create_resume(user)

    def _create_users(self, role: UserRole, count):
        users = []
        for i in range(count):
            print(f'Створення юзера {i+1}')
            u = self._create_user(role)
            users.append(u)

        return users


    def _create_user(self, role: UserRole):
        try:
            f = self._get_faker()
            u = User(
                username=f.user_name(),
                email=f.email(domain='d.com'),
                age=randint(18, 80),
                region=self._get_random_region()
            )
            u.set_password('123')
            u.save()
            u.assign_role(role)
        except Exception as ex:
            print(f'Помилка створення юзера {ex}')
        else:
            print(f'Юзера створено: Ел.пошта - {u.email}, роль - {role}')
            return u

    def _create_company(self, created_by):
        try:
            f = self._get_faker()
            c = Company(
                name=f.company(),
                address_text=f.address(),
                region=choice(REGIONS)[0],
                phone_number=f.phone_number(),
                employees_count=randint(1, 1000),
                created_by=created_by
            )
            c.save()
        except Exception as ex:
            print(f'Помилка створення компанії {ex}')
        else:
            print(f'Компанія створена: Назва {c.name}')
            return c


    def _create_resume(self, created_by):
        try:
            f = self._get_faker()
            r = Resume(
                position=self._get_random_position(),
                employment_type=self._get_random_employment_type(),
                salary=f'{randint(10000, 100000)} грн',
                description=''.join(f.sentences(10)),
                region=self._get_random_region(),
                phone_number=f.phone_number(),
                email=f.email(),
                created_by=created_by
            )
            r.save()
            r.skills.add(*self._get_random_job_skills())
        except Exception as ex:
            print(f'Помилка створення резюме {ex}')
        else:
            print(f'Резюме створено: Позиція {r.position.title}')
            return r

    def _create_vacancy(self, created_by):
        try:
            f = self._get_faker()
            v = Vacancy(
                position=self._get_random_position(),
                employment_type=self._get_random_employment_type(),
                salary=f'{randint(10000, 100000)} грн',
                description=''.join(f.sentences(10)),
                phone_number=f.phone_number(),
                email=f.email(),
                created_by=created_by
            )
            v.save()
            v.skills.add(*self._get_random_job_skills())
        except Exception as ex:
            print(f'Помилка створення вакансії {ex}')
        else:
            print(f'Вакансія створена: Позиція {v.position.title}')
            return v

    def _get_faker(self) -> Faker:
        return Faker('uk_UA')

    def _get_random_position(self):
        return self.job_positions[randint(0, len(self.job_positions) - 1)]

    def _get_random_job_skills(self):
        return sample(self.job_skills, k=randint(0, len(self.job_skills) - 1))

    def _get_random_employment_type(self):
        return choice(EMPLOYMENT_TYPE)[0]

    def _get_random_region(self):
        return choice(REGIONS)[0]