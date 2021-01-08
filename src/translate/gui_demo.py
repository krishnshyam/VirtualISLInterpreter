import tkinter
import requests

from spacy_rules import translate_text

i = 0
started = False
isrecording = False

wordlist = "he, i, me, it, my, that, we, you, your, her, his, she, they, this, how, no, not, please, sorry, how, no, " \
           "not, please, sorry, what, why, when, what, who, cheap, equal, everything, green, together, tomorrow, " \
           "cool , friend, home, person, sleep, birthday, hospital, man, student, do, eat, give, make, take, talk, " \
           "finish, know, like, think, address, job, jump, go, "

wordcolumns = []
words = ""
f = open("wordVerb", "r")
words = f.read()
wordcolumns.append(words)
wordlist+=", ".join(words.split('\n'))
words = ""
f = open("wordNoun", "r")
words = f.read()
wordcolumns.append(words)
wordlist+=", ".join(words.split('\n'))
words = ""
f = open("wordNoun2", "r")
words = f.read()
wordcolumns.append(words)
wordlist+=", ".join(words.split('\n'))
words = ""
f = open("wordAdj", "r")
words = f.read()
wordcolumns.append(words)
wordlist+=", ".join(words.split('\n'))
words = ""
f = open("wordMisc", "r")
words = f.read()
wordcolumns.append(words)
wordlist+=", ".join(words.split('\n'))

def setmessage(message):
    textentry.insert(0, message)


def send_text(event):
    entered_text = textentry.get()
    output = translate_text(entered_text).upper()
    textoutput.config(text=output)
    
    #OPTIONAL: Send code to animation demo
    #r = requests.post('http://localhost:9000', json={"text": output})
    #r.status_code


def clear_text(event):
    textentry.delete(0, tkinter.END)


main = tkinter.Tk()

labelheadingmain = tkinter.Label(main, text="Indian Sign Language Translation",
                                 font="Helvetica 20 bold")
labelheadingmain.grid(row=0, column=0, columnspan=15)

text_button = tkinter.Button(main, text='Go', width=20)
text_button.grid(row=1, column=7, columnspan=2, pady=10)
text_button.bind("<Button-1>", send_text)

textentry = tkinter.Entry(main, width=60)
textentry.bind("<Button-1>", clear_text)
textentry.grid(row=1, column=1, columnspan=6, padx=10, pady=10)

labeloutput = tkinter.Label(main, text='Output: ', width=20)
labeloutput.grid(row=1, column=9, columnspan=1, pady=10)

textoutput = tkinter.Label(main, anchor="nw", width=60, bg="white")
textoutput.grid(row=1, column=10, columnspan=6, padx=10, pady=10)

labelheading1 = tkinter.Label(main, text="Example Sentences",
                              font="Helvetica 18 bold")
labelheading1.grid(row=2, column=1, columnspan=6, pady=10)

labelsentences = tkinter.Label(main, text="He is my friend\n"
                                          "Tomorrow is his birthday\n"
                                          "Where is the hospital?\n"
                                          "I like my job\n"
                                          "The student jumped\n"
                                          "That's his room\n"
                                          "Open the door\n"
                                          "I'm meeting my friend\n"
                                          "She's a big child\n"
                                          "The cat is thin\n"
                                          "What is your address?\n"
                                          "That is a big sentence\n"
                                          "I'm going home",
                               font="Helvetica 12",
                               padx=10)

labelsentences.grid(row=3, column=1, columnspan=6)

labelheading2 = tkinter.Label(main, text="Sign Vocabulary",
                              font="Helvetica 18 bold")
labelheading2.grid(row=2, column=7, columnspan=8, pady=10)

labelwords = []
for i in range(0, 4):
    labeltext = tkinter.Label(main, text=wordcolumns[i],
                              font="Helvetica 12",
                              justify=tkinter.LEFT,
                              # wraplength=450,
                              padx=20)
    labelwords.append(labeltext)
    labelwords[i].grid(row=3, column=9 + i, columnspan=1)

main.grid_columnconfigure(13, weight=3)
main.mainloop()
