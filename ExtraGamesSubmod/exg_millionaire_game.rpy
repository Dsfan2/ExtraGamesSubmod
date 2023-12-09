#File format: question|correctAnswer|wrongAnswer1|wrongAnswer2|wrongAnswer3
#DO NOT MARK THE ANSWERS WITH A, B, C, OR D! The submod will automatically do that at random

init python:
    import random

    # This class holds a question, as well as the one right and three wrong answers
    class Question:
        def __init__(self, question, correctAnswer, wrongAnswer1, wrongAnswer2, wrongAnswer3):
            self.question = question
            self.correctAnswer = correctAnswer
            self.wrongAnswer1 = wrongAnswer1
            self.wrongAnswer2 = wrongAnswer2
            self.wrongAnswer3 = wrongAnswer3

    # Building the normal questions list
    normal_questionlist = []
    with renpy.file('Submods/ExtraGamesSubmod/Millionaire/QuestionsList.txt') as wordfile:
        for line in wordfile:
            # Ignore lines beginning with '#' and empty lines
            line = line.strip()

            if line == '' or line[0] == '#': continue

            # File format: question,correctAnswer,wrongAnswer1,wrongAnswer2,wrongAnswer3
            x = line.split('|')
            normal_questionlist.append(Question(x[0], x[1], x[2], x[3], x[4]))

    # Building the HARD questions list
    hard_questionlist = []
    with renpy.file('Submods/ExtraGamesSubmod/Millionaire/QuestionsListHARD.txt') as wordfile:
        for line in wordfile:
            # Ignore lines beginning with '#' and empty lines
            line = line.strip()

            if line == '' or line[0] == '#': continue

            # File format: question,correctAnswer,wrongAnswer1,wrongAnswer2,wrongAnswer3
            x = line.split('|')
            hard_questionlist.append(Question(x[0], x[1], x[2], x[3], x[4]))

    # Building the Million Dollar questions list
    million_questionlist = []
    with renpy.file('Submods/ExtraGamesSubmod/Millionaire/QuestionsListMILLION.txt') as wordfile:
        for line in wordfile:
            # Ignore lines beginning with '#' and empty lines
            line = line.strip()

            if line == '' or line[0] == '#': continue

            # File format: question,correctAnswer,wrongAnswer1,wrongAnswer2,wrongAnswer3
            x = line.split('|')
            million_questionlist.append(Question(x[0], x[1], x[2], x[3], x[4]))


# Unlock the game
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="millionaire_game_unlock",
            conditional="store.mas_games._total_games_played() > 19",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label millionaire_game_unlock:
    $ persistent._extragames_unlocked = True
    m 2eub "Hey [player]..."
    m 3rua "So, you know that we have a few games that we can play."
    m 3rusdla "But I feel like the games we have are getting a bit... repetitive... so to speak."
    m 2euc "And maybe you noticed this too..."
    m 4rud "I figured that maybe we could use some new, more fresh games to play."
    m 6luc "So I've done some digging on the internet to get new game ideas..."
    m 6eua "And I think I might've found some new games for us to play!"
    m 7lusdrb "Now, it might take a while for me to add in some of these games..."
    m 1eua "But, while you were away... {w=1}{nw}"
    extend 1hub "I already added in a new game for us!"
    m 2rub "Granted... the game's admittedly... a little simple..."
    m 1wub "But I don't mind, as long as I'm playing with you!"
    m 1eua "So [player], you're aware of game shows, right?"
    m 3eub "TV shows in which one or more people play games on a stage for a prize, {w=1}{nw}"
    extend "usually large amounts of money..."
    m 2eub "And I chose to recreate the game show, 'Who Wants To Be A Millionaire.'"
    m 3eua "Basically, you have to answer a bunch of trivia questions correctly."
    m 3eub "The more you get right, the more money you win."
    m 4sub "If you can answer all questions correctly, you can win a million dollars!"
    m 2lusdra "Now... In my version, you can't {i}actually{/i} win a million dollars..."
    m 2eub "But... You'll be a millionaire to me~"
    show monika 5hub at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5hub "I think it'll be fun for both of us!"
    m 5kua "You can ask to play this new game in the 'Play' menu."
    show monika 6rusdrb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 6rusdrb "Ehehehe~ Sorry if I've gone on for a bit too long..."
    m 6hub "I'm just so excited I get to play a brand new game with you!"
    show monika 5fkbsa at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 5fkbsa "I love you, [player]."
    m 5hubsb "Let's have fun playing a new game together!"
    $ mas_unlockGame("The Millionaire Game")
    return

