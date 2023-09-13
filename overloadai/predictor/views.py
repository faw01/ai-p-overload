from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback
import joblib
import json
import csv
from django.http import HttpResponse

model = joblib.load('random_forest_model.joblib')

@csrf_exempt
def predict(request):
    if request.method == "POST":
        data = json.loads(request.body)
        volume = float(data.get("volume", 0))
        reps = float(data.get("reps", 0))
        seconds = float(data.get("seconds", 0))
        
        # Make prediction
        prediction = model.predict([[volume, reps, seconds]])
        
        # Return the prediction as JSON response
        return JsonResponse({"prediction": prediction})

    return render(request, "predictor/index.html")

@csrf_exempt
def store_feedback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        # Extract data
        volume = data.get('volume')
        reps = data.get('reps')
        seconds = data.get('seconds')
        predicted_weight = data.get('predicted_weight')
        actual_weight = data.get('actual_weight')
        feedback = data.get('feedback')
        
        # Store in database
        Feedback.objects.create(
            volume=volume,
            reps=reps,
            seconds=seconds,
            predicted_weight=predicted_weight,
            actual_weight=actual_weight,
            feedback=feedback
        )
        
        return JsonResponse({'status': 'success'})
    return HttpResponse(status=400)

def get_user_data(request):
    workouts = Workout.objects.filter(user=request.user).order_by('date')
    # Convert the QuerySet to a list of dictionaries and return as JSON
    data = [{"date": workout.date, "weight": workout.weight, "sets": workout.sets, "reps": workout.reps_per_set} for workout in workouts]
    return JsonResponse(data, safe=False)

def export_workouts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="workouts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Exercise', 'Weight', 'Sets', 'Reps'])

    workouts = Workout.objects.filter(user=request.user).order_by('date')
    for workout in workouts:
        writer.writerow([workout.date, workout.exercise, workout.weight, workout.sets, workout.reps_per_set])

    return response