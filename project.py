from pprint import pprint
import random
import movie_storage


def main():
    """main funciton that is calling all the
    functions such as add, delete,update, soritng,etc by the respective commandas."""
    # dictionary of all the functions on different commands
    command_dic = {"1": list_all_movies, "2": movie_storage.add_movie,
                   "3": movie_storage.delete_movie, "4": movie_storage.update_movie,
                   "5": stats, "6": random_movie, "7": search_movie,
                   "8": sorted_by_rating, "9": generate_website}
    while True:
        menu_list()
        movies_new = movie_storage.list_movies()
        try:
            choice = input(" Enter choice (0-9) : ")
            if choice == "0":
                print("Bye!")
                break

            command_dic[choice](movies_new)
        except Exception as e:
            print(f"The error is :{e}. The value is not an integer between 0-9, please enter the value between 0-9")


def list_all_movies(movies):
    """Function to print all the movies with rating and year"""
    count = 0
    for movie in movies.items():
        print(f"{count + 1}. {movie[0]}: {movie[1]['year']}, rating-{movie[1]['Rating']}")
        count += 1
    print(f"Total number of the movies is {count}")


# function to print the mwnu list.
def menu_list():
    """Function to print the menu of all the commands """
    print("***********************************************")
    print("** Enter the number from the command  **  ")
    print("Menu : ")
    print("0. Exit")
    print("1. List Movies")
    print("2. Add movies")
    print("3. Delete movies")
    print("4. Update movies")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search  movie ")
    print("8. Movies sorted by rating")
    print("9. Generate Website")


# function to get the statistics of values in dictionary , and finding the best and worst movie.
def stats(movies):
    """Function to get average rating , median,
     the best movie and worst movie
      according to rating"""
    movies = movie_storage.list_movies()
    value_list = list(movies.values())
    for item in movies.items():
        if item[1]["Rating"] == "N/A":
            movies[item[0]]["Rating"] = 5
    avg_rating = 0
    rating_list = []
    for i in value_list:
        avg_rating += float(i["Rating"])
        rating_list.append(i["Rating"])
    print(f"The average rating is {round(avg_rating / len(value_list), 2)}")
    if len(value_list) % 2 != 0:
        median_rating = rating_list[int((len(rating_list) + 1) / 2)]
        print(f"Median rating is {median_rating}")
    else:
        median_rating = (rating_list[int((len(rating_list)) / 2)] + rating_list[int(((len(rating_list)) / 2) + 1)]) / 2
        print(f"Median rating is {median_rating}")

    list2 = list(movies.items())
    sorted_list = sorted(list2, key=lambda pair: float(pair[1]["Rating"]))

    print(f"The best movie is : {sorted_list[-1][0]} ->({sorted_list[-1][1]['year']}) {sorted_list[-1][1]['Rating']}* ")
    print(f"The worst movie is : {sorted_list[0][0]} -> ({sorted_list[0][1]['year']} ) {sorted_list[0][1]['Rating']}* ")


# function to get the random movie from the dictionary
def random_movie(movies):
    """To get the random movie from the movie json file."""
    movies = movie_storage.list_movies()
    key_list = list(movies.keys())
    value_list = list(movies.values())
    random_m = random.choice(key_list)
    index = 0
    index = key_list.index(random_m)
    random_r = value_list[index]
    print(f""" The random movie is :
     {random_m} --> year: {random_r['year']}
    rating: {random_r['Rating']}""")


# function to search the movies by entering the part of a movie
def search_movie(movies):
    """to search the movie by key word and display all the movies that contain that keywords"""

    key_list = list(movies.keys())
    value_list = list(movies.values())
    search_movie_string = input("Enter the part of a movie name :")
    str1 = search_movie_string.lower()
    index = 0
    for key in key_list:
        if str1 in key.lower():
            index = key_list.index(key)
            print(f"{key} : {value_list[index]['year']},Rating-{value_list[index]['Rating']}")


# function to sort the dictionary in descending order
def sorted_by_rating(movies):
    """To sort the movie list form the json file on the basis of ratings """
    movies = movie_storage.list_movies()
    for item in movies.items():
        if item[1]["Rating"] == "N/A":
            movies[item[0]]["Rating"] = 5
    list2 = list(movies.items())
    sorted_list = sorted(list2, key=lambda pair: float(pair[1]["Rating"]), reverse=True)
    print("***THE List of MOVIES in Descending order : ***")
    for item in sorted_list:
        pprint(f" {item[0]} ({item[1]['year']}), {item[1]['Rating']}*")


def website_code(movies):
    """html code for adding title, poster and year into the string format
        and returning the html code as output"""
    html_code = " "
    for movie in movies.items():
        title = movie[0]
        year = movie[1]["year"]
        rating = movie[1]["Rating"]
        html_code += '<li>\n <div class="movie">\n'
        note = " "
        if "note" in movie[1].keys():
            note = movie[1]["note"]

        if "Poster" in movie[1]:
            image = movie[1]["Poster"]
            html_code += f"""<a href="https://www.omdbapi.com/" >
                         <img title="{note}"  class="movie-poster" src = {image} />
                         </a>\n"""
        else:
            html_code += f"""<a href="https://www.omdbapi.com/" >
                        <img title="{note}" class="movie-poster" src = " " />
                          </a>\n"""
        html_code += f' <div class="movie-title"> {title}</div>\n'
        html_code += f' <div class="movie-year"> {year}</div>\n'
        html_code += f' <div class="movie-year"> <mark>{rating}</mark></div>\n'
        html_code += '</div> \n </li>\n'
    return html_code


def generate_website(movies):
    """replacing the html code with the format string and writing it into a html file
    and thus generating the website"""

    website_title = "Masterschool`s Movie App"
    output = website_code(movies)

    with open("_static/index_template.html", "r") as file_object:
        data = file_object.read()

    data = data.replace("__TEMPLATE_TITLE__", website_title)
    data = data.replace("__TEMPLATE_MOVIE_GRID__", output)

    with open("_static/index.html", "w") as f:
        f.write(data)
    print("Website was generated successfully")


# Dunder main
if __name__ == "__main__":
    main()
