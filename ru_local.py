from declaration import *
from ru_local import *


def read_file_rooms():
    """ Reading rooms from the file and forming room class elements. """
    single = 0
    two_place = 0
    half_luxe = 0
    luxe = 0
    with open('fund.txt', 'r', encoding='utf8') as f_in:
        rooms = []
        text = f_in.readlines()
        for item in text:
            item.strip('\n')
            element = item.split()
            rooms.append(Room(element[0], element[1], element[2], element[3]))
        for room in rooms:
            if room.type == 'одноместный':
                single += 1
            elif room.type == 'двухместный':
                two_place += 1
            elif room.type == 'полулюкс':
                half_luxe += 1
            elif room.type == 'люкс':
                luxe += 1
    return rooms, single, two_place, half_luxe, luxe


def empty_hotel(rooms):
    """ Getting an empty hotel where for all the rooms the thirty first day is free. """
    occupation = {}
    for room in rooms:
        empty_days = {}
        for day in range(1, 32):
            empty_days[day] = FREE
        occupation[room.number] = empty_days
    return Hotel(occupation)


def variants(rooms):
    """ Creating the dictionary with costs and without food. """
    options = {}
    type_of_room = {'одноместный': 2900.0, 'двухместный': 2300.0, 'полулюкс': 3200.0, 'люкс': 4100.0}
    type_of_comfort = {'стандарт': 1.0, 'стандарт_улучшенный': 1.2, 'апартамент': 1.5}
    for room in rooms:
        options[room.number] = type_of_room[room.type]*type_of_comfort[room.comfort]
    return options


def food(options, rooms):
    """ Formation of tuples with number, food, number of people and type of food. """
    lst = []
    type_of_food = {'без питания': 0.0, 'завтрак': 280.0, 'полупансион': 1000.0}
    for key in options.keys():
        for meal in type_of_food.keys():
            for room in rooms:
                if room.number == key:
                    food = (key, options[key] + type_of_food[meal], int(room.max_people), meal)
                    lst.append(food)
    return lst


def sort(for_sort):
    """ Sorting tuples. """
    order_ = sorted(for_sort, key=lambda x: x[1])
    order__ = list(reversed(order_))
    order = sorted(order__, key=lambda x: x[2])
    return order


def read_file_booking():
    """ Reading guest data file. """
    with open('booking.txt', 'r', encoding='utf-8-sig') as f_in:
        clients = []
        text = f_in.readlines()
        for item in text:
            item.strip('\n')
            element = item.split()
            clients.append(Client(element[0], element[1]+' '+element[2]+' '+element[3], element[4], element[5],
                                  element[6], element[7]))
    return clients


def hotel_filling(sorted_rooms, clients, hotel, rooms, sing, two, half, lux):
    """ Filling the hotel with customers. """
    first_date_in = clients[0].date_in
    last_date_in = clients[len(clients)-1].date_in
    main_date = clients[0].date_in.split('.')[1] + '.' + clients[0].date_in.split('.')[2]
    for day in range(int(first_date_in.split('.')[0]), int(last_date_in.split('.')[0]) + 1):
        count_room = 0
        current_money = 0
        lost_money = 0
        single = 0
        two_place = 0
        half_luxe = 0
        luxe = 0
        for client in clients:
            if day == int(client.date_in.split('.')[0]):
                search_people = int(client.people)
                search_summ = int(client.max_summ)
                search_date = int(client.date.split('.')[0])
                search_days = int(client.days)
                room_res = searching(sorted_rooms, search_people, search_summ, search_date, search_days, hotel,
                                     client.agreement)
                agreement = client.agreement
                print(EQUALLY * 150, '\n', '\n')
                print(BOOKING_REQUEST, '\n', '\n')
                print(client)
                print('\n')
                if room_res != 0:
                    print(FOUND, '\n', '\n')
                    for room in rooms:
                        if room.number == room_res[0][0]:
                            print(room, end='. ')
                            room_type = room.type
                    print(ACTUALLY, search_people, PEOPLE, room_res[0][3], THE_COST, room_res[0][1]*room_res[1],
                          RUBLES_PER_DAY, '\n', '\n')
                    if agreement:
                        print(AGREEMENT, '\n', '\n')
                        count_room += 1
                        current_money += room_res[0][1]*room_res[1] * search_people
                        if room_type == 'одноместный':
                            single += 1
                        elif room_type == 'двухместный':
                            two_place += 1
                        elif room_type == 'полулюкс':
                            half_luxe += 1
                        elif room_type == 'люкс':
                            luxe += 1
                    else:
                        print(REFUSAL, '\n', '\n')
                        lost_money += room_res[0][1]*room_res[1] * search_people
                else:
                    print(NOT_FOUND, '\n', '\n')
                    lost_money += search_summ
        print(EQUALLY * 150, '\n', '\n')
        print(TOTAL + str(day) + DOT + main_date + COLON, '\n', '\n')
        print(NUMBER_OF_BUSY_ROOMS, count_room, '\n', '\n')
        print(NUMBER_OF_AVAILABLE_ROOMS, len(rooms) - count_room, '\n', '\n')
        print(EMPLOYMENT_BY_CATEGORY, '\n', '\n')
        print(SINGLE_ROOM, single, FROM, sing, '\n', '\n')
        print(DOUBLE_ROOM, two_place, FROM, two, '\n', '\n')
        print(JUNIOR_SUITE, half_luxe, FROM, half, '\n', '\n')
        print(LUXURY, luxe, FROM, lux, '\n', '\n')
        print(PERCENTAGE_OF_BUSY_ROOMS, round((count_room / len(rooms)) * 100, 2), ' %', '\n', '\n')
        print(DAILY_INCOME, current_money, RUBLE, '\n', '\n')
        print(LOST_INCOME, lost_money, RUBLE, '\n', '\n')


def searching(sorted_rooms, search_people, search_summ, search_date, search_days, hotel, agreement, percent=1.0):
    """ Searching for a suitable option. """
    switch = 0
    for room in sorted_rooms:
        if search_people == room[2] and search_summ > room[1]:
            if hotel.checking(room[0], search_date) != BUSY:
                switch = [room, percent]
                if agreement:
                    hotel.taken(room[0], search_date, search_days)
                break

    if switch == 0 and search_people < 7:
        return searching(sorted_rooms, search_people+1, search_summ, search_date, search_days, hotel, 0.7)
    return switch


def main():
    """ The main function. """
    rooms, single, two_place, half_luxe, luxe = read_file_rooms()
    hotel = empty_hotel(rooms)
    for_sort = food(variants(rooms), rooms)
    sorted_rooms = sort(for_sort)
    clients = read_file_booking()
    hotel_filling(sorted_rooms, clients, hotel, rooms, single, two_place, half_luxe, luxe)


if __name__ == '__main__':
    main()
