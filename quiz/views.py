from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Question, QuizAttempt, Option
import random

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'quiz/subject_list.html', {'subjects': subjects})

@login_required
def take_quiz(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        score = 0
        total = 0
        questions_attempted = []
        
        for key, value in request.POST.items():
            if key.startswith('question_'):
                total += 1
                question_id = int(key.split('_')[1])
                option_id = int(value)
                
                question = Question.objects.get(id=question_id)
                selected_option = Option.objects.get(id=option_id)
                
                if selected_option.is_correct:
                    score += 1
                
                questions_attempted.append({
                    'question': question,
                    'selected_option': selected_option,
                    'is_correct': selected_option.is_correct
                })
        
        # Calculate score as percentage or raw? Let's do percentage.
        final_score = (score / total) * 100 if total > 0 else 0
        
        QuizAttempt.objects.create(
            user=request.user,
            subject=subject,
            score=final_score
        )
        
        # Pass data to result template directly or redirect. 
        # Redirect prevents resubmission, but we need to pass temporary context.
        # For simplicity, we can render the result page directly here.
        return render(request, 'quiz/quiz_result.html', {
            'subject': subject,
            'score': final_score,
            'total_questions': total,
            'correct_answers': score,
            'attempted': questions_attempted
        })
        
    else:
        # Get random questions (e.g., 20)
        all_questions = list(subject.questions.all())
        if len(all_questions) > 20:
            questions = random.sample(all_questions, 20)
        else:
            questions = all_questions
            
        return render(request, 'quiz/quiz_form.html', {'subject': subject, 'questions': questions})
