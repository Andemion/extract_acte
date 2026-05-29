base_schema = {
    "type": "object",
    "properties": {},
    "required": []
}

dateSignature = {
    "dateSignature": {
        "type": "string",
        "description": "La date de signature en lettres de l'acte. Elle est systématiquement sur la première page du document."
    },
}

notaires = {
    "notaires": {
        "type": "array",
        "description": "Les notaires on toujours leur prénom et leur nom précédé de leur titre ''' Maître ''' ",
        "items": {
            "type": "object",
            "properties": {
                "nom": {
                    "type": "string",
                    "description": "Le nom de famille du notaire identifié"
                },
                "prenom": {
                    "type": "string",
                    "description": "Le prénom du notaire identifié"
                },
                "etude": {
                    "type": "string",
                    "description": "L'étude notariale à laquelle le notaire est rattaché"
                },
                "adresse": {
                    "type": "string",
                    "description": "L'adresse de l'étude notariale du notaire"
                },
                "type": {
                    "type": "string",
                    "description": "Le partie de l'acte que le notaire représente. Si le document traité est un acte de vente, il peut représenter un vendeur ou un acquéreur. Si le document traité est une promesse de vente, il peut représenter un promettant ou un bénéficiaire. Si cette information n'apparaît pas clairement dans l'acte, ce champ doit être à null",
                    "enum": [
                        "vendeur",
                        "acquereur",
                        "promettant",
                        "beneficiaire",
                        "preteur",
                        "suppleant",
                        "null"
                    ]
                }
            }
        }
    }
}

parties = {
    "parties": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "nom": {
                    "type": "string",
                    "description": "Le nom de la partie identifiée"
                },
                "prénom": {
                    "type": "string",
                    "description": "Le prénom de la partie identifiée s'il s'agit d'une personne"
                },
                "adresse": {
                    "type": "string",
                    "description": "L'adresse de la partie identifiée"
                },
                "dateDeNaissance": {
                    "type": ["string", "null"],
                    "description": "La date de naissance de la partie identifiée s'il s'agit d'une personne. Cette date doit être au format DD/MM/YYYY."
                },
                "situationFamiliale": {
                    "type": ["string", "null"],
                    "description": "La situation familiale de la partie identifiée s'il s'agit d'une personne"
                },
                "nationalite": {
                    "type": "string",
                    "description": "La nationalite de la partie identifiée"
                },
                "formeJuridique": {
                    "type": ["string", "null"],
                    "description": "La forme juridique de la partie identifiée s'il s'agit d'une entreprise"
                },
                "capital": {
                    "type": ["number", "null"],
                    "description": "Le capital de la partie identifiée s'il s'agit d'une entreprise."
                },
                "registre": {
                    "type": ["string", "null"],
                    "description": "Le registre où est immatriculé la partie identifiée s'il s'agit d'une entreprise"
                },
                "siren": {
                    "type": "string",
                    "description": "Le numéro de SIREN de la partie identifiée s'il s'agit d'une entreprise"
                },
                "type": {
                    "type": "string",
                    "enum": [
                        "vendeur",
                        "acquereur",
                        "promettant",
                        "beneficiaire"
                    ],
                    "description": "La position qu'occupe cette partie au sein de l'acte. Si le document traité est un acte de vente, la partie peut être un vendeur ou un acquéreur. Si le document traité est une promesse de vente, la partie peut être un promettant ou un bénéficiaire."
                }
            }
        }
    }
}

natureFromContent = {
    "natureFromContent": {
        "type": "array",
        "items": {
            "type": "string",
            "enum": [
                "mariage en communaute de meubles et acquets",
                "mariage en communaute de biens reduite aux acquets",
                "mariage en separation de biens",
                "mariage en communaute universelle",
                "mariage en participation aux acquets",
                "vente de terrain a batir",
                "vente de terrain agricole",
                "vente de terrain viticole",
                "vente de maison batie",
                "vente d'immeuble entier bati",
                "vente de lot",
                "vente de volume",
                "vente de local batie",
                "vente de garage batie",
                "vente d'appartement en copro",
                "vente d'annexe en copro",
                "vente de cave en copro",
                "vente de garage en copro",
                "vente de grenier en copro",
                "vente de local en copro",
                "vente de maison en copro",
                "vente de parking en copro",
                "donation simple",
                "donation entre epoux",
                "donation-partage",
                "donation avec reserve usufruit",
                "donation demembrement de propriete",
                "succession legale",
                "succession testamentaire",
                "succession avec reserve hereditaire et quotite disponible",
                "succession indivision",
                "succession avec exécuteur testamentaire"
            ],
            "description": "La natureFromContent de l'acte traité, dépendant de sa nature."
        }
    }
}

