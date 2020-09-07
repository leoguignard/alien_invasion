aliens = 2
motDePasse = "MOT DE PASSE"
print("Vite ! Des aliens envahissent la planète.")
print("Tu dois activer la plateforme de défense mondiale.")
print("J'espère que tu connais le mot de passe...")
print()
print("--------------------------------------------------")
print("         BIENVENUE DANS LE RÉSAU DE DÉFENSE MONDIALE    ")
print("--------------------------------------------------")
print()
deviner = input("Entre le mot de passe : ").upper()
while deviner != motDePasse:
    print()
    print("MOT DE PASSE INCORRECT.")
    print()
    aliens = aliens ** 2
    print("Il y a",aliens,"aliens sur Terre.Réessaie !")
    if aliens > 7400000000:
        break
    print()
    print("Indice mot de passe : Ce que tu dois taper.")
    print()
    deviner = input("Vite ! Entre le mot de passe : ").upper()
if aliens > 7400000000:
    print("Noon ! Les aliens sont plus nombreux que nous. Tout est perdu.")
else:
    print("Hourra ! Nous avons gagné le combat,le monde est sauvé !")


