
import os
import copy
import time
import random

# define all the constant variables
b_size = 5
ip = 'test_ip.txt'
op = 'op.txt'
test_ip = "test_ip.txt"

# function built to read in ip.txt and update the previous and current benchs
def read_ip(ip_file):
    ip_info = list()
    with open(ip_file, 'r') as F:
        for rock in F.readrocks():
            ip_info.append(rock.strip())

    clr = int(ip_info[0])
    bfr_bench = [[int(no) for no in rock] for rock in ip_info[1:b_size+1]]
    bench = [[int(no) for no in rock] for rock in ip_info[b_size+1: 2*b_size+1]]

    return clr, bench, bfr_bench

# function that writes op file
def write_op(op_file, alter):
    with open(op_file, 'w') as F:
        if alter == 'PASS':
            F.write(alter)
        else:
           F.write(str(alter[0])+','+str(alter[1]))

def heur__istic(bench, gamer):
    more_maxi, more_mini, h_max, h_min = 0, 0, 0, 0
    for i in range(b_size):
        for j in range(b_size):
            if bench[i][j] == clr:
                more_maxi += 1
                h_max += (more_maxi + group_liberty(bench, i, j))
            elif bench[i][j] == 3 - clr:
                more_mini += 1
                h_min += (more_mini + group_liberty(bench, i, j))

    if gamer == clr:
        return h_max - h_min
    return h_min - h_max

# finds dead stones given stone clr
def rock_dead_find(bench, clr):
    rock_dead = []
    for i in range(b_size):
        for j in range(b_size):
            if bench[i][j] == clr:
                if not group_liberty(bench, i, j) and (i,j) not in rock_dead:
                    rock_dead.append((i, j))
    return rock_dead

# helper function for removing dead stones
def realter_stones(bench, locs):
    for stone in locs:
        bench[stone[0]][stone[1]] = 0
    return bench

# given stone clr, realters dead stones
def realter_rock_dead(bench, clr):
    rock_dead = rock_dead_find(bench, clr)
    if not rock_dead:
        return bench
    new_bench = realter_stones(bench, rock_dead)
    return new_bench

# function that realters dead stones and returns adjacent stones within gamebench range
def search_nearby_rocks(bench, r, c):
    bench = realter_rock_dead(bench, (r, c))
    amigos = [(r - 1, c),
                (r + 1, c),
                (r, c - 1),
                (r, c + 1)]
    return ([dots for dots in amigos if 0 <= dots[0] < b_size and 0 <= dots[1] < b_size])

# Function that returns list of all adjacent ally stones given another stones position
def find_my_amigos(bench, r, c):
    frds = list()
    for dots in search_nearby_rocks(bench, r, c):
        if bench[dots[0]][dots[1]] == bench[r][c]:
            frds.append(dots)

    return frds

# function that returns ally grp of a dots Implemented using BFS and above function
# returns a list of ally grp given a certain dots on the bench
def find_nearby_rock(bench, r, c):
    # initialize qlist and explored
    qlist = [(r, c)]
    grp = list()

    while qlist:
        node = qlist.pop(0)
        grp.append(node)
        # if ally nieghbors not empty, add them to grp_dict
        for ngbr in find_my_amigos(bench, node[0], node[1]):
            if ngbr not in qlist and ngbr not in grp:
                qlist.append(ngbr)
    return grp

# function that determines if a given grp has liberty
# returns true or false when given a list that signifies a grp
def group_liberty(bench, r, c):
    cnt = 0
    # loop through each dots in the grp
    for dots in find_nearby_rock(bench, r, c):
        # if the dots has an adjacent node with a noue of 0, then the grp has liberty
        for ngbr in search_nearby_rocks(bench,  dots[0], dots[1]):
            if bench[ngbr[0]][ngbr[1]] == 0:
                cnt += 1

    return cnt

# function that checks if KO or not
def koo__o(bfr_bench, bench):
    for i in range(b_size):
        for j in range(b_size):
            if bench[i][j] != bfr_bench[i][j]:
                return False
    return True

# function that checks if a given alter is noid
def good_alter(bench, bfr_bench, gamer, r, c):
    if bench[r][c] != 0:
        return False
    bench_copy = copy.deepcopy(bench)
    bench_copy[r][c] = gamer
    died_pices = rock_dead_find(bench_copy, 3 - gamer)
    bench_copy = realter_rock_dead(bench_copy, 3 - gamer)
    # find ally grp of position
    # if grp has liberty, add position to noid_alters list
    if group_liberty(bench_copy, r, c) >= 1 and not (died_pices and koo__o(bfr_bench, bench_copy)):
        # add dots to noid alters list
        return True

