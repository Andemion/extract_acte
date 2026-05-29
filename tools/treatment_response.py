from tools import calendar_dictionary


def sign_block_treatment(gpt_response):

    if "dateSignature" in gpt_response:
        print(f"date from GPT : {gpt_response['dateSignature']}")
        try:
            gpt_response["dateSignature"] = treatment_date(gpt_response["dateSignature"])
        except:
            return gpt_response

    return gpt_response


def parcelle_block_treatment(gpt_response):
    lots = {"lots": []}
    volumes = {"volumes": []}

    if isinstance(gpt_response["immeubles"], list):
        gpt_response["immeubles"] = gpt_response["immeubles"][0]

    for div in gpt_response["immeubles"]["divisions"]:

        if "type" in div:
            if div["type"] == "lot" or div["type"] == "lots de copropriété":
                lot = {
                    "numero": div.get("numero", None),
                    "surface": div.get("surface", None),
                    "millieme": div.get("millieme", None),
                    "description": div.get("description", None)
                }
                lots["lots"].append(lot)
            elif div["type"] == "volume" or div["type"] == "lot de volume" or div["type"] == "lotDeVolume":
                volume = {
                    "numero": div.get("numero", None),
                    "surface": div.get("surface", None),
                    "altitude": div.get("altitude", None),
                    "description": div.get("description", None)
                }
                volumes["volumes"].append(volume)

    gpt_response["immeubles"] = gpt_response["immeubles"] | lots | volumes
    del gpt_response["immeubles"]["divisions"]

    for immeuble in gpt_response["immeubles"]["parcellesCadastrales"]:
        if immeuble["section"] is not None:
            if "l" in immeuble["section"]:
                immeuble["section"] = immeuble["section"].replace("l", "I")

    return gpt_response


def treatment_date(response):

    day = ""
    month = ""
    year = ""
    millennium = ""
    full_date = ""
    partie_a_deplacer = ""
    partie_initiale = ""

    texte = response.upper().strip()
    texte = texte.replace("L'AN", "")

    position_mille = texte.find("MIL")
    if position_mille == -1:
        position_mille = texte.find("MILLE")

    if position_mille != -1:
        # Trouver "DEUX" juste avant "MILLE"
        position_deux = texte.rfind("DEUX", 0, position_mille)  # Cherche "DEUX" avant "MILLE"

        if position_deux != -1:
            index_debut = position_deux
        else:
            index_debut = position_mille

        # Extraire les parties de la chaîne
        partie_a_deplacer = texte[index_debut:].strip()  # La partie à mettre au début
        partie_initiale = texte[:index_debut].strip()  # La partie à déplacer à la fin
        # Réorganiser les parties
        texte = partie_a_deplacer + " " + partie_initiale

    if partie_initiale == "":
        liste_date = texte.strip().split(" LE ")
        if len(liste_date) > 1:
            day_month = liste_date[1].split(" ")
        else:
            day_month = []
        full_year = liste_date[0]
        split_year = full_year.split(" ")
    else:
        liste_date = partie_initiale.replace("LE", "").strip()
        day_month = liste_date.split(" ")
        split_year = partie_a_deplacer.split(" ")

    for ind, number in enumerate(split_year):
        if split_year[1].strip() == "NEUF":
            if ind <= 2:
                millennium += split_year[ind].strip() + " "
            elif ind > 2:
                year += split_year[ind].strip() + " "
        else:
            if ind <= 1:
                millennium += split_year[ind].strip() + " "
            elif ind > 1:
                year += split_year[ind].strip() + " "

    if len(day_month) > 1:
        if len(day_month) == 4:
            day = day_month[0].strip() + " " + day_month[1].strip() + " " + day_month[2].strip()
            month = day_month[3].strip()
        elif len(day_month) == 3:
            day = day_month[0].strip() + " " + day_month[1].strip()
            month = day_month[2].strip()
        elif len(day_month) == 2:
            day = day_month[0].strip()
            month = day_month[1].strip()
        else:
            day = day_month[0].strip()

    millennium = calendar_dictionary.millennium.get(millennium.strip())
    year = number_split_and_change(year.strip())
    month = calendar_dictionary.month.get(month.strip(), "00")
    day = number_split_and_change(day.strip())

    if day < 10:
        full_date = "0" + str(day) + "/" + month + "/" + str(millennium + year)
    else:
        full_date = "" + str(day) + "/" + month + "/" + str(millennium + year)

    return full_date


def number_split_and_change(number_in_lettre):

    number_in_lettre = remove_word(number_in_lettre)
    number_in_lettre_array = number_in_lettre.split()
    number_array = []

    for num in number_in_lettre_array:
        number_array.append(calendar_dictionary.unit.get(num, 00))
    if len(number_array) == 4:
        number = number_array[0]*number_array[1]+number_array[2]+number_array[3]
    elif len(number_array) == 3:
        if number_array[0] == 4 and number_array[1] == 20:
            number = number_array[0]*number_array[1]+number_array[2]
        else:
            number = number_array[0]+number_array[1]+number_array[2]
    elif len(number_array) == 2:
        if number_array[0] == 4 and number_array[1] == 20:
            number = number_array[0]*number_array[1]
        else:
            number = number_array[0]+number_array[1]
    elif len(number_array) == 1:
        number = number_array[0]
    else:
        number = 0

    return number


def remove_word(texte):
    texte = texte.replace("-", " ")

    word2replace = ["ET", "(", ")", "1", "2", "3", "4", "5", "6", "7", "8", "9", ","]
    for word in word2replace:
        texte = texte.replace(word, "")

    return texte