#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,eventlabel="millionaire_test",
#            category=["dev"],
#            prompt="TEST MILLIONAIRE GAME",
#            pool=True,
#            aff_range=(mas_aff.AFFECTIONATE, None)
#        ), 
#    code="EVE")

#label millionaire_test:
#    hide screen keylistener
#    m 1eua "Time to test out Millionaire Game."
#    $ musicpak = 1
#    $ questionnumber = 1
#    $ questionspassed = 0
#    $ curlifelines = 3
#    $ fiftyfifty = True
#    $ viewerpoll = True
#    $ resetquestion = True
#    $ refreshTime = False
#    $ helpmequestion = False
#    $ questionlist = list(normal_questionlist)
#    $ questionlisthard = list(hard_questionlist)
#    $ questionlistfinal = list(million_questionlist)
#    call mas_millionaire_game_loop
#    return

# Initialize the game
init 5 python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="millionaire_game",
            prompt="The Millionaire Game"
            #aff_range=(mas_aff.NORMAL, None)
        ),
        code="GME",
        restartBlacklist=True
    )

# I know, this code is kind of a long mess, but it works... I guess...
label millionaire_game:
    hide screen keylistener
    $ musicpak = 1
    $ questionnumber = 1
    $ questionspassed = 0
    $ curlifelines = 3
    $ fiftyfifty = True
    $ viewerpoll = True
    $ resetquestion = True
    $ refreshTime = False
    $ helpmequestion = False
    $ questionlist = list(normal_questionlist)
    $ questionlisthard = list(hard_questionlist)
    $ questionlistfinal = list(million_questionlist)
    call mas_millionaire_game_loop
    return

label mas_millionaire_game_loop:
    # Hide UI
    window hide
    $ HKBHideButtons()
    $ disable_esc()
    stop music

    if persistent._exg_millionaire_firsttime:
        m 2eua "Since this is our first time playing I'll explain how the game works."
        call millionaire_howtoplay
    else:
        m 3eub "Do you want me to explain how to play?{nw}"
        menu:
            m "Do you want me to explain how to play?{fast}"
            "Yes":
                m 1eka "Okay then."
                call millionaire_howtoplay
            "No":
                m 1eua "Alright then, {w=1}{nw}"
                extend 1hub "let's play!"
                call millionaire_setup_question
    return

label millionaire_howtoplay:
    show monika 3eub at t21
    show screen millionaire_hud
    $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/HowToPlay.ogg")
    m 3eub "There are 15 questions. Get them all right and you win the million."
    m 2rksdlb "But get one wrong and you lose."
    m 3lua "You also have 3 lifelines you can use."
    m 2lusdrb "But once you use one, you can't use it for the rest of the game."
    hide screen millionaire_hud
    show monika 1eua at t11
    stop music fadeout 0.3
    m 1eua "Let's begin, shall we?"

    call millionaire_setup_question
    return

