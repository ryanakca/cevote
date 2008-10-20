from django.shortcuts import render_to_response
from cevote.voting.models import Position

def index(request):
    candidate_position_dict = {}
    for pos in Position.objects.all():
        # Create a dictionary of positions : [ [candidate1, wins?], [candidate2,
        # wins?], ...]
        candidate_position_dict[pos] = []
        for can in pos.candidate_set.all().order_by('-votes'):
            candidate_position_dict[pos].append([can, False])
    for p in candidate_position_dict.keys():
        if candidate_position_dict[p] == []:
            # There aren't any candidates or nobody can win, let's remove
            # the position from the dictionary
            del candidate_position_dict[p]
        else:
        # Set the winners win value to True
            # Use min, because there might be less candidates than the required
            # amount
            for winner in range(min(p.amount_of_electees, \
                                len(candidate_position_dict[p]))):
                candidate_position_dict[p][winner][1] = True
            # If there are ties, set them to True too
            last_tie = p.amount_of_electees
            while (last_tie < len(candidate_position_dict[p])) and \
                  (candidate_position_dict[p][last_tie][0].votes \
                    == candidate_position_dict[p][last_tie - 1][0].votes):
                candidate_position_dict[p][last_tie][1] = True
                last_tie += 1
    return render_to_response('results/index.html', \
        {'candidate_position_dict': candidate_position_dict})
