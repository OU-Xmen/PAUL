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

# def story_two(file):
#     f

# def story_three(file):
#     f

# def story_four(file):
#     f

# def story_five(file):
#     f

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
        # elif file == 'mad_libs/assets/madlibs_story2.txt':
        #     story_two(file)
        #     print('Thank you for playing!')
        # elif file == 'mad_libs/assets/madlibs_story3.txt':
        #     story_three(file)
        #     print('Thank you for playing!')
        # elif file == 'mad_libs/assets/madlibs_story4.txt':
        #     story_four(file)
        #     print('Thank you for playing!')
        # elif file == 'mad_libs/assets/madlibs_story5.txt':
        #     story_five(file)
        #     print('Thank you for playing!')
            
    print()
    savedump()

main()