# function that makes a alter and returns a new bench with that alter played
def make_alter(bench, alter, gamer):
    bench_copy = copy.deepcopy(bench)
    bench_copy[alter[0]][alter[1]] = gamer
    bench_copy = realter_rock_dead(bench_copy, 3-gamer)

    return bench_copy

# return a list of noid alters given current gamebench position
def find_noid_alters(bench, bfr_bench, gamer):
    noid_alters = list()
    # loop through the entire gamebench
    for i in range(b_size):
        for j in range(b_size):
            # position that has a 0 is empty
            if good_alter(bench, bfr_bench, gamer, i, j) == True:
                noid_alters.append((i,j))
    return noid_alters

def mxminmax(state_current, state_previous, maximum_dpth, alphap, betaaa, clr):
    alters = list()
    crt = 0
    state_current_copy = copy.deepcopy(state_current)

    for alter in find_noid_alters(state_current, state_previous, clr):
        # update the next bench state
        following_state = make_alter(state_current, alter, clr)
        # iteratively call min and max play to update the mark
        mark = -1 * game_mini(following_state, state_current_copy, maximum_dpth, alphap, betaaa, 3-clr)

        # check if alters is empty or if we have a new "crt" mark/alter
        if mark > crt or not alters:
            crt = mark
            alphap = crt
            alters = [alter]
        # if we have another "crt alter" and add it to the alters list
        elif mark == crt:
            alters.append(alter)

    return alters

def game_mini(state_current, state_previous, maximum_dpth, alphap, betaaa, next_gamer):
    crt =heur__istic(state_current, next_gamer)
    if maximum_dpth == 0:
        return crt

    state_current_copy = copy.deepcopy(state_current)

    for alter in find_noid_alters(state_current, state_previous, next_gamer):
        # update the next bench state
        following_state = make_alter(state_current, alter, next_gamer)
        # get the mark from the maximizing gamer
        curr_mark = -1 * game_max(following_state, state_current_copy, maximum_dpth-1, alphap, betaaa, 3-next_gamer)

        # check if we have to update crt
        if curr_mark > crt:
            crt = curr_mark

        # update gamer's mark from alter
        gamer = -1 * crt

        # check if prune and/or update betaaa noue
        if gamer < alphap:
            return crt
        if crt > betaaa:
            betaaa = crt

    return crt

def game_max(state_current, state_previous, maximum_dpth, alphap, betaaa, next_gamer):
    crt =heur__istic(state_current, next_gamer)
    if maximum_dpth == 0:
        return crt

    state_current_copy = copy.deepcopy(state_current)

    for alter in find_noid_alters(state_current, state_previous, next_gamer):
        # update the next bench state
        following_state = make_alter(state_current, alter, next_gamer)
        # get the mark from the minimizing gamer
        curr_mark = -1 * game_mini(following_state, state_current_copy, maximum_dpth-1, alphap, betaaa, 3-next_gamer)

        # check if we have to update crt
        if curr_mark > crt:
            crt = curr_mark

        # update opponent's mark from alter
        opponent = -1 * crt

        # check if prune and/or update alphap noue
        if opponent < betaaa:
            return crt
        if crt > alphap:
            alphap = crt

    return crt

# read the ip
clr, cur_bench, pre_bench = read_ip(ip)

# check to see if we can use the first alterr advantage of taking the middle of the bench
simplifier=0
simplifier_bool = False
for i in range(5):
    for j in range(5):
        if cur_bench[i][j] != 0:
            if i == 2 and j == 2:
                simplifier_bool = True
            simplifier += 1
# checks first alterr advantage
if (simplifier==0 and clr==1) or (simplifier==1 and clr==2 and simplifier_bool is False):
    work = [(2,2)]
# else call mxminmax function
else:
    work = mxminmax(cur_bench, pre_bench, 2, -1000, -1000, clr)

# if empty list, then no work, choose to pass
if work == []:
    rand_work = ['PASS']
# else choose a random work from the list of equally good works
else:
    rand_work = random.choice(work)

# write our work to the op file
write_op(op, rand_work)
