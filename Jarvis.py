import speech_recognition as sr


def listen_text():

    r = sr.Recognizer();
    with sr.Microphone() as source:
        print "Say Something!";
        audio = r.listen(source);

    # recognize speech using Google Speech Recognition
    try:
        rec_text = r.recognize_google(audio)
        print "Heard:" +  rec_text
        return rec_text
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        return False

def match_question(sentence, syntax):

    matchedIndex = -1

    for onesyntax in syntax:

        #which will store the place where it is stored
        positionarr = []

        for cindex ,word in enumerate(onesyntax):

            positionarr.append(sentence.find(word))

            if -1 not in positionarr:
                sorted_positionarray = positionarr

                positionarr.sort()

                if sorted_positionarray == positionarr:
                    #This is perfect match
                    matchedIndex = cindex
                    break
            else:
                continue

        if matchedIndex != -1:
            break



    return matchedIndex




syntax = [["what", "time"], ["what", "date"]]

#Get the line what the user has said
print match_question(listen_text(), syntax)
