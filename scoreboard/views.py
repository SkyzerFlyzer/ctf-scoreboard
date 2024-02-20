import math
import time
from collections import defaultdict

from django.db.models import F
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Flag, Graph, Event, Challenge, FlagSubmission


# Create your views here.

def get_current_event():
    current_time = time.time()
    event_exists = Event.objects.filter(start_time__lt=current_time,
                                        start_time__gt=current_time - F('duration_in_seconds')).exists()
    if event_exists:
        current_event = Event.objects.filter(start_time__lt=current_time,
                                             start_time__gt=current_time - F('duration_in_seconds')).first()
        return current_event
    return None


def login(request):
    if request.method == 'GET':
        if request.session.get('user', None) is not None:
            return redirect('scoreboard:scoreboard')
        return render(request, 'scoreboard/login.html')
    elif request.method == 'POST':
        current_event = get_current_event()
        if current_event is None:
            return render(request, 'scoreboard/error.html', {'error': 'No current event'})
        graph_data = Graph.objects.filter(event=current_event)
        users = set(data.user for data in graph_data)
        if request.POST['username'] in users:
            return render(request, 'scoreboard/error.html', {'error': 'User already exists'})
        request.session['user'] = request.POST['username']
        request.session.modified = True
        # Create a graph data entry for the user
        graph_data = Graph.objects.create(event=current_event, user=request.session['user'], score=0,
                                          time=current_event.start_time)
        graph_data.save()
        return redirect('scoreboard:scoreboard')


def scoreboard(request):
    if request.session.get('user', None) is None:
        return redirect('scoreboard:login')
    if request.method == 'GET':
        current_event = get_current_event()
        if current_event is None:
            request.session['user'] = None
            request.session.modified = True
            most_recent_event = Event.objects.filter(start_time__lt=time.time()).order_by('-start_time').first()
            if most_recent_event is None:
                return render(request, 'scoreboard/error.html', {'error': f"No events have been held"})
            # Get the graph data and find the person with the highest score
            graph_data = Graph.objects.filter(event=most_recent_event)
            players = {}
            for data in graph_data:
                if data.user not in players:
                    players[data.user] = 0
                players[data.user] += data.score
            scores = {}
            for player, score in players.items():
                scores[player] = score
            scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            return render(request, 'scoreboard/previous_event.html', {'scores_leaderboard': scores,
                                                                      'event_name': most_recent_event.name})
        graph_data = Graph.objects.filter(event=current_event)
        players = defaultdict(int)
        for data in graph_data:
            players[data.user] += data.score
        current_time = time.time()
        minutes_passed = math.ceil((current_time - current_event.start_time) / 60)
        player_names = list(players.keys())
        labels = []
        graph_data_score_by_player = {}
        for player in player_names:
            graph_data_score_by_player[player] = []
            for i in range(minutes_passed):
                if i not in labels:
                    labels.append(i)
                graph_data = Graph.objects.filter(event=current_event, user=player,
                                                  time__lte=current_event.start_time + (i * 60))
                graph_data_score_by_player[player].append(sum(data.score for data in graph_data))
        scores = {}
        for player, score in graph_data_score_by_player.items():
            scores[player] = score[-1]
        # sort scores by value descending
        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        return render(request, 'scoreboard/scoreboard.html', {'players': players,
                                                              'graph_data': graph_data_score_by_player,
                                                              'labels': labels, 'scores_leaderboard': scores,
                                                              'user': request.session['user']})
    elif request.method == 'POST':
        # Check the flag submitted is correct
        # Get the flag object from the database
        flags_objects = Flag.objects.all()
        flag_object = None
        new_flag = request.POST.get('flag', None)
        for flag in flags_objects:
            if flag.name == request.POST.get('flag', None):
                flag_object = flag
                break
        if flag_object is None:
            return render(request, 'scoreboard/error.html', {'error': 'Invalid Flag'})
        # Check if the flag is already submitted
        current_flags = request.session.get('flags', {})
        if new_flag in current_flags.values():
            return render(request, 'scoreboard/error.html', {'error': 'Flag already submitted'})
        submit_time = time.time()
        current_flags[submit_time] = new_flag
        request.session['flags'] = current_flags
        request.session.modified = True
        # Save the flag to the database
        graph_data = Graph.objects.create(event=flag_object.event, user=request.session['user'],
                                          score=flag_object.points,
                                          time=submit_time)
        graph_data.save()
        flag_submission = FlagSubmission.objects.create(flag=flag_object, user=request.session['user'], time=submit_time)
        flag_submission.save()
        return render(request, 'scoreboard/success.html',
                      {'success': f'Flag submitted for {flag_object.points} points!'})
    else:
        return redirect('scoreboard:scoreboard')


def challenges(request):
    if request.session.get('user', None) is None:
        return redirect('scoreboard:login')
    if request.method == 'GET':
        current_event = get_current_event()
        if current_event is None:
            return render(request, 'scoreboard/error.html', {'error': 'No current event'})
        challenge_objects = Challenge.objects.filter(event=current_event)
        return render(request, 'scoreboard/challenges.html', {'challenges': challenge_objects})
    return redirect('scoreboard:scoreboard')


def challenge_download(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    file_path = challenge.files.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(challenge.files.name)
    return response


def first_blood(request):
    if request.session.get('user', None) is None:
        return redirect('scoreboard:login')
    if request.method == 'GET':
        current_event = get_current_event()
        if current_event is None:
            return render(request, 'scoreboard/error.html', {'error': 'No current event'})
        bloods = FlagSubmission.objects.filter(flag__event=current_event)
        first_bloods = {}
        for blood in bloods:
            blood_data = {'user': blood.user,
                          'time': blood.time,
                          'challenge_name': blood.flag.challenge,
                          'flag_name': f"Flag {blood.flag.number}"}
            key_name = blood_data['challenge_name'] + ' - ' + blood_data['flag_name']
            if key_name not in first_bloods:
                first_bloods[key_name] = blood_data
            else:
                if blood_data["time"] < first_bloods[key_name]["time"]:
                    first_bloods[blood.flag] = blood_data
        for key, value in first_bloods.items():
            human_time = value['time'] - current_event.start_time
            value["time"] = time.strftime('%H:%M:%S', time.gmtime(human_time))
            value["challenge_name"] = value["challenge_name"].name
        return render(request, 'scoreboard/first_bloods.html', {'first_bloods': first_bloods})
    return redirect('scoreboard:scoreboard')