immeubles = {
    "immeubles": {
        "type": "object",
        "description": "Toutes les informations rechercher ce situeront aprés l'expression ''' IDENTIFICATION DU/DES BIEN/S ''' ou ''' DESIGNATION DE L'IMMEUBLE ''' ou parfois seulement ''' DESIGNATION '''. ",
        "properties": {
            "parcellesCadastrales": {
                "type": "array",
                "items": {
                    "type": "object",
                    "description": "A part la commune toutes les information seront situé dans le texte suivant l'expression ''' figurant au cadastre ''' ou ''' cadastré '''.",
                    "properties": {
                        "prefixe": {
                            "type": ["string", "null"],
                            "description": "Seras trés souvent absent des actes. Si présent peut être écrit Pfx. Il est conposé de chiffres"
                        },
                        "section": {
                            "type": ["string", "null"],
                            "description": "Correspond à la section de la parcelle cadastrale. elle est composé d'une à trois lettres en majuscule jamais de chiffre. Attention a ne pas confondre avec la surface !"
                        },
                        "plan": {
                            "type": ["string", "null"],
                            "description": "Correspond au numéro de la parcelle cadastrale. Il est donc composé uniquement de chiffre. Attention a ne pas confondre avec la surface !"
                        },
                        "commune": {
                            "type": ["string", "null"],
                            "description": "Le nom de la commune seras situé dans le texte précédant l'expression ''' figurant au cadastre ''' ou ''' cadastré ''' "
                        },
                        "lieudit": {
                            "type": ["string", "null"],
                            "description": "Correspond au l'adresse de la parcelle cadastrale."
                        },
                        "surface": {
                            "type": ["string", "null"],
                            "description": "Correspond à la taille de la parcelle cadastrale. Elle seras indiqué en hectares (ha), ares (a) et centaires (ca)."
                        }
                    },
                    "required": ["prefixe", "section", "plan", "lieudit", "surface"]
                }
            },
            "divisions": {
                "type": "array",
                "description": "C'est information ne sont pas toujours présentent mais si elle le sont elle se situe dans le texte sous les parcelles cadastrales.",
                "items": {
                    "type": "object",
                    "properties": {
                        "numero": {
                            "type": "string",
                            "description": "Correspond au numéro du lot, volume, lot de volume ou lots de copropriété"
                        },
                        "surface": {
                            "type": ["string", "null"],
                            "description": "Correspond à la taille en metre carré."
                        },
                        "millieme": {
                            "type": ["string", "null"],
                            "description": "Information pour les lots ou lots de copropriété uniquement et non les lots de volume ou volume, correspond à la taille de la part du bien"
                        },
                        "altitude": {
                            "type": ["string", "null"],
                            "description": "Information pour les volumes ou lots de volumes correspondant à une hauteur."
                        },
                        "description": {
                            "type": ["string", "null"],
                            "description": "Correspond à la composition du lot ou volume. Exemple '2 chambre et 1 réserve"
                        },
                        "type": {
                            "type": "string",
                            "enum": [
                                "volume",
                                "lot",
                                "lotDeVolume",
                                "lots de copropriété"
                            ],
                            "description": "Le volume est au sens volumétrique et non un synonyme de livre."
                        }
                    },
                },
            },
        },
        "required": ["parcellesCadastrales", "divisions"]
    }
}

adresse = {
    "adresse": {
        "type": "string",
        "description": "L'adresse complète du bien immobilier vendu. Elle seras situé avant ou aprés l'expression ''' figurant au cadastre ''' ou ''' cadastré '''."
    }
}

