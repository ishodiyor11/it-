from django.core.management.base import BaseCommand
from quiz.models import Subject, Question, Option
import random

class Command(BaseCommand):
    help = 'Seeds database with subjects and questions'

    def handle(self, *args, **kwargs):
        subjects_data = {
            'HTML': ['Tags', 'Attributes', 'Forms', 'Tables', 'Semantic', 'Canvas', 'SVG', 'Video', 'Audio', 'Links'],
            'CSS': ['Selectors', 'Box Model', 'Flexbox', 'Grid', 'Colors', 'Fonts', 'Animations', 'Media Queries', 'Transform', 'Variables'],
            'JavaScript': ['Variables', 'Functions', 'Arrays', 'Objects', 'DOM', 'Events', 'ES6', 'Promises', 'Async/Await', 'Classes'],
            'Python': ['Variables', 'Lists', 'Dictionaries', 'Functions', 'Classes', 'Modules', 'File I/O', 'Exceptions', 'Decorators', 'Generators']
        }

        difficulties = ['beginner', 'intermediate', 'advanced']

        for sub_name, topics in subjects_data.items():
            subject, created = Subject.objects.get_or_create(name=sub_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created subject: {sub_name}'))

            # Generate 200 questions
            count = 0
            existing = Question.objects.filter(subject=subject).count()
            needed = 200 - existing
            
            if needed <= 0:
                self.stdout.write(f'{sub_name} already has 200+ questions.')
                continue

            self.stdout.write(f'Generating {needed} questions for {sub_name}...')

            for i in range(needed):
                topic = random.choice(topics)
                diff = random.choice(difficulties)
                content = f"{sub_name} Question {existing + i + 1}: What controls the behavior of {topic}?"
                
                q = Question.objects.create(
                    subject=subject,
                    content=content,
                    difficulty=diff
                )
                
                # Options
                correct_opt = random.randint(0, 3)
                for j in range(4):
                    is_correct = (j == correct_opt)
                    Option.objects.create(
                        question=q,
                        content=f"Option {j+1} for {topic}",
                        is_correct=is_correct
                    )
                
            self.stdout.write(self.style.SUCCESS(f'Successfully seeded {sub_name}'))