label millionaire_setup_question:
    if questionnumber >= 16:
        call mas_millionaire_game_end
    else:
        python:
            answers = []
            aSlot = ""
            bSlot = ""
            cSlot = ""
            dSlot = ""
    
            if questionnumber > 14:
                musicpak = 3
                curquestion = random.choice(questionlistfinal)
                questionlistfinal.remove(curquestion)
            elif questionnumber < 15 and questionnumber > 10:
                musicpak = 2
                curquestion = random.choice(questionlisthard)
                questionlisthard.remove(curquestion)
            else:
                musicpak = 1
                curquestion = random.choice(questionlist)
                questionlist.remove(curquestion)

            answers = [curquestion.correctAnswer, curquestion.wrongAnswer1, curquestion.wrongAnswer2, curquestion.wrongAnswer3]
            aSlot = random.choice(answers)
            answers.remove(aSlot)
            bSlot = random.choice(answers)
            answers.remove(bSlot)
            cSlot = random.choice(answers)
            answers.remove(cSlot)
            dSlot = random.choice(answers)
            answers.remove(dSlot)

            question = curquestion.question
            answerlist = answers
            aOption = aSlot
            bOption = bSlot
            cOption = cSlot
            dOption = dSlot

        if aOption == curquestion.correctAnswer:
            $ wronganswerlist = [bOption, cOption, dOption]
        elif bOption == curquestion.correctAnswer:
            $ wronganswerlist = [aOption, cOption, dOption]
        elif cOption == curquestion.correctAnswer:
            $ wronganswerlist = [aOption, bOption, dOption]
        elif dOption == curquestion.correctAnswer:
            $ wronganswerlist = [aOption, bOption, cOption]
        
        $ aRemoved = False
        $ bRemoved = False
        $ cRemoved = False
        $ dRemoved = False

        if question == "Is anything truly free?":
            $ helpmequestion = True
            $ curlifelines = 0
            if persistent._extragames_lore_status == 0:
                $ persistent._extragames_lore_status = 1

        if not refreshTime:
            if musicpak == 1:
                play sound("Submods/ExtraGamesSubmod/Millionaire/mus/StartNormal.ogg")
            elif musicpak == 2:
                play sound("Submods/ExtraGamesSubmod/Millionaire/mus/StartHard.ogg")
            elif musicpak == 3:
                play sound("Submods/ExtraGamesSubmod/Millionaire/mus/StartFinal.ogg")

            call millionaire_calculate_value

            if questionnumber == 15:
                m 2sfb "And now for the Million Dollar Question!"
                m 3wfa "This will be very challenging so be prepared!"
            else:
                m 1eua "Question [questionnumber]!"
                m 6dub "This is worth [questionvalue]!"

        if not renpy.music.get_playing():
            if musicpak == 1:
                $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/NormalQuestion.ogg")
            elif musicpak == 2:
                $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/HardQuestion.ogg")
            elif musicpak == 3:
                if helpmequestion == True:
                    $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/TerrorQuestion.ogg")
                else:
                    $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/FinalQuestion.ogg")

        if refreshTime == True and helpmequestion == True:
            $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/TerrorQuestion.ogg")

        if helpmequestion == False:
            if questionnumber == 15:
                m 4cfb "[question]{nw}"
            else:
                m 4eua "[question]{nw}"
                
        call millionaire_question
    return

label millionaire_question:
    $ refreshTime = False
    if helpmequestion == True:
        show black zorder 100
    if questionnumber == 15:
        show monika 4cfb at t21
    else:
        show monika 4eua at t21
    menu:
        m "[question]{fast}"

        "A: [aOption]" if not aRemoved or aOption == curquestion.correctAnswer:
            call millionaire_guess_a
        "B: [bOption]" if not bRemoved or bOption == curquestion.correctAnswer:
            call millionaire_guess_b
        "C: [cOption]" if not cRemoved or cOption == curquestion.correctAnswer:
            call millionaire_guess_c
        "D: [dOption]" if not dRemoved or dOption == curquestion.correctAnswer:
            call millionaire_guess_d
        "Lifelines" if curlifelines > 0:
            call millionaire_lifelines
    return


