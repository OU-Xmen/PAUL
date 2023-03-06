f = open("current.theme", "r")
theme = f.readline()
if theme == 'dark':
    BACKGROUND = (10, 10, 10)
    TEXT = (255, 255, 255)
    GAME_BUTTONS = (50, 30, 75)
    PAGE_BUTTONS = (50, 37, 48)

elif theme == 'midnight':
    BACKGROUND = (10, 10, 45)
    TEXT = (255, 255, 255)
    GAME_BUTTONS = (40, 30, 48)
    PAGE_BUTTONS = (30, 37, 48)

elif theme == 'light':
    import freakout
    f = open("current.theme", "w")
    f.write("dark")