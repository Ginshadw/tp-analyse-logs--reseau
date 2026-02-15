#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 256

typedef struct {
    char date[20];
    char heure[20];
    char ip[50];
    int port;
    char protocole[10];
    char statut[10];
} Log;

int main() {

    FILE *f = fopen("../network_log.txt", "r");
    if (f == NULL) {
        printf("Erreur ouverture fichier\n");
        return 1;
    }

    Log *logs = NULL;
    int capacite = 10;
    int taille = 0;

    logs = malloc(capacite * sizeof(Log));

    char ligne[MAX_LINE];

    while (fgets(ligne, MAX_LINE, f)) {

        if (taille >= capacite) {
            capacite *= 2;
            logs = realloc(logs, capacite * sizeof(Log));
        }

        char *token = strtok(ligne, ";");
        strcpy(logs[taille].date, token);

        token = strtok(NULL, ";");
        strcpy(logs[taille].heure, token);

        token = strtok(NULL, ";");
        strcpy(logs[taille].ip, token);

        token = strtok(NULL, ";");
        logs[taille].port = atoi(token);

        token = strtok(NULL, ";");
        strcpy(logs[taille].protocole, token);

        token = strtok(NULL, ";\n");
        strcpy(logs[taille].statut, token);

        taille++;
    }

    fclose(f);

    int total = taille;
    int succes = 0, echec = 0;

    for (int i = 0; i < taille; i++) {
        if (strcmp(logs[i].statut, "SUCCES") == 0)
            succes++;
        else if (strcmp(logs[i].statut, "ECHEC") == 0)
            echec++;
    }

    printf("===== RESULTATS =====\n");
    printf("Total connexions : %d\n", total);
    printf("Succes : %d\n", succes);
    printf("Echecs : %d\n", echec);

    free(logs);

    return 0;
}
