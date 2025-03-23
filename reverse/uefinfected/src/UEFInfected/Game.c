#include "Game.h"

#define GRID_SIZE 15

// Position de la reine
typedef struct
{
    UINT8 x;
    UINT8 y;
} Position;

Position queen = {GRID_SIZE - 1, GRID_SIZE - 1}; // Position initiale en bas à droite

// Vérifie si un déplacement est légal
BOOLEAN IsMoveLegal(Position current, Position next)
{
    if (next.x > GRID_SIZE || next.y > GRID_SIZE)
        return FALSE;
    if (next.x > current.x || next.y > current.y)
        return FALSE;
    if (next.x == current.x && next.y == current.y)
        return FALSE;
    return (next.x == current.x || next.y == current.y || (current.x - next.x == current.y - next.y));
}

// Lit une entrée utilisateur (exactement 4 octets)
VOID ReadHexInput(CHAR16 *Buffer)
{
    EFI_INPUT_KEY Key;
    UINT8 Index = 0;

    while (Index < 2)
    { // Bloque jusqu'à obtenir 2 caractères
        UINTN EventIndex;
        gBS->WaitForEvent(1, &gST->ConIn->WaitForKey, &EventIndex); // Bloquant
        gST->ConIn->ReadKeyStroke(gST->ConIn, &Key);

        if ((Key.UnicodeChar >= L'0' && Key.UnicodeChar <= L'9') ||
            (Key.UnicodeChar >= L'A' && Key.UnicodeChar <= L'F') ||
            (Key.UnicodeChar >= L'a' && Key.UnicodeChar <= L'f'))
        {

            Buffer[Index++] = Key.UnicodeChar;
            Print(L"%c", Key.UnicodeChar); // Afficher le caractère saisi
        }
    }

    Buffer[Index] = L'\0'; // Terminateur
}

BOOLEAN HackerMove(UINT8 X, UINT8 Y)
{
    queen.x = X;
    queen.y = Y;

    if (queen.x == 0 && queen.y == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

BOOLEAN PlayerMove(UINT8 *X, UINT8 *Y)
{

    BOOLEAN isLegalMove = FALSE;
    Position next = {};
    CHAR16 inputBuffer[3]; // 3 caractères dont '\0'
    while (!isLegalMove)
    {
        Print(L"> What did you have to say : ");
        ReadHexInput(inputBuffer);
        next.x = (UINT8)StrHexToUintn(inputBuffer);
        ReadHexInput(inputBuffer);
        next.y = (UINT8)StrHexToUintn(inputBuffer);

        if (IsMoveLegal(queen, next))
        {
            queen = next;
            isLegalMove = TRUE;
            *X = queen.x;
            *Y = queen.y;
            Print(L"\n");
        }
        else
        {
            Print(L"\nWhat are you doing ?!\n");
        }
    }

    if (queen.x == 0 && queen.y == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