label millionaire_calculate_value:
    if questionnumber == 1:
        $ questionvalue = "$100"
        $ winnings = "$0"
    elif questionnumber == 2:
        $ questionvalue = "$500"
        $ winnings = "$100"
    elif questionnumber == 3:
        $ questionvalue = "$1,000"
        $ winnings = "$500"
    elif questionnumber == 4:
        $ questionvalue = "$2,000"
        $ winnings = "$1,000"
    elif questionnumber == 5:
        $ questionvalue = "$3,000"
        $ winnings = "$2,000"
    elif questionnumber == 6:
        $ questionvalue = "$5,000"
        $ winnings = "$3,000"
    elif questionnumber == 7:
        $ questionvalue = "$7,000"
        $ winnings = "$5,000"
    elif questionnumber == 8:
        $ questionvalue = "$10,000"
        $ winnings = "$7,000"
    elif questionnumber == 9:
        $ questionvalue = "$25,000"
        $ winnings = "$10,000"
    elif questionnumber == 10:
        $ questionvalue = "$50,000"
        $ winnings = "$25,000"
    elif questionnumber == 11:
        $ questionvalue = "$100,000"
        $ winnings = "$50,000"
    elif questionnumber == 12:
        $ questionvalue = "$250,000"
        $ winnings = "$100,000"
    elif questionnumber == 13:
        $ questionvalue = "$500,000"
        $ winnings = "$250,000"
    elif questionnumber == 14:
        $ questionvalue = "$750,000"
        $ winnings = "$500,000"
    elif questionnumber == 15:
        $ questionvalue = "$1,000,000"
        $ winnings = "$750,000"
    return

label millionaire_guess_a:
    if helpmequestion == True:
        "..."
        if aOption == curquestion.correctAnswer:
            "That's right..."
            $ questionspassed += 1
            $ questionnumber += 1
            stop music
            hide black
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            call mas_millionaire_win_results
        else:
            "No! No! No!"
            stop music
            hide black
            call mas_millionaire_lose_results
    else:
        show monika 6duc at t11
        stop music fadeout 1.0
        m 6duc "You chose A: [aOption]."
        if aOption == curquestion.correctAnswer:
            if musicpak == 3:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            else:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/correct.ogg")

            m 7hub "That's the correct answer!{w=6}"
            $ questionspassed += 1
            $ questionnumber += 1
            call millionaire_transition
        else:
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/wrong.ogg")
            m 2lksdld "That's incorrect. Sorry.{w=2}"
            call mas_millionaire_lose_results
    return

label millionaire_guess_b:
    if helpmequestion == True:
        "..."
        if bOption == curquestion.correctAnswer:
            "That's right..."
            $ questionspassed += 1
            $ questionnumber += 1
            stop music
            hide black
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            call mas_millionaire_win_results
        else:
            "No! No! No!"
            stop music
            hide black
            call mas_millionaire_lose_results
    else:
        show monika 6duc at t11
        stop music fadeout 1.0
        m 6duc "You chose B: [bOption]."
        if bOption == curquestion.correctAnswer:
            if musicpak == 3:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            else:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/correct.ogg")

            m 7hub "That's the correct answer!{w=6}"
            $ questionspassed += 1
            $ questionnumber += 1
            call millionaire_transition
        else:
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/wrong.ogg")
            m 2lksdld "That's incorrect. Sorry.{w=2}"
            call mas_millionaire_lose_results
    return

label millionaire_guess_c:
    if helpmequestion == True:
        "..."
        if cOption == curquestion.correctAnswer:
            "That's right..."
            $ questionspassed += 1
            $ questionnumber += 1
            stop music
            hide black
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            call mas_millionaire_win_results
        else:
            "No! No! No!"
            stop music
            hide black
            call mas_millionaire_lose_results
    else:
        show monika 6duc at t11
        stop music fadeout 1.0
        m 6duc "You chose C: [cOption]."
        if cOption == curquestion.correctAnswer:
            if musicpak == 3:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            else:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/correct.ogg")

            m 7hub "That's the correct answer!{w=6}"
            $ questionspassed += 1
            $ questionnumber += 1
            call millionaire_transition
        else:
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/wrong.ogg")
            m 2lksdld "That's incorrect. Sorry.{w=2}"
            call mas_millionaire_lose_results
    return

