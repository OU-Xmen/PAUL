import random

def save(text):
    save = input('Would you like to save this generated Mad Lib? (y/n) ')
    if save.upper() == 'Y':
        with open('mad_libs/assets/obituary.txt', 'a') as madlib:
            madlib.write(text)
            madlib.write('\n')
    print()

def saveclear():
    clear = input('Would you like to clear the list? (y/n) ')
    if clear.upper() == 'Y':
        f = open('mad_libs/assets/obituary.txt', 'w')
        f.truncate(0)
        f.close()
    
        print()
        print('Done! Have a nice day!')
        print()
    
    else: 
        print()
        print('Have a nice day!')
        print()


def savedump():
    dump = input('Would you like to view previous mad libs? (y/n) ')

    print()

    if dump.upper() == 'Y':
        with open('mad_libs/assets/obituary.txt', 'r') as save:
            contents = save.read()
            print(contents)
    else:
        print()

    saveclear()

def story_one(file):
    
    f = open(file)
    text = f.read()
    print('Mad Lib: What is Paul?')
    search_text = 'noun1'
    replace_text = input('Enter a noun (plural): ')
    text = text.replace(search_text, replace_text)

    search_text = 'noun2'
    replace_text = input('Enter another noun (singular): ')
    text = text.replace(search_text, replace_text)

    search_text = 'noun3'
    replace_text = input('Enter another noun (plural): ')
    text = text.replace(search_text, replace_text)

    search_text = 'noun4'
    replace_text = input('Enter another noun (singular): ')
    text = text.replace(search_text, replace_text)

    search_text = 'verb1'
    replace_text = input('Enter a verb (-ed suffix): ')
    text = text.replace(search_text, replace_text)

    search_text = 'verb2'
    replace_text = input('Enter another verb (no suffix): ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective1'
    replace_text = input('Enter an adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective2'
    replace_text = input('Enter another adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective3'
    replace_text = input('Enter another adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'interrogative'
    replace_text = input('Enter an interrogative word (capitalize): ')
    text = text.replace(search_text, replace_text)

    search_text = 'language'
    replace_text = input('Enter a language: ')
    text = text.replace(search_text, replace_text)

    search_text = 'class_level'
    replace_text = input('Enter a class level in college (capitalize): ')
    text = text.replace(search_text, replace_text)

    search_text = 'family_member'
    replace_text = input('Enter a type of family member: ')
    text = text.replace(search_text, replace_text)

    search_text = 'crime'
    replace_text = input('Enter a crime or felony: ')
    text = text.replace(search_text, replace_text)

    search_text = 'month'
    replace_text = input('Enter a month (capitalize): ')
    text = text.replace(search_text, replace_text)

    search_text = 'year'
    replace_text = input('Enter a year: ')
    text = text.replace(search_text, replace_text)

    search_text = 'body part'
    replace_text = input('Enter a body part: ')
    text = text.replace(search_text, replace_text)
    
    search_text = 'your_name'
    replace_text = input('Enter your first name: ')
    text = text.replace(search_text, replace_text)

    print()
    print(text)
    save(text)
    f.close()

def story_two(file):
    f = open(file)
    text = f.read()
    print('Holiday Party Gone Wrong (NOT CLICKBAIT)')
    
    search_text = 'adjective1'
    replace_text = input('Enter an adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'holiday'
    replace_text = input('Enter a holiday (capitalize): ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective2'
    replace_text = input('Enter another adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'verb'
    replace_text = input('Enter a verb: ')
    text = text.replace(search_text, replace_text)

    search_text = 'beverage'
    replace_text = input('Enter a type of drink: ')
    text = text.replace(search_text, replace_text)

    search_text = 'bodypart1'
    replace_text = input('Enter a body part: ')
    text = text.replace(search_text, replace_text)

    search_text = 'derogatory_saying'
    replace_text = input('Enter a derogatory saying (proper capitalization and punctuation suggested): ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective3'
    replace_text = input('Enter another adjective: ')
    text = text.replace(search_text, replace_text)  

    search_text = 'bodypart2'
    replace_text = input('Enter another body part: ')
    text = text.replace(search_text, replace_text)

    search_text = 'food'
    replace_text = input('Enter a type of food: ')
    text = text.replace(search_text, replace_text)

    search_text = 'place'
    replace_text = input('Enter a place: ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective4'
    replace_text = input('Enter another adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'number'
    replace_text = input('Enter a number (add a rank suffix, e.g. -st, -nd, -rd, -th): ')
    text = text.replace(search_text, replace_text)

    print()
    print(text)
    save(text)
    f.close()

def story_three(file):
    f = open(file)
    text = f.read()
    print('My First Performance!')
    
    search_text = 'adjective1'
    replace_text = input('Enter an adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'action'
    replace_text = input('Enter an action: ')
    text = text.replace(search_text, replace_text)

    search_text = 'verb1'
    replace_text = input('Enter a verb ending in -ing: ')
    text = text.replace(search_text, replace_text)

    search_text = 'noun1'
    replace_text = input('Enter a noun: ')
    text = text.replace(search_text, replace_text)

    search_text = 'number'
    replace_text = input('Enter a number between 1 and 12: ')
    text = text.replace(search_text, replace_text)

    search_text = 'noun2'
    replace_text = input('Enter a plural noun: ')
    text = text.replace(search_text, replace_text)

    search_text = 'adjective2'
    replace_text = input('Enter another adjective: ')
    text = text.replace(search_text, replace_text)

    search_text = 'verb2'
    replace_text = input('Enter another verb: ')
    text = text.replace(search_text, replace_text)  

    search_text = 'noun3'
    replace_text = input('Enter another noun: ')
    text = text.replace(search_text, replace_text)

    print()
    print(text)
    save(text)
    f.close()
    

def main():
    
    print()
    play = input('Welcome to the P.A.U.L. Mad Libs Generator! Would you like to play? (y/n) ')

    if play.upper() == 'Y':

        print()
        
        files = ['mad_libs/assets/madlibs_story1.txt', 'mad_libs/assets/madlibs_story2.txt', 'mad_libs/assets/madlibs_story3.txt', 'mad_libs/assets/madlibs_story4.txt', 'mad_libs/assets/madlibs_story5.txt']

        file = random.choice(files)

        if file == 'mad_libs/assets/madlibs_story1.txt':
            story_one(file)
            print('Thank you for playing!')
        elif file == 'mad_libs/assets/madlibs_story2.txt':
            story_two(file)
            print('Thank you for playing!')
        elif file == 'mad_libs/assets/madlibs_story3.txt':
            story_three(file)
            print('Thank you for playing!')
            
    print()
    savedump()

main()
