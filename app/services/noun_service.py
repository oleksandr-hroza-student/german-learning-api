from app.repositories.noun_repository import lookup_noun


def process_multiple_nouns(text):
    words = text.split()
    result = []
    for word in words:
        result.append(process_noun(word))

    return(result)



def process_noun(noun):
    lookup_result = lookup_noun(noun)
    genders = []

    for i in range(0, len(lookup_result)):
        gender = lookup_result[i][1]
        if gender is not None and gender not in genders:
            genders.append(lookup_result[i][1])

    #print(lookup_result)

    if len(lookup_result) == 0:
        #print("No results found")
        result = {
            "status" : "not_found",
            "word" : noun
        }
    elif len(genders) == 0:
        #print("Missing gender")
        result = {
            "status" : "gender_missing",
            "word" : lookup_result[0][0]
        }
    elif len(genders) == 1:
        #print("Single result found")

        result = {
            "status" : "found",
            "word" : lookup_result[0][0],
            "gender" : genders[0]
        }
    else:
        #print("Ambiguous result found, multiple genders found")
        result = {
            "status" : "ambiguous",
            "word" : lookup_result[0][0],
            "genders" : genders
        }
    return result

#print(process_noun("Hund"))
print(process_multiple_nouns("HunD und Katze"))