label millionaire_guess_d:
    if helpmequestion == True:
        "..."
        if dOption == curquestion.correctAnswer:
            "That's right..."
            $ questionspassed += 1
            $ questionnumber += 1
            stop music
            hide black
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            call mas_millionaire_win_results
        else:
            "No! No! No!"
            stop music
            hide black
            call mas_millionaire_lose_results
    else:
        show monika 6duc at t11
        stop music fadeout 1.0
        m 6duc "You chose D: [dOption]."
        if dOption == curquestion.correctAnswer:
            if musicpak == 3:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/winner.ogg")
            else:
                play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/correct.ogg")

            m 7hub "That's the correct answer!{w=6}"
            $ questionspassed += 1
            $ questionnumber += 1
            call millionaire_transition
        else:
            play sound("Submods/ExtraGamesSubmod/Millionaire/sfx/wrong.ogg")
            m 2lksdld "That's incorrect. Sorry.{w=2}"
            call mas_millionaire_lose_results
    return

label millionaire_transition:
    if questionnumber >= 16:
        call mas_millionaire_win_results
    else:
        show monika 3eua at t21
        show screen millionaire_hud
        call millionaire_calculate_value
        m 3eua "So far you've correctly answered [questionspassed] out of 15 questions."
        m 3lub "Your current winnings are at [winnings]."
        m 2eua 'Time to advance to the next question!'
        hide screen millionaire_hud
        show monika 1eua at t11
        call millionaire_setup_question
    return

label millionaire_lifelines:
    show monika 3eud at t11
    m 3eud "You have [curlifelines] of your lifelines left."
    m 1lua "Which one do you want to use?{nw}"
    show monika 1lua at t21
    menu:
        m "Which one do you want to use?{fast}"
        "50:50" if fiftyfifty:
            $ curlifelines -= 1
            $ fiftyfifty = False
            show monika 2eub at t11
            call millionaire_lifeline_fiftyfifty
        "Audience Poll" if viewerpoll:
            $ curlifelines -= 1
            $ viewerpoll = False
            show monika 2eub at t11
            call millionaire_lifeline_viewerpoll
        "Question Change" if resetquestion:
            $ curlifelines -= 1
            $ resetquestion = False
            show monika 2eub at t11
            call millionaire_lifeline_resetquestion
        "Nevermind":
            show monika 1eua at t11
            m "Okay then."
            call millionaire_question
    return

label millionaire_lifeline_fiftyfifty:
    m 2eub "50:50. Two of the wrong answers will be removed."
    m 6duc "Give me a moment.{w=1}.{w=1}.{w=3}{nw}"

    $ outlier = wronganswerlist[renpy.random.randint(0,2)]
    if outlier == aOption:
        $ bRemoved = True
        $ cRemoved = True
        $ dRemoved = True
    elif outlier == bOption:
        $ aRemoved = True
        $ cRemoved = True
        $ dRemoved = True
    elif outlier == cOption:
        $ aRemoved = True
        $ bRemoved = True
        $ dRemoved = True
    elif outlier == dOption:
        $ aRemoved = True
        $ bRemoved = True
        $ cRemoved = True

    m 1eub "Okay! Two of the wrong answers have been removed from your possible choices!"
    m 1eua "Now back to the question."
    call millionaire_question
    return

