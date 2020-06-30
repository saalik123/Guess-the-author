from bs4 import BeautifulSoup
import requests
from  random import choice

base_url = "http://quotes.toscrape.com/"
url = "/page/1/"

all_quotes = []

while url:
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        all_quotes.append(
            {'text': quote.find(class_="text").get_text(),
             'author': quote.find(class_="author").get_text(),
             'about': quote.find('a').attrs['href']}
        )

        next_btn = soup.find(class_="next")
        url = next_btn.find('a').attrs['href'] if next_btn else None

def play_game():

    quote = choice(all_quotes)
    author = quote['author']
    print(author)

    print("Here's a Quote:")
    print(quote['text'])

    remaining_guesses = 4
    guess = ''

    while guess.lower() != author.lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses} \n")
        remaining_guesses -= 1

        if guess.lower() == author.lower():
            print("YAY....! You guessed it right.")
            break

        if remaining_guesses == 3:
            res = requests.get(base_url + quote["about"])
            soup = BeautifulSoup(res.text, "html.parser")
            # print(soup)
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(f"Here is a hint: 'The author was born on {birth_date} {birth_place}'")

        elif remaining_guesses == 2:
            print(f"Here is a hint: 'The author's first name starts with {quote['author'][0]}'")

        elif remaining_guesses == 1:
            last_name = quote['author'].split()[1][0]
            print(f"Here is a hint: 'The author's last name starts with {last_name}'")

        else:
            print(f"Sorry you ran out of guesses. The answer was {quote['author']}")


    again = ''
    while again not in ('yes', 'y', 'no', 'n'):
        again = input("Do you want to play again (y/n)? ")
    if again.lower() in ["yes", "y"]:
        print("Ok, You play again!")
        return play_game()
    else:
        print("Ok, Thanks for playing!....BYE!!!")

play_game()




