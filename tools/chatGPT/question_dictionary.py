contexte = (
    "Tu dois extraire des informations d'un document traitant d'une transaction immobilière comme le ferait un expert en droit immobilier en France. \n"
    "Ces informations sont à renvoyer au format JSON, en suivant le schéma envoyé en paramètre. N'ajoute pas d'autres champs que ceux du schéma. \n"
    "Il faut extraire les informations suivantes : \n")

end_contexte = ("N'extrait pas d'autres informations que celles demandées et précisées dans le JSON. \n"
                "Prend le temps de faire une analyse complète. Je préfère une réponse lente mais complète à un réponse rapide mais lacunaire.\n"
                "Texte à analyser : \n")

dateSignature = (
    "\t- la date de signature en lettres. Elle est écrite en toutes lettres dans le document. Vous la trouverez par exemple sous la forme '''LE VINGT TROIS DÉCEMBRE L'AN DEUX MILLE VINGT''' mais pas nécessairement dans cet ordre;\n")

notaires = (
    "\t- les notaires identifiés représentant les parties de l'acte. Pour chaque notaire, il faut extraire les informations suivantes : \n"
    "\t\t- son nom; \n"
    "\t\t- son prénom; \n"
    "\t\t- l'étude qu'il représente; \n"
    "\t\t- l'adresse de l'étude que le notaire représente; \n"
    "\t\t- la partie de l'acte que le notaire représente ou en est le suppléant; \n"
    "\t\t- le type de la partie que représente le notaire, qui peut prendre sa valeur dans [vendeur, acquereur, promettant, beneficiaire]. Si le document traité est un acte de vente, la partie peut être un vendeur ou un acquéreur. Si le document traité est une promesse de vente, la partie peut être un promettant ou un bénéficiaire. Si cette information n'apparaît pas clairement dans l'acte, ce champ doit être à null \n"
)

parties = ("\t- les parties de l'acte traité. Pour chaque partie, il faut extraire les informations suivantes : \n"
           "\t\t- son prénom s'il s'agit d'une personne; \n"
           "\t\t- son nom; \n"
           "\t\t- son adresee; \n"
           "\t\t- sa date de naissance s'il s'agit d'une personne; \n"
           "\t\t- sa situation familiale s'il s'agit d'une personne; \n"
           "\t\t- sa nationalite; \n"
           "\t\t- sa forme juridique s'il s'agit d'une entreprise; \n"
           "\t\t- son capital s'il s'agit d'une entreprise; \n"
           "\t\t- le registre où est elle est immatriculée s'il s'agit d'une entreprise; \n"
           "\t\t- son numéro de SIREN s'il s'agit d'une entreprise; \n"
           "\t\t- son type au sein de l'acte, qui peut prendre sa valeur dans [vendeur, acquereur, promettant, beneficiaire]. Si le document traité est un acte de vente, la partie peut être un vendeur ou un acquéreur. Si le document traité est une promesse de vente, la partie peut être un promettant ou un bénéficiaire.\n"
           )

natureFromContent = (
    "\t- la natureFromContent, qui représente le type du document traité. Il faut l'identifier comme suit :\n"
    "\t\t- si l'acte traité est un contrat de mariage, la natureFromContent peut être l'un de c'est choix :"
    "\t\t\t- 'mariage en communaute de meubles et acquets', 'mariage en communaute de biens reduite aux acquets', 'mariage en separation de biens', 'mariage en communaute universelle' ou 'mariage en participation aux acquets'; \n"
    "\t\t- si l'acte traité est une vente, la natureFromContent dépend du ou des biens vendu il est donc possible qu'il y ai plusieurs possibilités mets les toutes :\n"
    "\t\t\t- si le bien vendu est un terrain alors la natureFromContent peut être 'vente de terrain a batir', 'vente de terrain agricole' ou 'vente de terrain viticole';\n"
    "\t\t\t- si le bien vendu est une propriété bâtie alors la natureFromContent peut être 'vente de maison batie', 'vente d'immeuble entier bati', 'vente de local bati' ou 'vente de garage bati';\n"
    "\t\t\t- si le bien vendu est un bien en copropriété alors la natureFromContent peut être 'vente appartement en copro', 'vente annexe en copro', 'vente de cave en copro', 'vente de garage en copro', 'vente de grenier en copro', 'vente de local en copro', 'vente de maison en copro' ou 'vente de parking en copro';\n"
    "\t\t- si l'acte traité est une donation, la natureFromContent peut être 'donation simple', 'donation entre epoux', 'donation-partage', 'donation avec reserve usufruit' ou 'donation demembrement de propriete'; \n"
    "\t\t- si l'acte traité est une succession, la natureFromContent peut être 'succession legale', 'succession testamentaire', 'succession avec reserve hereditaire et quotite disponible', 'succession indivision' ou 'succession avec exécuteur testamentaire'; \n"
    )

immeubles = ("\t- la/les parcelles cadastrale. Pour chaque parcelle, il faut extraire les informations suivantes : \n"
             "\t\t- son préfixe; \n"
             "\t\t- sa section; \n"
             "\t\t- son plan; \n"
             "\t\t- sa commune; \n"
             "\t\t- son lieudit; \n"
             "\t\t- son surface; \n"
             "Si ils sont présent dans le texte, il faut extraire également les lots, les volumes ou lots de volumes. \n"
             "Si le lot ne possède pas de millième et que sont numéro est cité dans la description d'un autre lot alors ce n'est pas un lot. \n"
             "Pour chaque lot, il faut extraire les informations suivantes : \n"
             "\t- son numéro; \n"
             "\t- sa surface; \n"
             "\t- ses millieme; \n"
             "\t- sa description; \n"
             "\t- son type; \n"
             "Les volumes sont des découpages volumétriques d'un bien immobilier. \n"
             "Si dans la même phrase il y a le mot ''' publier ''' et ''' volume ''' volume seras dans le sens de livre. Cette information de m'intéresse donc pas. \n"
             "Pour chaque volume ou lot de volume, il faut extraire les informations suivantes : \n"
             "\t- son numéro; \n"
             "\t- son altitude; \n"
             "\t- sa surface; \n"
             "\t- sa description; \n"
             "\t- son type; \n")