conditions_suspensives = {
    "conditions_suspensives": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "string",
                    "description": "Numéro de la page où la condition suspensive est mentionnée"
                },
                "conditionSuspensive": {
                    "type": "string",
                    "description": "Texte de la condition suspensive"
                },
                "comparant": {
                    "type": "string",
                    "enum": ["Beneficiaire", "Promettant", "Beneficiaire et Promettant"],
                    "description": "Partie concernée par la condition suspensive"
                },
                "nature": {
                    "type": "string",
                    "enum": ["obtention pret",
                             "absence pret",
                             "vente bien immobilier",
                             "cautionnement bancaire",
                             "caducité de la promesse",
                             "période de gratuité",
                             "acquisition concomitante",
                             "archéologie préventive",
                             "absence de pollution",
                             "absence d’amiante",
                             "notification renonciation",
                             "affichage du obligatoire",
                             "absence de fondations spéciales",
                             "prorogation des délais",
                             "droit de préemption",
                             "travaux conformité",
                             "obtention permis construire",
                             "absence servitude",
                             "absence de prescriptions sur l’eau",
                             "origine de propriété",
                             "situation hypothécaire",
                             "urbanisme"],
                    "description": "Nature de la condition suspensive"
                },
                "delai": {
                    "type": ["string", "null"],
                    "description": "Délai de la condition suspensive. Elle peut être afficher sous le format d'une date exemple '19 mai 1982' ou d'un délai exemple 'sous trois mois'."
                },
            },
            "required": ["page", "conditionSuspensive", "comparant", "nature", "delai"]
        }
    },
    # "delai": {
    #     "type": "array",
    #     "description": "Liste de toutes les dates des conditions suspensives",
    #     "items": {
    #         "type": "object",
    #         "properties": {
    #             "operation": {
    #                 "type": "string",
    #                 "description": "Type de l'opération'. Ne m'invente pas de nouveau type utilise uniquement ceux enummérés.",
    #                 "enum": ["obtentionPermisConstruire",
    #                          "demandePermisConstruire",
    #                          "cautionnement bancaire",
    #                          "caducité de la promesse",
    #                          "période de gratuité",
    #                          "acquisition parcelle",
    #                          "archéologie préventive",
    #                          "absence de pollution",
    #                          "absence d’amiante",
    #                          "notification renonciation",
    #                          "affichage du permis",
    #                          "absence de fondations spéciales",
    #                          "défaut de signature",
    #                          "prorogation des délais",
    #                          "droit de préemption"],
    #             },
    #             "date": {
    #                 "type": "string",
    #                 "description": "Délai de la condition suspensive. Elle peut être afficher sous le format d'une date exemple '19 mai 1982' ou d'un délai exemple 'sous trois mois' "
    #             },
    #             "page": {
    #                 "type": "string",
    #                 "description": "Numéro de la page où la condition suspensive est mentionnée"
    #             },
    #         },
    #         "required": ["denomination", "date", "page"]
    #     }
    # }
}

prixVente = {
    "prixVente": {
        "type": "object",
        "properties": {
            "prix": {
                "type": "number",
                "description": "Prix auquel est vendu le bien immobilier en chiffre."
            },
            "devise": {
                "type": "string",
                "description": "Devise a laquelle est vendu le bien immobilier."
            }
        },
        "required": ["prix", "devise"]
    }
}

paiementPrix = {
    "paiementPrix": {
        "type": "array",
        "description": "Correspond au divers paiement du prix.",
        "items": {
            "type": "object",
            "properties": {
                "montant": {
                    "type": "number",
                    "description": "Prix auquel est vendu le bien immobilier en chiffre."
                },
                "devise": {
                    "type": "string",
                    "description": "Devise a laquelle est vendu le bien immobilier."
                },
                "date": {
                    "type": "string",
                    "enum": ["avant ce jour", "ce jour", "a l'instant", "le jour de la vente", "au fur et à mesure"],
                    "description": "Moment du payement"
                }
            }
        }
    }
}

origineFond = {
    "origineFond": {
        "type": "array",
        "description": "Ce tableau ne doit être rempli que si et seulement si un chapitre nommé 'origine des fonds' est présent dans le texte",
        "items": {
            "type": "object",
            "properties": {
                "origine": {
                    "type": "string",
                    "description": "Correspond a l'origine d'une partie des fonds"
                },
                "montant": {
                    "type": ["number", "null"],
                    "description": "Correspond au montant du fond."
                }
            }
        }
    }
}

pret = {
    "pret": {
        "type": "boolean",
        "description": "False si absence de prêt est signaler dans le texte."
    },
    "detailPret": {
        "type": "array",
        "description": "Le total du prêt peut être divisé en plusieurs prêt.",
        "items": {
            "type": "object",
            "description": "S'il est mentionné un prêt dans le texte.",
            "properties": {
                "dateLimiteObtentionPret": {
                    "type": ["string", "null"],
                    "description": "Dans le cadres d'une promesse de vente c'est la date limite de l'obtention du prêt immobilier. Cette date doit être au format DD/MM/YYYY."
                },
                "montantTotalPret": {
                    "type": ["number", "null"],
                    "description": "Dans le cadres d'un acte de vente c'est le montant du prêt immobilier."
                },
                "preteur": {
                    "type": "object",
                    "description": "Sociètè accordant le prêt",
                    "properties": {
                        "nom": {
                            "type": ["string", "null"],
                            "description": "Le nom de la partie identifiée"
                        },
                        "adresse": {
                            "type": ["string", "null"],
                            "description": "L'adresse de la partie identifiée"
                        },
                        "formeJuridique": {
                            "type": ["string", "null"],
                            "description": "La forme juridique de la partie identifiée s'il s'agit d'une entreprise"
                        },
                        "capital": {
                            "type": ["number", "null"],
                            "description": "Le capital de la partie identifiée s'il s'agit d'une entreprise"
                        },
                        "registre": {
                            "type": ["string", "null"],
                            "description": "Le registre où est immatriculé la partie identifiée s'il s'agit d'une entreprise"
                        },
                        "siren": {
                            "type": ["string", "null"],
                            "description": "Le numéro de SIREN de la partie identifiée s'il s'agit d'une entreprise"
                        },
                    }
                }
            }
        }
    }
}

