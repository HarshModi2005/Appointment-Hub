from django.core.management.base import BaseCommand
from professionals.models import ProfessionalCategory

class Command(BaseCommand):
    help = 'Set up initial professional categories and sample data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial professional categories...')
        
        categories = [
            {
                'name': 'Accountant',
                'description': 'Certified public accountants providing tax preparation, bookkeeping, and financial statement services.',
                'icon': 'fas fa-calculator'
            },
            {
                'name': 'Financial Advisor',
                'description': 'Licensed financial advisors offering investment planning, retirement planning, and wealth management services.',
                'icon': 'fas fa-chart-line'
            },
            {
                'name': 'Tax Consultant',
                'description': 'Tax specialists providing tax planning, preparation, and consultation services for individuals and businesses.',
                'icon': 'fas fa-file-invoice-dollar'
            },
            {
                'name': 'Business Consultant',
                'description': 'Business strategy consultants helping with business planning, operations, and growth strategies.',
                'icon': 'fas fa-briefcase'
            },
            {
                'name': 'Insurance Advisor',
                'description': 'Insurance professionals providing life, health, property, and business insurance consultation.',
                'icon': 'fas fa-shield-alt'
            },
            {
                'name': 'Investment Advisor',
                'description': 'Investment specialists offering portfolio management, asset allocation, and investment strategy services.',
                'icon': 'fas fa-coins'
            }
        ]
        
        created_count = 0
        for category_data in categories:
            category, created = ProfessionalCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        ) 