label millionaire_lifeline_viewerpoll:
    m 2eub "Audience Poll. The audience will vote for which answer they think is correct."
    m 2eua "..."
    m 3lksdlb "Well... Since we don't {i}actually{/i} have an audience watching this..."
    m 1rksdla "The closest thing we can get for that is running a random number generator 100 times in rapid succession."
    m 6duc ".{w=1}.{w=1}.{w=3}{nw}"

    $ aVotes = 0
    $ bVotes = 0
    $ cVotes = 0
    $ dVotes = 0
    python:
        for i in range(100):
            integerThing = renpy.random.randint(1, 45)
            if integerThing >= 1 and integerThing <= 15:
                if aOption == curquestion.correctAnswer:
                    aVotes += 1
                elif bOption == curquestion.correctAnswer:
                    bVotes += 1
                elif cOption == curquestion.correctAnswer:
                    cVotes += 1
                elif dOption == curquestion.correctAnswer:
                    dVotes += 1
            elif integerThing >= 16 and integerThing <= 25:
                if aOption == curquestion.wrongAnswer1:
                    aVotes += 1
                elif bOption == curquestion.wrongAnswer1:
                    bVotes += 1
                elif cOption == curquestion.wrongAnswer1:
                    cVotes += 1
                elif dOption == curquestion.wrongAnswer1:
                    dVotes += 1
            elif integerThing >= 26 and integerThing <= 35:
                if aOption == curquestion.wrongAnswer2:
                    aVotes += 1
                elif bOption == curquestion.wrongAnswer2:
                    bVotes += 1
                elif cOption == curquestion.wrongAnswer2:
                    cVotes += 1
                elif dOption == curquestion.wrongAnswer2:
                    dVotes += 1
            elif integerThing >= 36 and integerThing <= 45:
                if aOption == curquestion.wrongAnswer3:
                    aVotes += 1
                elif bOption == curquestion.wrongAnswer3:
                    bVotes += 1
                elif cOption == curquestion.wrongAnswer3:
                    cVotes += 1
                elif dOption == curquestion.wrongAnswer3:
                    dVotes += 1
                    
    m 7eua "The audience (or rather the random number generator) has spoken."
    m 3eub "[aVotes] percent answered A\n[bVotes] percent answred B\n[cVotes] percent answered C\n[dVotes] percent answred D."
    m 1eua "Now, back to the question..."
    call millionaire_question
    return

label millionaire_lifeline_resetquestion:
    m 2eub "Question Change. The question will change to a different one."
    m 4lua "In case if you were wondering, the answer was [curquestion.correctAnswer]."
    m 2dua "Here's your new question."
    $ refreshTime = True
    call millionaire_setup_question
    return

label mas_millionaire_lose_results:
    $ play_song("Submods/ExtraGamesSubmod/Millionaire/mus/FinalResults.ogg")
    show monika 1eua at t21
    show screen millionaire_hud
    $ lifelinesused = 3 - curlifelines
    m "Let's review your final results..."
    m 3eua "You've correctly answered [questionspassed] out of 15 questions."
    m 3lua "And you've used [lifelinesused] out of your 3 lifelines."
    m 3rub "Your total winnings for this game are [winnings]."
    if questionspassed == 14:
        m 3wksdlb "You were so very close to the million!"
        m 7hub "I'm sure you'll win it next time! I believe in you!"
    elif questionspassed < 14 and questionspassed > 9:
        m 2lksdlc "Well...{w=0.5} it may not have been the million dollars... {w=0.3}{nw}"
        extend 3kua "but at least you won a good sum of cash."
        m 1eka "I know you'll be able to win the million next time!"
    elif questionspassed < 10 and questionspassed > 0:
        m 2lksdlb "Well...{w=0.5} you didn't get very far in the game..."
        m 3fka "But keep trying! I know you can do it!"
    else:
        m 3ekd "You didn't even get one single question right!"
        m 2gfp "You really suck at this game..."
        m 2dusdlc "..."
        m 1hksdlb "Ahahaha~ I'm just teasing you!"
        m 3eksdla "Just keep trying! I know you'll get it eventually!"
    stop music fadeout 1.0
    $ persistent._exg_millionaire_last_win = False
    call mas_millionaire_game_end
    return