family = {
    "family": {
        "type": "array",
        "description": "Client concerné par l'acte présent dans le texte hors notaires",
        "items": {
            "type": "object",
            "properties": {
                "nom": {
                    "type": "string",
                    "description": "Le nom de famille"
                },
                "prenom": {
                    "type": "string",
                    "description": "Le prénom"
                },
                "adresse": {
                    "type": "string",
                    "description": "L'adresse"
                },
                "profession": {
                    "type": "string",
                    "description": "La proféssion"
                },
                "dateDeNaissance": {
                    "type": "string",
                    "description": "La date de naissance. Cette date doit être au format DD/MM/YYYY."
                },
                "nationalite": {
                    "type": "string",
                    "description": "La nationalite"
                },
                "situationFamiliale": {
                    "type": "string",
                    "description": "La situation familiale"
                },
                "epoux": {
                    "type":  "object",
                    "description": "Epoux ou épouse de cette persoone",
                    "properties": {
                        "nom": {
                            "type": "string",
                            "description": "Le nom de famille de l'époux/épouse"
                        },
                        "prenom": {
                            "type": "string",
                            "description": "Le prénom de l'époux/épouse"
                        },
                        "dateDeNaissance": {
                            "type": "string",
                            "description": "La date de naissance. Cette date doit être au format DD/MM/YYYY."
                        },
                        "adresse": {
                            "type": "string",
                            "description": "L'adresse de l'époux/épouse"
                        },
                    }
                },
                "parente": {
                    "type": "array",
                    "description": " ",
                    "items": {
                        "type": "object",
                        "properties": {
                            "liens": {
                                "type": "string",
                                "description": "Liens de parenté avec la personne"
                            },
                            "nom": {
                                "type": "string",
                                "description": "Le nom de famille du parent"
                            },
                            "prenom": {
                                "type": "string",
                                "description": "Le prénom du parent"
                            },
                            "dateDeNaissance": {
                                "type": "string",
                                "description": "La date de naissance. Cette date doit être au format DD/MM/YYYY."
                            },
                            "adresse": {
                                "type": "string",
                                "description": "L'adresse du parent"
                            },
                            "profession": {
                                "type": "string",
                                "description": "Proféssion du parent"
                            },
                        }
                    }
                },
                "decede": {
                    "type": "boolean",
                    "description": "True si précisé dans le texte."
                }
            }
        }
    }
}

donation = {
    "donations": {
        "type": "array",
        "description": "Type de donation, montant de la donation et nombre de part si applicable trié par donateur et donataire",
        "items": {
            "type": "object",
            "properties": {
                "donateurs": {
                    "type": "array",
                    "description": "Liste des donateur",
                    "items": {
                        "type": "object",
                        "properties": {
                            "nom": {
                                "type": "string",
                                "description": "Le nom de famille du Donateur"
                            },
                            "prenom": {
                                "type": "string",
                                "description": "Le prénom du Donateur"
                            },
                        },
                    },
                },
                "donataire": {
                    "type": "object",
                    "properties": {
                        "nom": {
                            "type": "string",
                            "description": "Le nom de famille du Donataire"
                        },
                        "prenom": {
                            "type": "string",
                            "description": "Le prénom du Donataire"
                        },
                    },
                },
                "detailDonation": {
                    "type": "object",
                    "properties": {
                        "typeDonation": {
                            "type": "string",
                            "description": "type de donation exemple: 'donation de biens', 'donation immobilière', 'donation de part de société'"
                        },
                        "dateDonation": {
                            "type": "string",
                            "description": "date de la donation au format DD/MM/YYYY"
                        },
                        "montantDonation":{
                            "type": "number",
                            "description": "Montant de la donation. Si il n'est pas écrit 'chaqu'un', avant ou aprés le montant, ou que le nom d'une personne n'est pas précisé il faut donc le divisé par le nombre de donataire"
                        },
                        "nombrePartDonation":{
                            "type": ["string", "null"],
                            "description": "Nombre de part de la donation en pourcentage ou fraction (peut être écrit en lettre). Si il n'est pas écrit 'chaqu'un', avant ou aprés le montant, ou que le nom d'une personne n'est pas précisé il faut donc le divisé par le nombre de donataire"
                        },
                        "nomBien":{
                            "type": ["string", "null"],
                            "description": "Nom de la socièté ou ville du bien immobilier"
                        },
                    },
                },
            }
        }
    }
}