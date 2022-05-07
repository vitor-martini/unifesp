from pickle import TRUE
import random
import math
import copy

def intra_route_swap(route, point_one_index, point_one_value, point_two_index, point_two_value):     
    route[point_one_index] = point_two_value    
    route[point_two_index] = point_one_value   
              
def intra_route_shift(route, point_one_value, point_two_index):  
    route.remove(point_one_value)
    route.insert(point_two_index, point_one_value)

def inter_route_swap(route_one, route_two, point_one_index, point_one_value, point_two_index, point_two_value):  
    route_one[point_one_index] = point_two_value
    route_two[point_two_index] = point_one_value

def inter_route_shift(route_one, route_two, point_one_value, point_two_index): 
    route_one.remove(point_one_value)
    route_two.insert(point_two_index, point_one_value)

def random_route(routes):
    # Sorteia uma das rotas que tenha pelo menos dois pontos além da garagem
    route_index = random.randint(0, len(routes) - 1)
    while len(routes[route_index]) <= 2:
        route_index = random.randint(0, len(routes) - 1)
    return route_index

def random_route_two(routes, route_one_index):    
    route_two_index = route_one_index
    while(route_one_index == route_two_index):
        route_two_index = random.randint(0, len(routes) - 1) # Sorteia uma rota, diferente da primeira
    return route_two_index

def random_point(point_one_index, routes, route_index):
    point_two_index = point_one_index
    while point_two_index == point_one_index:
        point_two_index = random.randint(1, len(routes[route_index]) - 1) # Sorteia um outro ponto, diferente do primeiro     
    point_two_value = routes[route_index][point_two_index]
    return point_two_index, point_two_value

def isOnlyDepot(routes, route_index):
    len(routes[route_index]) <= 1

def random_neighbor(routes):    
    routes_copy = copy.deepcopy(routes)
    option = random.randint(0, 3) # Sorteia uma das operações
    route_one_index = random_route(routes)
    point_one_index = random.randint(1, len(routes[route_one_index]) - 1) # Sorteia um ponto da rota selecionada
    point_one_value = routes[route_one_index][point_one_index]
    
    # Intra rota
    if option <= 1: 
        point_two_index, point_two_value = random_point(point_one_index, routes, route_one_index)  
        if option == 0:
            intra_route_swap(routes_copy[route_one_index], point_one_index, point_one_value, point_two_index, point_two_value)
            
        if option == 1:
            intra_route_shift(routes_copy[route_one_index], point_one_value, point_two_index)
    
    # Inter rota
    if option > 1:
        route_two_index = random_route_two(routes, route_one_index)        
        if isOnlyDepot(routes, route_two_index): # Caso a rota 2 sorteada só tenha a garagem, então só é possível fazer o shift
            point_two_index = 1
            option = 3
        else:
            point_two_index = random.randint(1, len(routes[route_two_index]) - 1) # Sorteia um ponto da rota 2  
            point_two_value = routes[route_two_index][point_two_index]          

        if option == 2:
            inter_route_swap(routes_copy[route_one_index], routes_copy[route_two_index], point_one_index, point_one_value, point_two_index, point_two_value)
        
        if option == 3:
            inter_route_shift(routes_copy[route_one_index], routes_copy[route_two_index], point_one_value, point_two_index)
    
    return routes_copy

def generate_neighbor(instance, S):   
    S_neighbor = random_neighbor(S)
    fo_neighbor = instance.calculate_FO(S_neighbor)

    return S_neighbor, fo_neighbor

def SA(instance, T0, SAMax, alpha):
    S = copy.deepcopy(instance.current_solution)
    S_best = copy.deepcopy(S)
    fo_best = instance.current_solution_fo
    iterations = 0
    T = T0
    while T > 0.0001:
        while iterations < SAMax:
            iterations += 1
            S_neighbor, fo_neighbor = generate_neighbor(instance, S) 
            fo_S = instance.calculate_FO(S)
            delta = fo_neighbor - fo_S

            if delta <= 0:
                S = copy.deepcopy(S_neighbor)
                fo_S = fo_neighbor
                if fo_neighbor < fo_best:
                    S_best = copy.deepcopy(S_neighbor)
                    fo_best = fo_neighbor
                    instance.add_best_solution(fo_best, S_best)
            else:
                x = random.uniform(0, 1)
                if x < math.exp(-delta/T):                    
                    S = copy.deepcopy(S_neighbor)    
                    fo_S = fo_neighbor            

        print(T, fo_S, fo_best)
        T = T * alpha
        iterations = 0