label mas_millionaire_win_results:
    show monika 1eua at t21
    show screen millionaire_hud
    m 2wub "Wow! You've correctly answered all 15 questions."
    m 3hub "And you won the one million dollars!"
    if persistent._exg_millionaire_firsttime == True:
        m 7suo "Wow! This was our first time playing, and you won?!"
        m 5hubsb "You truly are incredible, [player]!"
    elif curlifelines == 3:
        m 7wuo "I'm surprised you didn't use a single lifeline!"
        m 1hublb "You must be really smart to acomplish that!"
    elif persistent._exg_millionaire_last_win == True:
        m 6wuo "I'm impressed, you won multiple times in a row!"
        m 2eub "That takes some real effort!"
    elif persistent._exg_millionaire_last_win == False:
        m 1hub "I knew you could do it!"
        m 3kub "You kept trying and you finally managed to win!"
    $ persistent._exg_millionaire_last_win = True
    call mas_millionaire_game_end
    return

label mas_millionaire_game_end:
    # We finished the game
    show monika 1eua at t11
    hide screen millionaire_hud
    $ persistent._exg_millionaire_firsttime = False
    m "Do you want to play again?{nw}"
    menu:
        m "Do you want to play again?{fast}"
        "Yes":
            m 1hub "Alright then!"
            if persistent._exg_millionaire_last_win == False:
                m 3rua "Maybe this time you'll be able to win!"
            $ musicpak = 1
            $ questionnumber = 1
            $ questionspassed = 0
            $ curlifelines = 3
            $ fiftyfifty = True
            $ viewerpoll = True
            $ resetquestion = True
            $ refreshTime = False
            $ helpmequestion = False
            $ questionlist = list(normal_questionlist)
            $ questionlisthard = list(hard_questionlist)
            $ questionlistfinal = list(million_questionlist)
            call millionaire_setup_question
        "No":
            m 1eka "Oh, okay."
            m 2hub "Thanks for playing The Millionaire Game!"
            m 1eub "Let's play again sometime soon!"
            call mas_postmillionaire
    return

label mas_postmillionaire:
    # Show UI
    $ enable_esc()
    $ HKBShowButtons()
    window auto
    $ play_song(persistent.current_track)
    return

screen millionaire_hud():
    layer "master"
    zorder 7

    style_prefix "millionaire"

    #if questionnumber == 1:
    if mas_isNightNow():
        add MASFilterSwitch(
            "Submods/ExtraGamesSubmod/Millionaire/img/MoneyList[questionnumber]-d.png"
        ) pos (850, 60) anchor (0, 0)
    else:
        add MASFilterSwitch(
            "Submods/ExtraGamesSubmod/Millionaire/img/MoneyList[questionnumber].png"
        ) pos (850, 60) anchor (0, 0)

    if fiftyfifty:
        if mas_isNightNow():
            add MASFilterSwitch(
                "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Fiftyfifty-d.png"
            ) pos (865, 0) anchor (0, 0)
        else:
            add MASFilterSwitch(
                "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Fiftyfifty.png"
            ) pos (865, 0) anchor (0, 0)
    else:
        add MASFilterSwitch(
            "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Fiftyfifty-used.png"
        ) pos (865, 0) anchor (0, 0)

    if viewerpoll:
        if mas_isNightNow():
            add MASFilterSwitch(
                "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Audience_Poll-d.png"
            ) pos (965, 0) anchor (0, 0)
        else:
            add MASFilterSwitch(
                "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Audience_Poll.png"
            ) pos (965, 0) anchor (0, 0)
    else:
        add MASFilterSwitch(
            "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Audience_Poll-used.png"
        ) pos (965, 0) anchor (0, 0)

    if resetquestion:
        if mas_isNightNow():
            add MASFilterSwitch(
                "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Swap-d.png"
            ) pos (1065, 0) anchor (0, 0)
        else:
            add MASFilterSwitch(
                "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Swap.png"
            ) pos (1065, 0) anchor (0, 0)
    else:
        add MASFilterSwitch(
            "Submods/ExtraGamesSubmod/Millionaire/img/Lifeline_Swap-used.png"
        ) pos (1065, 0) anchor (0, 0)