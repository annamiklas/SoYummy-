from django.db.models import Func

class Levenshtein(Func):
    template = "%(function)s(%(expressions)s, '%(search_term)s', %(ins_cost)d, %(del_cost)d, %(sub_cost)d)"
    function = 'levenshtein'

    def __init__(self, expression, search_term, ins_cost=1, del_cost=1, sub_cost=1, **extras):
        super(Levenshtein, self).__init__(
            expression,
            search_term=search_term,
            ins_cost=ins_cost,
            del_cost=del_cost,
            sub_cost=sub_cost,
            **extras
        )

        
def levenshtein_distance(first, second):
    first_len = len(first)
    second_len = len(second)
    distance = 0    

    if first_len == 0 or second_len == 0:
        distance = max(first_len, second_len)
    else:
        tab = [[0 for col in range(second_len + 1)] for row in range(first_len + 1)]  

        for i in range(0, first_len + 1):
            tab[i][0] = i
        for i in range(1, second_len + 1):
            tab[0][i] = i 
        for i in range(1, first_len + 1):
            for j in range(1, second_len + 1):
                cost = 0 if first[i - 1] == second[j - 1] else 1
                tab[i][j] = min(tab[i - 1][j] + 1, tab[i][j - 1] + 1, tab[i - 1][j - 1] + cost)
                
        distance = tab[first_len][second_len] 
            
    return distance
  


