La carte distribuée est une carte NFC donnat l'url de démarrage.

Le joueur doit exploiter une XSS pour voler un coockie d'accès.

Puis désactiver 3 services sur 3 machines différentes par différents moyens (kill du process sur cabin1, idem sur cabin2 via un vuln sur DizqueTV, enfin en récupérant le pwd de la cabin3 en écoutant le trafic du port 3000 sur cabin1).

Ensuite il doit accéder au firewall OPNSense sur la machine footbridge et autoriser le trafic vers le réseau contenant la treasureroom.

C'est un gitlab contenant un vuln de reset de mdp. Il a alors accès au code permettant de reprogrammer la carte NFC et ouvrir le coffre au trésor.