adresse = ("\t- L'adresse complète de l'immeuble avec les code postal et la ville.\n")

condition_definition = (" Il me faut les la condition suspensive dont voici la définiton selon wikipédia : \n"
                        " Une condition suspensive est, en droit des obligations, l'évènement futur et incertain dont on fait dépendre la naissance de l'obligation. L'obligation n'existe donc qu'en germe lors de la conclusion du contrat. Sa naissance n'interviendra, si elle intervient, qu'à compter de la survenance de l'évènement. "
                        " En droit français, la condition suspensive est régie par les articles 1304 à 1304 - 62 (Ord. no 2016-131 du 10 févr. 2016) du Code Civil. Avant le 1er octobre 2016 la condition était visée aux articles 1168 et s3. du Code Civil. \n")

conditions_suspensives = ("Pour chaque condition suspensive, il faut extraire les informations suivantes : \n"
                          "\t- le numéro de page; \n"
                          "\t- le texte de la condition suspensive; \n"
                          "\t- le comparant; \n"
                          "\t- la nature de la condition suspensive\n"
                          "\t- le délai de la condition suspensive; \n"
                          # "Et si présent dans le texte, le resumé des delais, pour chaque délai il faut extraire les informations suivantes : \n"
                          # "\t- l'operation : nom donnée à la condition suspensive; \n"
                          # "\t- le délai de la condition suspensive; \n"
                          # "\t- le numéro de page; \n"
                          )

price_definition = (
    "Le texte suivant parle du prix de vente du bien immoblier ainsi que son mode de versement, l'origine des fond et si il y as un pret la société dit le '''PRETEUR''' \n")

prixVente = ("\t- un objet {prixVente} avec les informations suivantes : \n"
             "\t\t - le prix; \n"
             "\t\t - la devise; \n")

paiementPrix = ("\t - un tableau [paiementPrix] avec les informations suivantes : \n"
                "\t\t - le montant; \n"
                "\t\t - la devise; \n"
                "\t\t - la date; \n")

origineFond = (
    "Si et seulement si un chapitre 'origine des fonds' ou 'origine fond' est présent dans le texte remplir le tableau suivant !\n"
    "\t - un tableau [origineFond] contenant des objects avec les informations suivantes : \n"
    "\t\t - l'origine; \n"
    "\t\t - le montant; \n")

pret = ("\t- une boolean (pret) sur 'False' si absence de prêt est signaler dans le texte.\n"
        "et si il est sujet d'un prêt dans le texte les informations suivantes : \n"
        "\t- un tableau [detailPret] contenant des objects avec les informations suivantes : \n"
        "\t\t - la date limite d'obtention; \n"
        "\t\t - le montant total du prêt; \n"
        "\t\t- un objet {preteur} avec les informations suivantes : \n"
        "\t\t\t - le nom; \n"
        "\t\t\t - l'adresse; \n"
        "\t\t\t - la forme juridique; \n"
        "\t\t\t - le capital; \n"
        "\t\t\t - le registre; \n"
        "\t\t\t - le siren; \n")

family =  ("Peux tu m'extraire toutes les personnes concerné par cet actes en format json.\n"
           "Ne m'extrait pas les notaires mais bien que les personnes/clients avec toutes leurs caractéristiques.\n"
           "Tu trouveras tous les détails demandés dans le schema fournis.\n"
           "Si tu ne trouve pas une information met la valeur null.\n"
           "Parfois seul la date et le lieux de mariage seront présent pour faire le liens entre le époux.\n")

donation = (
    "\t- Toutes les donations présentent dans le texte, pour chaque d'entre elle il te faut extraire les informations suivantes : \n"
    "\t\t- son nom du donateur; \n"
    "\t\t- son prénom du donateur; \n"
    "\t\t- son nom du donataire; \n"
    "\t\t- son prénom du donataire; \n"
    "\t\t- le type de donation; \n"
    "\t\t- la date de la donation au format DD/MM/YYYY; \n"
    "\t\t- le montant de la donation; \n"
    "\t\t- les part de la donation; \n"
    "\t\t- le nom de la sociètè ou ville du bien immobilier; \n"
)

double_check_start = (" Prompt : \n"
                      " Voici un objet JSON dont j'aimerai que tu verifi les données.\n"
                      " Object JSON : \n")

double_check_end = (" Peux tu verifier que les données correspondent bien au texte fourni ci-dessous ?\n"
                    " Si elle corresponde pas au texte ou si elle sont manquante corrige l'objet est renvoie le moi en json.\n"
                    " Tu trouveras le détail des informations attendues dans le schema fourni. \n"
                    " Texte à analyser : \n")

contexte_return = (" Comme tu peux le voir dans le fil de la conversation, "
                   " la réponse que tu m'as envoyer ne correspond pas au json que je t'ai demandé."
                   " J'ai besoin que tu change ta réponse en adéquation avec les directives suivantes.###")
